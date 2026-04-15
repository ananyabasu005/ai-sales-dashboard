from flask import Flask, render_template, request, redirect, session, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression
from algorithms.dijkstra import dijkstra

app = Flask(__name__)
app.secret_key = "secret123"   # needed for login

# Dummy user (you can change)
USER = {"username": "admin", "password": "1234"}

@app.route('/')
def home():
    if "user" in session:
        return render_template("index.html")
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            return redirect('/')
        else:
            return "Invalid credentials ❌"

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect('/login')

@app.route('/run', methods=['POST'])
def run():
    data = request.json["sales"]

    days = np.array(range(1, len(data)+1)).reshape(-1,1)
    sales = np.array(data)

    model = LinearRegression()
    model.fit(days, sales)

    next_day = len(data) + 1
    prediction = float(model.predict([[next_day]])[0])

    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    }

    dijkstra_result = dijkstra(graph, 'A')

    return jsonify({
        "prediction": prediction,
        "sales": data,
        "next_day": next_day,
        "dijkstra": dijkstra_result
    })

if __name__ == '__main__':
    app.run(debug=True)