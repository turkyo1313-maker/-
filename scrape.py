import subprocess
import json
from datetime import datetime

def fetch_videos(search_query, count):
    # --print-json으로 데이터 정밀 추출
    command = ["yt-dlp", f"ytsearch{count}:{search_query}", "--dump-json", "--flat-playlist"]
    result = subprocess.run(command, capture_output=True, text=True)
    videos = []
    for line in result.stdout.strip().split('\n'):
        if line:
            data = json.loads(line)
            videos.append({
                'title': data.get('title', '제목없음'),
                'videoId': data.get('id'),
                'channelTitle': data.get('uploader'),
                'viewCount': data.get('view_count') or 0,
                'likeCount': data.get('like_count') or 0,
                'commentCount': data.get('comment_count') or 0,
                'uploadDate': data.get('upload_date', '00000000')
            })
    return videos

def update_dashboard():
    kr = fetch_videos("Claude 3.5 Sonnet 활용법 실전", 3)
    en = fetch_videos("Claude AI agent trends 2026", 2)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    new_section = f"""
    <details open style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 8px;">
        <summary style="font-size: 1.2em; font-weight: bold; cursor: pointer;">📅 {date_str} 업데이트 (금주 트렌드)</summary>
        {''.join([f"<div class='card'><b>{v['title']}</b><br>조회수: {v['viewCount']:,} | 좋아요: {v['likeCount']:,} | 댓글: {v['commentCount']:,} | <a href='https://youtube.com/watch?v={v['videoId']}' target='_blank'>링크</a></div>" for v in kr + en])}
    </details>
    """

    old_content = ""
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if "<!-- history -->" in content:
                old_content = content.split("<!-- history -->")[1]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html><html><body>
<h1>🚀 Claude 트렌드 대시보드</h1>
{new_section}
<div id="history">
    <h2>📂 지난 히스토리</h2>
    <!-- history -->{old_content}
</div>
</body></html>""")

if __name__ == "__main__":
    import os
    update_dashboard()
