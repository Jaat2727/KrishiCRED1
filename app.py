import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Krishi-Credit AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional rural banking theme (Clean white/gray with Green/Blue accents)
st.markdown("""
    <style>
    /* Main background adjustments */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Typography and Header Styling */
    h1, h2, h3 {
        color: #0f172a;
    }
    
    /* Custom Score CSS classes */
    .score-high { color: #10b981; font-weight: 800; font-size: 3.5rem; line-height: 1.1; }
    .score-med { color: #f59e0b; font-weight: 800; font-size: 3.5rem; line-height: 1.1; }
    .score-low { color: #ef4444; font-weight: 800; font-size: 3.5rem; line-height: 1.1; }
    
    /* Custom Metric Container */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6; /* Blue accent */
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. BACKEND PLACEHOLDER FUNCTIONS
#    (To be wired up by the Backend Team)
# ==========================================

def fetch_ml_score(user_id: str) -> tuple[int, dict]:
    """
    [DATABRICKS MLFLOW INTEGRATION POINT]
    Expects to ping a registered model in Databricks (e.g., models:/krishi_score/Production).
    
    Args:
        user_id: The ID of the farmer applicant.
    Returns:
        score: Integer between 300 and 900.
        features: Dictionary of alternative data footprint signals used by the model.
    """
    # Simulating API latency
    time.sleep(1.2)
    
    # Generate dummy score
    score = random.randint(300, 900)
    
    # Generate mock features (Alternative Data)
    # Generate mock features (Alternative Data)
    features = {
        "Telecom Streak": f"{random.randint(6, 36)} months active",
        "FASTag Activity": "High (Mandi Route)",
        "PM-Kisan Status": "Verified",
        "Crop Insurance": "Active (PMFBY)"
    }
