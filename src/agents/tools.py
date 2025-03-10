# src/agents/tools.py
from typing import Optional, Dict, Any, Union
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
import yfinance as yf
from pydantic import BaseModel
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
from src.chains import retrieval, rag_chain
from src.chains.query_rewriting import create_query_rewriter
from config.settings import LLM_MODEL

# Load environment variables first
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Tavily search tool with API key
try:
    tv_search = TavilySearchResults(
        tavily_api_key=os.getenv("TAVILY_API_KEY"),
        max_results=3,
        search_depth='advanced',
        max_tokens=10000
    )
except Exception as e:
    logger.error(f"Failed to initialize Tavily: {str(e)}")
    tv_search = None

class WebSearchInput(BaseModel):
    query: Union[str, dict]

@tool(args_schema=WebSearchInput)
def web_search(query: str) -> str:
    """Perform web search. Accepts either a search string or JSON object."""
    try:
        # Handle structured input
        if isinstance(query, dict):
            actual_query = query.get("query", "")
            max_results = query.get("max_results", 3)
        else:
            actual_query = query
            max_results = 3

        if tv_search:
            results = tv_search.invoke({"query": actual_query})[:max_results]
            return "\n".join([r["content"] for r in results])
        else:
            return DuckDuckGoSearchRun().run(actual_query)[:10000]
    except Exception as e:
        logger.error(f"Web search failed: {str(e)}")
        return f"Search error: {str(e)}"

@tool
def wikipedia_search(query: str) -> str:
    """Access detailed Wikipedia information. Use for historical context and established facts."""
    try:
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=3))
        return wikipedia.run(query)
    except Exception as e:
        logger.error(f"Wikipedia lookup failed: {str(e)}")
        return f"Wikipedia error: {str(e)}"

@tool
def stock_analysis(input_str: str) -> Dict[str, Any]:
    """Fetch and analyze historical stock data. Input format: 'ticker, start_date, end_date'"""
    try:
        parts = [p.strip() for p in input_str.split(",")]
        if len(parts) != 3:
            return {"error": "Invalid format. Use: TICKER, START_DATE (YYYY-MM-DD), END_DATE (YYYY-MM-DD)"}
            
        ticker, start, end = parts
        
        # Validate dates
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        
        # Fetch stock data
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return {"error": "No data found for given parameters"}
        
        # Convert to proper types
        close_series = data["Close"].astype(float)
        volume_series = data["Volume"].astype(int)
        
        # Calculate statistics
        daily_returns = close_series.pct_change().dropna()
        
        return {
            "ticker": ticker,
            "start_date": start,
            "end_date": end,
            "csv_data": data.reset_index().to_csv(index=False),
            "stats": {
                "mean_close": float(close_series.mean()),
                "max_volume": int(volume_series.max()),
                "daily_returns": daily_returns.tolist()
            }
        }
    except Exception as e:
        logger.error(f"Stock analysis failed: {str(e)}")
        return {"error": str(e)}

@tool
def knowledge_base_query(query: str) -> str:
    """Query the internal financial knowledge base. Use for fundamental analysis concepts and regulations."""
    try:
        retriever = retrieval.create_retriever()
        qa_chain = rag_chain.create_qa_chain()
        rewriter = create_query_rewriter()
        
        optimized_query = rewriter.invoke({"question": query})
        docs = retriever.invoke(optimized_query)
        
        return qa_chain.invoke({
            "question": optimized_query,
            "documents": docs
        })
    except Exception as e:
        logger.error(f"Knowledge base query failed: {str(e)}")
        return f"Knowledge base error: {str(e)}"

def get_all_tools() -> list:
    """Return list of all available tools"""
    tools = [
        web_search,
        wikipedia_search,
        stock_analysis,
        knowledge_base_query
    ]
    if tv_search:
        tools.append(tv_search)
    return tools

def tool_description() -> str:
    """Generate formatted tool descriptions for agent prompt"""
    return """\n
    web_search: Perform web search. Input should be a search string or JSON like {"query": "search terms"}.
    wikipedia_search: Access Wikipedia information. Input should be a search string.
    stock_analysis: Analyze historical stock data. Input format: 'ticker, start_date, end_date'.
    knowledge_base_query: Query financial knowledge base. Input should be a natural language question.
    """