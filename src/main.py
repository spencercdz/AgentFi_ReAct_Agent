from agent import create_agent  # Import the create_agent function directly

def main():
    print("Agent Fi, your all-in-one Finance Agent to Provide You with the Most Up To Date Financial Analysis! (Type 'exit' or 'quit' to end chat)")

    # Create the agent
    fi_agent = create_agent()  # Call the create_agent function directly

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Pleased to have helped you with FiAgent. Goodbye!")
            break
        
        response = fi_agent.run(user_input)
        print(f"Agent Fin: {response}")

if __name__ == "__main__":
    main()