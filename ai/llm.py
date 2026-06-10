from openai import OpenAI
from core.config import config
from core.database import db

class AIEngine:
    def __init__(self):
        self.provider = config.DEFAULT_MODEL
        if self.provider == "openai":
            self.client = OpenAI(api_key=config.OPENAI_KEY)

    def generate_response(self, prompt: str) -> str:
        db.log_chat("user", prompt)
        
        if self.provider == "openai":
            res = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are {config.NAME}, a desktop AI."},
                    {"role": "user", "content": prompt}
                ]
            ).choices[0].message.content
        else:
            res = "Model not configured in minimal setup."
            
        db.log_chat("assistant", res)
        return res

llm = AIEngine()