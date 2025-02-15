#!/bin/bash

echo "🚀 블로그 컨텐츠 생성 프로세스 시작..."

# 1. 주제 생성
echo "\n1️⃣ 블로그 주제 생성 중..."
python generate_topics.py
if [ $? -ne 0 ]; then
    echo "❌ 주제 생성 실패"
    exit 1
fi

# 2. 블로그 포스트 생성
echo "\n2️⃣ 블로그 포스트 생성 중..."
python generate_blog_posts.py
if [ $? -ne 0 ]; then
    echo "❌ 블로그 포스트 생성 실패"
    exit 1
fi

# 3. HTML 및 마케팅 컨텐츠 변환
echo "\n3️⃣ HTML 및 마케팅 컨텐츠 생성 중..."
python convert_posts.py
if [ $? -ne 0 ]; then
    echo "❌ 컨텐츠 변환 실패"
    exit 1
fi

echo "\n✨ 모든 프로세스가 성공적으로 완료되었습니다!" 