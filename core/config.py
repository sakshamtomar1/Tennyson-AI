import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        with open("config.yaml", "r") as f:
            self.settings = yaml.safe_load(f)
        self.OPENAI_KEY = os.getenv("OPENAI_API_KEY")
        self.GEMINI_KEY = os.getenv("GEMINI_API_KEY")
        self.NAME = self.settings["assistant"]["name"]
        self.WAKE_WORDS = self.settings["assistant"]["wake_words"]
        self.DB_PATH = self.settings["database"]["path"]
        self.DEFAULT_MODEL = self.settings["assistant"]["default_model"]

config = Config()