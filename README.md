# 일본 여행 경비 예측 서비스
## 목차
>1) [팀 프로젝트의 목표](#팀-프로젝트의-목표)
>2) [프로젝트 구성원](#프로젝트-구성원)
>3) [프로젝트 파이프라인](#프로젝트-파이프라인)
>4) [프로젝트 과정](#프로젝트-과정)
>5) [프로젝트 회고](#프로젝트-회고)

## 팀 프로젝트의 목표
- 일본 여행 경비를 예상해 최적의 여행을 위한 서비스를 제공을 목표
### 기대효과
- 일본 여행갈 날짜 및 기간에 맞춰 항공편과 숙소의 최저가를 구해서 지출이 가장 큰 부분의 비용을 파악이 가능
## 프로젝트 구성원
|팀원|역할|프로젝트 담당 업무|
|---|---|---|
|경동연|팀장|항공편 데이터 ETL, ML 모델링 및 고객이 데이터 입력시 가격 예측이 가능한 Flask 서비스 개발|
|박재현|팀원|호텔 데이터 ETL, ML 모델링|
|장혜수|팀원|항공권&호텔 데이터 크롤링, 프론트엔드 웹 개발|
|정재훈|팀원|항공권&호텔 데이터 크롤링, 호텔 데이터 EDA 및 항공권, 호텔 대시보드 작성|
## 프로젝트 파이프라인
<img src="https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/957f9a43-b6ae-4ba3-a8ef-e64aefddfbc6" width='840' height='400'>

## 프로젝트 과정
- 웹 데이터를 크롤링
  - Selenium 사용해 네이버 호텔 및 항공권 웹 데이터를 크롤링 및 자동화 작업
  - 크롤링한 데이터를 분석
<details>
  <summary>항공권 데이터 분석(상세보기 클릭)</summary>
    <ul>
      <li>항공권 데이터 46771 x 11 사용(네이버 항공편 사이트에서 오사카, 후쿠오카, 도쿄의 데이터)</li>
        <ol type=1>
          <li>학습 데이터 세부사항</li>
          <li>크롤링시 "2023-07-22" 같은 데이터를 연도, 월, 일로 데이터 세분화</li>
          <li>duration에 대한 문항을 불여 편리한 서비스를 제공할지 / 포함하여 더 정확한 정보를 제공할지 회의</li>
            <dl>-> 모델 학습 결과 duration을 포함했을 시 r2 값이 0.025 정도 높아짐</dl>
                	<div markdown="1">
                    <table>
                      <tr align=center>
                        <td>duration 제외</td>
                        <td>duration 포함</td>
                      </tr>
                      <tr>
                        <td><img src ="https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/6da9cda4-3f04-465b-8b68-314bbc714bcb"></td>
                        <td><img src ="https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/6245bc90-400d-4ca0-8e51-634ea4053a7c"></td>
                      </tr>
                    </table>
                  </div>
          </ol>
       </ul>
    <ul>
        <li>모델 성능 결과 더 정확한 정보를 주는것이 좋음으로 duration 문항을 포함, 그 과정에서 출발 & 도착 시간 데이터는 불필요해 삭제처리</li>
        <li>direct flight 컬럼은 One-Hot encoding을 사용해 단순화 시킴</li>
        <li>예측변수 : price , 입력변수 : price 이외 컬럼들</li>
        <li>사용한 모델 : XGBoost Regression</li>
          <dl>사용한 이유:</dl>
        <ol type=1>
          <li> 작업을 병렬로 처리하기 때문에 학습 속도가 빠름</li>
          <li>Greedy 알고리즘을 사용해 분산처리 하므로 과대적합의 위험이 낮아짐</li>
          <li>모델 자체가 유연해 커스터마이징이 쉽기 때문에</li>
        </ol>
    </ul>
</details>
<details>
  <summary>호텔 데이터 분석(상세보기 클릭)</summary>
  <ul>
    <table>
      <tr align=center>
        <td>전처리 전 데이터</td>
        <td>전처리 후 데이터</td>
      </tr>
      <tr>
        <td><img src="https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/3a598c17-9c23-47af-b5f8-8cb414e35bc1"></td>
        <td><img src="https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/9c13dfdc-b2fd-478b-9662-529ed1fd36a3"></td>
      </tr>
    </table>
    <li>date : 연도/월/일 합쳐져 있음으로 연도, 월, 일 구분해 컬럼 생성</li>
    <li>city의 경우 크롤링 과정에서 지역이 구분되어 있지 않아 One-Hot encoding을 사용해 3가지로 구분</li>
    <li>예측변수 : price, 입력변수 : price 이외 컬럼들</li>
    <li> 모델 선정 과정</li>
    <table>
      <tr>
        <td>Linear Regression</td>
        <td>Random Forest</td>
        <td>Random Forest+Grid Search</td>
      </tr>
      <tr>
        <td><img src="https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/bd15c855-663a-4705-a602-abbfc2f1163b"></td>
        <td><img src="https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/9da47a29-abb9-4d5c-bc8c-b7d7e362c7a3"></td>
        <td><img src="https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/a1c56181-f5c5-4dac-b480-fc4b1c1f7900"></td>
      </tr>
      <tr>
        <td>선형 모델의 경우 학습도 제대로 이루어 지지 않아 r2스코어의 값이 매우 낮았음</td>
        <td>운이 좋게도 3개의 모델중 가장 높은 점수가 나왔으며 가장 안정적임</td>
        <td>기본적인 Raondom 에서 Grid 기법을 이용했는데 더 낮은 점수에 안정성도 랜덤포레스트보다 낮아 채택하지 못함</td>
      </tr>
    </table>
  </ul>
</details>

- 데이터는 DBeaver를 사용해 MySQL로 데이터베이스에 저장
- ML 모델은 파이썬 라이브러리인 pkl을 사용해 복호화하여 사용함
- 이후 Flask 개발해 웹에서 데이터를 입력 받을시 모델을 이용해 최저값을 예측해서 웹에 리턴해주는 방식으로 진행함
### 완성된 결과물
![데이터 입력 창](https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/23127c09-bb2b-419c-9831-c1a1bca93e11)
![결과 출력](https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/afdf924d-99e7-463f-9464-7692c3c2ee72)

## 프로젝트 회고
- 느낀점
  >팀 프로젝트를 하면서 자신이 맡은 부분을 다하면 남는 시간이 있었는데  
  >그럴때 뭔가 불안해서 나만 도움이 안되고 있다는 느낌이 좀 들었다..  
  >그래서 크롤링이 끝나고 팀원들이 각자 맡은부분을 하고 있을때 DB에 적재하는 과정을 연습해보자 했지만  
  >실패해서 팀원들이 도와주었고 마지막에 가서 프론트엔드의 웹 디자인을 조금 해서 보여주니  
  >나쁘지 않다는 의견이 있어 반영을 했고 예측 결과 출력된 페이지를 도울 수 있어 기뻣다.  
  >만약 다음에 이런 팀 프로젝트를 다시 하게 된다면 불안해 하지말고 무리해서 도와줄려 하지말자.  
  >언제나 느꼇지만 팀 프로젝트의 경우 팀원과 소통이 가장 최우선이다.  
    소통이 안되면 마감기한이 다 되어갈때 기다리는 팀원들은 초조해지며 중간 과정에서는 프로젝트의 방향성이 틀어질 수 있기 때문이라 생각한다  
- 미흡한점
  - 내가 생각보다 SQL언어, 웹 디자인, Flask 사용이 많이 미숙하다는걸 알았고 도와줄려 했지만 큰 도움이 되진 않았다.
  - CS지식이 더 있었으면 웹 크롤링을 할때나 EDA 과정에서 좀더 의견을 낼 수 있지 않았을까 한다.
  - 개인적으로 계속 일을 하지 않으면 내가 한 일이 없다 생각하는 경향이 있는걸 이번에 깨달았다. 이런 생각을 없애기 위해 노력을하자!
