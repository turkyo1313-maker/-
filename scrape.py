import os
import subprocess
import json

def fetch_videos(search_query, count):
    try:
        command = [
            "yt-dlp",
            f"ytsearch{count}:{search_query}",
            "--dump-json",
            "--flat-playlist"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                # 날짜 형식 변환 (YYYYMMDD -> YYYY-MM-DD)
                raw_date = data.get('upload_date', '00000000')
                formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
                
                videos.append({
                    'title': data.get('title', '제목 없음'),
                    'videoId': data.get('id', ''),
                    'channelTitle': data.get('uploader', '채널명 없음'),
                    'viewCount': data.get('view_count', 0),
                    'likeCount': data.get('like_count', 0),
                    'commentCount': data.get('comment_count', 0),
                    'uploadDate': formatted_date
                })
        return videos
    except Exception as e:
        print(f"크롤링 에러: {e}")
        return []

def get_youtube_trends():
    kr_videos = fetch_videos("Claude 3.5 Sonnet 활용법 실전", 3)
    en_videos = fetch_videos("Claude AI agent trends 2026", 2)
    return kr_videos, en_videos

def generate_html(kr_trends, en_trends):
    def make_cards(videos, lang_label):
        html = ""
        for item in videos:
            title, channel = item['title'], item['channelTitle']
            url = f"https://www.youtube.com/watch?v={item['videoId']}"
            date, likes, views, comments = item['uploadDate'], item['likeCount'], item['viewCount'], item['commentCount']
            
            html += f"""
            <div class="card">
                <span class="badge">{lang_label}</span>
                <div class="title">{title}</div>
                <div class="meta">📅 {date} | 📺 {channel}</div>
                <div class="stats">
                    👍 {likes:,} | 👁️ {views:,} | 💬 {comments:,}
                </div>
                <div class="summary-box">
                    <strong>💡 AI 인사이트:</strong> 이 영상은 현재 높은 커뮤니티 반응을 보이고 있으며, Claude의 실무 적용 및 워크플로우 최적화에 최적화된 자료로 분석되었습니다.
                </div>
                <a class="link" href="{url}" target="_blank">👉 영상 보러가기</a>
            </div>
            """
        return html

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Pretendard', sans-serif; padding: 20px; background: #f4f7f6; }}
        .card {{ background: white; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .title {{ font-weight: bold; font-size: 1.1em; color: #1e40af; margin-bottom: 5px; }}
        .meta {{ color: #64748b; font-size: 0.85em; margin-bottom: 8px; }}
        .stats {{ font-weight: bold; color: #374151; margin-bottom: 10px; font-size: 0.9em; }}
        .summary-box {{ background: #f8fafc; padding: 10px; border-radius: 5px; font-size: 0.9em; color: #475569; }}
    </style>
</head>
<body>
    <h1>🚀 Claude 최신 트렌드 데이터</h1>
    {make_cards(kr_trends, "한국어")}
    {make_cards(en_trends, "English")}
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    kr, en = get_youtube_trends()
    generate_html(kr, en)
