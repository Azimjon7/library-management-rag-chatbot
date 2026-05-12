import shutil
import os
from langchain_chroma import Chroma
from src.config import DB_DIR
from src.document_loader import load_documents, split_documents
from src.model_factory import ModelFactory


def main():
    print("Loading documents from data/ ...")
    docs = load_documents()
    if not docs:
        raise ValueError("No documents found in data/ folder.")

    print(f"Loaded {len(docs)} documents. Splitting into chunks...")
    chunks = split_documents(docs)
    print(f"Created {len(chunks)} chunks.")

    if os.path.exists(DB_DIR):
        print("Removing old vector database...")
        shutil.rmtree(DB_DIR)

    print("Creating Chroma vector database...")
    Chroma.from_documents(
        documents=chunks,
        embedding=ModelFactory.create_embeddings(),
        persist_directory=DB_DIR,
    )
    print(f"Done. Vector database saved to {DB_DIR}/")


if __name__ == "__main__":
    main()
