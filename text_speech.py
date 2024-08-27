from deepgram import DeepgramClient, SpeakOptions
DEEPGRAM_API_KEY = "25dfc856a0652f84ff3e39100ae0a293bc8bec60"
FILENAME = "audio.mp3"
def create_audio(TEXT,actor):
    TEXT = {    
    "text": TEXT
}
    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        options = SpeakOptions(
            model=actor,
        )
        response = deepgram.speak.v("1").save(FILENAME, TEXT, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

