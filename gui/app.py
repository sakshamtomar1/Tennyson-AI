import customtkinter as ctk
import threading
import time
from core.config import config
from ai.audio import audio
from ai.llm import llm
from skills.commands import executor

ctk.set_appearance_mode("Dark")

class TennysonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{config.NAME} Dashboard")
        self.geometry("600x400")

        self.status_lbl = ctk.CTkLabel(self, text="Status: Booting up...", text_color="grey")
        self.status_lbl.pack(pady=10)

        self.chat_box = ctk.CTkTextbox(self, width=500, height=250)
        self.chat_box.pack(pady=10)

        self.is_listening = True
        
        # THE MAC FIX: Wait 1 full second (1000ms) AFTER the window appears 
        # on screen before attempting to access the microphone hardware.
        self.after(1000, self.start_listening_thread)

    def start_listening_thread(self):
        self.status_lbl.configure(text="Status: Sleeping (Listening for Wake Word)", text_color="grey")
        # Now it is safe to turn on the mic!
        threading.Thread(target=self.wake_word_loop, daemon=True).start()

    def log(self, text: str):
        self.chat_box.insert("end", f"{text}\n\n")
        self.chat_box.see("end")

    def wake_word_loop(self):
        while self.is_listening:
            phrase = audio.listen()
            if any(w in phrase for w in config.WAKE_WORDS):
                self.status_lbl.configure(text="Status: Listening...", text_color="green")
                audio.speak("Yes?")
                command = audio.listen()
                
                if command:
                    self.log(f"You: {command}")
                    self.status_lbl.configure(text="Status: Processing...", text_color="yellow")
                    
                    # Try local OS command first, fallback to LLM
                    response = executor.process_command(command)
                    if not response:
                        response = llm.generate_response(command)
                        
                    self.log(f"{config.NAME}: {response}")
                    audio.speak(response)
                    
                self.status_lbl.configure(text="Status: Sleeping (Listening for Wake Word)", text_color="grey")
            time.sleep(0.5)