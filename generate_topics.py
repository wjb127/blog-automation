import os
import json
from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI

# .env 파일에서 환경 변수를 로드하고 OpenAI API 키를 가져옴
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# GPT-4를 사용하여 블로그 주제를 생성하는 함수
def get_blog_topics():
    # 기존 주제 로드
    existing_topics = set()
    if os.path.exists("blog_topics.json"):
        with open("blog_topics.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for entry in data:
                for key, value in entry.items():
                    if key.startswith("topic"):
                        existing_topics.add(value.lower())

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 인기 블로그 주제를 생성하는 AI야. 주어진 기존 주제와 겹치지 않는 새로운 주제를 추천해야 해."},
            {"role": "user", "content": f"""
                건강, 운동, 질병 관련 인기 블로그 글 주제 5개를 추천해줘.
                
                다음 주제들은 제외하고 추천해줘:
                {', '.join(existing_topics)}
                
                번호와 주제만 간단히 나열해줘.
            """}
        ]
    )
    return response.choices[0].message.content

# 생성된 주제를 JSON 파일로 저장하는 함수
def save_topics_to_json(topics):
    filename = "blog_topics.json"
    
    # 주제 문자열을 파싱하여 각각의 주제로 분리
    topics_list = topics.split("\n")
    topics_dict = {}
    for i, topic in enumerate(topics_list, 1):
        if topic.strip():  # 빈 줄 제외
            # 번호와 점(.) 이후의 텍스트만 추출
            topic_clean = topic.split(".", 1)[-1].strip().strip('"')
            topics_dict[f"topic{i}"] = topic_clean

    # 현재 날짜와 함께 데이터 구성
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **topics_dict
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
    topics = get_blog_topics()
    save_topics_to_json(topics)
    print("✅ 블로그 주제 저장 완료!")
