from openai import OpenAI  
from os import getenv
from core.util.load_persona import load_persona

class ChatCore:
    def __init__(self):
        self.client = OpenAI(
            api_key=getenv("DESKTOP_PET_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    def get_response(self, message):
        model = "qwen-plus"
        persona = load_persona("ran")
        message = [
            {"role": "system", "content": persona["system_prompt"]},
            {"role": "user", "content": message}
        ]
        response = self.client.chat.completions.create(
            model=model,
            messages=message,
            max_tokens=4096
        )
        return response.choices[0].message.content

