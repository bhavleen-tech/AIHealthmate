from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load doctor data
with open("north_delhi_doctors.json", "r", encoding="utf-8") as f:
    doctor_data = json.load(f)

@app.route("/api/doctors", methods=["POST"])
def find_doctors():
    data = request.get_json()
    location = data.get("location", "").lower()
    specialty = data.get("specialty", "").lower()

    filtered = [
        doc for doc in doctor_data
        if location in doc["location"].lower() and specialty in doc["specialty"].lower()
    ]

    return jsonify(filtered)

if __name__ == '__main__':
    app.run(host='127.0.0.2', port=7000, debug=True)