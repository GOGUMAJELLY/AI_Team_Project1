import pandas as pd
import MySQLdb  
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, make_scorer,  r2_score
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle

hotel_data = pd.read_csv("hotel.csv")

hotel_data['date'] = pd.to_datetime(hotel_data['date'])
hotel_data['month'] = hotel_data['date'].dt.month
hotel_data['day'] = hotel_data['date'].dt.day
city_onehot = pd.get_dummies(hotel_data['city'], prefix='city').astype(int)
hotel_data = pd.concat([hotel_data, city_onehot], axis=1)

df = hotel_data.drop(columns=['Unnamed: 0', 'hotel_name','hotel_URL','date','review_score','city'])

X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# 그냥 랜덤포레스트 
rf = RandomForestRegressor(n_estimators=100, random_state=2)
rf.fit(X_train, y_train)

print(X_test.iloc[3,:])
y_pred = rf.predict(X_test)
print("예측", y_pred[3])

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MSE :", mse)
print("R2 :", r2)

with open('Hotel_rf_model.pkl', 'wb') as f:
    pickle.dump(rf, f)

with open('Hotel_rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)


## 그냥 해당 날짜의 호텔 등급에 따른 평균 가격
# average_price = df.loc[(df['month'] == 8) & (df['day'] == 1) & (df['hotel_star'] == 1), 'price'].mean()
# print("a" ,average_price )


# #그리드서치를 이용한 랜덤포레스트
# rf_model = RandomForestRegressor(random_state=2)

# param_grid = {
#     'n_estimators': [50, 100, 150],
#     'max_depth': [10, 20, 30],
#     'min_samples_split': [2, 5, 10], 
# }

# grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1)

# grid_search.fit(X_train, y_train)

# y_pred = grid_search.best_estimator_.predict(X_test)

# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)

# print("MSE :", mse)
# print("R2 :", r2)


# #k-fold사용
# kf = KFold(n_splits=5, shuffle=True, random_state=2)
# mse_scores = []
# r2_scores = []

# for i, j in kf.split(X):
#     X_train, X_test = X.iloc[i], X.iloc[j]
#     y_train, y_test = y.iloc[i], y.iloc[j]

#     rf_model = RandomForestRegressor(n_estimators=100, random_state=2)
#     rf_model.fit(X_train, y_train)

#     y_pred = rf_model.predict(X_test)

#     mse = mean_squared_error(y_test, y_pred)
#     r2 = r2_score(y_test, y_pred)

#     mse_scores.append(mse)
#     r2_scores.append(r2)

# print("MSE:", sum(mse_scores) / len(mse_scores))
# print("R2):", sum(r2_scores) / len(r2_scores))


# # 선형회귀
# X = df.drop('price', axis = 1)
# y = df.price

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# l_regression = LinearRegression()

# k_folds = 5
# mse_scorer = make_scorer(mean_squared_error)
# mse_scores = cross_val_score(l_regression , X_train, y_train, cv=k_folds, scoring=mse_scorer)

# print("Mean MSE:", np.mean(mse_scores))
# print("Standard Deviation of MSE:", np.std(mse_scores))

# l_regression .fit(X_train, y_train)
# print(X_test.iloc[3,:])
# y_pred = l_regression.predict(X_test)

# print("예측", y_pred[3])
# mse_test = mean_squared_error(y_test, y_pred)
# print("Test MSE:", mse_test)

# r2 = r2_score(y_test, y_pred)
# print("Test r2 :", r2 )

