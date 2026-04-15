import numpy as np
from sklearn.linear_model import LinearRegression

def predict_sales():
    days = np.array([1,2,3,4,5,6,7,8,9,10]).reshape(-1,1)
    sales = np.array([200,220,250,270,300,320,350,370,400,420])

    model = LinearRegression()
    model.fit(days, sales)

    future_day = np.array([[11]])
    prediction = model.predict(future_day)

    print("Predicted Sales for Day 11:", prediction[0])