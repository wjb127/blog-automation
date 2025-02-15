import os
import json
from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI, OpenAIError
import time
import logging

# .env 파일에서 환경 변수를 로드하고 OpenAI API 키를 가져옴
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f'api_requests_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()  # 콘솔 출력 추가
    ]
)

# GPT-4를 사용하여 블로그 주제를 생성하는 함수
def get_blog_topics():
    try:
        # 기존 주제 로드
        existing_topics = set()
        if os.path.exists("blog_topics.json"):
            with open("blog_topics.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for entry in data:
                    for key, value in entry.items():
                        if key.startswith("topic"):
                            existing_topics.add(value.lower())

        logging.info("API 요청 시작")
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 인기 블로그 주제를 생성하는 AI야. 주어진 기존 주제와 겹치지 않는 새로운 주제를 추천해야 해."},
                {"role": "user", "content": f"""
                    성병 관련 자극적인 인기 블로그 글 주제 1개를 추천해줘.
                    
                    다음 주제들은 제외하고 추천해줘:
                    {', '.join(existing_topics)}
                    
                    번호 없이 주제만 간단히 작성해줘.
                """}
            ]
        )
        logging.info("API 요청 성공")
        return response.choices[0].message.content
    except OpenAIError as e:
        logging.error(f"API 오류 발생: {str(e)}")
        print("🕐 API 요청이 너무 많습니다. 2분 후 다시 시도합니다...")
        time.sleep(120)
        return get_blog_topics()

# 생성된 주제를 JSON 파일로 저장하는 함수
def save_topics_to_json(topic):
    filename = "blog_topics.json"
    
    # 현재 날짜와 함께 데이터 구성
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic.strip().strip('"')
    }

    # 기존 데이터 로드 또는 새 리스트 생성
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(new_entry)

    # 저장
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

# 메인 실행 부분
if __name__ == "__main__":
    # 블로그 주제 생성 및 저장
    topic = get_blog_topics()
    save_topics_to_json(topic)
    print("✅ 블로그 주제 저장 완료!")
