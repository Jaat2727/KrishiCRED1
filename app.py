import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# ==========================================
# 1. PAGE CONFIG & DEEP DARK CSS
# ==========================================
st.set_page_config(page_title="Krishi-Credit AI", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    /* Darker Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    /* Global Background */
    .stApp {
        background-color: #0b0f1a;
    }

    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
    }

    /* Gradient Header Text */
    .hero-text {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }

    /* Professional Button */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #2563eb !important;
        color: white !important;
        font-weight: 600;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    # Use a cleaner logo or avatar
    st.markdown("### 🏦 Krishi-Credit AI")
    st.caption("Bharat's Sovereign Scoring Engine")
    st.write("---")
    
    # Improved Navigation Menu
    selected = option_menu(
        menu_title=None,
        options=["Analytics", "Data Hub", "Settings"],
        icons=["bar-chart-fill", "database-fill-gear", "gear-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "#94a3b8", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "color": "#94a3b8",
                "--hover-color": "#1e293b"
            },
            "nav-link-selected": {"background-color": "#2563eb", "color": "white"},
        }
    )

    st.write("---")
    st.subheader("Manager Portal")
    applicant_id = st.text_input("Aadhaar / ID", value="ADHR-9921")
    
    # Custom Button Styling
    run_engine = st.button("🚀 Evaluate Farmer")

# ==========================================
# 3. MAIN DASHBOARD CONTENT
# ==========================================
if selected == "Analytics":
    st.markdown('<h1 class="hero-text">Underwriting Dashboard</h1>', unsafe_allow_html=True)
    st.write("AI-driven credit assessment for informal economies.")
    st.write("---")

    # Layout for Results
    if run_engine:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Trust Score", "742", "+12% vs Avg")
        with c2:
            st.metric("Telecom Streak", "24 Mo", "Stable")
        with c3:
            st.metric("FASTag Pings", "15", "High Activity")
            
        # Add your Gauge and Radar charts below this...
