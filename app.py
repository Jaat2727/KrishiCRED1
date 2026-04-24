import streamlit as st
import pandas as pd
import time

# --- Page Config ---
st.set_page_config(page_title="Krishi-Credit AI", layout="wide")

# --- Custom CSS for "Sovereign" look ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_name_with_html=True)

# --- Sidebar: Input Section ---
st.sidebar.title("👨‍🌾 Applicant Portal")
st.sidebar.info("Enter details to calculate Sovereign Trust Score.")

user_id = st.sidebar.text_input("Enter Aadhaar / Phone Number", "9876543210")
recharge_streak = st.sidebar.slider("Telecom Recharge Streak (Months)", 0, 24, 12)
fastag_trips = st.sidebar.number_input("Mandi Trips (Fastag Pings)", 0, 50, 5)

# --- Header ---
st.title("🛡️ Krishi-Credit AI")
st.subheader("Financial Inclusion for Bharat's Informal Economy")
st.divider()

# --- Main Dashboard ---
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### 📊 ML Trust Analytics")
    # Simulation for now - we'll replace with real AutoML call soon
    score = 300 + (recharge_streak * 20) + (fastag_trips * 5)
    score = min(score, 900)
    
    st.metric(label="Sovereign Credit Score", value=f"{score}/900", delta="High Trust" if score > 700 else "Neutral")
    
    st.write("#### Key Indicators")
    st.write(f"✅ **Recharge Discipline:** {recharge_streak} Months")
    st.write(f"🚜 **Asset Activity:** {fastag_trips} Mandi Trips")
    st.write("🛒 **UPI P2M Ratio:** 0.85 (High Formalization)")

with col2:
    st.write("### 📝 GenAI Sovereign Advisory")
    if st.button("Generate Regional Advisory Letter"):
        with st.spinner("Retrieving RBI Guidelines & Translating..."):
            time.sleep(2) # Mocking the processing
            # This is where the AI Gateway call will go
            st.success("Advisory Generated Successfully!")
            
            st.markdown(f"""
            **Decision Summary (Language: Hindi)**
            
            महोदय/महोदया,
            आपकी वित्तीय प्रोफ़ाइल का विश्लेषण करने के बाद, हम आपकी ऋण पात्रता की पुष्टि करते हैं। 
            आपका लगातार मोबाइल रिचार्ज और मंडी की सक्रियता आपकी विश्वसनीयता दर्शाती है।
            
            **Loan Eligibility:** ₹50,000  
            **Interest Rate:** 1.5% Monthly
            """)

st.divider()
st.caption("Built on Databricks Free Edition | Medallion Architecture | BhashaBench Evaluated")
