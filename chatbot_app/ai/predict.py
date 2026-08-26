import os
import sys
import django
import joblib

# Project Root Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Django Settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Chatbot_project.settings")

# Initialize Django
django.setup()

from chatbot_app.ai.preprocess import preprocess_text

# Load Saved Files
model = joblib.load("chatbot_app/saved_models/naive_bayes_model.pkl")
vectorizer = joblib.load("chatbot_app/saved_models/tfidf_vectorizer.pkl")
label_encoder = joblib.load("chatbot_app/saved_models/label_encoder.pkl")


def predict_intent(question):

    # Clean user question
    question = preprocess_text(question)

    # Convert into TF-IDF
    vector = vectorizer.transform([question])

    # Predict Intent
    prediction = model.predict(vector)

    # Predict Probability (Confidence)
    probabilities = model.predict_proba(vector)
    confidence = max(probabilities[0])

    # Convert number back to intent
    intent = label_encoder.inverse_transform(prediction)[0]

    return intent, confidence


if __name__ == "__main__":

    question = input("Ask Question: ")

    intent, confidence = predict_intent(question)

    print("\nPredicted Intent:", intent)
    print("AI Confidence:", round(confidence * 100, 2), "%")