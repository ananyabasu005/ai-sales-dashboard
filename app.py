from flask import Flask, render_template, request, redirect, session, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression
from algorithms.dijkstra import dijkstra
from algorithms.alphabeta import alphabeta
import random

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

    # Calculate simple standard deviation for confidence intervals
    std_dev = float(np.std(sales)) if len(sales) > 1 else 10.0
    upper_bound = round(prediction + std_dev, 2)
    lower_bound = max(0, round(prediction - std_dev, 2))
    prediction = round(prediction, 2)

    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    }

    dijkstra_result = dijkstra(graph, 'A')

    return jsonify({
        "prediction": prediction,
        "upper_bound": upper_bound,
        "lower_bound": lower_bound,
        "sales": data,
        "next_day": next_day,
        "dijkstra": dijkstra_result
    })

@app.route('/chat', methods=['POST'])
def chat():
    if "user" not in session:
        return jsonify({"response": "Please log in first."}), 401
    
    message = request.json.get("message", "").lower()
    sales_data = request.json.get("sales", [])
    
    # Simulated AI logic
    if not sales_data:
        response = "Please enter some sales data first so I can analyze it!"
    elif "increase" in message or "up" in message or "trend" in message:
        trend = "upward" if sales_data[-1] >= sales_data[0] else "downward"
        response = f"Based on the data, the overall trend is {trend}."
    elif "why" in message or "reason" in message or "drop" in message:
        response = "While I only see raw numbers, external factors like marketing campaigns, seasonality, or economic conditions often drive these fluctuations."
    elif "predict" in message or "future" in message:
        response = "Our linear regression model predicts the next value based on historical trajectory. The bounds show an optimistic and pessimistic scenario."
    else:
        avg = sum(sales_data) / len(sales_data) if sales_data else 0
        response = f"I'm your Sales AI assistant! The historical average is {avg:.2f}. Ask me about trends or predictions."
        
    return jsonify({"response": response})

@app.route('/simulate_chaos', methods=['POST'])
def simulate_chaos():
    sales = request.json.get("sales", [])
    if not sales:
        return jsonify({"error": "No sales data"}), 400
    
    last_val = sales[-1]
    
    # Generate 3 multiverse scenarios for the next 5 days
    best_case = [last_val * (1 + 0.1 * i) * random.uniform(0.9, 1.2) for i in range(1, 6)]
    worst_case = [max(0, last_val * (1 - 0.1 * i) * random.uniform(0.8, 1.1)) for i in range(1, 6)]
    weird_case = [last_val * random.uniform(0.6, 1.4) for i in range(1, 6)]
    
    return jsonify({
        "multiverse": [
            {"label": "Viral Timeline (Best)", "data": [round(x, 2) for x in best_case], "borderColor": "#4ade80"},
            {"label": "Collapse Timeline (Worst)", "data": [round(x, 2) for x in worst_case], "borderColor": "#f87171"},
            {"label": "Volatile Timeline", "data": [round(x, 2) for x in weird_case], "borderColor": "#c084fc"}
        ]
    })

@app.route('/wargame', methods=['POST'])
def wargame():
    strategy = request.json.get("strategy")
    sales = request.json.get("sales", [])
    if not sales:
        return jsonify({"error": "No sales data"}), 400
        
    last_val = sales[-1]
    
    # Different strategies yield different leaf nodes for the Alpha-Beta tree
    # These represent percentage shift in sales (-20 to +30)
    if strategy == "Price Cut":
        leaves = [15, 5, 20, 10, -5, -10, 5, 0] 
    elif strategy == "Marketing Blitz":
        leaves = [25, 15, 5, -10, 10, 0, -5, -20]
    else: # Product Update
        leaves = [30, 20, 10, 5, 0, -5, -10, -15]
        
    # Run alphabeta (We are maximizing player)
    outcome_shift = alphabeta(0, 0, True, leaves, -1000, 1000)
    
    new_prediction = round(last_val * (1 + (outcome_shift / 100.0)), 2)
    
    reactions = {
        "Price Cut": "Competitor matched your price. Resulting market share shift: ",
        "Marketing Blitz": "Competitor released a new product feature to distract. Shift: ",
        "Product Update": "Competitor aggressively dropped prices. Shift: "
    }
    
    return jsonify({
        "outcome_shift": outcome_shift,
        "new_prediction": new_prediction,
        "competitor_reaction": f"{reactions.get(strategy, 'Competitor acted.')} {outcome_shift}%"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)