import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

def load_topics():
    try:
        # 토픽 JSON 파일 로드
        with open("blog_topics.json", "r", encoding="utf-8") as file:
            topics = json.load(file)
            if not topics:  # 빈 리스트인 경우
                print("⚠️ blog_topics.json 파일이 비어있습니다.")
            return topics
    except FileNotFoundError:
        print("❌ blog_topics.json 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError:
        print("❌ blog_topics.json 파일의 형식이 올바르지 않습니다.")
        return []
    except Exception as e:
        print(f"❌ 토픽 로드 중 오류 발생: {str(e)}")
        return []

def load_existing_posts():
    # 기존 블로그 포스트 로드
    if os.path.exists("blog_posts.json"):
        with open("blog_posts.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return {post["topic"].lower() for post in data}
    return set()

def generate_blog_post(topic):
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "당신은 건강 관련 블로그 포스트를 작성하는 전문가입니다."},
                {"role": "user", "content": f"다음 주제로 블로그 포스트를 작성해주세요: {topic}\n\n"
                                          f"포스트는 다음을 포함해야 합니다:\n"
                                          f"- 제목\n"
                                          f"- 서문\n"
                                          f"- 본문\n"
                                          f"- 해시태그\n"
                                          f"- 썸네일 이미지 설명\n\n"
                                          f"1500자 이상으로 작성해주세요."}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        content = response.choices[0].message.content
        char_count = len(content)
        
        if char_count < 1500:
            print(f"⚠️ 경고: 생성된 콘텐츠가 1500자 미만입니다 ({char_count}자)")
        
        return content, char_count
        
    except Exception as e:
        print(f"❌ 콘텐츠 생성 중 오류 발생: {str(e)}")
        raise

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

def get_unwritten_topics():
    try:
        # 기존에 작성된 포스트 주제들 로드
        existing_posts = load_existing_posts()
        
        # 전체 토픽 로드
        topics_data = load_topics()
        
        if not topics_data:
            print("⚠️ 처리할 토픽이 없습니다.")
            return []
            
        # 데이터 구조 정규화
        normalized_topics = []
        for entry in topics_data:
            # topic으로 시작하는 모든 키에서 비어있지 않은 주제 추출
            for key, value in entry.items():
                if key.startswith('topic') and value.strip():
                    normalized_topics.append({
                        "date": entry["date"],
                        "topic": value.strip()
                    })
        
        # 작성되지 않은 주제만 필터링
        unwritten_topics = [
            entry for entry in normalized_topics 
            if entry["topic"].lower() not in existing_posts
        ]
        
        print(f"📝 전체 토픽 수: {len(normalized_topics)}, 미작성 토픽 수: {len(unwritten_topics)}")
        return unwritten_topics
        
    except Exception as e:
        print(f"❌ 미작성 토픽 확인 중 오류 발생: {str(e)}")
        return []

def main():
    unwritten_topics = get_unwritten_topics()
    
    if not unwritten_topics:
        print("✨ 모든 주제의 글이 작성되었습니다!")
        return
        
    entry = unwritten_topics[0]
    topic = entry.get("topic", "").strip()
    
    if not topic:
        print(f"❌ 유효하지 않은 주제입니다. 주제 데이터: {entry}")
        return
        
    print(f"생성 중: {topic}")
    try:
        content, char_count = generate_blog_post(topic)
        
        post = {
            "date": entry["date"],
            "topic": topic,
            "content": content,
            "char_count": char_count
        }
        
        save_blog_posts([post])
        print(f"✅ 블로그 포스트가 성공적으로 생성되었습니다: {topic} (글자 수: {char_count}자)")
        
    except Exception as e:
        print(f"❌ '{topic}' 주제 처리 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    main() 