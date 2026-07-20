import sounddevice as sd
import soundfile as sf


def record_audio(filename="voice.wav", duration=5, samplerate=16000):
    print("🎤 Speak now...")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    sf.write(filename, audio, samplerate)

    print("✅ Recording saved.")

    return filename