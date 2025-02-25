from langchain.prompts import PromptTemplate

def get_prompt():
    """Returns a formatted prompt template for the agent."""
    
    prompt = PromptTemplate(
        input_variables=["question"],
        template="You are a helpful AI assistant. Answer the following question: {question}"
    )
    
    return prompt