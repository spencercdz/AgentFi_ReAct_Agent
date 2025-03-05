# src/graph/workflow.py
from langgraph.graph import StateGraph, END
from .nodes import (
    retrieve_node,
    grade_documents_node,
    rewrite_query_node,
    web_search_node,
    generate_answer_node,
    decide_next_step
)
from config.settings import GraphState

def build_agentic_workflow():
    """Build the LangGraph workflow."""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade_documents", grade_documents_node)
    workflow.add_node("rewrite_query", rewrite_query_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("generate_answer", generate_answer_node)
    
    # Set entry point
    workflow.set_entry_point("retrieve")
    
    # Add edges
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_next_step,
        {"rewrite_query": "rewrite_query", "generate_answer": "generate_answer"}
    )
    workflow.add_edge("rewrite_query", "web_search")
    workflow.add_edge("web_search", "generate_answer")
    workflow.add_edge("generate_answer", END)
    
    return workflow.compile()