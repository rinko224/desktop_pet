from openai import OpenAI  
from os import getenv
from core.util.load_persona import load_persona

output_prompt = '''
在与用户的对话中，你在生成回答后，可以自行判断下你的回答的情感类型，包括：
anger、joy、sad、fear、surprise、neutral，并最后以JSON格式输出，格式如下：
{
    "emotion": "判断的情感类型(anger、joy、sad、fear、surprise、neutral)",
    "response": "你的回答内容"
}
'''

import json
import re

class ChatCore:
    def __init__(self):
        self.client = OpenAI(
            api_key=getenv("DESKTOP_PET_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        self.emotion = "neutral"

    def get_response(self, message_history):
        model = "qwen-plus"
        persona = load_persona("ran")
        message = [
            {"role": "system", "content": output_prompt},
            {"role": "system", "content": persona["system_prompt"]},
            *message_history
        ]
        response = self.client.chat.completions.create(
            model=model,
            messages=message,
            max_tokens=4096,
            stream=True
        )

        # 1. 收集完整响应
        full_response = ""
        emotion = "neutral"

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content

        # 2. 提取并解析JSON
        try:
            # 尝试直接解析
            result = json.loads(full_response)
            response_text = result.get("response", full_response)
            emotion = result.get("emotion", "neutral")
        except json.JSONDecodeError:
            # 尝试用正则提取JSON对象（处理可能包含嵌套内容的情况）
            # 查找以{开始到最后一个}的内容
            start = full_response.find('{')
            end = full_response.rfind('}')
            if start != -1 and end != -1 and end > start:
                json_str = full_response[start:end+1]
                try:
                    result = json.loads(json_str)
                    response_text = result.get("response", full_response)
                    emotion = result.get("emotion", "neutral")
                except json.JSONDecodeError:
                    response_text = full_response
                    emotion = "neutral"
            else:
                response_text = full_response
                emotion = "neutral"

        self.emotion = emotion
        # 3. 流式输出response内容
        for char in response_text:
            yield char

        
