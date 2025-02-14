import os
import openai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# API 호출
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me about the benefits of exercise."},
    ],
    max_tokens=150,
    temperature=0.7,
)

# 응답 출력
print(response['choices'][0]['message']['content'])
