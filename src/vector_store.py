import os
from langchain_chroma import Chroma
from .config import DB_DIR
from .model_factory import ModelFactory


class VectorStoreManager:
    """Singleton pattern: reuse one vector store connection at runtime."""

    _instance = None

    @classmethod
    def get_vector_store(cls):
        if cls._instance is None:
            if not os.path.exists(DB_DIR):
                raise RuntimeError("Vector database not found. Run: python ingest.py")
            cls._instance = Chroma(
                persist_directory=DB_DIR,
                embedding_function=ModelFactory.create_embeddings(),
            )
        return cls._instance
