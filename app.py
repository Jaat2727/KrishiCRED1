import streamlit as st
import pandas as pd
import random
import time
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# ==========================================
# 1. PAGE CONFIGURATION & PREMIUM CSS
# ==========================================
st.set_page_config(page_title="Krishi-Credit AI", page_icon="🌾", layout="wide")

st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sleek background gradient for the main header */
    .premium-header {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .sub-header {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Glass-morphism effect for all Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    /* Hover effect for metrics */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.2);
    }
    
    /* GenAI Advisory Box Styling */
    .ai-box {
        background-color: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #10b981;
        padding: 25px;
        border-radius: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        color: #f8fafc;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOCK DATA ENGINE (Until you connect SQL)
# ==========================================
def fetch_ml_data(user_id: str):
    time.sleep(1.2) # Simulate backend calculation
    seed = sum(ord(c) for c in user_id)
    random.seed(seed)
    
    score = random.randint(550, 850)
    features = {
        "telecom": random.randint(12, 48),
        "fastag": random.randint(10, 50),
        "pm_kisan": random.randint(1, 3),
        "upi": random.randint(10, 70),
        "insurance": random.choice(["Active", "Inactive"])
    }
    return score, features

# ==========================================
# 3. SIDEBAR: NAVIGATION & INPUT
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=60)
    st.markdown("## Krishi-Credit AI")
    st.caption("Databricks Hackathon V1")
    st.divider()
    
    selected_menu = option_menu(
        menu_title=None,
        options=["Underwriting Engine", "Data Lineage", "API Settings"],
        icons=["cpu", "database-check", "gear"],
        default_index=0,
        styles={
            "container": {"background-color": "transparent", "padding": "0!important"},
            "nav-link-selected": {"background-color": "#2563eb"},
        }
    )
    
    st.divider()
    st.markdown("### Manager Portal")
    applicant_id = st.text_input("Aadhaar / Farmer ID", value="ADHR-7729")
    run_engine = st.button("🚀 Evaluate Applicant", use_container_width=True, type="primary")

# ==========================================
# 4. MAIN DASHBOARD: THE WOW FACTOR
# ==========================================
if selected_menu == "Underwriting Engine":
    st.markdown('<p class="premium-header">Sovereign Credit Engine</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Evaluating cash-economy farmers via alternative digital footprints.</p>', unsafe_allow_html=True)
    
    if run_engine:
        with st.spinner("Querying Unity Catalog Gold Table & running MLflow..."):
            score, features = fetch_ml_data(applicant_id)
        
        # Risk logic
        tier = "Prime" if score >= 750 else "Near-Prime" if score >= 600 else "Sub-Prime"
        gauge_color = "#10b981" if score >= 600 else "#ef4444"

        # --- TOP ROW: GAUGE AND KEY METRICS ---
        col_gauge, col_metrics = st.columns([1.2, 2])
        
        with col_gauge:
            # Beautiful Plotly Gauge Chart
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = score,
                delta = {'reference': 600, 'increasing': {'color': "#10b981"}, 'decreasing': {'color': "#ef4444"}},
                title = {'text': "Trust Score", 'font': {'size': 24, 'color': "white"}},
                gauge = {
                    'axis': {'range': [300, 900], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': gauge_color},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [300, 600], 'color': 'rgba(239, 68, 68, 0.2)'},
                        {'range': [600, 750], 'color': 'rgba(245, 158, 11, 0.2)'},
                        {'range': [750, 900], 'color': 'rgba(16, 185, 129, 0.2)'}],
                }
            ))
            fig_gauge.update_layout(height=320, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_metrics:
            st.write("") # Spacer
            st.markdown(f"**Applicant Status:** Risk Tier `{tier}` | Limit: **₹{int(score * 120)}**")
            
            # Sleek Grid for Metrics
            m1, m2 = st.columns(2)
            m1.metric(label="📱 Telecom Streak", value=f"{features['telecom']} Months", delta="High Liquidity")
            m2.metric(label="🚜 Mandi Logistics", value=f"{features['fastag']} FASTag Pings", delta="Verified Route")
            
            st.write("") # Spacing
            m3, m4 = st.columns(2)
            m3.metric(label="🌾 PM-Kisan Welfare", value=f"{features['pm_kisan']} Installments", delta="Gov Verified")
            m4.metric(label="🛡️ Crop Insurance", value=features['insurance'], delta="PMFBY Registry")

        st.divider()

        # --- BOTTOM ROW: RADAR CHART & GENAI ---
        col_radar, col_ai = st.columns([1, 1.2])
        
        with col_radar:
            st.subheader("📊 Data Footprint Analysis")
            st.caption("Applicant vs. Prime Baseline")
            
            # Premium Radar Chart
            categories = ['Telecom', 'Transport', 'Welfare', 'Insurance', 'UPI Density']
            fig_radar = go.Figure()
            # Baseline
            fig_radar.add_trace(go.Scatterpolar(
                r=[80, 70, 90, 85, 50], theta=categories, fill='toself', name='Prime Baseline',
                line_color='rgba(148, 163, 184, 0.5)', fillcolor='rgba(148, 163, 184, 0.1)'
            ))
            # Applicant
            fig_radar.add_trace(go.Scatterpolar(
                r=[features['telecom']*2, features['fastag']*2, features['pm_kisan']*30, 90 if features['insurance'] == 'Active' else 20, features['upi']],
                theta=categories, fill='toself', name='Applicant Profile',
                line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.4)'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=False, range=[0, 100]),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=True, height=350, margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_ai:
            st.subheader("🤖 GenAI Sovereign Advisor")
            st.caption("Powered by Databricks AI Gateway (Llama-3 & Vector Search)")
            
            # Custom GenAI UI Box
            if score >= 600:
                ai_text = f"""
                <div class="ai-box">
                <b>✅ Approval Recommended</b><br><br>
                This applicant demonstrates strong alternative credit reliability despite a cash-heavy profile. 
                <br><br>
                The <b>{features['telecom']}-month telecom streak</b> indicates steady disposable income. The <b>{features['fastag']} FASTag transactions</b> verify active agricultural logistics, and PM-Kisan linkage confirms land asset ownership. 
                <br><br>
                <i>Compliant with RBI Master Direction on Microfinance Loans (2022) regarding proxy-income assessment.</i>
                </div>
                """
            else:
                ai_text = f"""
                <div class="ai-box" style="border-left-color: #ef4444;">
                <b>⚠️ Field Verification Required</b><br><br>
                This applicant's alternative data footprint is currently insufficient for an automated AI underwriting decision. 
                <br><br>
                While some data exists, the volume falls below the risk threshold. Proceed with standard physical field inspection and manual cash-flow estimation.
                </div>
                """
            st.markdown(ai_text, unsafe_allow_html=True)

    else:
        # Beautiful empty state
        st.write("")
        st.write("")
        st.info("👈 Enter a Farmer ID in the sidebar to run the Databricks AutoML Underwriting Pipeline.")

# --- OTHER TABS (For presentation purposes) ---
elif selected_menu == "Data Lineage":
    st.markdown('<p class="premium-header">Unity Catalog Lineage</p>', unsafe_allow_html=True)
    st.write("This tab will display your Medallion Architecture graph during the pitch.")
