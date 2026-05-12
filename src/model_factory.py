from langchain_ollama import ChatOllama, OllamaEmbeddings
from .config import EMBED_MODEL, LLM_MODEL, LLM_NUM_PREDICT, OLLAMA_BASE_URL, OLLAMA_TIMEOUT


class ModelFactory:
    """Factory Method pattern: creates model objects from configuration."""

    @staticmethod
    def create_llm():
        return ChatOllama(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.2,
            num_predict=LLM_NUM_PREDICT,
            client_kwargs={"timeout": OLLAMA_TIMEOUT},
        )

    @staticmethod
    def create_embeddings():
        return OllamaEmbeddings(
            model=EMBED_MODEL,
            base_url=OLLAMA_BASE_URL,
            client_kwargs={"timeout": OLLAMA_TIMEOUT},
        )
