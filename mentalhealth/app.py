from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load('model/mental_health_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form inputs
    mood = int(request.form['mood'])
    sleep = int(request.form['sleep_hours'])
    journal = request.form['journal']

    # Correct: Use DataFrame with column names matching training data
    input_data = pd.DataFrame([{
        'mood': mood,
        'sleep_hours': sleep,
        'journal': journal
    }])

    # Predict
    prediction = model.predict(input_data)[0]

    # Interpret result
    if prediction == 1:
        result = "⚠️ High risk of mental health issue (Anxiety/Depression/Burnout). Please consider talking to someone or seeking help."
    else:
        result = "✅ No immediate signs of mental health risk."

    return render_template('result.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)
