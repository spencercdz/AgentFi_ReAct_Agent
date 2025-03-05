# src/graph/nodes.py
from typing import Dict, Any
from langchain_core.documents import Document
from src.chains.query_rewriting import create_query_rewriter
from src.chains.retrieval import create_retriever
from src.chains.grading import create_document_grader
from src.chains.rag_chain import create_qa_chain
from config.settings import GraphState

def retrieve_node(state: GraphState) -> Dict[str, Any]:
    """Retrieve documents from the vector store."""
    print("📚 Retrieving documents...")
    retriever = create_retriever()
    return {"documents": retriever.invoke(state["question"])}

def grade_documents_node(state: GraphState) -> Dict[str, Any]:
    """Grade document relevance."""
    print("📊 Grading documents...")
    grader = create_document_grader()
    filtered_docs = []
    web_search_needed = "No"
    
    for doc in state["documents"]:
        score = grader.invoke({"question": state["question"], "document": doc.page_content})
        if score.strip().lower() == "yes":
            filtered_docs.append(doc)
        else:
            web_search_needed = "Yes"
    
    return {
        "documents": filtered_docs,
        "web_search_needed": web_search_needed
    }

def rewrite_query_node(state: GraphState) -> Dict[str, Any]:
    """Rewrite the query for better retrieval."""
    print("🔍 Rewriting query...")
    rewriter = create_query_rewriter()
    better_question = rewriter.invoke({"question": state["question"]})
    return {"question": better_question}

def web_search_node(state: GraphState) -> Dict[str, Any]:
    """Perform web search."""
    print("🌐 Searching web...")
    from src.agents.tools import web_search
    results = web_search(state["question"])
    return {"documents": [Document(page_content=results)]}

def generate_answer_node(state: GraphState) -> Dict[str, Any]:
    """Generate the final answer."""
    print("💡 Generating answer...")
    qa_chain = create_qa_chain()
    return {"generation": qa_chain.invoke(state)}

def decide_next_step(state: GraphState) -> str:
    """Decide the next step in the workflow."""
    return "rewrite_query" if state["web_search_needed"] == "Yes" else "generate_answer"

__all__ = [
    "retrieve_node",
    "grade_documents_node",
    "rewrite_query_node",
    "web_search_node",
    "generate_answer_node",
    "decide_next_step"
]