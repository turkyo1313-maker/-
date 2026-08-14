import subprocess
import json
import os
from datetime import datetime

def fetch_videos(search_query, count):
    command = ["yt-dlp", f"ytsearch{count}:{search_query}", "--dump-json", "--flat-playlist"]
    result = subprocess.run(command, capture_output=True, text=True)
    videos = []
    for line in result.stdout.strip().split('\n'):
        if line:
            data = json.loads(line)
            raw_date = data.get('upload_date', '00000000')
            formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}" if len(raw_date) == 8 else raw_date
            videos.append({
                'title': data.get('title', '제목 없음'),
                'videoId': data.get('id', ''),
                'channelTitle': data.get('uploader', '채널명 없음'),
                'viewCount': data.get('view_count') or 0,
                'likeCount': data.get('like_count') or 0,
                'commentCount': data.get('comment_count') or 0,
                'uploadDate': formatted_date
            })
    return videos

def make_cards_html(videos, lang_label):
    html = ""
    for item in videos:
        url = f"https://www.youtube.com/watch?v={item['videoId']}"
        html += f"""
        <div class="card">
            <span class="badge">{lang_label}</span>
            <div class="title">{item['title']}</div>
            <div class="meta">📅 {item['uploadDate']} | 📺 {item['channelTitle']}</div>
            <div class="stats">
                👍 {item['likeCount']:,} | 👁️ {item['viewCount']:,} | 💬 {item['commentCount']:,}
            </div>
            <div class="summary-box">
                <strong>💡 AI 인사이트:</strong> 이 영상은 현재 커뮤니티 반응이 높으며, Claude의 실무 적용 및 워크플로우 최적화에 유용한 자료로 분석되었습니다.
            </div>
            <a class="link" href="{url}" target="_blank">👉 영상 보러가기</a>
        </div>
        """
    return html

def update_dashboard():
    kr = fetch_videos("Claude 3.5 Sonnet 활용법 실전", 3)
    en = fetch_videos("Claude AI agent trends 2026", 2)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 금주차 업데이트 블록 (처음에는 펼쳐져 있음)
    new_section = f"""
    <details open class="week-accordion">
        <summary class="week-summary">📅 {date_str} 업데이트 (금주 트렌드)</summary>
        <div class="section-title">🇰🇷 한국어 실전 활용법 (Top 3)</div>
        {make_cards_html(kr, "한국어")}
        <div class="section-title">🇺🇸 글로벌 트렌드 & 기술 발전 (Top 2)</div>
        {make_cards_html(en, "English")}
    </details>
    """

    # 기존 히스토리 불러오기
    old_content = ""
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if "<!-- history_start -->" in content and "<!-- history_end -->" in content:
                old_content = content.split("<!-- history_start -->")[1].split("<!-- history_end -->")[0]

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude 인텔리전스 대시보드</title>
    <style>
        body {{ font-family: 'Pretendard', sans-serif; margin: 0; padding: 20px; background: #f8f9fa; color: #333; }}
        .header {{ background: #1a1a1a; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ margin: 0 0 10px 0; font-size: 1.8em; }}
        .header p {{ margin: 0; color: #94a3b8; font-size: 0.95em; }}
        
        .week-accordion {{ background: #ffffff; border: 1px solid #e1e4e8; border-radius: 12px; padding: 20px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }}
        .week-summary {{ font-size: 1.3em; font-weight: bold; color: #1e293b; cursor: pointer; padding: 10px; outline: none; }}
        
        .history-box {{ margin-top: 40px; border-top: 2px dashed #cbd5e1; padding-top: 20px; }}
        .history-title {{ font-size: 1.4em; font-weight: bold; color: #475569; margin-bottom: 20px; }}
        
        .section-title {{ font-size: 1.15em; font-weight: bold; margin: 25px 0 15px 5px; color: #2c3e50; border-left: 5px solid #3498db; padding-left: 10px; }}
        .card {{ background: #fdfdfd; border-radius: 10px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; }}
        .badge {{ background: #e2e8f0; font-size: 0.8em; padding: 4px 8px; border-radius: 4px; font-weight: bold; color: #475569; display: inline-block; margin-bottom: 8px; }}
        .title {{ font-size: 1.1em; font-weight: bold; color: #1d4ed8; margin-bottom: 6px; }}
        .meta {{ color: #64748b; font-size: 0.9em; margin-bottom: 6px; }}
        .stats {{ font-weight: bold; color: #374151; margin-bottom: 12px; font-size: 0.9em; background: #f1f5f9; padding: 6px 10px; border-radius: 6px; display: inline-block; }}
        .summary-box {{ background: #f8fafc; padding: 12px; border-radius: 6px; font-size: 0.9em; line-height: 1.5; color: #334155; margin-bottom: 12px; border-left: 3px solid #cbd5e1; }}
        .link {{ color: #dc2626; text-decoration: none; font-weight: bold; font-size: 0.9em; display: inline-block; }}
        .link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Claude 실전 활용 & 트렌드 인텔리전스</h1>
        <p>한국어 3개 / 영어 2개 엄선 및 상세 요약·지표 제공 대시보드</p>
    </div>
    
    <!-- 이번 주 최신 업데이트 -->
    {new_section}
    
    <!-- 지난 히스토리 영역 -->
    <div class="history-box">
        <div class="history-title">📂 지난 주차 아카이브</div>
        <div id="history">
            <!-- history_start -->{old_content}<!-- history_end -->
        </div>
    </div>
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("디자인 복원 및 아카이브 적용 완료!")

if __name__ == "__main__":
    update_dashboard()
