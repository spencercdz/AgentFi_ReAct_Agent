from typing import List, Dict, TypedDict
from langchain_core.documents import Document

class GraphState(TypedDict):
    """State representation for LangGraph workflow"""
    question: str
    generation: str
    web_search_needed: str
    documents: List[Document]
    history: List[Dict[str, str]]

# Path configurations
WIKI_DB_PATH = "./data/simplewiki-latest-pages-articles.xml.bz2"
PERSIST_DIRECTORY = "./wikipedia_db"

# Model configurations
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"

# Search configurations
TAVILY_API_KEY = "your_tavily_api_key_here"
SEARCH_DEPTH = "advanced"
MAX_SEARCH_RESULTS = 3

# Retrieval configurations
RETRIEVAL_K = 5
SCORE_THRESHOLD = 0.65

# Text processing configurations
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 300