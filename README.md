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

## 진행방식
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-21%2017-58-23.png)

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
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-24%2017-53-56.png)
<br>
##### Intertopic Distance Map & Top30_Most Relevant Terms for Topic 2 
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-24%2018-02-52.png)
<br>
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-24%2018-05-22.png)
<br>
##### Word_Cloud
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-24%2017-49-17.png)
<br>
##### GEOINT Data Visualization
![image](https://github.com/Kyungdeok-Koo/first-repository/blob/main/Aiffel_DataScientist_3rd/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202025-03-21%2015-35-47.png)

<br>
<br>

## 프로젝트 목적
- #### 방대한 기사 빅데이터를 요약 정리 및 해당분야에 관심있는 독자들에게 제공
  

<br>
