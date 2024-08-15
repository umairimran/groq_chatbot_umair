# voice_assistant/audio.py

import speech_recognition as sr
import pygame
import time
import logging
import pydub
from io import BytesIO
from pydub import AudioSegment
# Configure logging
logging.basicConfig(level=logging.INFO)
def record_audio(file_path, timeout=10, phrase_time_limit=None, retries=3):
    recognizer = sr.Recognizer()
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                print("Calibrating for ambient noise...")
                recognizer.adjust_for_ambient_noise(source)
                print("Recording started")
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("Recording complete")
                
                # Save the audio data as a WAV file
                with open(file_path, "wb") as file:
                    file.write(audio_data.get_wav_data())
                return
        except sr.WaitTimeoutError:
            print(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            print(f"Failed to record audio: {e}")
            break
def play_audio(file_path):
    """
    Play an audio file using pygame.
    
    Args:
    file_path (str): The path to the audio file to play.
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
    except pygame.error as e:
        logging.error(f"Failed to play audio: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while playing audio: {e}")