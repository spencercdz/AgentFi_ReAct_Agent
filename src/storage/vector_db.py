from config.settings import PERSIST_DIRECTORY, EMBEDDING_MODEL
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from .document_processing import load_and_process_documents

def initialize_vector_store():
    """Initialize ChromaDB with processed documents."""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    documents = load_and_process_documents()
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="wiki_rag"
    )