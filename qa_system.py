import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains import RetrievalQA

load_dotenv()

def answer_question(question, video_id):
    """Answer question using PostgreSQL vector store"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")
    
    # Create embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Simple collection name (same as storage)
    collection_name = f"video_{video_id.replace('-', '_')}"
    
    # Connect to existing vector store
    vectorstore = PGVector(
        connection=database_url,
        embeddings=embeddings,
        collection_name=collection_name
    )
    
    # Set up LLM
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    
    # Get answer
    result = qa_chain.invoke(question)
    return result