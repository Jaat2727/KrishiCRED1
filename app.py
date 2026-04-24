import streamlit as st
import pandas as pd
import random
import time
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# ==========================================
# 1. PAGE CONFIGURATION & ENTERPRISE CSS
# ==========================================
st.set_page_config(page_title="Krishi-Credit AI", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sleek Metric Cards with Hover Effect */
    div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 10px;
        color: white;
        transition: transform 0.2s ease-in-out;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }
    
    /* Custom Headers */
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    
    /* GenAI Terminal Box */
    .ai-terminal {
        background-color: #0f172a;
        border-left: 4px solid #8b5cf6;
        padding: 20px;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        color: #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BACKEND INTEGRATION PIPELINES (MOCKS)
# ==========================================
def fetch_ml_score(user_id: str):
    time.sleep(1.2) # Network latency simulation
    seed = sum(ord(c) for c in user_id)
    random.seed(seed)
    
    score = random.randint(500, 850)
    features = {
        "telecom_streak": random.randint(12, 48), # out of 48 months
        "fastag_activity": random.randint(10, 50), # out of 50 pings
        "pm_kisan": random.randint(60, 100), # % confidence
        "upi_ratio": random.randint(10, 80), # % usage
        "crop_insurance": random.randint(50, 100) # % coverage history
    }
    return score, features

def get_genai_advisory(score):
    time.sleep(1.5)
    if score >= 650:
        return f"✅ **APPROVED:** Model confidence high. Applicant demonstrates strong digital footprint resilience despite low formal banking liquidity. Alternative proxies (Telecom/FASTag) align with RBI Master Direction for Microfinance."
    return f"⚠️ **MANUAL REVIEW:** Alternative footprint insufficient for automated clearing. Trigger physical field verification per risk matrix."

# ==========================================
# 3. SIDEBAR NAVIGATION (APP STYLE)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=60)
    
    # Sleek navigation menu
    selected_tab = option_menu(
        menu_title="Main Menu",
        options=["Underwriting Engine", "Medallion Lineage", "API Docs"],
        icons=["shield-check", "database", "code-slash"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link-selected": {"background-color": "#3b82f6"},
        }
    )
    
    st.divider()
    st.subheader("Manager Portal")
    farmer_id = st.text_input("Applicant ID (Aadhaar/Phone)", "ADHR-9982")
    run_engine = st.button("🚀 Execute AI Pipeline", use_container_width=True, type="primary")

# ==========================================
# 4. MAIN DASHBOARD: UNDERWRITING ENGINE
# ==========================================
if selected_tab == "Underwriting Engine":
    st.markdown('<p class="gradient-text">Krishi-Credit Sovereign AI</p>', unsafe_allow_html=True)
    st.caption("Databricks MLflow & Foundation Model Inference Dashboard")
    st.divider()

    if run_engine:
        with st.spinner("Connecting to Databricks Unity Catalog..."):
            score, features = fetch_ml_score(farmer_id)
            advisory = get_genai_advisory(score)
            
        risk_color = "green" if score >= 650 else "red"
        tier = "Prime" if score >= 700 else "Near-Prime" if score >= 600 else "Sub-Prime"

        # --- ROW 1: METRICS ---
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Trust Score", f"{score}/900", delta=f"Tier: {tier}", delta_color="normal" if score>600 else "inverse")
        c2.metric("Telecom Resilience", f"{features['telecom_streak']} mo", delta="High Confidence")
        c3.metric("Mandi Transport (FASTag)", f"{features['fastag_activity']} pings", delta="Verified")
        c4.metric("Est. Pre-Approval", f"₹{score * 150}", delta="Based on RBI limits")

        st.write("") # Spacer

        # --- ROW 2: CHARTS & AI ADVISORY ---
        col_chart, col_ai = st.columns([1.2, 1])
        
        with col_chart:
            st.subheader("🕸️ Alternative Data Footprint")
            st.caption("Applicant vs. Prime Farmer Benchmark")
            
            # THE RADAR CHART (Judges love this)
            categories = ['Telecom History', 'FASTag/Logistics', 'PM-Kisan Gov', 'UPI Density', 'Crop Insurance']
            
            fig = go.Figure()
            # Applicant Profile
            fig.add_trace(go.Scatterpolar(
                r=[features['telecom_streak']*2, features['fastag_activity']*2, features['pm_kisan'], features['upi_ratio'], features['crop_insurance']],
                theta=categories,
                fill='toself',
                name='Applicant Profiling',
                line_color='#3b82f6'
            ))
            # Prime Benchmark
            fig.add_trace(go.Scatterpolar(
                r=[80, 70, 90, 60, 85],
                theta=categories,
                fill='toself',
                name='Prime Benchmark',
                line_color='#10b981'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                height=350,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_ai:
            st.subheader("🤖 GenAI Rationale")
            st.caption("Powered by Databricks AI Gateway (Llama-3)")
            
            # Terminal-style output box
            st.markdown(f'<div class="ai-terminal">{advisory}</div>', unsafe_allow_html=True)
            
            st.write("")
            with st.expander("View FAISS Vector References"):
                st.write("📄 `rbi_microfinance_master_direction_2022.pdf` (Page 14)")
                st.write("📄 `nabard_agri_loan_framework.pdf` (Page 3)")

    else:
        st.info("👈 Enter an Applicant ID and execute the pipeline to view the Sovereign Credit Report.")

# ==========================================
# 5. OTHER TABS (For Hackathon Flexing)
# ==========================================
elif selected_tab == "Medallion Lineage":
    st.title("🗄️ Databricks Architecture")
    st.image("https://docs.databricks.com/en/_images/medallion-architecture.png", caption="Our Unity Catalog Data Flow")
    st.markdown("""
    * **Bronze:** Raw JSON streams from Telecom providers and FASTag APIs.
    * **Silver:** Delta Live Tables (DLT) performing Aadhaar-hashing and deduping.
    * **Gold:** Feature Store tables driving the MLflow underwriting model.
    """)

elif selected_tab == "API Docs":
    st.title("🔌 Integration Endpoints")
    st.code("""
    POST /api/v1/predict_trust_score
    {
        "applicant_id": "ADHR-9982",
        "consent_token": "bearer_abc123"
    }
    """, language="json")
