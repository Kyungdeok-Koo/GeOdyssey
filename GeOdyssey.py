!pip install googlemaps
!pip install image
!pip install konlpy
!pip install selenium
!pip install webdriver-manager
!pip install pillow
!wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -fy
!google-chrome --headless --no-sandbox --disable-gpu --remote-debugging-port=9222 &>/dev/null &
!google-chrome --version || echo "Chrome is not installed"
!pkill -9 chrome || echo "No Chrome process found"
!pkill -9 chromedriver || echo "No ChromeDriver process found"
!python -c "import selenium; print(f'Selenium 설치 완료! 버전: {selenium.__version__}')"
!ls /content/drive/MyDrive/cybernk_data_cleaned.csv

import json
import nltk
import os
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from google.colab import drive, files, userdata
import googlemaps
from konlpy.tag import Okt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from nltk.data import find
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import folium
import chardet
import numpy as np

"""# **2016~2025년도 기사들을 2개년씩 나누어서 진행한 크롤링 코드**
## **자료 양이 많아서 2개년씩 나누어서 총 5번 코드 진행**
"""

def setup_colab():
    """Google Drive를 마운트하고 저장 경로를 설정"""
    from google.colab import drive
    drive.mount('/content/drive')
    save_path = "/content/drive/MyDrive/YTN_News"
    os.makedirs(save_path, exist_ok=True)
    return save_path

def get_all_news_links(search, start_date, end_date):
    """페이지네이션을 자동 탐색하여 모든 뉴스 기사 링크를 가져옴"""
    base_url = "https://www.ytn.co.kr/search/index.php"
    page = 1
    news_links = set()  # 중복 제거를 위해 set 사용

    while True:
        params = {
            "type": 1, "callSite": 1,
            "q": search,
            "ds": start_date, "de": end_date,
            "se_date": 3, "target": 0, "mtarget": 0,
            "page": page  # 페이지 번호 추가
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(base_url, params=params, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # 뉴스 기사 링크 가져오기
        articles = soup.select("div.search_news_list a[href]")
        links = {urljoin("https://www.ytn.co.kr", a["href"]) for a in articles}

        if not links:
            print(f"페이지 {page}에 더 이상 기사가 없습니다. 크롤링 종료.")
            break  # 더 이상 기사가 없으면 종료

        news_links.update(links)  # 중복 제거하면서 링크 추가
        print(f"페이지 {page} 크롤링 완료. {len(links)}개 기사 추가됨.")
        page += 1  # 다음 페이지로 이동

        time.sleep(1)  # 과부하 방지를 위한 딜레이 추가

    return list(news_links)

def fetch_news_content(url):
    """기사의 제목, 날짜, 본문을 가져옴"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 기존 CSS 선택자 사용
    title_element = soup.select_one("h2.news_title span")
    title = title_element.get_text(strip=True) if title_element else "(제목 없음)"

    date_element = soup.select_one("div.date")
    date = date_element.get_text(strip=True) if date_element else "(날짜 없음)"

    content_elements = soup.select("div#CmAdContent.paragraph span")
    content = " ".join([p.get_text(strip=True) for p in content_elements]) if content_elements else "(내용 없음)"

    print(f"[DEBUG] URL: {url}")
    print(f"[DEBUG] Title: {title}")
    print(f"[DEBUG] Date: {date}")
    print(f"[DEBUG] Content Length: {len(content)}")

    return date, title, url, content

def main():
    """메인 함수"""
    search = input("검색어를 입력하세요: ")
    start_date = input("검색 시작 날짜 (YYYYMMDD): ")
    end_date = input("검색 종료 날짜 (YYYYMMDD): ")
    save_path = setup_colab()

    # 전체 기사 링크 수집
    news_links = get_all_news_links(search, start_date, end_date)
    print(f"총 {len(news_links)}개의 기사 링크를 찾았습니다.")

    # 기사 내용 크롤링
    news_data = [fetch_news_content(url) for url in news_links]

    # 데이터 저장
    df = pd.DataFrame(news_data, columns=['date', 'title', 'link', 'content'])
    df.drop_duplicates(subset=['title', 'content'], inplace=True)
    file_name = f"{search}_{start_date}_{end_date}.csv"
    df.to_csv(os.path.join(save_path, file_name), index=False, encoding='utf-8-sig')

    print(f"파일이 저장되었습니다: {save_path}/{file_name}")

if __name__ == "__main__":
    main()

"""# **'북한지역정보넷'에 있는 장소명, 지명 추출 코드**"""

# ✅ Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.binary_location = "/usr/bin/google-chrome"  # Chrome 실행 경로 지정

# ✅ WebDriver Manager를 사용하여 ChromeDriver 자동 다운로드 및 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ 정상 실행 확인 (구글 페이지 열기)
driver.get("https://www.google.com")
print(f"✅ Chrome 실행 성공! 현재 페이지 제목: {driver.title}")

# ✅ WebDriver 종료
driver.quit()

drive.mount('/content/drive')

save_dir = "/content/drive/MyDrive"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# ✅ Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.binary_location = "/usr/bin/google-chrome"

# ✅ WebDriver 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ 크롤링할 URL
base_url = "https://cybernk.net/infoText/InfoHumanCultureList.aspx?mc=CC02&sc=A315&direct=1&ac="
driver.get(base_url)
time.sleep(3)  # 페이지 로딩 대기

# ✅ 전체 페이지 개수 가져오기
try:
    total_pages = int(driver.find_element(By.CLASS_NAME, "Forange").text.strip())
except:
    total_pages = 1  # 기본값
print(f"📄 총 {total_pages} 페이지 크롤링 시작...")

# ✅ 데이터를 저장할 리스트
data = []

# ✅ 페이지네이션을 고려한 크롤링
for page in range(1, total_pages + 1):
    print(f"📄 {page} 페이지 크롤링 중...")

    # ✅ 현재 페이지의 데이터 크롤링
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")[1:]  # 첫 번째 행(헤더) 제외
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 3:
            title = cells[1].text.strip().replace("\n", " ").replace("\t", " ")
            region = cells[2].text.strip().replace("\n", " ").replace("\t", " ")
            if title and region:
                data.append([title, region])

    # ✅ 다음 페이지로 이동 (JavaScript 실행)
    if page < total_pages:
        driver.execute_script(f"Page({page + 1});")
        time.sleep(3)  # 페이지 로딩 대기

print("✅ 모든 페이지 크롤링 완료!")

# ✅ WebDriver 종료
driver.quit()

# ✅ 데이터프레임으로 변환
df = pd.DataFrame(data, columns=["제목", "행정구역"])

# ✅ 데이터 정제 (불필요한 행 제거 및 괄호 안 한자 제거)
remove_keywords = ["통합검색", "행정구역선택", "Total", "Page", "조회 할 행정구역", "텍스트", "이미지", "동영상", "교육·학술·연구", "전체", "검색 결과", "조회수", "스크랩", "검색어입력", "위의 조건을 포함하는"]
df = df[~df["제목"].astype(str).str.contains('|'.join(remove_keywords), na=False)]
df = df[~df["행정구역"].astype(str).str.contains('|'.join(remove_keywords), na=False)]

# ✅ 제목에서 괄호 안 한자 제거
df["제목"] = df["제목"].apply(lambda x: re.sub(r"\(.*?\)", "", x))

# ✅ 잘못된 행(정확한 제목이 없는 행) 제거
df = df[df["제목"].str.len() > 2]
df = df[df["행정구역"].str.len() > 2]

# ✅ 숫자만 포함된 행 제거
df = df[~df["제목"].str.match(r"^\d+$", na=False)]
df = df[~df["행정구역"].str.match(r"^\d+$", na=False)]

# ✅ 의미 없는 지역명 나열 행 제거 (학교, 연구소 등은 유지)
def is_invalid_location(title):
    location_keywords = ["시", "도", "구", "군", "읍", "면", "동", "리"]
    keep_keywords = ["학교", "대학", "연구소", "센터", "기관", "협회", "병원", "박물관"]

    # 학교, 연구소 등의 키워드가 포함된 경우 유지
    if any(kw in title for kw in keep_keywords):
        return False

    # 두 개 이상의 지역명만 포함된 경우 제거
    words = title.split()
    if len(words) >= 2 and all(any(loc in word for loc in location_keywords) for word in words):
        return True

    return False

df = df[~df["제목"].apply(is_invalid_location)]

# ✅ 단순 명사 나열 행 제거 (의미 없는 기관명 조합 삭제)
df = df[~df["제목"].str.match(r"^[가-힣]{2,} [가-힣]{2,}$", na=False)]

df = df.dropna().reset_index(drop=True)

# ✅ CSV 파일로 저장 (Google Drive 경로)
save_path = "/content/drive/MyDrive/cybernk_data_cleaned.csv"
df.to_csv(save_path, index=False, encoding="utf-8-sig")
print(f"✅ 크롤링 및 데이터 정제 완료! 데이터가 Google Drive에 저장되었습니다: {save_path}")

from google.colab import files
files.download("/content/drive/MyDrive/cybernk_data_cleaned.csv")

"""# **구글 맵 API 사용을 위한 준비**"""

gmap_keys = userdata.get('GOOGLE_MAPS_API_KEY2')

"""# **2개년 파일 불러오기 후 2016_2025_ytn_news_data.csv로 통합**"""

# CSV 파일에서 검색어 읽기
csv_file = "/content/drive/MyDrive/Colab Notebooks/ytn_data_merged_folder/20160101-20171231 (1).csv"

# 파일의 인코딩 감지
with open(csv_file, "rb") as f:
    result = chardet.detect(f.read(100000))  # 처음 100,000바이트 읽기
    detected_encoding = result["encoding"]

print(f"Detected Encoding: {detected_encoding}")  # 감지된 인코딩 출력

# CSV 파일에서 검색어 읽기
csv_file = "/content/drive/MyDrive/Colab Notebooks/ytn_data_merged_folder/20160101-20171231 (1).csv" # CSV 파일 경로
active_df_1 = pd.read_csv(csv_file, encoding='cp949')  # CSV 파일 읽기

active_df_1

csv_file = "/content/drive/MyDrive/Colab Notebooks/ytn_data_merged_folder/20180101-20191231 (1).csv" # CSV 파일 경로
active_df_2 = pd.read_csv(csv_file, encoding='cp949')  # CSV 파일 읽기

active_df_2

active_df_2 = active_df_2.filter(items=["date", "title", "link", "content", "location", "address", "latitude", "longitude"])

active_df_2

csv_file = "/content/drive/MyDrive/Colab Notebooks/ytn_data_merged_folder/20200101-20211231 (1).csv" # CSV 파일 경로
active_df_3 = pd.read_csv(csv_file, encoding='cp949')  # CSV 파일 읽기

active_df_3

csv_file = "/content/drive/MyDrive/Colab Notebooks/ytn_data_merged_folder/20220101-20231231 (1).csv" # CSV 파일 경로
active_df_4 = pd.read_csv(csv_file, encoding='cp949')  # CSV 파일 읽기

active_df_4

csv_file = "/content/drive/MyDrive/Colab Notebooks/ytn_data_merged_folder/20240101-20250218 (1).csv" # CSV 파일 경로
active_df_5 = pd.read_csv(csv_file, encoding='cp949')  # CSV 파일 읽기

active_df_5

# 예제: 16개의 데이터프레임 (active_df1 ~ active_df16)
dfs = [active_df_1, active_df_2, active_df_3, active_df_4, active_df_5]

# 세로 방향으로 합치기
merged_df = pd.concat(dfs, ignore_index=True)

merged_df

# 데이터 확인
print("\n===== 데이터 요약 정보 =====\n")
merged_df.info()

"""# **active_df (원본데이터) copy**"""

data_df = merged_df

data_df

data_df.info()

print("\n===== 데이터 샘플 =====\n")
data_df.head()

print("\n===== 데이터 샘플 =====\n")
print(data_df.head())

# 기본 통계 요약
print("\n===== 기본 통계 =====\n")
print(data_df.describe(include='all'))

active_df = data_df.copy()

active_df

"""# **title 컬럼, content 컬럼 합쳐서 texts로 뽑아두기**"""

texts = active_df['title'][0:] + active_df['content'][0:]

texts

texts.info()

texts_df = pd.DataFrame(texts)

print(texts_df.columns)

"""# **자연어 처리(NLP)기반 NLTK 사용을 위한 준비**"""

nltk.download('punkt')

try:
    find('tokenizers/punkt')
    print("punkt 데이터가 이미 설치됨.")
except LookupError:
    print("punkt 데이터가 없음. 다운로드 중...")
    nltk.download('punkt')

nltk.download('punkt_tab')

nltk.download('averaged_perceptron_tagger_eng')

"""# **자연어 처리(NLP)기반 NLTK를 활용한 장소 추출하기**"""

texts_df

texts_df.columns = ["content"]  # 단, 컬럼이 1개일 경우만 가능

texts_df

texts_df['content'].isna().sum()

# 결측값 확인
print("\n===== 결측값 개수 =====\n")
texts_df.isnull().sum()

texts_df = texts_df.dropna(subset=["content"])

texts_df.isnull().sum()

# 한글 이외의 문자 제거
texts_df['content'] = texts_df['content'].str.replace(r'[^가-힣]', ' ', regex=True)

# 빈 값('')을 NaN으로 변환
texts_df['content'] = texts_df['content'].replace('', np.nan)

# 결과 확인
print(texts_df[['content']].head(10))

# 필요한 리소스 다운로드
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')  # 추가 다운로드

# 장소명 추출 함수 (명사 판별)
def extract_nouns(text):
    words = word_tokenize(text)  # 단어 토큰화
    tagged = pos_tag(words)  # 품사 태깅
    places = [word for word, pos in tagged if pos in ["NNP", "NN"]]  # 고유명사/명사 필터링
    return ", ".join(places) if places else None

# df["location"] 컬럼 추가
texts_df["location"] = texts_df['content'].apply(extract_nouns)

# 결과 확인
texts_df

texts_df = texts_df.rename(columns={"content": "contents"})
texts_df = texts_df.rename(columns={"location": "locations"})

texts_df

total_df = pd.concat([active_df, texts_df], axis=1)

total_df

"""# **locations 컬럼의 각 행마다 여러개의 값들을 하나하나 쪼개기**"""

# 'location' 컬럼을 쉼표(,) 기준으로 분리하여 리스트로 변환
total_df['locations'] = total_df['locations'].str.split(', ')

# 리스트를 개별 행으로 변환
total_df_exploded = total_df.explode('locations', ignore_index=True)

# 결과 출력
total_df_exploded

# 'locations' 컬럼에서 중복된 값 제거
total_df_exploded = total_df_exploded.drop_duplicates(subset=['locations'])

# 결과 출력
total_df_exploded

# Okt 객체 생성
okt = Okt()

# 조사 제거 함수
def remove_josa_konlpy(text):
    if isinstance(text, str):  # 텍스트가 문자열인 경우에만 처리
        words = okt.pos(text, norm=True, stem=True)  # 단어와 품사 태깅
        return ''.join([word[0] for word in words if word[1] != 'Josa'])  # 조사 제거
    return ''  # 문자열이 아닌 경우 빈 문자열 반환

# NaN 값 처리 후 적용
total_df_exploded['location_clean'] = total_df_exploded['locations'].fillna('').apply(remove_josa_konlpy)

# 결과 출력
print(total_df_exploded)

total_df_exploded['location_clean'].isna().sum()

# 제거할 조사 리스트
josa_list = ['에서', '이냐','이라는', '라는', '라고', '탈북자','으로도', '이라든가','이냐',' 으로', '까지', '을', '를', '의', '에', '은', '는', '이', '가', '도', '만', '밖에', '조차']

# 정규식 패턴 생성
josa_pattern = '|'.join(josa_list)  # '에서|이냐|라는|으로|까지|을|를|의|...' 형태

# 조사 제거 함수
def remove_josa(text):
    return re.sub(f'({josa_pattern})$', '', text)  # 끝에 붙은 조사만 제거

# 적용
total_df_exploded['location_clean'] = total_df_exploded['location_clean'].apply(remove_josa)

# 결과 출력
total_df_exploded

print(list(total_df_exploded['location_clean']))

# 한글 이외의 문자 제거
total_df_exploded['location_clean'] = total_df_exploded['location_clean'].str.replace(r'[^가-힣]', '', regex=True)

# 빈 값('')을 NaN으로 변환
total_df_exploded['location_clean'] = total_df_exploded['location_clean'].replace('', np.nan)

# 결과 확인
print(total_df_exploded[['location_clean']].head(10))

# 결측값 확인
print("\n===== 결측값 개수 =====\n")
total_df_exploded.isnull().sum()

total_df_exploded = total_df_exploded.dropna(subset=["locations"])

total_df_exploded.isnull().sum()

location_list = ['주목북한', '금강산관광', '평양시간', '백두산', '과학기술전당', '당창건', '금강산', '원산', '칠보산', '개성공단', '삼지연', '금수산태양궁전', '김일성광장', '풍계리', '무산광산연합기업소', '김책공업종합대학', '순안국제공항', '교예', '청진', '함경북', '길주군', '양강', '백암군', '만탑산', '영변', '전해주다', '평천', '평성', '혜산', '통천', '평양시르다', '만경대', '개성', '용천역', '자강', '원자력총국', "'신포", '무산', '봉화진료소', '백두산영웅청년발전소', '인민문화궁전', '평안남', '중등학원', '신의주', '황해남', '평안북', '철산군', '구성시', '방현', '식료공장', '정치범수용소', '남포', '통일각', '마식령', '무수단리', '주체사상탑', '함경남', '평화변전소', '강건종합군관학교', '송악프라자', '황해북', '밀영', '청진항', '원산항', '만수대', '김일성종합대학', '대성백화점', '김일성정치군사대학', '평양역', '개성만월대', '만수대의사당', '요덕', '합영회사', '김일성고급당학교', '인민경제', '나진', '회령', '단천산업은행', '나선특별시', '함흥컴퓨터기술대학', '황주군', '숙천군', '숙천', '김형권군', '대성산', '평강', '과학자거리', '황해제철연합기업소', '옥류관', '장철구평양상업종합대학', '평양체육관', '통일거리', '강계', '평양과기대', '철도성', '개천시', '혁명학원', '학생소년궁전', '묘향산', '전승', '순안', '축전북한', '류경정주영체육관', '창광거리', '창광원', '평양외국어대학교', '김일성종합군사대학', '초대소', '보통강구역', '서장회관', '국제관계대학', '자연박물관', '중앙동물원', "'류경김치공장", '곡산', '사리원', '삭주군', '평양산원이다.평양산원', '평양중등학원', '라선시', '금강산댐', '백두산건축연구원', '성천담배', '서해갑문', '아오지', '창전거리', '평양민속공원', '희천', '강동군', '중구역', '고연봉', '국가계획위원회', '온성', '갈다공항', '북강원', '흥남항', '주사기공장', '태타다', '문수물놀이장', '연사군', '은산군', '함경북도인민위원회', '신포조선소', '봉수교회', '대봉광산', '형제산', '애국열사릉', '류경동', '흥남', '조선혁명박물관', '모란봉구역', '평양대극장', '금강군', '피현군', '안주시', '해주항', '김책시', '청년중앙회관', '선봉', '승리화학연합기업소', '과일군', '동해함대사령부', '남포조선소', '벽성군', '안변', '승산', '류원신발공장', '판문각', '평산', '우의탑', '종합상점', '정주', '정일봉', '국가학원이다', '인민대학습당', '고방산', '강남군', '개성역', '신도군', '천리마군', '어랑천발전소', '어랑군', '두만강역', '남신의주·용천', '화대군', '서해위성발사대', '은률군', '영변원자로', '을밀대', '원산갈다해안관광지구', '양덕군', '외금강', '문천시', '대동강수산물식당', '장충성당', '강령', '미사일기지', '대관유리공장', '왕건왕릉', '대홍단', '능라도5.1경기장', '판문역', '함흥역', '청진역', '원산역', '송림', '태천', '기정동', '박천', '장전항', '영흥', '통천', '선덕비행장', '우시군', '김일성경기장', '중평남새온실농장', '경성군', '울림폭포', '박연폭포', '평양의대', '김형직군', '평양종합병원', '선천', '김만유병원', '금강산역', '정평', '제1백화점', "'광복지구상업중심", '순천린비료공장', '온정리', '개성공단기업협회장', '개풍군', '평강군', '금천군', '강령군', '애송', '평양애육원', '모란봉극장', '만수대예술극장', '남산중', '온천군', '함주', '보통문', '다락식', '의주', '의주비행장', '조국해방전쟁승리기념탑', '신흥군', '옥류아동병원', '류경안과종합병원', '룡림군', '도양리', '장진군', '조선미술박물관', '중앙검찰소', '송화지구', '김책항', '평안북도예술극장', '만경대혁명학원·강반석혁명학원', '금강펜션타운', '갑산군', '승리거리', '서포지구', '리원군', '평양골프장', '만포운하공장', '단고기식당', '신천박물관', '금성학원이다.금성학원', '대동문', '강서구역', '은률광산', '단군릉', '체육성', '리파역', "'통일역", '개선역', '구장군', '동신군', '고산군', '이천군', '장풍군', '띄다.내각종합청사', '해방탑', '정백사원', '금수산영빈관', '평양고려호텔', '만포시', '평양과학기술대', '덕천시', '양각도국제호텔','조선노동당1호청사', '김일성광장', '텔레비죤총국', '금수산궁전', '평성국가과학원', '장충성당', '산림기자재공장', '김일성경기장', '메기양어장', '금산포젓갈가공공장', '창린도방어부대', '판문역', '판문점', '남북공동연락사무소', '개성공단', '원산갈마국제공항', '원산갈마해안관광공원', '온정각 ', '원산미사일발사장', '금강산아난티리조트골프장', '북부핵시험장', '어랑천박전소', '락산바다연어양식사업소', '염분진호텔', '라진항', '남포조선조련기업소', '운곡지구종합목장', '양덕온천문화휴양지', '평성미사일생산공장', '서해위성발사장', '동창리미사일발사장', '미사일발사장', '구성공군비행장', '약수동95호탄약공장', '신의주화학섬유공장', '중조압록강대교', '대관유리공장', '동창리미사일발사장', '녹말생산공장', '백두산','평안남도', '황해북도', '만수대의사당', '나선국제통신센터', '국제통신국', '평양프로그램센터', '강계우편국', '평안남도', '황해북도', '평양음악무용대학', '개성공산대학', '강계교원대학', '백두산건축연구원', '개성예술대학', '강계제2사범대학', '갑산공업대학', '2월14일학생소년회관', '김일성종합대학', '평양도시설계사업소', '강계중학교', '원산농업대학', '정준택원산경제대학', '최희숙함흥제1교원대학', '평양의학대학', '장철구평양상업대학', '고려성균관', '김철주사범대학', '평양기계대학', '김형직사범대학', '조옥희해주교원대학', '함흥화학공업대학', '김일성고급당학교', '평양미술대학', '리계순사리원제1사범대학', '한덕수평양경공업대학', '창덕학교', '함흥의학대학', '평양학생소년궁전', '인민경제대학', '김정숙탁아소', '김책공업종합대학', '조선체육대학', '혜산교원대학', '강계제1사범대학', '사리원교원대학', '정일봉중학교', '동평양제1중학교', '흥남공업대학', '평양교원대학', '평양외국어대학', '만경대중학교', '자강도농업과학분원', '평양연극영화대학', '김정숙제1중학교', '평양학원', '해주제2사범대학', '평양인쇄공업대학', '사리원제2사범대학', '개성학생소년궁전', '황해남도농업과학분원', '평양교예학원', '남포사범대학', '평성의학대학', '평양천문대', '평양공업대학', '신의주공업대학', '신의주영예군인학교', '혜산농림대학', '김보현대학', '신의주제2사범대학', '평양수예연구소', '고건원공업대학', '창광유치원', '평양제1중학교', '평양외과대학', '길주임업단과대학', '평양남새과학연구소', '평성교원대학', '평양철도대학', '해주공업대학', '함경남도농업과학분원', '안주공업대학', '평양9.15주탁아소', '신의주교원대학', '피현국토관리대학', '만경대혁명학원', '함흥임상의학연구소', '평성석탄공업대학', '강계체육대학', '원산중등학원', '희천공업대학', '창전소학교', '남포공업대학', '평양농업대학', '남포혁명학원', '혜산광업대학', '회령경공업전문학교', '남포교원대학', '나진해운대학', '신의주경공업대학', '평양컴퓨터기술대학', '사리원공업대학', '청진광산금속대학', '어랑군농기계전문학교', '평안북도농업과학분원', '태탄농업전문학교', '해주의학대학', '대홍단농림전문학교', '신의주농업대학', '사리원지질대학', '청진의학대학', '삭주군당학교', '함흥컴퓨터기술대학', '함흥제2교원대학', '평양화성공업대학', '원산공산대학', '곡산농업전문학교', '평양국제부녀절50주년유치원', '조군실원산공업대학', '배천광업전문학교', '평산농업전문학교', '단천공업대학', '단천광업단과대학', '평안남도당학교', '삼흥중학교', '용강경제전문학교', '함경남도당학교', '개천역', '평양역', '길주청년역', '갈천역', '개풍역[토성역]', '승리거리', '간리역', '천리마거리', '안상택거리', '광복거리', '김책항', '충성의다리', '모란봉거리', '서해갑문', '서문거리', '보통교', '평양국제항공역', '영광거리', '만수대거리', '통일거리', '서성거리', '봉화거리', '칠성문거리', '옥류교', '영웅거리', '경흥거리', '황금벌네거리', '거차역', '신의주청년역', '새마을거리', '화도역', '비파거리', '시중호역', '동평양역전', '원산역', '하신거리', '옥류교거리', '해방산거리', '청년거리', '붉은거리', '역전거리[술막거리]', '신남포역', '오탄강안거리', '대학거리[인민경제대학앞거리]', '평남신덕역', '삼천역[삼천온천역]', '배화역', '서포역', '삼지연역', '금릉동굴', '남포[당포]', '못가역', '복계역', '김책역', '묘향산역', '두만강역', '배산점역', '동대원거리', '창광거리', '산수역', '인흥거리', '신의주항', '덕동역', '칠골역', '재동역', '역전거리', '평남온천역', '금천역', '세포청년역', '혁신거리', '후평청년역', '덕원역', '문수거리', '월봉역', '북창역', '탑제거리', '상신거리', '옥평역', '한포역', '신령리역', '대평역', '청수역', '연안역', '곡산다리', '대령강역', '송화역', '재령역', '원리역', '서천거리', '북송리역', '신대역', '선천역', '검산리역', '동정호역', '남포거리', '강서역', '해주항', '각암역', '신계역', '과일역', '금강산청년역', '귀성역', '중평역', '지하리역', '북신현역', '청춘거리', '자작역', '청남역', '도내역', '수교역', '북계수역', '송화온천역', '고성역', '이천청년역', '방현역', '신강령역', '상도내역', '동광량역', '문천역', '천동역', '평천강안거리', '서광량역', '석탕온천역', '문동청년역', '풍천역', '신흥동역', '석름역', '비단항', '체육촌거리[윤환선거리]', '신성천역', '태백산성역', '판막역', '남신의주역', '신생역', '수풍역', '동사리원역', '맹중리역', '삼사역', '구현역', '선교강안거리', '서평양역', '침촌청년역', '백산청년역', '새살림거리', '금산포역', '전천역', '청강역', '곽산역', '숙천역', '긴등역', '봉산역', '신주막역', '신온역', '체육촌', '원산항', '충성다리', '송남청년역', '피현통로', '은산역', '부풍역', '신의주통로', '학현역', '후창역', '신천역', '용천역', '연평역', '북중역', '동평양역', '기산청년역', '침교역', '구룡평역', '상단역', '굴송역', '삼덕역', '천수역', '피현역', '연암역', '금봉강역', '하황토역', '대택역', '염주역', '평산역', '회령청년역', '위연역', '개성역', '청계역', '평성역', '희천포', '평양배재나루터', '운흥역', '양덕역', '성천역', '혜산청년역', '동선봉역', '운흥리역', '순안역', '강안역', '함흥역', '선봉역[백학역]', '고원역', '청천강역', '두포역', '석하역', '남중역', '송가역', '청진청년역', '성천갑문', '신안주청년역', '양곡역', '사리원청년역', '해주청년역', '삭주통로', '장연역', '흥수역', '홍의역', '서하역', '태천역', '정주청년역', '신련포역', '문덕역[만성역]', '백암청년역', '삼등역', '웅상역', '새동역', '사회역', '청학역', '명호역', '대동강역', '가창역', '벽성역', '구장청년역', '팔원청년역', '남덕역', '남계역', '청룡역', '미림역', '명고역', '송림청년역', '석현역', '온정역', '삼방역', '운전역', '만달리역', '송신역', '중이역', '상황토역', '장상역', '대교역', '부포역', '강령역', '천태역', '어파역', '부흥역', '봉학역', '대오천역', '서두역', '은파역', '묵천역', '정도역', '수양역', '거흥역', '내동역', '회안역', '염탄역', '계정역', '황주역', '서흥역', '천내역', '오현역', '옹진역', '남애역', '금평역', '안변역', '오계역', '내중역', '운암역', '배천역', '홍현역', '은률역', '기탄역', '물개역', '청단역', '황해룡문역', '검불랑역', '성산역', '딴메거리', '사도역', '마영역', '흑교역', '지수역', '신양역', '신룡역', '연중역', '구정역', '풍년역', '의주나루터', '3대혁명전시관', '고려박물관', '인민문화궁전', '모란봉극장', '평양혁명사적지답사숙영소', '천리마동상', '동평양대극장', '송도원국제소년단야영소', '평양체육관', '평양교예극장', '중앙동물원', '왕재산혁명박물관', '정방산유원지', '삼지연스키장', '대성산유원지', '만수대예술극장', '4.25문화회관', '만수대분수공원', '김일성광장', '삼지연혁명전적지답사숙영소', '김일성종합대학과학도서관', '조선혁명박물관', '주체사상탑', '평양교예단', '신의주역사박물관', '인민대학습당', '만수대대기념비', '청년중앙회관', '개선영화관', '학당골분수공원', '개성시예술단', '조국해방전쟁승리기념탑', '집선봉전망대', '창광원공원', '함경남도예술단', '김일성종합대학체육관', '강안공원', '빙상관', '중앙미술창작사', '칠성대', '금수산기념궁전', '원산동물원', '평양종합인쇄공장', '국제친선전람관', '만경대유희장', '평안남도김일성동지혁명사적관', '평안북도김일성동지혁명사적관', '영명사터', '5월1일경기장', '평양볼링관', '김일성경기장', '보천보전투승리기념탑', '평양대극장', '만수대텔레비전방송', '수영경기관', '경암산공원', '평양신문사', '몽금포해수욕장', '양각도축구경기장', '만경대혁명사적관', '평양국제문화회관', '고방산성터', '남포체육촌', '오탄아동공원', '평북일보', '평양시체육선수단', '창광원', '삼지연빙상경기장', '송진산전투장소', '삼지연전적지', '평양인형극단', '평양고등교육도서인쇄공장', '남포신문', '조선예술영화촬영소', '해방산공원', '해방탑', '안주극장', '함흥대극장', '개성시김일성동지혁명사적관', '태권도전당', '사리원문화회관', '판문각', '상흥아동공원', '자강도김일성동지혁명사적관', '중경기관', '조선미술박물관', '백송혁명사적관', '메아리사격관', '우의탑', '장자산소년단야영소', '평양골프장', '평산봉수대', '조선민속박물관', '정주청년체육관', '평양석암소년단야영소', '서산축구경기장', '평성방송', '신의주시경기장', '집단체조창작단', '탁구경기관', '황해북도예술단', '함남일보', '개성신문', '강계시경기장', '중앙식물원옹진분원', '애국열사릉', '회령시혁명사적관', '강계역사박물관', '사리원청년경기장', '명고제터거리', '함북일보', '강계방송', '원산방송', '백두산밀영', '용악산소년단야영소', '민예전시관', '감토봉전적지', '평양국제영화회관', '문수공원', '원산청년회관', '함흥역사박물관', '개성문화회관', '어은혁명사적지', '황해남도예술단', '대홍단혁명전적지', '신풍경기장', '함경북도예술단', '신천박물관', '평안북도예술단', '평양시소년단등산야영소', '함흥경기장', '봉화혁명사적관', '자강도예술단', '양강도예술단', '함흥방송', '봉화예술극장', '혜산시인민경기장', '개성방송', '개성물놀이장', '남포시립극장', '신의주방송', '사리원방송국', '원산혁명사적관', '선봉혁명사적관', '혜산방송', '용연군문화회관', '통일전선탑', '대홍단종합농장유래비', '유진해군정찰장소[감토봉전적지]', '평양방직공장', '평양기초식품공장', '만경대영예군인만년필공장', '남포편직공장', '평양어린이옷공장', '마람배합사료공장', '회령곡산공장', '평양신발공장', '평양어린이식료품공장', '경성도자기공장', '신의주화학섬유공장', '회령제지공장', '광복거리김치공장', '길주식료공장', '사리원방직공장', '평양창광옷공장', '자남산수출피복공장', '원산영예군인수지일용품공장', '개성고려인삼주공장', '평양곡산공장', '신의주신발공장', '만수대윈드아시아합작회사', '남포전극공장', '평양일용품공장', '신의주법랑철기공장', '묘향산의료기구공장', '벽동가구공장', '평성합성가죽공장', '사리원타월수출품공장', '평양제사공장', '함흥곡산공장', '평양남자옷공장', '개성수지일용품공장', '평양목재공장', '평양구두공장', '강계포도술공장', '혜산방직공장', '길주펄프공장', '함흥영예군인수지일용품공장', '혜산철제일용품공장', '함흥목재가공공장', '태천철제일용품공장', '혜산들쭉가공공장', '함흥모방직공장', '평양애국편직물공장', '의주곡산공장', '평양선교편직공장', '개성방직공장', '삭주식료공장', '평양방직기재공장', '평양염화비닐신발공장', '애국모란피복공장', '곡산식료공장', '신의주방직공장', '혜산들쭉가공공장삼지연분공장', '사리원곡산공장', '대동강맥주공장', '향산종합식료공장', '생기령요업공장', '평양조명기구종합공장', '평양밀가루종합가공공장', '영변견직공장', '평양대흥모피가공공장', '평양정미공장', '삭주직물공장', '평양고무공장', '평양8월17일부재공장', '삭주수출솔공장', '길주합판공장', '개성종합식료공장', '개성사기제품공장', '회령크라프트지공장', '원산방직공장', '혜산신발공장', '평양가죽이김공장', '보통강양해합영회사', '경련애국사이다공장', '함흥염화비닐신발공장', '안악식료공장', '대동강구역식료품종합상점', '평양모란영예군인악기공장', '태천초물제품공장', '문천영예군인전기일용품공장', '혜산종이공장', '평산식료공장', '평양알루미늄제품공장', '금강식료공장', '함흥건설자기공장', '원산철제일용품공장', '요덕종이공장', '신안주직물공장', '안변식료공장', '평양모피수출품가공공장', '정주수출피복공장', '원산수출피복공장', '평양필름공장', '사리원담배공장', '판문초물제품공장', '벽성영예군인식료공장', '안악초물공장', '신의주구두공장', '신의주가정용품공장', '안변요업공장', '단천가죽일용품공장', '안학궁왕궁우물', '평남관개수로', '만경대닭공장', '어대진수산사업소', '평양돼지공장', '대홍단군종합농장', '평남관개관리소', '단천수산사업소', '만경대양어장', '평양과수농장', '광명성제염소', '몽금포수산사업소', '내중간선', '희새봉물동', '평양온실농장', '사리원과수농장', '두단오리공장', '남포제염소', '단천저수지', '어대진어구공장', '영변양어장', '모봉저수지', '평양제1백화점', '청류관', '엠페러오락호텔[영황호텔]', '옥류관', '개성민속여관', '개성백화점', '평양역전백화점', '평양아동백화점', '삼지연여관', '서평양백화점', '평양고려호텔', '사리원여관', '사리원백화점', '평양지성차봉사소', '평양지하상점', '평양단고기집', '향산호텔', '양각도국제호텔', '대성백화점', '평양숭어국집', '남포백화점', '혜산여관', '무산광산연합기업소', '은률광산', '갑산광산', '갑산광상', '고건원탄광', '고무산광산', '은률광산대형장거리벨트컨베이어수송관리소', '혜산광상', '오가산임산사업소', '풍서임산사업소', '태탄광산', '태천광산', '온성탄광', '북계수탄광', '명천탄광', '신창탄광[평남신창종합청년탄광]', '혜산청년광산', '평남신창종합청년탄광', '부래산석회석광산', '백두산청년들쭉사업소', '평산탄광', '회령탄광기계공장', '문천탄광', '평산광상', '함경북도조림사업소', '메아리음향사', '남포통신기계공장', '평양영화필름복사공장', '평양도시계획설계사업소', '평북제련소', '동평양화력발전소', '황해제철연합기업소', '용성기계연합총국', '원산조선소', '승리화학연합기업소', '순천비날론공장', '금강원동합영회사', '단천제련소', '원산칠감공장', '흥남제약공장', '상원시멘트연합기업소', '함흥실리케이트벽돌공장', '평양강철공장', '6.16화력발전소', '강계청년발전소', '나남제약공장', '신의주화장품공장', '단천마그네시아공장', '평양방직기계공장', '남포조선소연합기업소', '남포선박수리공장', '박천선박수리공장', '평양화력발전소', '남포선박공장', '만경대공작기계공장', '금강산발전소', '평양수지건재공장', '대동강축전지공장', '함북조선소연합기업소', '희천공작기계공장', '피현벽돌공장', '평양제약공장', '남포어린이약공장', '평양화학건재공장', '만경대뢴트겐공장', '평양화장품공장', '원산시멘트공장', '부래산시멘트공장', '고무산시멘트공장', '흥남제련소', '승호리시멘트공장', '평양승강기공장', '원산전선공장', '평양금속건재공장', '정주전진호트랙터조립공장', '평양기포부재공장', '안악군농기계작업소', '원산가성소다공장', '혜산흄관공장', '요덕제약공장', '문천염료공장', '문천물감공장', '의주건재공장', '정주트랙터부속품공장', '평안남도', '황해북도', '공민왕릉', '단군릉', '을밀대', '백상루', '인풍루', '왕건왕릉', '소현서원', '최승대', '강선루', '금강산유물유적', '경성읍성', '부벽루', '남평양유적', '유점사터', '성불사', '안악3호무덤', '정방산성', '길주동헌', '함흥본궁', '불영대', '연광정', '강서사', '만월대', '보통문', '개성남대문', '구주성', '경암루', '만수대궁전터', '함흥성', '함흥선화당', '강계아사', '벽동남문', '숭령전', '단천아사터', '동명왕릉(東明王陵·진주묘, ...', '숭인전', '안주성', '함흥성구천각', '칠성문', '중강군토성리유적(中江郡土城里...', '의주연대봉수', '삼성사', '벽동서문', '귀진사', '벽동동문', '광법사', '동명왕릉능원내의14호무덤과1...', '동명왕릉능원내의7호무덤과9호...', '정양사', '표훈사터', '육승정', '대동문', '부용당터', '동명왕릉', '치악산성[배천산성...', '자혜사', '길주향교', '황룡산성', '동명왕릉능원내의고분군', '영변철옹성', '부용당', '영변남문', '원산산성', '배천산성', '고암산성터', '봉오산봉수', '안악제3호무덤', '개성옛성', '혜산진성', '평양역전벽화고분(平壤驛前壁畵...', '성불사터', '미둔성지', '만달산고분군', '정주동성', '마귀할미바위', '쌍기둥무덤', '안악제1호무덤', '제월루', '와산동유적', '비백산봉수터', '회령학포북봉봉수(會寧鶴浦北峯...', '하삼봉원시유적(下三峯原始遺跡...', '박천산성', '신계사터', '안악1호무덤', '회령행성', '안악제2호무덤', '수항루', '민봉봉수', '평안남도', '황해북도', '고방산휴양소', '평양시제3인민병원', '시중호요양소', '김만유병원', '송화온천', '고려의학종합병원', '함흥의학대학병원', '평양산원', '송흥온천', '삭주온천', '함경남도구강병예방원', '남포시구강예방원', '달천온천', '평양친선병원', '조선적십자종합병원', '평양시제1인민병원', '석탕온천요양소', '해주의학대학병원', '피현휴양소', '십일온천', '삭주휴양소', '송화온천요양소', '남포시인민병원', '남포시산원', '침교요양소', '송단휴양소', '청진의학대학병원', '단천휴양소', '학송휴양소', '선천군요양소', '혜산산원', '성천휴양소', '평안남도', '황해북도', '평양준평원', '강계분지', '평양벌[평양준평원]', '순안벌', '개성분지', '긴등벌', '함주백리벌', '함흥벌', '함흥벌[함주백리벌]', '평양벌', '갑산분지', '정주벌', '희천분지', '함흥벌[함주벌 , 함주백리벌]', '금강산터', '곡산분지', '길주벌', '말메뒤벌', '옥평벌', '몽금포벌', '영변분지', '남포벌', '개성벌', '평양목', '치마대', '태천분지', '사리원벌', '의주벌', '안봉벌', '회령분지', '안변삼십리벌', '평산벌', '복계벌[복깨벌]', '평안남도', '황해북도', '칠성바위[칠성봉]', '칠성봉', '경성만', '경성만[청진만]', '함흥만', '용대갑', '오포단[우암각]', '만풍산', '신증산', '평안남도', '황해북도', '몽금포코끼리바위', '명경대', '은선대[은신대]', '흥남구경대', '삼불암', '칠보대', '길주조개화석층', '흑교삼엽충화석', '금강산닭알바위', '만월대', '을밀대', '칠성대', '마귀할미바위[차돌바위]', '은선대', '초대봉', '칠성대[칠삭대]', '칠성대[칠층대]', '할미바위', '백두산만물상', '할미바위[할머니바위]', '길주장덕', '금바위', '고천덕', '쌍류대', '곰동산바위', '마구할미바위', '평안남도', '황해북도', '시중호', '삼지연', '상팔담', '일룡담', '금강산저수지', '곡산저수지', '묘향산팔담', '평성저수지', '안봉저수지', '단천저수지', '견룡담', '갑산저수지', '빨래해주']

unique_count = pd.Series(location_list).nunique()
print(unique_count)

# 리스트 데이터를 JSON 파일로 저장
with open('/content/drive/MyDrive/Colab Notebooks/location_list.json', 'w', encoding='utf-8') as f:
    json.dump(location_list, f, ensure_ascii=False, indent=4)

# JSON 파일에서 리스트 불러오기
with open('/content/drive/MyDrive/Colab Notebooks/location_list.json', 'r', encoding='utf-8') as f:
    locations_list_from_file = json.load(f)  # 리스트 형태라고 가정

# 파일에서 불러온 데이터를 사용하여 필터링
filtered_locations = total_df_exploded[total_df_exploded['location_clean'].isin(locations_list_from_file)]

# 결과 확인
filtered_locations

# 인덱스를 0부터 다시 시작하도록 설정
final_df = filtered_locations.reset_index(drop=True)

# 결과 출력
final_df

final_df['location'] = final_df['location_clean']

final_df

final_df = final_df.drop(columns=['locations', 'location_clean', 'contents'])

final_df

"""# **Google API 사용**"""

final_df

# 'location' 와 'content' 컬럼에서 중복된 값 제거
final_df = final_df.drop_duplicates(subset=['location'])

# 결과 출력
final_df

test_building_addreess = []
test_building_lat = []
test_building_lng = []

gmaps = googlemaps.Client(gmap_keys)

# 예시: place_db에 있는 이름들을 하나씩 처리
for name in final_df['location']:
    if not name or pd.isna(name):  # 빈 값 체크
        print(f"Skipping empty location: {name}")
        test_building_addreess.append("주소를 찾을 수 없습니다.")
        test_building_lat.append(None)
        test_building_lng.append(None)
        continue  # 다음 루프로 넘어감

    tmp = gmaps.geocode(name, language='ko')

    if tmp:
        test_building_addreess.append(tmp[0].get("formatted_address"))
        tmp_loc = tmp[0].get("geometry")
        test_building_lat.append(tmp_loc['location']['lat'])
        test_building_lng.append(tmp_loc['location']['lng'])
    else:
        test_building_addreess.append("주소를 찾을 수 없습니다.")
        test_building_lat.append(None)
        test_building_lng.append(None)

    print(name + '-->' + test_building_addreess[-1])

test_building_lat

test_building_lng

final_df['address'] = test_building_addreess
final_df['latitude'] = test_building_lat
final_df['longitude'] = test_building_lng

final_df

# "주소를 찾을 수 없습니다." 값의 개수 확인
address_count = (final_df['address'] == "주소를 찾을 수 없습니다.").sum()
print(f"주소를 찾을 수 없습니다.인 행의 개수: {address_count}")

# address컬럼에 '조선민주주의인민공화국'이 포함된 행만 필터링
final_df = final_df[final_df['address'].str.contains('조선민주주의인민공화국', na=False)]

# 결과 출력
final_df

# 'latitude' 와 'longitude' 컬럼에서 중복된 값 제거
final_df = final_df.drop_duplicates(subset=['latitude','longitude'])

# 결과 출력
final_df

# 인덱스를 0부터 다시 시작하도록 설정
final_df = final_df.reset_index(drop=True)

# 결과 출력
final_df

final_df_mid_lat = final_df['latitude'].mean()  # 위도 평균 계산
final_df_mid_lng = final_df['longitude'].mean()  # 경도 평균 계산

print(final_df_mid_lat, final_df_mid_lng)

"""# **Folium 시각화**"""

# Folium이 지원하는 색상 리스트
icon_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue',
               'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray',
               'black', 'lightgray']

# 고유한 장소 리스트 생성
unique_places = final_df['location'].unique()

# 장소별 색상 매핑 (고유한 장소 개수만큼 색상 지정, 부족하면 반복)
place_color_map = {place: icon_colors[i % len(icon_colors)] for i, place in enumerate(unique_places)}

# 지도 생성
map_1 = folium.Map(location=[final_df_mid_lat, final_df_mid_lng], zoom_start=6)

# 마커 추가
for n in final_df.index:
    place = final_df['location'][n]
    color = place_color_map[place]  # 해당 장소의 색상 가져오기

    folium.Marker(
        [final_df['latitude'][n], final_df['longitude'][n]],
        icon=folium.Icon(color=color),  # 아이콘 색상 변경
        tooltip=f'<b>- place</b>: {place}',
    ).add_to(map_1)

map_1

# data_df와 final_df를 content 컬럼을 기준으로 merge
total_final_df = data_df.merge(final_df[['content', 'location', 'address', 'latitude', 'longitude']],
                          on='content', how='left', suffixes=('', '_final'))

# NaN 값들을 final_df에서 가져온 값으로 채우기
for col in ['location', 'address', 'latitude', 'longitude']:
    total_final_df[col] = total_final_df[col].fillna(total_final_df[f"{col}_final"])

# 임시 컬럼 삭제
total_final_df.drop(columns=['location_final', 'address_final', 'latitude_final', 'longitude_final'], inplace=True)

# 결과 확인
total_final_df

total_final_df.info()
