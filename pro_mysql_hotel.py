import numpy as np
import pandas as pd
import pymysql

df = pd.read_csv('Tokyo_hotel.csv')
#df.replace({np.nan: None}, inplace=True)
df['review_score'].replace(-1, None, inplace=True)

# MySQL 서버에 연결합니다
conn = pymysql.connect(
    host='127.0.0.1', 
    user='root', 
    password='ax1010ax1010', 
    db='Project1', 
    charset='utf8'
)

curs = conn.cursor()

curs.execute('''DROP TABLE IF EXISTS tokyo_hotel''')

curs.execute("""
    CREATE TABLE tokyo_hotel (
        ID SERIAL PRIMARY KEY,
        date DATE,
        hotel_name VARCHAR(64),
        price INT,
        hotel_star INT,
        review_score FLOAT,
        hotel_URL VARCHAR(255)
    );
""")

# 데이터프레임의 데이터를 테이블에 삽입
for row in df.itertuples(index=False):
    curs.execute("""
        INSERT INTO tokyo_hotel (date, hotel_name, price, hotel_star, review_score, hotel_URL)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (row.date, row.hotel_name, row.price, row.hotel_star, row.review_score, row.hotel_URL))


curs.close()
conn.commit() 
conn.close() 