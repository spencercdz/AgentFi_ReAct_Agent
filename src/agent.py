from langchain_community.llms import Ollama
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
import yfinance as yf

# Load Ollama LLM
llm = Ollama(model="llama3.2")  # Change model if needed

# Load vector store for RAG
def load_and_store_documents():
    loader = TextLoader("data/knowledge.txt")
    docs = loader.load()

    text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(split_docs, embeddings)
    
    return vectorstore

# Define agent tools
def get_tools():
    # Define existing tools
    search = DuckDuckGoSearchRun()
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    # Define the new yfinance tool
    def fetch_stock_data(ticker_symbol, start_date, end_date):
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        return stock_data.to_dict()

    def fetch_stock_balance_sheet():
        pass

    # List of all tools
    tools = [
        StructuredTool.from_function(name="Web Search", func=search.run, description="Searches the web for information."),
        StructuredTool.from_function(name="Wikipedia", func=wikipedia.run, description="Finds information from Wikipedia."),
        StructuredTool.from_function(name="Fetch Stock Data", func=fetch_stock_data, description="Fetch historical stock data from Yahoo Finance using the ticker symbol."),
    ]

    return tools

# Create agent with RAG and tools
def create_agent():
    vectorstore = load_and_store_documents()
    retriever = vectorstore.as_retriever()

    tools = get_tools()

    memory = ConversationBufferMemory(memory_key="chat_history")

    agent = initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        verbose=True,
        memory=memory,
        retriever=retriever
    )

    return agent
