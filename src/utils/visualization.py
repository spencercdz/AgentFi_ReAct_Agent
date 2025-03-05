import tempfile
from IPython.display import Image, display
from langgraph.graph import StateGraph

def visualize_workflow(workflow: StateGraph, filename: str = "workflow.png"):
    """Visualize LangGraph workflow and display in notebook"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            # Generate and save visualization
            workflow.get_graph().draw_mermaid_png().save(tmpfile.name)
            
            # Display in notebook
            display(Image(filename=tmpfile.name))
            
            # Save permanent copy
            if filename:
                with open(filename, "wb") as f:
                    f.write(open(tmpfile.name, "rb").read())
                    
    except Exception as e:
        print(f"Visualization error: {str(e)}")
        return None

def print_state_transition(state_name: str, state_data: dict):
    """Print formatted state transition information"""
    print(f"\n🔀 Transitioning to {state_name} state:")
    print(f"- Current Question: {state_data.get('question', 'None')}")
    print(f"- Documents Count: {len(state_data.get('documents', []))}")
    print(f"- Web Search Needed: {state_data.get('web_search_needed', 'Unknown')}")
    print(f"- Generation Preview: {state_data.get('generation', 'None')[:200]}...")