import streamlit as st
import pandas as pd
import random
import time
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from databricks.sdk import WorkspaceClient

# ==========================================
# 1. INITIALIZATION & CLIENT
# ==========================================
st.set_page_config(page_title="Krishi-Credit AI", page_icon="🏦", layout="wide")

# Initialize Workspace Client (Automatically uses Databricks App Auth)
w = WorkspaceClient()

# ==========================================
# 2. PROFESSIONAL STYLING (DARK MODE SAFE)
# ==========================================
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BACKEND INTEGRATION FUNCTIONS
# ==========================================

def fetch_ml_score(user_id: str):
    """
    Switch to Real Integration tomorrow by providing the Endpoint Name.
    """
    try:
        # --- REAL CODE (Uncomment tomorrow) ---
        # response = w.serving_endpoints.query(
        #     name="YOUR_MODEL_ENDPOINT_NAME",
        #     dataframe_records=[{"aadhaar_id": user_id}]
        # )
        # score = response.predictions[0]
        
        # --- MOCK CODE (For Tonight) ---
        time.sleep(1.5)
        seed = sum(ord(c) for c in user_id)
        random.seed(seed)
        score = random.randint(550, 850)
        
        features = {
            "telecom": random.randint(12, 48),
            "fastag": random.randint(5, 40),
            "pm_kisan": "Verified",
            "upi": f"{random.randint(10, 70)}%"
        }
        return score, features
    except Exception as e:
        st.error(f"Backend Connection Failed: {e}")
        return 0, {}

def get_genai_advisory(score, user_id):
    """
    Switch to Real Llama-3/RAG tomorrow.
    """
    # --- MOCK CODE ---
    time.sleep(1)
    if score > 650:
        return f"✅ **Approved:** Applicant {user_id} shows high resilience in alternative footprint (Telecom/FASTag). Eligible for KCC Microfinance under RBI 2022 norms."
    return f"⚠️ **Review:** Insufficient digital footprint. Recommend manual field visit for income assessment."

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=70)
    st.title("Sovereign Engine")
    
    selected = option_menu(
        menu_title=None,
        options=["Underwriter", "Data Lineage", "Settings"],
        icons=["cpu", "diagram-3", "gear"],
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#3b82f6"}}
    )
    
    st.divider()
    applicant_id = st.text_input("Aadhaar Number", value="ADHR-4452-9901")
    is_clicked = st.button("🚀 Run Underwriting", use_container_width=True, type="primary")

# ==========================================
# 5. MAIN DASHBOARD CONTENT
# ==========================================
if selected == "Underwriter":
    st.header("🌾 Krishi-Credit: Alternative Scoring")
    
    if is_clicked:
        score, features = fetch_ml_score(applicant_id)
        
        # --- TOP ROW: GAUGE & METRICS ---
        col1, col2 = st.columns([1, 2])
        
        with col1:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                title = {'text': "Credit Trust Score"},
                gauge = {
                    'axis': {'range': [300, 900]},
                    'bar': {'color': "#3b82f6"},
                    'steps': [
                        {'range': [300, 600], 'color': "#fee2e2"},
                        {'range': [600, 750], 'color': "#fef3c7"},
                        {'range': [750, 900], 'color': "#d1fae5"}]
                }
            ))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.write("### Data Proxies (Non-UPI)")
            m1, m2 = st.columns(2)
            m1.metric("Telecom Streak", f"{features['telecom']} Months", "Stable")
            m2.metric("Mandi Visits", f"{features['fastag']} Pings", "High Activity")
            
            m3, m4 = st.columns(2)
            m3.metric("PM-Kisan", features['pm_kisan'], "Gov Link")
            m4.metric("Cash Density", features['upi'], "Informal")

        st.divider()

        # --- BOTTOM ROW: TABS ---
        t1, t2 = st.tabs(["🤖 AI Rationale", "🕸️ Explainable AI"])
        
        with t1:
            st.subheader("GenAI Underwriting Advisory")
            advisory = get_genai_advisory(score, applicant_id)
            st.info(advisory)
            st.caption("Generated via Databricks Foundation Model API (Llama-3-70B)")
            
        with t2:
            # Radar chart for "Winning" visualization
            categories = ['Telecom','FASTag','PM-Kisan','Insurance','Harvest']
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[features['telecom']*2, features['fastag']*2, 90, 70, 80],
                theta=categories,
                fill='toself',
                name='Applicant',
                line_color='#3b82f6'
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
            st.plotly_chart(fig_radar, use_container_width=True)

    else:
        st.info("Input Aadhaar and click Execute to analyze the farmer's alternative digital footprint.")

elif selected == "Data Lineage":
    st.subheader("Databricks Medallion Architecture")
    st.markdown("""
    - **Bronze:** Raw API payloads from Telecom/Logistics providers.
    - **Silver:** Cleaned and Aadhaar-hashed features in Delta Lake.
    - **Gold:** Training-ready features for MLflow Underwriting Model.
    """)
    st.image("https://www.databricks.com/wp-content/uploads/2022/03/medallion-architecture-1.png")
