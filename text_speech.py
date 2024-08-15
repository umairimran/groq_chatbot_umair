from deepgram import DeepgramClient, SpeakOptions

DEEPGRAM_API_KEY = "8598f938ee0737a52402f6ead078a26f6c88faf4"


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

