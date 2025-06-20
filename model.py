from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()


def get_embedding_model(model_type='hugging_face'):
    if model_type == 'open_ai':
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    elif model_type == 'hugging_face':
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    else:
        print("please select model_type as hugging_face or open_ai")
        embeddings = None
    return embeddings


def get_chat_model(model_type='google'):
    if model_type == 'open_ai':
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    elif model_type == 'google':
        model = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=os.getenv('api_key'))
    else:
        print("please select model_type as google or open_ai")
        model = None
    return model