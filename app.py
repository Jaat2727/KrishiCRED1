import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Krishi-Credit AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
    <style>
    /* Dark theme overrides for a sleek look */
    .stApp { background-color: #0e1117; }
    .stMetric { 
        background-color: #1f2937; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header { font-size: 2.5rem; font-weight: 700; color: #10b981; margin-bottom: 0rem; }
    .sub-header { font-size: 1.2rem; color: #9ca3af; margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: DATA INPUT (THE SOVEREIGN PROXIES) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=60) # Placeholder logo
    st.title("Applicant Portal")
    st.caption("Enter alternative data proxies to evaluate cash-economy borrowers.")
    
    st.divider()
    
    # Base Data
    applicant_id = st.text_input("Aadhaar / Phone No.", "9876543210")
    upi_ratio = st.slider("UPI Merchant vs P2P Ratio", 0.0, 1.0, 0.2, help="Low ratio implies high cash usage.")
    
    st.subheader("Alternative Footprint")
    recharge_streak = st.slider("Telecom Recharge Streak (Months)", 0, 24, 12, help="Proxy for liquid cash flow.")
    fastag_trips = st.number_input("Mandi Trips (Fastag Pings, Last 6M)", 0, 50, 5, help="Proxy for harvest transport.")
    pm_kisan = st.selectbox("PM-Kisan Installments Received", [0, 1, 2, 3], index=2, help="Proxy for verified land ownership.")
    
    st.divider()
    analyze_btn = st.button("Generate Underwriting Report", type="primary", use_container_width=True)

# --- 4. MAIN DASHBOARD ---
st.markdown('<p class="main-header">🛡️ Krishi-Credit AI Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Financial Inclusion for Bharat\'s Informal Economy | Powered by Databricks</p>', unsafe_allow_html=True)

if analyze_btn:
    # --- MOCK ML ENGINE (Replace with real Databricks AutoML later) ---
    with st.spinner("Analyzing Alternative Data via Databricks AutoML..."):
        time.sleep(1.5) # Simulating ML prediction time
        
        # Fake logic for demo purposes tonight
        base_score = 300
        cash_proxy_boost = (recharge_streak * 15) + (fastag_trips * 8) + (pm_kisan * 30)
        final_score = min(base_score + cash_proxy_boost, 900)
        
        risk_category = "Low Risk (Prime)" if final_score > 700 else "Medium Risk" if final_score > 550 else "High Risk"
        delta_color = "normal" if final_score > 550 else "inverse"

    # --- TOP ROW: CORE METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Sovereign Trust Score", value=f"{int(final_score)}/900", delta=risk_category, delta_color=delta_color)
    with col2:
        st.metric(label="Cash-Flow Stability", value="High", delta="Based on Telecom")
    with col3:
        st.metric(label="Asset Verification", value="Verified", delta="PM-Kisan Match")
    with col4:
        st.metric(label="Est. Loan Limit", value=f"₹{int(final_score * 120)}", delta="Pre-Approved")

    st.divider()

    # --- BOTTOM ROW: CHARTS & GEN AI ---
    chart_col, genai_col = st.columns([1.2, 1])
    
    with chart_col:
        st.write("### 📈 Feature Importance (Explainable AI)")
        st.caption("Why did the ML model assign this score?")
        
        # Simple Plotly bar chart
        fig = go.Figure(go.Bar(
            x=[recharge_streak*15, fastag_trips*8, pm_kisan*30, (upi_ratio*100)],
            y=['Telecom Streak', 'Fastag Pings', 'Govt Schemes', 'UPI Volume'],
            orientation='h',
            marker_color=['#10b981', '#3b82f6', '#8b5cf6', '#6b7280']
        ))
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with genai_col:
        st.write("### 🤖 GenAI Sovereign Advisory")
        st.caption("Contextual lending advice powered by Indian LLMs.")
        
        with st.status("Querying RBI Circulars via FAISS...", expanded=True) as status:
            time.sleep(1)
            st.write("✓ Found match: *RBI Master Circular - Microfinance Loans*")
            time.sleep(1)
            st.write("✓ Generating empathetic response in local language...")
            status.update(label="Response Generated!", state="complete", expanded=False)
            
        st.success("Decision summary generated for field agent.")
        
        # The fake LLM output
        st.markdown(f"""
        **Applicant {applicant_id} Summary:**
        
        > "इस आवेदक का UPI उपयोग कम है क्योंकि वे नकद अर्थव्यवस्था (Cash Economy) में काम करते हैं। हालांकि, उनका 12 महीने का मोबाइल रिचार्ज रिकॉर्ड और PM-Kisan सत्यापन उच्च वित्तीय अनुशासन को दर्शाता है। RBI के माइक्रोफाइनेंस दिशानिर्देशों के अनुसार, वे ₹{int(final_score * 120)} के कृषि ऋण के लिए पात्र हैं।"
        
        *Confidence Score: 94% | Language: Hindi | Evaluated by BhashaBench*
        """)

else:
    # What shows before they click the button
    st.info("👈 Enter applicant data in the sidebar and click 'Generate Underwriting Report' to see the AI analysis.")
