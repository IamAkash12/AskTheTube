# Ask The Tube

 Ask The Tube is a Python project that fetches a YouTube video transcript and allows you to ask questions about the video using **LangChain**, **ChromaDB**, and **OpenAI** (RAG-based system).

---

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies.

```bash
pip install youtube-transcript-api
pip install langchain
pip install langchain-openai
pip install langchain-chroma
pip install python-dotenv
```

## Environment Setup

Create a .env file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```
## Usage

Run the program from the terminal:

```bash
python main.py
```
## Project Structure

- get_transcript.py → Fetches transcript from YouTube
- store_embeddings.py → Stores transcript as embeddings in ChromaDB
- qa_system.py → Sets up RetrievalQA for answering questions
- main.py → CLI entry point for the system

## Dependencies

- youtube-transcript-api → Fetches YouTube video transcripts
- youtube-transcript-api → Fetches YouTube video transcripts
- langchain-openai → OpenAI LLM & Embeddings
- langchain-chroma → Vector storage with ChromaDB
- python-dotenv → Load environment variables

