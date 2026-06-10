import speech_recognition as sr
import threading
import subprocess

class AudioManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # LAZY INIT FIX: Set this to None on startup so it doesn't trigger macOS security
        self.microphone = None 

    def speak(self, text: str):
        def _speak():
            safe_text = text.replace("'", "").replace('"', "")
            subprocess.run(["say", safe_text])
        threading.Thread(target=_speak, daemon=True).start()

    def listen(self) -> str:
        # Turn on the microphone ONLY when the listen loop actually starts
        if self.microphone is None:
            self.microphone = sr.Microphone()

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio_data = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                return self.recognizer.recognize_google(audio_data).lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""

audio = AudioManager()