from src.rag_service import RagService


def main():
    print("Library Management RAG Chatbot")
    print("Type 'exit' to quit.\n")
    bot = RagService()

    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            break

        answer, sources = bot.ask(question)
        print("\nBot:", answer)
        print("\nSources:")
        if sources:
            for i, src in enumerate(sources, start=1):
                print(f"{i}. {src['source']}, page={src['page']}")
        else:
            print("No relevant source found.")
        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
