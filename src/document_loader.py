from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import DATA_DIR


def load_documents():
    """Loads PDF, TXT, and Markdown documentation from the data folder."""
    loaders = [
        DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True),
        DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader, show_progress=True),
        DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader, show_progress=True),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs


def split_documents(docs):
    """Splits docs into overlapping chunks to preserve context across boundaries."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )
    return splitter.split_documents(docs)
