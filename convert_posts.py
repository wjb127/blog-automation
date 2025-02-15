import json
import os
from datetime import datetime
import re
from openai import OpenAI
from dotenv import load_dotenv
import requests

# .env 파일에서 환경 변수 로드
load_dotenv()

def load_posts():
    # blog_posts.json 파일 로드
    with open("blog_posts.json", "r", encoding="utf-8") as file:
        return json.load(file)

def convert_markdown_to_tistory(content):
    # 제목 스타일 정의
    title_style = 'style="color: #333; font-size: 24px; font-weight: bold; margin: 40px 0 20px 0; text-align: center;"'
    subtitle_style = 'style="color: #444; font-size: 20px; font-weight: bold; margin: 35px 0 15px 0; border-left: 4px solid #4CAF50; padding-left: 15px;"'
    paragraph_style = 'style="font-size: 16px; line-height: 1.8; color: #333; margin: 20px 0;"'
    
    # 마크다운 변환
    paragraphs = content.split('\n\n')
    formatted_content = []
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
            
        if p.startswith('제목:'):
            # 메인 제목 (위아래 공백 추가)
            title_text = p.replace('제목:', '').strip().strip('"')
            p = f'\n<h1 {title_style}>{title_text}</h1>\n'
        elif p.startswith('안녕하세요'):
            # 서문
            p = f'<p {paragraph_style}>{p}</p><br>'
        elif p.endswith('중요성') or p.endswith('기법'):
            # 소제목
            p = f'<h2 {subtitle_style}>{p}</h2>'
        elif p.startswith('해시태그:') or p.startswith('썸네일'):
            # 해시태그와 썸네일 설명은 건너뛰기
            continue
        else:
            # 일반 단락
            p = f'<p {paragraph_style}>{p}</p>'
            
        formatted_content.append(p)
    
    # 하단 링크 추가
    bottom_links = """
<div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee;">
    <p style="font-size: 14px; color: #666;">▼ 함께 보면 좋은 글 ▼</p>
    <p style="font-size: 14px; line-height: 1.8;">
        <a href="https://health-info-archive.tistory.com/77" style="color: #4CAF50; text-decoration: none; display: block; margin: 10px 0;">
            성병 걸리면 인생 끝? 절대 걸리면 안되는 위험한 성병 TOP4
        </a>
        <a href="https://health-info-archive.tistory.com/76" style="color: #4CAF50; text-decoration: none; display: block; margin: 10px 0;">
            가다실9, 과연 안전할까? 부작용과 진실을 파헤치다
        </a>
        <a href="https://health-info-archive.tistory.com/72" style="color: #4CAF50; text-decoration: none; display: block; margin: 10px 0;">
            성병검사: 알고 계셨나요? STD 12종 검사가 이렇게 중요하다니!
        </a>
    </p>
</div>
"""
    
    # 최종 HTML 구성
    html_content = f"""
<div class="article" style="font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    {'\n'.join(formatted_content)}
    {bottom_links}
</div>
"""
    
    return html_content

def sanitize_filename(filename):
    # 윈도우에서 사용할 수 없는 특수문자들을 제거하거나 대체
    invalid_chars = r'[\\/:*?"<>|]'
    return re.sub(invalid_chars, '', filename)

def save_html_posts(posts):
    os.makedirs("blog_posts_html", exist_ok=True)
    
    for post in posts:
        date = post["date"].split()[0].replace("-", "")
        title = post["topic"][:100]
        sanitized_title = sanitize_filename(title)
        filename = f"{date}_{sanitized_title}"
        
        # HTML 파일만 저장
        html_content = convert_markdown_to_tistory(post["content"])
        with open(f"blog_posts_html/{filename}.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML 저장 완료: {filename}.html")

def create_marketing_content(post_content):
    paragraphs = post_content.split('\n\n')
    title = ""
    content_preview = []
    
    for p in paragraphs:
        if p.startswith('제목:'):
            title = p.replace('제목:', '').strip().strip('"')
        elif (not any(x in p.lower() for x in [
            '안녕하세요', '건강톡톡', '서문:', '해시태그:', '썸네일', 
            '소제목:', '중요성', '기법', '마법'  # 소제목 관련 키워드 추가
        ]) and not p.startswith('제목:') and len(p.strip()) > 0):
            # 본문 내용에서 핵심 문장 추출
            sentences = p.split('. ')
            if len(sentences) > 2:
                content_preview.append('. '.join(sentences[:2]) + '.')
            else:
                content_preview.append(p)
            if len(content_preview) >= 2:
                break
    
    marketing_text = f"""{title}

{'. '.join(content_preview)}

[블로그 링크]"""
    return marketing_text

def save_marketing_texts(posts):
    os.makedirs("marketing_contents", exist_ok=True)
    
    for post in posts:
        date = post["date"].split()[0].replace("-", "")
        title = post["topic"][:50]
        sanitized_title = sanitize_filename(title)
        filename = f"{date}_{sanitized_title}_marketing.txt"
        
        marketing_content = create_marketing_content(post["content"])
        with open(f"marketing_contents/{filename}", "w", encoding="utf-8") as file:
            file.write(marketing_content)
        print(f"마케팅 컨텐츠 저장 완료: {filename}")

def main():
    # 블로그 포스트 로드
    posts = load_posts()
    
    # HTML 파일로 변환하여 저장
    save_html_posts(posts)
    print(f"\n✅ 총 {len(posts)}개의 HTML 파일이 'blog_posts_html' 디렉토리에 저장되었습니다.")

    # 마케팅 컨텐츠 저장
    save_marketing_texts(posts)
    print(f"\n✅ 총 {len(posts)}개의 마케팅 컨텐츠가 'marketing_contents' 디렉토리에 저장되었습니다.")

if __name__ == "__main__":
    main() 