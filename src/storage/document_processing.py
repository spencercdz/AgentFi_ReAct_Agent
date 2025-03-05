from config.settings import WIKI_DB_PATH
from langchain_core.documents import Document
from langchain.text_splitter import TokenTextSplitter
import bz2
import xml.etree.ElementTree as ET

def load_and_process_documents():
    """Load and process Wikipedia dump into documents."""
    docs = []
    with bz2.open(WIKI_DB_PATH, 'rt', encoding='utf8') as f:
        context = ET.iterparse(f, events=("end",))
        for event, elem in context:
            if elem.tag == 'page':
                title = elem.findtext('title', '').strip()
                text = elem.findtext('.//text', '').strip()
                if text and len(text) > 500:
                    docs.append(Document(
                        page_content="\n\n".join(text.split('\n\n')[:20]),
                        metadata={"title": title, "source": "wikipedia"}
                    ))
                elem.clear()
    
    splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=300)
    return splitter.split_documents(docs)
