from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

app = FastAPI()

# Model loading
def load_or_train_model():
    model_path = 'model/language_detector.joblib'
    vectorizer_path = 'model/vectorizer.joblib'
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
    else:
        # Train new model
        data = pd.read_csv("https://raw.githubusercontent.com/amankharwal/Website-data/master/dataset.csv")
        X = data['Text']
        y = data['language']
        
        vectorizer = CountVectorizer()
        X_cv = vectorizer.fit_transform(X)
        
        model = MultinomialNB()
        model.fit(X_cv, y)
        
        # Save model and vectorizer
        os.makedirs('model', exist_ok=True)
        joblib.dump(model, model_path)
        joblib.dump(vectorizer, vectorizer_path)
    
    return model, vectorizer

model, vectorizer = load_or_train_model()

class TextRequest(BaseModel):
    text: str

@app.post("/api/detect")
async def detect_language(request: TextRequest):
    try:
        # Transform text
        text_cv = vectorizer.transform([request.text])
        
        # Predict
        prediction = model.predict(text_cv)
        probabilities = model.predict_proba(text_cv)
        confidence = float(np.max(probabilities))
        
        return {
            "language": prediction[0],
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 