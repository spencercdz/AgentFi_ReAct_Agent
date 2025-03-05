from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config.settings import LLM_MODEL

def create_qa_chain():
    """Create final QA generation chain"""
    prompt = ChatPromptTemplate.from_template(
        """As a financial analyst, answer the question using ONLY the context below.
        If unsure, state you don't know. Be detailed but concise.
        Always mention the source of your information.
        
        Context: {context}
        
        Question: {question}
        Answer:"""
    )
    
    return (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(x["documents"])
        )
        | prompt
        | ChatOllama(model=LLM_MODEL, temperature=0.3)
        | StrOutputParser()
    )

def format_docs(docs):
    """Format documents for context"""
    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}"
        for doc in docs
    )