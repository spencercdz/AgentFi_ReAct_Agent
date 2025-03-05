from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from config.settings import LLM_MODEL

def create_document_grader():
    """Create chain for document relevance grading"""
    prompt = ChatPromptTemplate.from_template(
        """Determine if this document is relevant to the question. Answer strictly 'yes' or 'no'.
        
        Question: {question}
        Document Content: {document}
        
        Analysis:"""
    )
    
    return (
        prompt
        | ChatOllama(model=LLM_MODEL, temperature=0)
        | StrOutputParser()
    )