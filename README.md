# 📔✨ Divine’s Blog Companion

**Divine’s Blog Companion** is an AI-powered writing assistant designed to help me brainstorm, revise, and enhance blog drafts. Leveraging **Google's Gemini model** and a **FAISS-based semantic search engine**, this tool uses my own high-quality articles to provide context-aware feedback and suggestions.

---

## ✨ Features

- 🧠 **Contextual Suggestions**: Pulls relevant content from a local article vector store to guide the improvement of your draft.
- ✍️ **LLM-powered Feedback**: Uses Gemini 2.0 Flash for quick, thoughtful responses.
- 🗃️ **Custom Knowledge Base**: Vector database built from previously written articles or blogs.
- 🎯 **Prompt Template Control**: Easily adjustable instructions via `prompt.txt`.

---

## 🧱 Tech Stack

- [LangChain](https://github.com/langchain-ai/langchain)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Streamlit](https://streamlit.io/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/blog-companion.git
cd blog-companion

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
