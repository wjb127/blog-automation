import json
import os
from datetime import datetime

def load_posts():
    # blog_posts.json 파일 로드
    with open("blog_posts.json", "r", encoding="utf-8") as file:
        return json.load(file)

def convert_markdown_to_tistory(content):
    # 마크다운 헤더를 HTML로 변환
    for i in range(4, 0, -1):  # h4부터 h1까지 처리
        content = content.replace('#' * i + ' ', f'<h{i}>')
        content = content.replace('\n#' * i + ' ', f'</h{i}>\n<h{i}>')
    
    # 볼드 텍스트 변환
    content = content.replace('**', '')
    
    # 기본 단락 처리
    paragraphs = content.split('\n\n')
    formatted_content = []
    
    for p in paragraphs:
        if p.strip():
            if not (p.startswith('<h') or p.startswith('</h')):
                # 단락이 헤더가 아니면 p 태그로 감싸기
                p = f'<p>{p.strip()}</p>'
            formatted_content.append(p)
    
    # 최종 HTML 구성
    html_content = """
<div class="article">
    {}
</div>
""".format('\n'.join(formatted_content))
    
    return html_content

def save_html_posts(posts):
    # 마크다운 파일을 저장할 디렉토리 생성
    output_dir = "blog_posts_html"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 각 포스트를 개별 HTML 파일로 저장
    for post in posts:
        # 파일명에 사용할 날짜 형식 변환
        date = datetime.strptime(post["date"], "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
        
        # 제목에서 특수문자 제거하고 공백을 언더스코어로 변환
        title = post["topic"].replace(":", "").replace("?", "").replace("!", "")
        title = title.replace(" ", "_")
        
        # 파일명 생성
        filename = f"{date}_{title[:50]}.html"
        filepath = os.path.join(output_dir, filename)
        
        # 마크다운을 HTML로 변환
        html_content = convert_markdown_to_tistory(post["content"])
        
        # HTML 파일로 저장
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(html_content)
        
        print(f"HTML 저장 완료: {filename}")

def main():
    # 블로그 포스트 로드
    posts = load_posts()
    
    # HTML 파일로 변환하여 저장
    save_html_posts(posts)
    print(f"\n✅ 총 {len(posts)}개의 HTML 파일이 'blog_posts_html' 디렉토리에 저장되었습니다.")

if __name__ == "__main__":
    main() 