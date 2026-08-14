import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build

def get_optimized_trends():
    youtube = build("youtube", "v3", developerKey=os.environ.get("YOUTUBE_API_KEY"))
    
    # 2달(60일) 전 날짜 계산
    two_months_ago = (datetime.now() - timedelta(days=60)).isoformat() + "Z"
    
    # ① 검색 키워드 정교화 (실무 세팅, 터미널, 워크플로우 관련 확장 쿼리)
    queries = [
        "Claude Code", 
        "클로드 코워크", 
        "Claude 3.7 Sonnet workflow", 
        "Claude Code 터미널"
    ]
    all_video_ids = []

    for q in queries:
        search_response = youtube.search().list(
            q=q,
            part="id,snippet",
            maxResults=10,
            publishedAfter=two_months_ago,
            type="video",
            order="viewCount"
        ).execute()
        
        for item in search_response.get("items", []):
            all_video_ids.append(item["id"]["videoId"])

    video_ids = list(set(all_video_ids))
    if not video_ids:
        return []

    stats_response = youtube.videos().list(
        part="statistics,snippet",
        id=','.join(video_ids)
    ).execute()

    # ③ 노이즈 제거를 위한 제외 단어(Blacklist) 설정 (관련 없는 브이로그, 주식 뉴스 등 차단)
    blacklist = ["vlog", "음악", "music", "shorts", "쇼츠", "주가", "전망"]

    refined_data = []
    for item in stats_response.get("items", []):
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        
        title = snippet["title"].lower()
        
        # 블랙리스트 단어가 포함된 영상은 수집 대상에서 제외
        if any(word in title for word in blacklist):
            continue
            
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))
        
        if views == 0:
            continue

        # ② '조회수 대비 좋아요' 비율(Engagement Rate) 및 반응 가중치 적용 공식
        engagement_rate = likes / views  
        score = (views * 0.3) + (likes * 0.4) + (comments * 0.1) + (engagement_rate * 100000 * 0.2)
        
        refined_data.append({
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "views": views,
            "likes": likes,
            "score": score
        })
    
    # 점수 기준 상위 5개 추출
    return sorted(refined_data, key=lambda x: x["score"], reverse=True)[:5]

def generate_html(data):
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
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
        <h1>🚀 Claude 실전 활용법 트렌드 TOP 5 (필터 강화 버전)</h1>
    </div>
"""
    for i, v in enumerate(data, 1):
        html_content += f"""
    <div class="card">
        <div class="title">{i}. {v['title']}</div>
        <div class="meta">채널: {v['channel']} | 조회수: {v['views']:,}회 | 좋아요: {v['likes']:,}개</div>
        <a href="{v['url']}" class="link" target="_blank">영상 바로가기 &rarr;</a>
    </div>
"""
    html_content += "</body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    trends = get_optimized_trends()
    generate_html(trends)
    print("최적화된 트렌드 대시보드 HTML 생성 완료")
