# 일본 여행 경비 예측 서비스
## 목차
>1) [팀 프로젝트의 목표](#팀-프로젝트의-목표)
>2) [프로젝트 구성원](#프로젝트-구성원)
>3) [프로젝트 파이프라인](#프로젝트-파이프라인)
>4) [프로젝트 과정](#프로젝트-과정)
>5) [프로젝트 회고](#프로젝트-회고)
## 팀 프로젝트의 목표
- 일본 여행 경비를 예상해 최적의 여행을 위한 서비스를 제공을 목표
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
  - Selenium 사용해 네이버 호텔 및 항공권 웹 데이터를 크롤링 및 자동화 작업, 크롤링 데이터 CSV 파일로 저장
- 대시보드 작성(Looker Studio)
  - 대시보드를 고민중 Meata base와 Looker Studio중 진입 및 바로 수정 및 적용이 가능한 Looker를 채택  
    [항공권 대시보드 링크](https://lookerstudio.google.com/reporting/feefb17d-5196-4754-883a-b716340cd9a5/page/YzzXD)  
    [호텔 대시보드 링크](https://lookerstudio.google.com/reporting/b28f27d3-65eb-4e11-b791-ed570d2f7be9/page/nZ2XD)
<details>
  <summary>항공권 데이터 분석(상세보기 클릭)</summary>
    <ul>
      <li>항공권 데이터 46771 x 11 사용(네이버 항공편 사이트에서 오사카, 후쿠오카, 도쿄의 데이터)</li>
        <ol type=1>
          <li>학습 데이터 세부사항</li>
          <li>크롤링시 "2023-07-22" 같은 데이터를 연도, 월, 일로 데이터 세분화</li>
          <li>duration에 대한 문항을 불여 편리한 서비스를 제공할지 / 포함하여 더 정확한 정보를 제공할지 팀원들의 의견을 모음</li>
            <dl>-> 모델 학습 결과 duration을 포함했을 시 r2 값이 0.025 정도 높아지는 결과가 확인되서 포함하는 쪽으로 결정함</dl>
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
        <li>출발 & 도착 시간 컬럼은 불필요해 삭제처리</li>
        <li>direct flight 컬럼은 One-Hot encoding을 적용</li>
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
    <li>city의 경우 크롤링 과정에서 지역이 구분되어 있지 않아 One-Hot encoding을 적용시켜 구분함</li>
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
        <td>3개의 모델중 가장 높은 점수가 나왔으며 가장 안정적이어서 채택함 </td>
        <td>기본적인 Raondom 에서 Grid 기법을 이용했는데 더 낮은 점수에 안정성도 랜덤포레스트보다 낮아 채택하지 못함</td>
      </tr>
    </table>
  </ul>
</details>

- 데이터는 DBeaver를 사용해 MySQL로 데이터베이스에 저장
- ML 모델은 파이썬 라이브러리인 pkl을 사용해 복호화하여 사용함
- 이후 Flask 사용해 웹에서 데이터를 입력 받을시 모델을 이용해 최저값을 예측해서 웹에 리턴해주는 방식으로 진행함
### 완성된 결과물
![데이터 입력 창](https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/23127c09-bb2b-419c-9831-c1a1bca93e11)
![결과 출력](https://github.com/GOGUMAJELLY/AI_Team_Project1/assets/60537140/afdf924d-99e7-463f-9464-7692c3c2ee72)

## 프로젝트 회고
- 문제 해결 과정
  - 웹 크롤링 중 첫 페이지는 가져올 수 있는데 다음 2번째 이후로 가져오지 않고 크롤링이 에러가 뜸  
    > 팀원들끼리 상의한 결과 웹 페이지에서 각 Elements이 로딩되는 시간이 달라서 어느것이 가장 늦게 나오는지 모르고  
    > 시간이 오래 걸려도 데이터를 확실히 수집해야 해서 time.sleep()을 사용함  
  - 파일 같은걸 전부 한 폴더에 넣어 놨었는데 웹이 작동하지 않아서 문제를 공유함  
    > 파일마다 특정 폴더에 넣어야 제대로 작동이 한다 해서 파일 경로의 중요성을 깨달음
  - 시간이 부족해 웹 디자인을 어떻게 할지 의견을 모음  
    > 가장 직관적인 디자인으로 하자 결정
- 미흡한점
  - 내가 생각보다 SQL언어, 웹 디자인, Flask 사용이 많이 미숙하다는걸 알았고 도와줄려 했지만 큰 도움이 되진 않았다.
  - CS지식이 더 있었으면 웹 크롤링을 할때나 EDA 과정에서 더 빠르게 작업이 가능했을 것이다.
  - 개인적인 팀의 문제점중 하나가 있었는데 각자의 업무 진척도 및 문제점을 바로 공유 했으면 좋지 않았을까 생각을 한다.  
    > 내가 완료한 작업을 다른 팀원이 해메는 중 이였단걸 알앗을때 꽤 많은 시간이 흘러있었기 때문..
