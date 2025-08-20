import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

def answer_question(question, persist_directory="db"):
    # Load vector DB and embeddings
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    # Set up LLM
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Set up RetrievalQA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )

    # Run query
    answer = qa.invoke(question)
    return answer
