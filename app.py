from flask import Flask, render_template, request, jsonify, session
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import urlparse, parse_qs
from model import get_chat_model, get_embedding_model
import re
import os
from utils import download_subtitles
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret-key'

embedding_model = get_embedding_model()
chat_model = get_chat_model()

vectorstore = None
main_chain = None


def extract_youtube_id(url):
    if re.fullmatch(r'[a-zA-Z0-9_-]{11}', url):
        return url
    parsed_url = urlparse(url)
    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.strip('/')
    elif 'youtube.com' in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    return None

def extract_questions(response_text):
    # Simple split if LLM returns 1. ..., 2. ..., etc.
    import re, json
    response_text = response_text.replace("```json", "").replace('```', '')
    response_text = json.loads(response_text)
    return response_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_video', methods=['POST'])
def process_video():
    global vectorstore, main_chain

    url = request.form.get('video_url')
    transcript, status_code = download_subtitles(url, lang='en')
    video_id = extract_youtube_id(url)
    if status_code in [400, 500]:
        return jsonify({'error': transcript}), status_code

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer ONLY from provided transcript context.
        If the context is insufficient, Just say you don't know.
        Context: {context}
        Question: {question}
        """,
        input_variables=["context", "question"]
    )

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })

    prompt1 = PromptTemplate(
            template="""
            Generate 5 short questions that could be asked \
                from the following YouTube transcript as json like below\n '{{"qustion1" : "This is sample question", "question2" : "This is sample question"}}' transcript:\n\n{transcript}
            """,
            input_variables=["transcript"]
        )

    main_chain = parallel_chain | prompt | chat_model | StrOutputParser()

    questions_response_chain = prompt1 | chat_model | StrOutputParser()
    questions_response = questions_response_chain.invoke({'transcript' : transcript})
    questions = extract_questions(questions_response)
    questions['question'] = "Summarize this video"
    return jsonify({
    'message': 'Transcript processed successfully!',
    'video_id': video_id,
    "questions": questions
})


@app.route('/ask', methods=['POST'])
def ask():
    global main_chain
    question = request.form.get('question')
    if not main_chain:
        return jsonify({'error': 'Please process a video first.'}), 400
    result = main_chain.invoke(question)
    return jsonify({'answer': result})


if __name__ == '__main__':
    app.run(debug=True)
