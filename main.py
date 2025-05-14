import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import os
import joblib

# Create model directory
os.makedirs('model', exist_ok=True)

# Load and prepare the data
print("Loading dataset...")
data = pd.read_csv("https://raw.githubusercontent.com/amankharwal/Website-data/master/dataset.csv")
print(f"Dataset shape: {data.shape}")

# Create feature vectors
X = data['Text']
y = data['language']

# Create training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a CountVectorizer to convert text to numerical features
cv = CountVectorizer()
X_train_cv = cv.fit_transform(X_train)
X_test_cv = cv.transform(X_test)

# Train the model
print("\nTraining the model...")
model = MultinomialNB()
model.fit(X_train_cv, y_train)

# Save model and vectorizer
print("\nSaving model and vectorizer...")
joblib.dump(model, 'model/language_detector.joblib')
joblib.dump(cv, 'model/vectorizer.joblib')
print("Model and vectorizer saved successfully!")

# Evaluate the model
y_pred = model.predict(X_test_cv)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nModel is ready for deployment!")

def detect_language(text):
    """
    Detect the language of the given text.
    
    Args:
        text (str): Text to detect language for
        
    Returns:
        str: Detected language
    """
    # Transform the text using the same vectorizer
    text_cv = cv.transform([text])
    # Predict the language
    prediction = model.predict(text_cv)
    # Get probability scores for all languages
    probabilities = model.predict_proba(text_cv)
    confidence = np.max(probabilities)
    return prediction[0], confidence

# Example usage
print("\nTesting with some example texts:")
test_texts = [
    "Hello, how are you doing today?",
    "Bonjour, comment allez-vous aujourd'hui?",
    "Hola, ¿cómo estás hoy?",
    "Hallo, wie geht es dir heute?"
]

for text in test_texts:
    lang, conf = detect_language(text)
    print(f"\nText: {text}")
    print(f"Detected Language: {lang}")
    print(f"Confidence: {conf:.2%}")

# Interactive testing
print("\nEnter 'quit' to exit")
while True:
    text = input("\nEnter text to detect language: ")
    if text.lower() == 'quit':
        break
    lang, conf = detect_language(text)
    print(f"Detected Language: {lang}")
    print(f"Confidence: {conf:.2%}")