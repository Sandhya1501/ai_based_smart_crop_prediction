from flask import Flask, render_template, jsonify, request
import random
from datetime import datetime, timedelta

app = Flask(__name__)

fan_state = {
    "fan1": 0,
    "fan2": 0,
    "fan3": 0
}

# Live room data
def get_sensor_data():
    return {
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "fans": fan_state
    }

# Last 5 days + today (outside room)
def get_past_5_days():
    data = []
    for i in range(5, -1, -1):
        day = (datetime.now() - timedelta(days=i)).strftime("%d-%b")
        data.append({
            "day": day,
            "temperature": round(random.uniform(25, 40), 2),
            "humidity": round(random.uniform(20, 60), 2)
        })
    return data

# Same 5 days last year
def get_last_year_data():
    data = []
    for i in range(5, -1, -1):
        day = (datetime.now() - timedelta(days=i)).strftime("%d-%b")
        data.append({
            "day": day,
            "temperature": round(random.uniform(20, 38), 2),
            "humidity": round(random.uniform(25, 65), 2)
        })
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(get_sensor_data())

@app.route('/past-data')
def past_data():
    return jsonify(get_past_5_days())

@app.route('/last-year')
def last_year():
    return jsonify(get_last_year_data())

@app.route('/set_fan', methods=['POST'])
def set_fan():
    data = request.json
    fan = data.get("fan")
    speed = data.get("speed")

    if fan in fan_state:
        fan_state[fan] = speed

    return jsonify({"status": "success", "fans": fan_state})

if __name__ == '__main__':
    app.run(debug=True)