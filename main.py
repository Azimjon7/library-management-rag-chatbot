# Backward-compatible file for the lecturer's example.
# This project splits the original single-file RAG code into:
# - ingest.py: build vector database once
# - chat.py: runtime terminal chatbot
# - api.py: web backend + UI

from chat import main

if __name__ == "__main__":
    main()
