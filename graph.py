from flask import Flask, render_template_string, request
import csv
import os

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Weekly Health Tracker</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background: #f2f2f2; padding: 30px; }
        .container { max-width: 700px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type=number], input[type=text] { width: 80%; padding: 8px; margin: 5px 0; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 20px; margin-top: 10px; border: none; background: #007bff; color: white; border-radius: 5px; }
        canvas { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📊 Weekly Tracker for <span style="color: #007bff">{{ disease }}</span></h2>
        
        <form method="POST">
            <label>Disease Name:</label><br>
            <input type="text" name="disease" placeholder="Enter disease (e.g. Diabetes)" value="{{ disease }}"><br><br>
            
            {% for i in range(7) %}
                <label>{{ days[i] }} Value:</label>
                <input type="number" name="day{{ i+1 }}" value="{{ levels[i] }}"><br>
            {% endfor %}
            <button type="submit">Update Graph</button>
        </form>

        <canvas id="healthChart"></canvas>
    </div>

    <script>
        const ctx = document.getElementById('healthChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ days | tojson }},
                datasets: [{
                    label: '{{ disease }} Weekly Data',
                    data: {{ levels | tojson }},
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true,
                    pointRadius: 5,
                    pointBackgroundColor: 'rgba(0, 123, 255, 1)'
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: 200
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    levels = [0] * 7
    disease = "Your Condition"

    if request.method == "POST":
        disease = request.form.get("disease", "Unknown Condition")
        levels = [int(request.form.get(f"day{i+1}", 0)) for i in range(7)]

        save_to_csv(disease, levels)

    return render_template_string(template, days=days, levels=levels, disease=disease)

def save_to_csv(disease, levels):
    file_exists = os.path.isfile("health_data.csv")
    with open("health_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Disease", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        writer.writerow([disease] + levels)

if __name__ == '__main__':
    app.run(host='127.0.0.5', port=5000, debug=True)
