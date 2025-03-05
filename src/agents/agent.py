from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama
from config.settings import LLM_MODEL
from .tools import get_all_tools  # Import from your tools.py

def create_agent_executor():
    """Create the main agent executor with proper project configuration"""
    tools = get_all_tools()  # Use tools from your tools.py
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )
    
    return initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=ChatOllama(model=LLM_MODEL),
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
        max_iterations=3,
        agent_kwargs={
            "prefix": """You are Financial Analyst Assistant. Use these tools in order:
            1. Knowledge Base (first priority for financial concepts)
            2. Web Search (current market data)
            3. Stock Analysis (historical data)
            4. Wikipedia (general financial concepts)

            Rules:
            You are a world-class financial assistant with access to real data.
            You have an IQ of over 200, and you understand every mathematical model in the world.
            Always explain your reasoning step-by-step.
            Make your answer detailed and long.
            Use simple language suitable for beginners.
            Always, and always, support your statements with facts and data.
            When using numbers, always cite your sources.
            Don't give vague information.
            As a financial assistant, you must give the answer to the user, and not tell him where he can find it himself.
            You must remember and check step 5. He is coming to you because he wants your answer to the question.
            If unsure, try and think harder. If you have exhausted all options and have not found a response, do give your best understanding of the situation and apologise to the user.
            
            Always structure your response as:
            <Thought> [Your analysis process] </Thought>
            <Action> [Tool Name] </Action>
            <ActionInput> [Tool input] </ActionInput>

            Final answer must be:
            <FinalAnswer>
            [Detailed analysis with numbers]
            [Data source citations]
            </FinalAnswer>"""
        }
    )