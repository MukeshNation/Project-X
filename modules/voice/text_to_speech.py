import subprocess

def speak(text: str):
    subprocess.run(["say", text])