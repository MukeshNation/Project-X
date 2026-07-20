from modules.voice.listener import record_audio
from modules.voice.speech_to_text import transcribe
from modules.voice.text_to_speech import speak
from modules.chatbot.service import ChatbotService

bot = ChatbotService()


def start_voice():

    audio = record_audio()

    text = transcribe(audio)

    print(f"\n🎤 You: {text}")

    reply = bot.ask(text)

    print(f"\n🤖 Nyra: {reply}")

    speak(reply)