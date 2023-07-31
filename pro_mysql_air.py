import numpy as np
import pandas as pd
import pymysql

df = pd.read_csv('Tokyo_air.csv')

# MySQL 서버에 연결합니다
conn = pymysql.connect(
    host='127.0.0.1', 
    user='root', 
    password='ax1010ax1010', 
    db='Project1', 
    charset='utf8'
)

curs = conn.cursor()
curs.execute('''DROP TABLE  if exists tokyo_air;''')


curs.execute("""
    CREATE TABLE tokyo_air (
        ID SERIAL PRIMARY KEY,
        date DATE,
        air_class VARCHAR(64),
        airline_name VARCHAR(64),
        departure_time TIME,
        departure_airport VARCHAR(64),
        arrival_time TIME,
        arrival_airport VARCHAR(64),
        direct_flight TINYINT(1),
        duration TIME,
        price INT
    );
""")

# 데이터프레임의 데이터를 테이블에 삽입
for row in df.itertuples(index=False):
    curs.execute("""
        INSERT INTO tokyo_air (date, air_class, airline_name, departure_time, departure_airport,
                                   arrival_time, arrival_airport, direct_flight, duration, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (row.date, row.air_class, row.airline_name, row.departure_time, row.departure_airport,
              row.arrival_time, row.arrival_airport, row.direct_flight, row.duration, row.price))


conn.commit() 
curs.close()
conn.close() 
