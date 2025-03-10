from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config.settings import (
    PERSIST_DIRECTORY,
    EMBEDDING_MODEL,
    RETRIEVAL_K,
    SCORE_THRESHOLD
)

def create_retriever():
    """Create similarity threshold retriever with ChromaDB"""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Initialize existing vector store
    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name="wiki_rag"
    )
    
    return vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": RETRIEVAL_K,
            "score_threshold": SCORE_THRESHOLD,
            "filter": {"source": "wikipedia"}
        }
    )