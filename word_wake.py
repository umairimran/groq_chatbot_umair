
import sys
import threading 
import tkinter as tk
import speech_recognition 
import pyttsx3 as tts

from neuralintents import GenericAssistant
class Assistant:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty('rate', 150)
        self.assistant = GenericAssistant('intents.json')
        self.assistant.load_model()  # Use load_model instead of train_model
        self.root = tk.Tk()
        self.label = tk.Label(self.root, text="Assistant is listening...", font="Arial 20")
        self.label.pack()
        threading.Thread(target=self.run_assistant).start()
        self.root.mainloop()

    def create_file(self):
        with open("somefile.txt", "w") as file:
            file.write("This is a file created by the assistant")

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)
                    text = self.recognizer.recognize_google(audio)

                    if "hey umair" in text:
                        self.label.config(text="Assistant is listening...")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say(text="Assistant is stopped")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                                self.label.config(fg="black", text=response)

            except Exception as e:
                self.label.config(fg="black", text=f"An error occurred: {e}")
                continue
Assistant()