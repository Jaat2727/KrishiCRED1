import streamlit as st
import pandas as pd
import random
import time
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIGURATION & SAFE STYLING
# ==========================================
st.set_page_config(
    page_title="Krishi-Credit AI Engine",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit default branding for a cleaner app look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOCK BACKEND FUNCTIONS (DETERMINISTIC)
# ==========================================

def fetch_ml_score(user_id: str):
    """Simulates hitting the Databricks MLflow endpoint."""
    time.sleep(1.5) # Fake network latency
    
    # Use the length of the ID to generate a pseudo-random but consistent score for demos
    seed = sum(ord(c) for c in user_id)
    random.seed(seed)
    
    score = random.randint(450, 850)
    features = {
        "telecom_streak_mos": random.randint(6, 48),
        "fastag_trips_6m": random.randint(2, 30),
        "pm_kisan_verified": random.choice(["Yes", "Yes", "No"]), # Weighted towards Yes
        "upi_p2m_ratio": round(random.uniform(0.1, 0.8), 2)
    }
    return score, features

def generate_rbi_advisory(score: int) -> str:
    """Simulates Llama-3 response via Databricks Foundation Model APIs."""
    time.sleep(2.0)
    
    if score >= 650:
        return f"""
        **Sovereign GenAI Advisory (BhashaBench Evaluated)**
        
        **निर्णय: ऋण पूर्व-स्वीकृत (Pre-Approved)** आवेदक का कृषक विश्वास स्कोर **{score}/900** है। 
        
        **विवेचना (Rationale):** यद्यपि आवेदक का पारंपरिक बैंकिंग इतिहास सीमित है, उनका दूरसंचार (Telecom) भुगतान अनुशासन और निरंतर मंडी परिवहन (FASTag) एक स्थिर नकदी प्रवाह (Cash Flow) को प्रमाणित करते हैं। PM-Kisan योजना में इनका सत्यापन भूमि स्वामित्व की पुष्टि करता है।
        
        **अनुपालन (Compliance):** यह त्वरित स्वीकृति भारतीय रिज़र्व बैंक (RBI) के 'सूक्ष्म वित्त ऋण' (Master Direction - Microfinance Loans, 2022) के परिपत्र के अनुरूप है। 
        """
    else:
        return f"""
        **Sovereign GenAI Advisory (BhashaBench Evaluated)**
        
        **निर्णय: क्षेत्रीय सत्यापन आवश्यक (Field Verification Required)** आवेदक का कृषक विश्वास स्कोर **{score}/900** है।
        
        **विवेचना (Rationale):** वैकल्पिक डेटा प्रोफ़ाइल अपर्याप्त है। RBI के जोखिम प्रबंधन (Risk Management) दिशा-निर्देशों के अनुसार, ऋण स्वीकृति से पूर्व फील्ड एजेंट द्वारा प्रत्यक्ष आय मूल्यांकन (Physical Income Assessment) अनिवार्य है।
        """

# ==========================================
# 3. SIDEBAR: THE PORTAL
# ==========================================
with st.sidebar:
    st.title("🏦 Krishi-Credit AI")
    st.caption("v1.0 | Powered by Databricks Apps")
    st.divider()
    
    st.subheader("Branch Manager Input")
    farmer_id = st.text_input("Enter Applicant ID / Aadhaar", placeholder="e.g., ADHR-1094")
    
    evaluate_btn = st.button("Run ML Underwriting", type="primary", use_container_width=True)
    
    st.divider()
    st.markdown("### ⚙️ Pipeline Status")
    st.markdown("🟢 Unity Catalog: **Connected**")
    st.markdown("🟢 MLflow Model: **Active**")
    st.markdown("🟢 AI Gateway: **Active**")

# ==========================================
# 4. MAIN DASHBOARD UI
# ==========================================
st.title("🌾 Sovereign Underwriting Dashboard")
st.markdown("Automated risk assessment for the rural cash economy using alternative digital footprints.")
st.divider()

if evaluate_btn and farmer_id:
    with st.spinner("Fetching data from Unity Catalog & running MLflow inference..."):
        score, features = fetch_ml_score(farmer_id)
        
        risk_tier = "Prime" if score >= 700 else "Near Prime" if score >= 600 else "Subprime"
        color = "green" if score >= 650 else "red"

    # --- TOP ROW: GAUGE CHART & METRICS ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Professional Plotly Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Trust Score", 'font': {'size': 24}},
            delta = {'reference': 600, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [300, 900], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#3b82f6"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [300, 600], 'color': '#fee2e2'},
                    {'range': [600, 700], 'color': '#fef3c7'},
                    {'range': [700, 900], 'color': '#d1fae5'}],
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        st.subheader("Key Alternative Footprints")
        st.markdown(f"**Applicant Profile:** `{farmer_id}` | **Assigned Tier:** `{risk_tier}`")
        st.write("") # Spacing
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="Telecom Streak", value=f"{features['telecom_streak_mos']} mo", delta="Verified", delta_color="normal")
        m2.metric(label="FASTag Pings", value=f"{features['fastag_trips_6m']}", help="Mandi trips in last 6 months")
        m3.metric(label="PM-Kisan", value=features['pm_kisan_verified'], delta="Gov. Linked" if features['pm_kisan_verified']=="Yes" else "Unverified", delta_color="normal" if features['pm_kisan_verified']=="Yes" else "inverse")
        m4.metric(label="UPI P2M Ratio", value=features['upi_p2m_ratio'], help="Low ratio indicates cash dependency")

    st.divider()

    # --- BOTTOM ROW: THE "HACKATHON WINNING" TABS ---
    tab1, tab2, tab3 = st.tabs(["🤖 GenAI Advisory", "📈 Explainable AI (XAI)", "🗄️ Data Lineage"])
    
    with tab1:
        st.subheader("RBI-Compliant Decision Rationale")
        with st.spinner("Querying FAISS Vector Search & Llama-3..."):
            advisory = generate_rbi_advisory(score)
        
        if score >= 650:
            st.success(advisory)
        else:
            st.warning(advisory)
            
    with tab2:
        st.subheader("Model Feature Importance")
        st.caption("Visualizing the weights assigned by the Databricks AutoML model.")
        
        # Explainable AI Bar Chart
        fig_xai = go.Figure(go.Bar(
            x=[35, 25, 20, 10, 10],
            y=['Telecom History', 'FASTag Activity', 'PM-Kisan Link', 'UPI Volume', 'Bank Bal'],
            orientation='h',
            marker_color=['#10b981', '#3b82f6', '#8b5cf6', '#6b7280', '#9ca3af']
        ))
        fig_xai.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_xai, use_container_width=True)

    with tab3:
        st.subheader("Medallion Architecture (Databricks)")
        st.caption("How data flowed into this prediction:")
        st.markdown("""
        * 🥉 **Bronze:** Raw JSON logs from Telecom APIs, FASTag CSVs, and UPI dumps.
        * 🥈 **Silver:** Cleansed and joined on `Aadhaar_Hash` using Delta Live Tables.
        * 🥇 **Gold:** Aggregated feature store serving the MLflow model.
        """)

elif not evaluate_btn:
    # Beautiful empty state
    st.info("👈 Enter an Applicant ID in the sidebar to initiate the AI Underwriting sequence.")
    st.markdown("""
    ### Why Krishi-Credit?
    Traditional banks reject farmers with low UPI balances. We use **Databricks ML** to discover creditworthiness hidden in alternative data, empowering the unbanked.
    """)
