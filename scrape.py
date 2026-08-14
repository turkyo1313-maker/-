import os
import subprocess
import json
from datetime import datetime

def fetch_videos(search_query, count):
    try:
        command = ["yt-dlp", f"ytsearch{count}:{search_query}", "--dump-json", "--flat-playlist"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                raw_date = data.get('upload_date', '00000000')
                formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
                videos.append({
                    'title': data.get('title'),
                    'videoId': data.get('id'),
                    'channelTitle': data.get('uploader'),
                    'viewCount': data.get('view_count', 0),
                    'likeCount': data.get('like_count', 0),
                    'commentCount': data.get('comment_count', 0),
                    'uploadDate': formatted_date
                })
        return videos
    except: return []

def make_cards_html(videos, lang_label):
    html = ""
    for item in videos:
        url = f"https://www.youtube.com/watch?v={item['videoId']}"
        html += f"""
            <div class="card">
                <span class="badge">{lang_label}</span>
                <div class="title">{item['title']}</div>
                <div class="meta">📅 {item['uploadDate']} | 📺 {item['channelTitle']}</div>
                <div class="stats">👍 {item['likeCount']:,} | 👁️ {item['viewCount']:,} | 💬 {item['commentCount']:,}</div>
                <a class="link" href="{url}" target="_blank">👉 영상 보러가기</a>
            </div>
        """
    return html

def update_dashboard():
    kr, en = fetch_videos("Claude 3.5 Sonnet 활용법", 3), fetch_videos("Claude AI agent trends", 2)
    new_data = f"<div class='week-section'><h2>📅 {datetime.now().strftime('%Y-%m-%d')} 업데이트</h2>" + make_cards_html(kr, "한국어") + make_cards_html(en, "English") + "</div>"
    
    # 기존 내용 읽기 (없으면 새로 생성)
    old_content = ""
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            # <div id='history'> 이후의 내용을 가져옴
            if "<div id='history'>" in content:
                old_content = content.split("<div id='history'>")[1].split("</div>")[0]

    final_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: sans-serif; padding: 20px; background: #f4f7f6; }}
        .card {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .week-section {{ border-bottom: 2px solid #ccc; margin-bottom: 30px; }}
        .title {{ font-weight: bold; color: #1e40af; }}
    </style>
</head>
<body>
    <h1>🚀 Claude 트렌드 아카이브</h1>
    <div id='history'>
        {new_data}
        {old_content}
    </div>
</body>
</html>"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    update_dashboard()
