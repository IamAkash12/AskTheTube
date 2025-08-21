import os
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import hashlib

load_dotenv()

def store_transcript_as_embeddings(transcript, video_id):
    """Store transcript as embeddings in PostgreSQL"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")
    
    # Split transcript
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_text(transcript)
    
    # Create embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Simple collection name from video ID
    collection_name = f"video_{video_id.replace('-', '_')}"
    connection = database_url
    # Store in PostgreSQL
    vectorstore = PGVector.from_texts(
        texts=texts,
        embedding=embeddings,
        connection=connection,
        collection_name=collection_name,
        pre_delete_collection=True
    )
    
    return vectorstore