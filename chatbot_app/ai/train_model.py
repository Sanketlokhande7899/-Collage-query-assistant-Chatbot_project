import os
import sys
import django
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

# Project Root Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Django Settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Chatbot_project.settings")

# Initialize Django
django.setup()

# Import after django.setup()
from chatbot_app.models import FAQ
from chatbot_app.ai.preprocess import preprocess_text


# Get all FAQ records
faqs = FAQ.objects.all()

questions = []
intents = []

for faq in faqs:
    questions.append(preprocess_text(faq.question))
    intents.append(faq.intent)

print("Questions:")
print(questions)

print("\nIntents:")
print(intents)

# Encode intents
label_encoder = LabelEncoder()

encoded_intents = label_encoder.fit_transform(intents)

print("\nEncoded Intents:")
print(encoded_intents)

# Convert questions into TF-IDF vectors
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(questions)

print("\nTF-IDF Shape:")
print(X.shape)

# Train Naive Bayes Model
model = MultinomialNB()

model.fit(X, encoded_intents)

print("\nModel Trained Successfully!")

# Create folder if it doesn't exist
os.makedirs("chatbot_app/saved_models", exist_ok=True)

# Save Naive Bayes Model
joblib.dump(
    model,
    "chatbot_app/saved_models/naive_bayes_model.pkl"
)

# Save TF-IDF Vectorizer
joblib.dump(
    vectorizer,
    "chatbot_app/saved_models/tfidf_vectorizer.pkl"
)

# Save Label Encoder
joblib.dump(
    label_encoder,
    "chatbot_app/saved_models/label_encoder.pkl"
)

print("\nAll Models Saved Successfully!")