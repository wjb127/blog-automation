@echo off
chcp 65001 > nul

:: 로그 파일 경로 설정 (인수가 있으면 사용)
if "%1"=="" (
    set LOG_FILE=blog_generation.log
) else (
    set LOG_FILE=%1
)

:: 시작 시간 기록
echo %date% %time% - 블로그 컨텐츠 생성 프로세스 시작... >> %LOG_FILE%

:: 1. 주제 생성
echo %date% %time% - 블로그 주제 생성 중... >> %LOG_FILE%
python generate_topics.py >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo %date% %time% - ❌ 주제 생성 실패 >> %LOG_FILE%
    exit /b 1
)

:: 2. 블로그 포스트 생성
echo %date% %time% - 블로그 포스트 생성 중... >> %LOG_FILE%
python generate_blog_posts.py >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo %date% %time% - ❌ 블로그 포스트 생성 실패 >> %LOG_FILE%
    exit /b 1
)

:: 3. HTML 및 마케팅 컨텐츠 변환
echo %date% %time% - HTML 및 마케팅 컨텐츠 생성 중... >> %LOG_FILE%
python convert_posts.py >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo %date% %time% - ❌ 컨텐츠 변환 실패 >> %LOG_FILE%
    exit /b 1
)

echo %date% %time% - ✨ 모든 프로세스가 성공적으로 완료되었습니다! >> %LOG_FILE% 