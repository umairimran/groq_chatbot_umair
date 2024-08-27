import os
from groq import Groq

api = "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"
client = Groq(api_key=api)
# Correctly join the file path
def transcribe(audio_file="combined_speechh.mp3"):

    filename = os.path.join(os.path.dirname(__file__), audio_file)
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),  # Ensure this format is correct based on API documentation
            model="whisper-large-v3",
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
    )

    return transcription.text
