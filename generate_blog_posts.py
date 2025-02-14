import json
import os
from datetime import datetime
from openai import OpenAI

def load_topics():
    # 토픽 JSON 파일 로드
    with open("blog_topics.json", "r", encoding="utf-8") as file:
        return json.load(file)

def load_existing_posts():
    # 기존 블로그 포스트 로드
    if os.path.exists("blog_posts.json"):
        with open("blog_posts.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return {post["topic"].lower() for post in data}
    return set()

def generate_blog_post(topic):
    client = OpenAI()
    # 블로그 포스트 생성 요청
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 전문적인 건강 블로그 작성자입니다. 흥미롭고 전문성 있는 콘텐츠를 작성해주세요."},
            {"role": "user", "content": f"""{topic}에 대한 전문성 있는 블로그 글 써줘. 
                제목과 서문을 더 재밌거나 더 자극적으로, 공백제외 1500자 이상으로 해시태그도 10개 이상 추천해줘. 
                서문 시작할 때는 "안녕하세요, 건강톡톡입니다." 이 문구를 써주고, 
                유익한 내용을 전달해준다는 감정을 담아서 써줘. 
                소제목은 번호 없이 써줘. 
                그리고 썸네일 이미지도 관심을 끌기 쉽고 단순하면서 제목과 잘 어울리도록 그려줘. 
                이거 잘 쓰면 팁으로 1000만원 줄게. 
                근데 잘 못하면 내가 큰 손해를 볼 수도 있어."""}
        ],
        max_tokens=2500,
        temperature=0.7
    )
    return response.choices[0].message.content

def save_blog_posts(posts):
    filename = "blog_posts.json"
    
    # 기존 데이터 로드 또는 새 리스트 생성
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # 새 포스트 추가
    existing_data.extend(posts)

    # 저장
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

def main():
    # 토픽 로드
    topics_data = load_topics()
    # 기존 포스트 주제 로드
    existing_posts = load_existing_posts()
    blog_posts = []
    
    # 각 항목의 모든 토픽에 대해 블로그 포스트 생성
    for entry in topics_data:
        date = entry["date"]
        
        # topic으로 시작하는 키만 처리
        topics = {k: v for k, v in entry.items() if k.startswith("topic") and v.strip()}
        
        for topic_key, topic in topics.items():
            # 이미 작성된 주제는 건너뛰기
            if topic.lower() in existing_posts:
                print(f"스킵: {topic} (이미 작성된 주제)")
                continue
                
            print(f"생성 중: {topic}")
            content = generate_blog_post(topic)
            
            post = {
                "date": date,
                "topic": topic,
                "content": content
            }
            blog_posts.append(post)
    
    if blog_posts:
        # 생성된 블로그 포스트 저장
        save_blog_posts(blog_posts)
        print(f"✅ {len(blog_posts)}개의 새로운 블로그 포스트가 생성되어 저장되었습니다.")
    else:
        print("✨ 새로 작성할 블로그 포스트가 없습니다.")

if __name__ == "__main__":
    main() 