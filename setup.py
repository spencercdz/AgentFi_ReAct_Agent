# setup.py
from setuptools import setup, find_packages

setup(
    name="financial_assistant",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langgraph",
        "ollama",
        "yfinance",
        "duckduckgo-search",
        "tavily-python",
        "chromadb",
    ],
)