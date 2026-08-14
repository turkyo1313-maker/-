import os
import subprocess
import json

def get_youtube_trends_no_api():
    print("yt-dlp를 통해 유튜브 트렌드 수집 중...")
    try:
        # yt-dlp로 'Claude 활용' 검색 결과 5개 추출 (json 형식)
        command = [
            "yt-dlp",
            "ytsearch5:Claude 00",  # 검색어 설정
            "--dump-json",
            "--flat-playlist"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                videos.append({
                    'title': data.get('title', '제목 없음'),
                    'videoId': data.get('id', ''),
                    'channelTitle': data.get('uploader', '채널명 없음')
                })
        return videos
    except Exception as e:
        print(f"크롤링 중 에러 발생: {e}")
        return []

def generate_html(trends):
    cards_html = ""
    if not trends:
        cards_html = """
        <div class="card">
            <div class="title">수집된 데이터가 없습니다.</div>
            <div class="meta">잠시 후 다시 시도해 주세요.</div>
        </div>
        """
    else:
        for item in trends:
            title = item['title']
            channel = item['channelTitle']
            video_id = item['videoId']
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            cards_html += f"""
            <div class="card">
                <div class="title">{title}</div>
                <div class="meta">채널: {channel}</div>
                <a class="link" href="{url}" target="_blank">👉 영상 보러가기</a>
            </div>
            """

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude 최적화 트렌드 대시보드</title>
    <style>
        body {{ font-family: 'Pretendard', sans-serif; margin: 20px; background: #f4f7f6; color: #333; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .card {{ background: white; border-radius: 8px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .title {{ font-size: 1.1em; font-weight: bold; color: #2980b9; margin-bottom: 8px; }}
        .meta {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 10px; }}
        .link {{ color: #e74c3c; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Claude 실전 활용법 트렌드 TOP 5</h1>
        <p>API 키 없이 웹 크롤링으로 자동 업데이트되는 대시보드</p>
    </div>
    {cards_html}
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("index.html 파일 갱신 완료!")

if __name__ == "__main__":
    trends = get_youtube_trends_no_api()
    generate_html(trends)
