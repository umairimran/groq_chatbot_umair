import pyaudio
import numpy as np
import webrtcvad
import wave
import os
from scraping_response import *
from audio import *
from pyannote.audio import Model
from jarvis import *
from pydub.playback import play
import os
from pyannote.audio.pipelines import VoiceActivityDetection
from pydub import AudioSegment
import pyttsx3

######audio setup
# Set up audio parameters
SAMPLE_RATE = 16000
FRAME_DURATION_MS = 30  # Duration of each frame in milliseconds
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)
conversation_history = ""
# Create a VAD object
vad = webrtcvad.Vad()
# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=FRAME_SIZE)

# Initialize WAV file writing
temp_wav_file = "temp.wav"
wav_file = wave.open(temp_wav_file, "wb")
wav_file.setnchannels(1)
wav_file.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
wav_file.setframerate(SAMPLE_RATE)





####### using the model to detect the speech
# Replace 'YOUR_AUTH_TOKEN' with your actual Hugging Face token
model = Model.from_pretrained('pyannote/segmentation-3.0', use_auth_token='xJVrQgqVRnTNDNVzMTQDBqWKFpyHdwrosu')
pipeline = VoiceActivityDetection(segmentation=model)
HYPER_PARAMETERS = {
    "min_duration_on": 0.5,
    "min_duration_off": 0.5
}
pipeline.instantiate(HYPER_PARAMETERS)






##### api key 
api = "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"






##### declarations
chat_history=[]




#### functions 
def get_response_from_groq(history):
    client = Groq(api_key=api)
    chat_completion = client.chat.completions.create(
        messages=history,
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content
def format_history_from_groq(history):
    messages = []
    for message in history:
        messages.append({"role": "user", "content": message["human"]})
        messages.append({"role": "assistant", "content": message["AI"]})
    return messages
def check_if_playable(file_path):
    try:
        # Load the audio file to check if it is playable
        audio = AudioSegment.from_file(file_path)

        # If loading is successful, the file is considered playable
        print(f"The file {file_path} is playable.")
        return True

    except Exception as e:
        # If an error occurs during loading, the file is not playable
        print(f"The file {file_path} is not playable: {e}")
        return False
def speak_with_customizations(message, voice_index=0, speed=150):
    """Initialize the TTS engine, set voice and speed, and speak a message.

    Args:
        message (str): The message to be spoken.
        voice_index (int): Index of the voice to use (default is 0).
        speed (int): Speech rate (words per minute) (default is 200).
    """
    engine = pyttsx3.init()
    
    # Set voice
    voices = engine.getProperty('voices')
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
        print(f"Voice set to: {voices[voice_index].name}")
    else:
        print(f"Invalid voice index: {voice_index}")
    
    # Set speed
    engine.setProperty('rate', speed)
    print(f"Speech rate set to: {speed} words per minute")

    # Speak the message
    engine.say(message)
    engine.runAndWait()
def check_file_and_process(file_path):
    # Check if the file exists
    if os.path.isfile(file_path):
        # Check if the file is playable
        if check_if_playable(file_path):
            # Proceed with transcription
            transcription_result = transcribe(file_path)
            formatted_history = format_history_from_groq(chat_history)
            formatted_history.append({"role": "user", "content": transcription_result})
            response_text = get_response_from_groq(formatted_history)
            chat_history.append({"human": transcription_result, "AI": response_text})
            print(chat_history)
            print(f"Transcription result: {transcription_result}")
            speak_with_customizations(response_text, voice_index=1, speed=200)
            # Proceed with playback (optional, as it's already checked in check_if_playable)
           
            print(f"Successfully played {file_path}.")
            
            # Chat-like response
            response = "The file was successfully processed and played."
        
        else:
            response = "The file is not playable."
    
    else:
        response = f"The file {file_path} does not exist."

    # Return or print the chat-like response
    print(response)
    return response
def extract_speech_segments(audio_file, output_file="combined_speechh.mp3"):
    # Run Voice Activity Detection on the audio file
    vad = pipeline(audio_file)
    # Load the audio file
    audio = AudioSegment.from_wav(audio_file)
    # Create an empty AudioSegment for concatenation
    combined_audio = AudioSegment.empty()
    
    # Extract and combine speech segments
    for segment in vad.get_timeline().support():
        start_time = segment.start
        end_time = segment.end
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)
        segment_audio = audio[start_ms:end_ms]
        combined_audio += segment_audio  # Append the segment to the combined audio
    
    # Export the combined audio to MP3 format
    combined_audio.export(output_file, format="mp3")
    print(f"Saved combined speech segments to: {output_file}")

