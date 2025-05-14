import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import time

# Custom CSS and JavaScript styling
def local_css():
    st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
    }
    
    /* Header styling */
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }

    .main-header h1 {
        color: #1E3D59;
        margin: 0;
        font-size: 2.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .main-header p {
        color: #666;
        margin: 0.5rem 0 0 0;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1.1rem;
        min-height: 150px;
        background: white;
        transition: all 0.3s ease;
        color: #1E3D59;
        width: 100%;
        margin-bottom: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #1E3D59;
        box-shadow: 0 0 0 3px rgba(30, 61, 89, 0.1);
    }
    
    .stTextArea textarea::placeholder {
        color: #888;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #1E3D59, #2E5E8A);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 61, 89, 0.2);
    }
    
    /* Results styling */
    .results-content {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .detected-language {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3D59;
        margin: 1rem 0;
    }
    
    .confidence-score {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
    }
    
    .confidence-label {
        color: #666;
        margin-bottom: 0.5rem;
    }
    
    .confidence-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E3D59;
    }

    .placeholder-text {
        color: #888;
        font-size: 1.1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 2rem;
    }

    .placeholder-text .emoji {
        font-size: 3rem;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Container spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load and prepare the model
@st.cache_resource
def load_model():
    # Load data
    data = pd.read_csv("https://raw.githubusercontent.com/amankharwal/Website-data/master/dataset.csv")
    
    # Create feature vectors
    X = data['Text']
    y = data['language']
    
    # Create and fit CountVectorizer
    cv = CountVectorizer()
    X_cv = cv.fit_transform(X)
    
    # Train model
    model = MultinomialNB()
    model.fit(X_cv, y)
    
    return cv, model

def detect_language(text, cv, model):
    """Detect the language of the given text."""
    text_cv = cv.transform([text])
    prediction = model.predict(text_cv)
    probabilities = model.predict_proba(text_cv)
    confidence = np.max(probabilities)
    return prediction[0], confidence

def main():
    local_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 Language Detective</h1>
        <p>Detect the language of any text instantly</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    cv, model = load_model()
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        text_input = st.text_area("", 
                                height=150, 
                                placeholder="Type or paste your text here...",
                                key="text_input")
        submit_button = st.button("🔍 Detect Language", key="submit")
    
    with col2:
        if submit_button and text_input:
            with st.spinner("🔍 Analyzing..."):
                time.sleep(0.3)
                detected_lang, confidence = detect_language(text_input, cv, model)
            
            st.markdown(f"""
            <div class="results-content">
                <div class="detected-language">
                    {detected_lang}
                </div>
                <div class="confidence-score">
                    <div class="confidence-label">Confidence Score</div>
                    <div class="confidence-value">{int(confidence * 100)}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence bar
            st.progress(confidence)
        else:
            st.markdown("""
            <div class="results-content">
                <div class="placeholder-text">
                    <span class="emoji">🔍</span>
                    <span>Enter text to detect its language</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 