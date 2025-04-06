import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# Sample dataset
data = {
    'mood': [3, 5, 2, 8, 7, 4, 1, 6, 2, 7, 1, 8],
    'sleep_hours': [4, 6, 3, 8, 7, 5, 2, 6, 3, 7, 2, 8],
    'journal': [
        "I feel tired and unmotivated.",
        "My day was okay, a little stressful.",
        "I can't focus and feel worthless.",
        "Feeling good and productive!",
        "I enjoyed my work and time with family.",
        "Things are okay but I'm a little down.",
        "I feel hopeless and constantly anxious.",
        "Today was fine, not too bad.",
        "I feel numb and disconnected.",
        "Grateful for a productive day at work.",
        "I’m panicking a lot and can’t breathe.",
        "Life feels balanced today."
    ],
    'label': [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0]  # 1 = Risk, 0 = Normal
}

df = pd.DataFrame(data)

# Features and labels
X = df[['mood', 'sleep_hours', 'journal']]
y = df['label']

# Combine text features with numerical using ColumnTransformer
pipeline = Pipeline([
    ('features', ColumnTransformer([
        ('text', TfidfVectorizer(), 'journal')
    ], remainder='passthrough')),  # passthrough mood and sleep_hours
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Evaluate
preds = pipeline.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, preds))

# Save the model
os.makedirs('model', exist_ok=True)
joblib.dump(pipeline, 'model/mental_health_model.pkl')
