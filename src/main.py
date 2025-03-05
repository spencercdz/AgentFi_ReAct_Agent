from src.graph.workflow import build_agentic_workflow
from src.agents.agent import create_agent_executor

def main():
    workflow = build_agentic_workflow()
    agent = create_agent_executor()
    
    print("🤖 FiAgent Assistant Initialized!")
    while True:
        query = input("\n💬 User: ")
        if query.lower() in ["exit", "quit"]:
            break
        try:
            graph_state = workflow.invoke({"question": query})
            response = agent.invoke({
                "input": graph_state["generation"],
                "chat_history": agent.memory.buffer_as_str
            })
            print(f"\n🤖 FiAgent: {response['output']}")
        except Exception as e:
            print(f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    main()