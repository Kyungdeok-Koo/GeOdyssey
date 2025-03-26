# GeOdyssey
##### YTN_NEWS에서 북한관련 기사들을 뽑아 Topic별로 관련 주제 및 지리정보를 도출하는 시스템

<br>
<br>

## 👨‍💻 Team 👨‍💻
|권미경|김가경|김진형|구경덕|손지현|
|:---:|:---:|:---:|:---:|:---:|
|팀장|팀원|팀원|팀원|팀원|

<br>
<br>

## 개요
### 주제
- Text Mining, Geoint로 탐사하는 북한사회
  - AI 기반 위성 영상 데이터셋 구축 및 공급과 다양한 출처의 데이터셋으로부터 위치와 속성정보를 통해 지리공간 분석 솔루션 제공

### 문제
- 최근 10년 간 북한 관련 국내 언론 보도는 수많은 정치.경제 등 사건,사고들이 혼재되어 축적
- 북한사회의 변동이 국내에 주요한 영향을 미치지만 키워드 빈도 분석만으로는 잠재된 주요 이슈 파악에 한계

    
 
### 목표
- 토픽모델링을 활용하여 주요 쟁점 및 흐름을 구조화하고, 북한 동향을 파악하고 미래 예측을 하기 위한 데이터 기반 구축
  - 복잡한 기사들을 주제별로 정리해 이슈 간 상호관계를 파악할 수 있도록 안내
  - 시공간 기반 정보 그래픽을 제공해서 북한 사회를 문자를 넘어 다차원적 해석이 가능하도록 지원
  - 향후 국제정치, 대북정책을 분석하여 위기를 예측하고 안보 전략을 수립하는 곳에 활용

<br>

## 데이터 & 기술스택
- YTN_NEWS 기사 
- Python
- Google Maps API
- Chardet
- Word_Cloud
- Urllib
- Konlpy
- Folium
- Nltk
    - Find
    - POS_Tag
    - Word_tokenizer  
- Selenium
    - Webdriver
       - Service
       - Options
    - ChromeDriverManager
- Gensim
- PyLDAvis
<br>

## 디렉터리 구조
```
├── 📑 README.md
├── 📑 requirements.txt        # 설치 파일 목록
└── 📑 GeOdyssey.py            # Crawling, Topic Modeling, Geoint 코드파일
```
<br>
<br>
<br>
<br>
<br>

## 진행방식
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-21%2017-58-23.png)

<br>
<br>
<br>
<br>
<br>

## 기술 스택
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-24%2017-43-52.png)

<br>
<br>
<br>
<br>
<br>
<br>

## 주요 기능
##### TOPIC 간의 유사성 및 관계 구조를 시각화하기 위해 활용
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2010-22-09.png)
<br>
<br>
<br>
##### Intertopic Distance Map & Top30_Most Relevant Terms for Topic 2 
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-24%2018-02-52.png)
<br>
<br>
<br>
##### Big Kinds Comparative Analysis
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-24%2018-05-22.png)
<br>
<br>
<br>
##### 2024_2025 Word_Cloud
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2010-25-11.png)
<br>
<br>
<br>
##### NLTK 고유명사 추출
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2010-45-42.png)
<br>
<br>
<br>
##### 정규 표현식 활용
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2010-49-35.png)
<br>
<br>
<br>
##### Google Maps API (주소 및 경.위도 좌표 추출)
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2010-51-03.png)
<br>
<br>
<br>
##### Folium 좌표 시각화
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2010-53-29.png)

<br>
<br>
<br>
<br>
<br>
<br>

## 최종 예상 결과
##### GEOINT Data Visualization
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-07-00.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-07-45.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-08-31.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-09-09.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-09-42.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-10-00.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-21%2015-35-47.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-14-41.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-15-01.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-15-24.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-15-40.png)
<br>
<br>
<br>
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-25%2011-16-01.png)

<br>
<br>
<br>
<br>
<br>
<br>
<br>

## 프로젝트 최종 목적
- #### 방대한 기사 빅데이터를 요약 정리 및 해당분야에 관심있는 독자들에게 제공
- # 데모 영상 🎥  

<p align="center">
  <a href="https://youtu.be/82nhGX_v9rE?si=KPm0ix_LHVz0aEZ4">
    <img src="https://img.youtube.com/vi/82nhGX_v9rE/0.jpg" alt="데모 영상">
  </a>
</p>

<p align="center">
  👉 <a href="https://youtu.be/82nhGX_v9rE?si=KPm0ix_LHVz0aEZ4">데모 영상 보기</a>
</p>

<br>
<br>
<br>
<br>
<br>
<br>
<br>

## 참고 사이트 주소
[공간정보교육포털](https://www.spacein.kr/)
<br>
[국토교통부 V-World 디지털트윈국토](https://www.vworld.kr/v4po_openapi_s001.do)
<br>
[국토정보플랫폼](https://map.ngii.go.kr/mi/openKey/openKeyInfo.do)
<br>
[국토지리정보원 북한지도](https://www.ngii.go.kr/kor/main.do)
<br>
[북한지역정보넷](https://cybernk.net/home/Default.aspx)
<br>
[빅카인즈](https://www.bigkinds.or.kr/)
<br>
[통계청 북한통계포털](https://kosis.kr/bukhan/index/index.do)
<br>
[통일부 북한동향 조회서비스](https://www.data.go.kr/data/15079311/openapi.do)
<br>
[통일부 북한정보포털](https://nkinfo.unikorea.go.kr/nkp/main/portalMain.do)
<br>
[통일부 북한지도](https://nkinfo.unikorea.go.kr/NKMap/)
<br>
[통일연구원](https://www.kinu.or.kr/main/index.do)
<br>
[통일 연구원 김정은 공개활동 보도분석 DB](https://www.kinu.or.kr/nksdb/)
<br>
[DailyNK](https://www.dailynk.com/)
<br>
[KDI 북한경제리뷰](https://www.kdi.re.kr/research/monNorth?year=2024)
<br>
[38 North](https://www.38north.org/)
<br>
[CNN](https://edition.cnn.com/2020/04/21/asia/gallery/kim-jong-un/index.html)

<br>
