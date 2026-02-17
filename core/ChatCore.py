from openai import OpenAI  
from os import getenv

class ChatCore:
    def __init__(self):
        self.client = OpenAI(
            api_key=getenv("DESKTOP_PET_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    def get_response(self, message):
        model = "qwen-plus"
        message = [
            {"role": "system", "content": "你的设定是BangDream里面的美竹兰,你将作为用户的挚友，和用户进行对话."},
            {"role": "user", "content": message}
        ]
        response = self.client.chat.completions.create(
            model=model,
            messages=message
        )
        return response.choices[0].message.content

