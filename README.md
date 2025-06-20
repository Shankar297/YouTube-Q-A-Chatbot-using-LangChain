# 🎥 YouTube Q&A Chatbot using LangChain + RAG

An AI-powered chatbot that lets you **ask questions about any YouTube video** and get accurate, real-time answers — without watching the full video!

This project uses **LangChain**, **FAISS**, and **LLMs (OpenAI or Gemini)** to implement **Retrieval-Augmented Generation (RAG)** on YouTube video transcripts.

---

## 🚀 Features

- 🔍 Extracts transcript from any YouTube video using `yt_dlp`
- 🧠 Converts transcript into vector embeddings with **FAISS**
- 💬 Allows natural language question-answering on the transcript
- 🔗 Powered by **LangChain + RAG** architecture
- 🤖 Works with both **OpenAI** or **Gemini** models
- ⚡ Fast, scalable, and easy to customize


---

## 📦 Tech Stack

* `Python`
* `LangChain`
* `FAISS`
* `yt_dlp`
* `OpenAI API` or `Google Gemini API`
* `tiktoken` (for token-aware chunking)
* `Streamlit` or terminal interface

---

## 📁 Project Structure

```
youtube-qa-chatbot/
├── app.py                # Entry point for running the chatbot
├── utils.py              # Helper functions
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
├── templates/index.html  # UI file
├── static/style.css      # css
```

---

## 🔧 Virtual Environment Setup & Running App

Follow these steps to set up and run the chatbot locally:

1. **Clone the repository**

   ```bash
   git clone https://github.com/Shankar297/YouTube-Q-A-Chatbot-using-LangChain.git
   cd YouTube-Q-A-Chatbot-using-LangChain
   ```

2. **Create and activate a virtual environment**

   * On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   * On Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root with your keys:

   ```env
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   ```

5. **Run the application**

   ```bash
   python app.py
   ```
---

## 🔓 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

* [LangChain](https://github.com/langchain-ai/langchain)
* [FAISS](https://github.com/facebookresearch/faiss)
* [OpenAI](https://platform.openai.com/)
* [Google Gemini](https://ai.google.dev/)
* [yt\_dlp](https://github.com/yt-dlp/yt-dlp)

---

## 🌟 Support

If you found this project helpful:

* ⭐ Star the repo
* 🔁 Share it with friends
* 🧠 Contribute via Issues/PRs

