from flask import Flask, request, render_template, redirect
import joblib
import pickle
import pandas as pd
import os
import numpy as np

app = Flask(__name__)

JP_air_model = joblib.load('./models/JP_air_model.pkl')

# models 폴더 경로
models_folder = 'models'

# 파일 경로 생성
file_path = os.path.join(models_folder, 'Hotel_rf_model.pkl')

# 파일 읽기
with open(file_path, 'rb') as f:
    JP_hotel_model = pickle.load(f)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

route_data = {
    'GMP_to_FUK': ['에바항공', '중국국제항공', '일본항공', 'ANA', '제주항공', '에어부산', 'ANA항공', '여러항공사'],
    'GMP_to_HND': ['에바항공', '중국국제항공', '일본항공', '대한항공', '아시아나항공', '상하이항공', 'ANA', '여러항공사', 'ANA항공'],
    'GMP_to_KIX': ['상하이항공', '제주항공', '에바항공', '중국국제항공', '한에어', '대한항공', '아시아나항공', '여러항공사', '일본항공', 'ANA'],
    'GMP_to_NRT': ['상하이항공', '제주항공', '에바항공', '중국국제항공', '대한항공', '일본항공', 'ANA'],
    'ICN_to_FUK': ['한에어', '에바항공', '싱가포르항공', '중국국제항공', '제주항공', '티웨이항공', '에어서울', '아시아나항공', '대한항공', '일본항공', 'ANA', '홍콩익스프레스항공', '필리핀항공', '비엣젯항공', '홍콩항공', '싱가포르항공'],
    'ICN_to_HND': ['상하이항공', '에바항공', '중국남방항공', '싱가포르항공', '중국국제항공', '피치항공', '일본항공', 'ANA', '캐세이퍼시픽항공', '아시아나항공', '대한항공', '중국동방항공'],
    'ICN_to_KIX': ['에바항공', '대한항공', '피치항공', '일본항공', 'ANA', '캐세이퍼시픽항공', '아시아나항공', '중국국제항공', '상하이항공'],
    'ICN_to_NRT': ['제주항공', '마카오항공', '대한항공', '한에어', '홍콩항공', '상하이항공', '아시아나항공', '필리핀항공', '베트남항공', '에바항공', '캐세이퍼시픽항공', '비엣젯항공', '상해항공', '일본항공', '티웨이항공', '진에어', 'ANA'],
    'FUK_to_GMP': ['에바항공', '중국국제항공', '일본항공', 'ANA', '제주항공', '에어부산', 'ANA항공', '여러항공사'],
    'HND_to_GMP': ['에바항공', '중국국제항공', '일본항공', '대한항공', '아시아나항공', '상하이항공', 'ANA', '여러항공사', 'ANA항공'],
    'KIX_to_GMP': ['상하이항공', '제주항공', '에바항공', '중국국제항공', '한에어', '대한항공', '아시아나항공', '여러항공사', '일본항공', 'ANA'],
    'NRT_to_GMP': ['상하이항공', '제주항공', '에바항공', '중국국제항공', '대한항공', '일본항공', 'ANA'],
    'FUK_to_ICN': ['한에어', '에바항공', '싱가포르항공', '중국국제항공', '제주항공', '티웨이항공', '에어서울', '아시아나항공', '대한항공', '일본항공', 'ANA', '홍콩익스프레스항공', '필리핀항공', '비엣젯항공', '홍콩항공', '싱가포르항공'],
    'HND_to_ICN': ['상하이항공', '에바항공', '중국남방항공', '싱가포르항공', '중국국제항공', '피치항공', '일본항공', 'ANA', '캐세이퍼시픽항공', '아시아나항공', '대한항공', '중국동방항공'],
    'KIX_to_ICN': ['에바항공', '대한항공', '피치항공', '일본항공', 'ANA', '캐세이퍼시픽항공', '아시아나항공', '중국국제항공', '상하이항공'],
    'NRT_to_ICN': ['제주항공', '마카오항공', '대한항공', '한에어', '홍콩항공', '상하이항공', '아시아나항공', '필리핀항공', '베트남항공', '에바항공', '캐세이퍼시픽항공', '비엣젯항공', '상해항공', '일본항공', '티웨이항공', '진에어', 'ANA'],
}

# 성급 별 출력 함수
def get_star_rating_symbol(star_rating):
    full_star = '★'
    half_star = '☆'
    empty_star = '☆'
    
    num_full_stars = int(star_rating)
    num_half_stars = round(star_rating * 2) % 2
    
    stars = full_star * num_full_stars + half_star * num_half_stars + empty_star * (5 - num_full_stars - num_half_stars)
    return stars
# 숙소 머물 날 계산 함수
def calculate_stay_period(dep_date, re_date):
    dep_year, dep_month, dep_day = map(int, dep_date.split('-'))
    re_year, re_month, re_day = map(int, re_date.split('-'))
    departure_date = pd.to_datetime(f'{dep_year}-{dep_month}-{dep_day}')
    return_date = pd.to_datetime(f'{re_year}-{re_month}-{re_day}')

    stay_period = return_date - departure_date
    num_nights = stay_period.days
    num_days = num_nights + 1

    return num_nights, num_days

@app.route('/project_web', methods=['GET','POST'])
def predict_web():
    # 출발하는 날짜, 예시: '2023-07-22'
    dep_date= request.form.get('departure_date')
    dep_year, dep_month, dep_day = map(int, dep_date.split('-'))

    # 돌아오는 날짜
    re_date= request.form.get('return_date')
    if re_date:
        re_year, re_month, re_day = map(int, re_date.split('-'))
        dates = pd.date_range(start=dep_date, end=re_date)
    else:
        re_date = dep_date
        re_year, re_month, re_day = map(int, dep_date.split('-'))
        dates = [pd.to_datetime(dep_date)]

    # 왕복 이면 1 편도면 0
    round_trip = request.form.get('round_trip')
    #round_trip = 1 if check == 'on' else 0
    # 직항이면 1 아니면 0
    one_way = request.form.get('one_way')
    direct_flight = 1 if one_way == 'on' else 0


    # 희망 비행 시간
    hours = int(request.form.get('hours'))
    minutes = int(request.form.get('minutes'))
    total_minutes = hours * 60 + minutes


    # 호텔 성급
    hotel_star = request.form.get('hotel_class')

    # 항공편 결과를 저장할 딕셔너리 초기화
    result_air_prediction = {}
    # 호텔 예측 결과 저장 리스트
    result_hotel_prediction = []

    # 목적지별 공항과 항공사 이름
    departure_airport = request.form.get('departure_airport')
    arrival_airport = request.form.get('arrival_airport')
    region = ''
    if departure_airport == 'HND' or departure_airport == 'NRT' or arrival_airport == 'HND' or arrival_airport == 'NRT':
        region = '도쿄'
        city_Fukuoka = 0
        city_Osaka = 0
        city_Tokyo = 1
    elif departure_airport == 'FUK' or arrival_airport == 'FUK': 
        region = '후쿠오카'
        city_Fukuoka = 1
        city_Osaka = 0
        city_Tokyo = 0
    elif departure_airport == 'KIX' or arrival_airport == 'KIX': 
        region = '오사카'
        city_Fukuoka = 0
        city_Osaka = 1
        city_Tokyo = 0

    # 항공편 예측
    if round_trip == 'on': # 왕복인 경우
        # 결과를 저장할 딕셔너리 초기화
        result_air_prediction = {}
        # 각 경로의 항공사 이름들로 예측
        airline_names = route_data.get(f'{departure_airport}_to_{arrival_airport}')
        for airline_name in airline_names:
            for air_class in ['일반석', '프리미엄 일반석', '비즈니스석', '일등석']:
                air_data = {
                    'air_class': [air_class],
                    'airline_name': [airline_name],
                    'departure_airport': [departure_airport],
                    'arrival_airport': [arrival_airport],
                    'direct_flight': [direct_flight],
                    'duration': [total_minutes],
                    'region': [region],
                    'year': [dep_year],
                    'month': [dep_month],
                    'day': [dep_day]
                }
                df = pd.DataFrame(air_data)
                prediction = JP_air_model.predict(df)
                if airline_name not in result_air_prediction:
                    result_air_prediction[airline_name] = {}
                if air_class not in result_air_prediction[airline_name]:
                    result_air_prediction[airline_name][air_class] = prediction[0]
                else:
                    result_air_prediction[airline_name][air_class] += prediction[0]

        # 돌아올 때의 항공편
        airline_names = route_data.get(f'{arrival_airport}_to_{departure_airport}')
        for airline_name in airline_names:
            for air_class in ['일반석', '프리미엄 일반석', '비즈니스석', '일등석']:
                air_data = {
                    'air_class': [air_class],
                    'airline_name': [airline_name],
                    'departure_airport': [departure_airport],
                    'arrival_airport': [arrival_airport],
                    'direct_flight': [direct_flight],
                    'duration': [total_minutes],
                    'region': [region],
                    'year': [dep_year],
                    'month': [dep_month],
                    'day': [dep_day]
                }
                df = pd.DataFrame(air_data)
                prediction = JP_air_model.predict(df)
                if airline_name not in result_air_prediction:
                    result_air_prediction[airline_name] = {}
                if air_class not in result_air_prediction[airline_name]:
                    result_air_prediction[airline_name][air_class] = prediction[0]
                else:
                    result_air_prediction[airline_name][air_class] += prediction[0]
    else: # 편도인 경우
        # 결과를 저장할 딕셔너리 초기화
        result_air_prediction = {}
        # 각 경로의 항공사 이름들로 예측
        airline_names = route_data.get(f'{departure_airport}_to_{arrival_airport}')
        for airline_name in airline_names:
            for air_class in ['일반석', '프리미엄 일반석', '비즈니스석', '일등석']:
                air_data = {
                    'air_class': [air_class],
                    'airline_name': [airline_name],
                    'departure_airport': [departure_airport],
                    'arrival_airport': [arrival_airport],
                    'direct_flight': [direct_flight],
                    'duration': [total_minutes],
                    'region': [region],
                    'year': [dep_year],
                    'month': [dep_month],
                    'day': [dep_day]
                }
                df = pd.DataFrame(air_data)
                prediction = JP_air_model.predict(df)
                if airline_name not in result_air_prediction:
                    result_air_prediction[airline_name] = {}
                if air_class not in result_air_prediction[airline_name]:
                    result_air_prediction[airline_name][air_class] = prediction[0]
                else:
                    result_air_prediction[airline_name][air_class] += prediction[0]


    # 좌석 등급별로 상위 3개 항공사의 결과를 저장하는 딕셔너리 초기화
    top_airlines_by_class = {air_class: [] for air_class in ['일반석', '프리미엄 일반석', '비즈니스석', '일등석']}
    # 상위 3개 항공사 구하기
    for air_class in top_airlines_by_class.keys():
        # 데이터 필터링 - 음수 값 제외
        filtered_data = {airline_name: price for airline_name, price in result_air_prediction.items() if price.get(air_class, 0) >= 0}

        # 데이터 정렬 및 상위 3개 선택
        sorted_data = sorted(filtered_data.items(), key=lambda item: item[1].get(air_class, 0))[:3]

        # 상위 3개 항공사 저장
        top_airlines_by_class[air_class] = dict(sorted_data)

    trip_type = "왕복" if round_trip == 'on' else "편도"

    # ---------------------------------------------------------------
    # 호텔 예측
    for date in dates:
        hotel_dep_month, hotel_dep_day = date.month, date.day
        hotel_data = {
                'hotel_star': [hotel_star],
                'month': [hotel_dep_month],
                'day': [hotel_dep_day],
                'city_Fukuoka': [city_Fukuoka],
                'city_Osaka': [city_Osaka],
                'city_Tokyo': [city_Tokyo]
            }
        df2 = pd.DataFrame(hotel_data)
        hotel_prediction = JP_hotel_model.predict(df2)
        result_hotel_prediction.append(hotel_prediction[0])
    total_hotel_prediction = sum(result_hotel_prediction)

    star_rating_symbol = get_star_rating_symbol(int(hotel_star))
    # 숙박 기간 계산
    num_nights, num_days = calculate_stay_period(dep_date, re_date)

    # 예측 결과를 HTML로 전달
    return render_template('index.html', top_airlines_by_class=top_airlines_by_class, trip_type=trip_type, hotel_star=star_rating_symbol, hotel_prediction=total_hotel_prediction, num_nights=num_nights, num_days=num_days)


# 항공편 대시보드 보기
@app.route('/airport_dashboard', methods=['GET','POST'])
def airport_to_dashboard():
    return redirect("https://lookerstudio.google.com/reporting/feefb17d-5196-4754-883a-b716340cd9a5", code=302)

# 호텔 대시보드 보기
@app.route('/hotel_dashboard', methods=['GET','POST'])
def hotel_to_dashboard():
    return redirect("https://lookerstudio.google.com/reporting/b28f27d3-65eb-4e11-b791-ed570d2f7be94", code=302)


if __name__ == '__main__':
    app.run(debug=True)
