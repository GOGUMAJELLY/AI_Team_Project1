import numpy as np
import pandas as pd
import pymysql


# MySQL 서버에 연결합니다
conn = pymysql.connect(
    host='127.0.0.1', 
    user='root', 
    password='ax1010ax1010', 
    db='Project1', 
    charset='utf8'
)

curs = conn.cursor()

# 테이블에서 데이터 가져올 때
curs.execute("SELECT * FROM osaka_air;")
df1 = curs.fetchall()

curs.execute("SELECT * FROM fukuoka_air;")
df2 = curs.fetchall()

curs.execute("SELECT * FROM tokyo_air;")
df3 = curs.fetchall()

curs.close()
conn.commit() 
conn.close() 

df_osaka_air = pd.DataFrame(df1, columns = ['ID', 'date', 'air_class', 'airline_name', 'departure_time', 'departure_airport',
                                   'arrival_time', 'arrival_airport', 'direct_flight', 'duration', 'price'])

# '0 days' 부분을 없애고 시간 형식으로 변환
df_osaka_air['departure_time'] = df_osaka_air['departure_time'].astype(str).str.split().str[-1]
df_osaka_air['arrival_time'] = df_osaka_air['arrival_time'].astype(str).str.split().str[-1]
df_osaka_air['duration'] = df_osaka_air['duration'].astype(str).str.split().str[-1]
df_osaka_air['region'] = '오사카'
df_osaka_air = df_osaka_air.drop('ID', axis=1)
print(df_osaka_air.iloc[0])
print('-----------------------')


df_fukuoka_air = pd.DataFrame(df2, columns = ['ID', 'date', 'air_class', 'airline_name', 'departure_time', 'departure_airport',
                                   'arrival_time', 'arrival_airport', 'direct_flight', 'duration', 'price'])

df_fukuoka_air['departure_time'] = df_fukuoka_air['departure_time'].astype(str).str.split().str[-1]
df_fukuoka_air['arrival_time'] = df_fukuoka_air['arrival_time'].astype(str).str.split().str[-1]
df_fukuoka_air['duration'] = df_fukuoka_air['duration'].astype(str).str.split().str[-1]
df_fukuoka_air['region'] = '후쿠오카'
df_fukuoka_air = df_fukuoka_air.drop('ID', axis=1)
print(df_fukuoka_air.iloc[0])
print('-----------------------')

df_tokyo_air = pd.DataFrame(df3, columns = ['ID', 'date', 'air_class', 'airline_name', 'departure_time', 'departure_airport',
                                   'arrival_time', 'arrival_airport', 'direct_flight', 'duration', 'price'])

df_tokyo_air['departure_time'] = df_tokyo_air['departure_time'].astype(str).str.split().str[-1]
df_tokyo_air['arrival_time'] = df_tokyo_air['arrival_time'].astype(str).str.split().str[-1]
df_tokyo_air['duration'] = df_tokyo_air['duration'].astype(str).str.split().str[-1]
df_tokyo_air['region'] = '도쿄'
df_tokyo_air = df_tokyo_air.drop('ID', axis=1)
print(df_tokyo_air.iloc[0])

df_air = pd.concat([df_osaka_air, df_fukuoka_air,df_tokyo_air], ignore_index=True)
df_air.to_csv('Total_air.csv')