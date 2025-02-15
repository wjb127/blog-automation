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
    title_style = 'style="color: #333; font-size: 24px; font-weight: bold; margin: 40px 0 20px 0;"'
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
            # 메인 제목
            title_text = p.replace('제목:', '').strip().strip('"')
            p = f'<h1 {title_style}>{title_text}</h1>'
        elif p.startswith('안녕하세요'):
            # 서문
            p = f'<p {paragraph_style}>{p}</p><br>'
        elif p.endswith('중요성') or p.endswith('기법'):
            # 소제목
            p = f'<h2 {subtitle_style}>{p}</h2>'
        elif p.startswith('해시태그:'):
            # 해시태그
            tags = p.replace('해시태그:', '').strip()
            tags_list = tags.split()
            formatted_tags = ' '.join([f'<a href="#" style="color: #4CAF50; margin-right: 10px; text-decoration: none;">{tag}</a>' for tag in tags_list])
            p = f'<div style="margin: 40px 0;">{formatted_tags}</div>'
        elif p.startswith('썸네일'):
            # 썸네일 설명 (관리용으로 숨김)
            p = f'<div style="display: none;">{p}</div>'
        else:
            # 일반 단락
            p = f'<p {paragraph_style}>{p}</p>'
            
        formatted_content.append(p)
    
    # 최종 HTML 구성
    html_content = """
<div class="article" style="font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    {}
</div>
""".format('\n'.join(formatted_content))
    
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

def main():
    # 블로그 포스트 로드
    posts = load_posts()
    
    # HTML 파일로 변환하여 저장
    save_html_posts(posts)
    print(f"\n✅ 총 {len(posts)}개의 HTML 파일이 'blog_posts_html' 디렉토리에 저장되었습니다.")

if __name__ == "__main__":
    main() 