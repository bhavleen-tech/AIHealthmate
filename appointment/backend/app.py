from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Use absolute path to avoid file not found issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "north_delhi_doctors.json")

@app.route('/api/doctors', methods=['POST'])
def get_doctors():
    try:
        data = request.get_json()
        location = data.get('location', '')
        specialty = data.get('specialty', '')

        # Load JSON data
        with open(DATA_PATH, "r", encoding='utf-8') as file:
            doctors = json.load(file)

        # Filter by location and specialty (case insensitive)
        filtered = [
            doc for doc in doctors
            if doc['location'].lower() == location.lower() and
               doc['specialty'].lower() == specialty.lower()
        ]

        return jsonify(filtered), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Doctor Booking API is running 🚀"

if __name__ == '__main__':
    app.run(host='127.0.0.5', port=9500, debug=True)
