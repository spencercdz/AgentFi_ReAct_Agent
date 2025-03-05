from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from config.settings import LLM_MODEL

def create_query_rewriter():
    """Create query optimization chain"""
    prompt = ChatPromptTemplate.from_template(
        """Rephrase this question for improved retrieval and web search.
        Maintain the original intent while using optimal search terms.
        Include important financial terminology when relevant.
        
        Original Question: {question}
        Improved Question:"""
    )
    
    return (
        prompt
        | ChatOllama(model=LLM_MODEL, temperature=0.2)
        | StrOutputParser()
    )