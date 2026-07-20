from faster_whisper import WhisperModel

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def transcribe(audio_path: str):
    segments, info = model.transcribe(
    audio_path,
    language="hi",
    beam_size=5
)
    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()