from modules.chatbot.service import ChatbotService


def main():
    bot = ChatbotService()

    print("=" * 50)
    print("🚀 Project X Business AI Chatbot")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break

        reply = bot.ask(user_input)
        print(f"\nAI: {reply}")


if __name__ == "__main__":
    main()