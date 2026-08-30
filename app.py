import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from bs4 import BeautifulSoup

# 페이지 레이아웃 설정
st.set_page_config(page_title="대한민국 AI 전략 글로벌 로드맵", layout="wide")

st.title("🇰🇷 대한민국 AI 전략 및 글로벌 협력 로드맵")
st.markdown("글로벌 국가별 최신 AI 동향응ㄹ 확인하는 대시보드입니다.")

# 실시간 뉴스 크롤링
@st.cache_data(ttl=3600)
def get_latest_news(keyword):
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'xml')
        item = soup.find('item')
        if item:
            title = item.find('title').text if item.find('title') else "제목 없음"
            link = item.find('link').text if item.find('link') else "#"
            return {"title": title, "link": link}
    except Exception:
        pass
    return {"title": "최신 데이터를 불러올 수 없습니다.", "link": "#"}

# 1. 국가 데이터 구조 (초기 주요국 + 아세안 10개국 + EU 추가)
# 미주 대륙은 한국(127도) 기준 오른쪽에 오도록 경도에 +360 적용
countries_data = [
    # ---- 북미 / 남미 (오른쪽 배치) ----
    {
        "country": "미국",
        "location": [38.9072, -77.0369 + 360], 
        "ai_models": "OpenAI (GPT-4), Google (Gemini), Anthropic, Meta",
        "search_msit": "과기정통부 미국 인공지능",
        "search_local": "미국 AI 산업 동향"
    },
    {
        "country": "캐나다",
        "location": [56.1304, -106.3468 + 360],
        "ai_models": "Mila, Vector Institute, Cohere",
        "search_msit": "과기정통부 캐나다 인공지능",
        "search_local": "캐나다 AI 연구"
    },
    {
        "country": "브라질",
        "location": [-14.2350, -51.9253 + 360],
        "ai_models": "Ceboria, 라틴아메리카 오픈소스 LLM 생태계",
        "search_msit": "과기정통부 브라질 인공지능",
        "search_local": "브라질 인공지능 정책"
    },
    
    # ---- 유럽 (왼쪽 배치) ----
    {
        "country": "영국",
        "location": [51.5074, -0.1278],
        "ai_models": "DeepMind, Stability AI, AI 안전 연구소(AISI)",
        "search_msit": "과기정통부 영국 인공지능",
        "search_local": "영국 AI 산업 동향"
    },
    {
        "country": "프랑스 (EU)",
        "location": [46.2276, 2.2137],
        "ai_models": "Mistral AI, Hugging Face, EU 디지털 파트너십",
        "search_msit": "과기정통부 프랑스 인공지능",
        "search_local": "프랑스 AI 미스트랄"
    },
    {
        "country": "독일 (EU)",
        "location": [52.5200, 13.4050],
        "ai_models": "Aleph Alpha, DFKI (독일인공지능연구소)",
        "search_msit": "과기정통부 독일 인공지능",
        "search_local": "독일 인공지능 정책"
    },
    {
        "country": "벨기에 (EU)",
        "location": [50.8503, 4.3517],
        "ai_models": "한-EU AI·디지털 공동선언문, 호라이즌 유럽",
        "search_msit": "과기정통부 EU 인공지능",
        "search_local": "유럽연합 AI 법안 동향"
    },
    {
        "country": "이탈리아 (EU)",
        "location": [41.8719, 12.5674],
        "ai_models": "유럽 AI 초거대 모델 연구(CINECA), iGenius",
        "search_msit": "과기정통부 이탈리아 인공지능",
        "search_local": "이탈리아 AI 규제 및 육성"
    },
    {
        "country": "룩셈부르크 (EU)",
        "location": [49.8153, 6.1296],
        "ai_models": "MeluXina 슈퍼컴퓨터, AI for Good 전략",
        "search_msit": "과기정통부 룩셈부르크 인공지능",
        "search_local": "룩셈부르크 AI 슈퍼컴퓨팅"
    },

    # ---- 아세안 (ASEAN) 10개국 ----
    {
        "country": "인도네시아 (아세안)",
        "location": [-0.7893, 113.9213],
        "ai_models": "AI 학습용 한국형 슈퍼컴퓨터 센터 구축",
        "search_msit": "과기정통부 인도네시아 인공지능",
        "search_local": "인도네시아 AI 산업"
    },
    {
        "country": "싱가포르 (아세안)",
        "location": [1.3521, 103.8198],
        "ai_models": "아세안 신진 연구자 발굴 및 AI 혁신 파트너십",
        "search_msit": "과기정통부 싱가포르 인공지능",
        "search_local": "싱가포르 국가 AI 전략"
    },
    {
        "country": "베트남 (아세안)",
        "location": [14.0583, 108.2772],
        "ai_models": "FPT Software 협력, 국내 AI 기업 현지 진출",
        "search_msit": "과기정통부 베트남 인공지능",
        "search_local": "베트남 AI 산업 생태계"
    },
    {
        "country": "말레이시아 (아세안)",
        "location": [4.2105, 101.9758],
        "ai_models": "MyDIGITAL, 말레이시아 AI 로드맵(AIRMAP)",
        "search_msit": "과기정통부 말레이시아 인공지능",
        "search_local": "말레이시아 국가 AI 전략"
    },
    {
        "country": "태국 (아세안)",
        "location": [15.8700, 100.9925],
        "ai_models": "태국 국가 AI 전략(National AI Strategy), NECTEC",
        "search_msit": "과기정통부 태국 인공지능",
        "search_local": "태국 인공지능 혁신"
    },
    {
        "country": "필리핀 (아세안)",
        "location": [12.8797, 121.7740],
        "ai_models": "국가 인공지능 로드맵(AI Roadmap), 아시아 AI 허브 도약",
        "search_msit": "과기정통부 필리핀 인공지능",
        "search_local": "필리핀 AI 산업 생태계"
    },
    {
        "country": "캄보디아 (아세안)",
        "location": [12.5657, 104.9910],
        "ai_models": "디지털 경제 발전 전략 및 AI 윤리 가이드라인 추진",
        "search_msit": "과기정통부 캄보디아 디지털",
        "search_local": "캄보디아 인공지능 기술"
    },
    {
        "country": "브루나이 (아세안)",
        "location": [4.5353, 114.7277],
        "ai_models": "국가 디지털 전략(Digital Economy Masterplan)",
        "search_msit": "과기정통부 브루나이 인공지능",
        "search_local": "브루나이 AI 정책 동향"
    },
    {
        "country": "라오스 (아세안)",
        "location": [19.8563, 102.4955],
        "ai_models": "디지털 라오스 발전 전략 및 공공 인프라 확충",
        "search_msit": "과기정통부 라오스 디지털",
        "search_local": "라오스 디지털 트랜스포메이션"
    },
    {
        "country": "미얀마 (아세안)",
        "location": [21.9162, 95.9560],
        "ai_models": "디지털 인프라 및 e-거버넌스 협력 거점",
        "search_msit": "과기정통부 미얀마 디지털 협력",
        "search_local": "미얀마 인공지능 동향"
    },

    # ---- 아시아-태평양 주요국 ----
    {
        "country": "중국",
        "location": [39.9042, 116.4074],
        "ai_models": "Baidu (ERNIE), Alibaba (Qwen), Tencent",
        "search_msit": "과기정통부 중국 ICT 협력",
        "search_local": "중국 인공지능 독자모델"
    },
    {
        "country": "호주",
        "location": [-35.2809, 149.1300],
        "ai_models": "CSIRO, 퀀텀 및 AI 윤리 협력",
        "search_msit": "과기정통부 호주 인공지능",
        "search_local": "호주 AI 규제 및 산업"
    },
    
    # ---- 중심 (대한민국) ----
    {
        "country": "대한민국",
        "location": [37.5665, 126.9780],
        "ai_models": "Naver (HyperCLOVA X), LG (EXAONE), Kakao",
        "search_msit": "과기정통부 인공지능 글로벌 협력",
        "search_local": "대한민국 AI 3대 강국"
    }
]

# 2. 지도 생성 (회색 배경 방지 및 단일 지도 뷰 설정)
m = folium.Map(
    location=[30.0, 140.0],  # 한국 중심 태평양 시야 
    zoom_start=3,            # 국가가 늘어났으므로 줌을 약간 조정
    min_zoom=2,
    max_bounds=True,
    min_lat=-80, max_lat=80,
    min_lon=-60, max_lon=350,
    tiles=None
)

folium.TileLayer(
    tiles='https://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}',
    attr='Google Maps',
    name='Google Maps (Korean)',
    no_wrap=False
).add_to(m)

# 3. 마커 및 3단 리포트 팝업, Polyline 연결
korea_loc = [37.5665, 126.9780]

for item in countries_data:
    msit_data = get_latest_news(item["search_msit"])
    local_data = get_latest_news(item["search_local"])
    
    popup_html = f"""
    <div style="width:320px; font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; color:#2d3748;">
        
        <div style="border-bottom: 2px solid #3182ce; padding-bottom: 6px; margin-bottom: 10px;">
            <h3 style="margin: 0; font-size:18px; font-weight:800; color:#2b6cb0;">
                {item['country']}
            </h3>
        </div>
        
        <div style="margin-bottom: 12px;">
            <div style="font-size:10px; font-weight:bold; color:#fff; background-color:#3182ce; padding:3px 6px; border-radius:4px; display:inline-block; margin-bottom:4px;">
                과기정통부 최신 동향
            </div>
            <p style="margin:0 0 6px 0; font-size:12px; line-height:1.4; color:#4a5568;">
                <a href="{msit_data['link']}" target="_blank" style="color:#2d3748; text-decoration:none;">
                    {msit_data['title']}
                </a>
            </p>
        </div>
        
        <div style="margin-bottom: 12px; padding: 8px; background-color: #f7fafc; border-radius: 6px; border-left: 3px solid #cbd5e0;">
            <b style="font-size:11px; color:#4a5568;">🤖 대표 AI 현황 및 모델</b>
            <p style="margin:4px 0 0 0; font-size:12px; color:#718096; line-height:1.4;">
                {item['ai_models']}
            </p>
        </div>
        
        <div>
            <div style="font-size:10px; font-weight:bold; color:#e53e3e; margin-bottom:4px;">
                🔴 실시간 현지 동향
            </div>
            <p style="margin:0; font-size:12px; line-height:1.4;">
                <a href="{local_data['link']}" target="_blank" style="color:#2d3748; text-decoration:underline; font-weight:500;">
                    {local_data['title']}
                </a>
            </p>
        </div>
        
    </div>
    """
    
    is_korea = "대한민국" in item['country']
    icon_color = 'red' if is_korea else 'blue'
    icon_type = 'star' if is_korea else 'info-sign'
    
    folium.Marker(
        location=item["location"],
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=f"{item['country']} AI 로드맵",
        icon=folium.Icon(color=icon_color, icon=icon_type)
    ).add_to(m)

    # 한국을 중심으로 하는 직관적이고 깔끔한 점선 네트워크
    if not is_korea:
        folium.PolyLine(
            locations=[korea_loc, item["location"]],
            color="#3182ce", 
            weight=1.5, 
            opacity=0.6, 
            dash_array='4'
        ).add_to(m)

st.markdown("### 🌍 글로벌 AI 협력 네트워크 맵")
# 4. 지도 풀화면 출력
st_folium(m, width=None, height=750, use_container_width=True)