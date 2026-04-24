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

# NOTE: Custom background CSS removed to allow native Streamlit Dark/Light mode!

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
    features = {
        "Telecom Streak": f"{random.randint(6, 36)} months active",
        "FASTag Activity": "High (Mandi Route)",
        "PM-Kisan Status": "Verified",
        "Crop Insurance": "Active (PMFBY)"
    }
    
    return score, features


def generate_rbi_letter(score: int, features: dict) -> str:
    """
    [DATABRICKS AI GATEWAY / RAG INTEGRATION POINT]
    Expects to call an LLM (like Llama-3) via Foundation Model APIs, querying a FAISS
    vector store containing RBI Microfinance directives.
    
    Args:
        score: The applicant's ML-generated trust score.
        features: The alternative data points driving the decision.
    Returns:
        A Markdown-formatted string in Hindi.
    """
    # Simulating LLM generation latency
    time.sleep(1.5)
    
    # Dummy Hindi payload
    if score >= 600:
        return f"""
        **निर्णय: ऋण स्वीकृत (Approved)** इस आवेदक का वैकल्पिक डेटा प्रोफ़ाइल अत्यधिक सकारात्मक है। इनका कृषक विश्वास स्कोर (Trust Score) **{score}/900** है।  
        
        यद्यपि इनका नकद-अर्थव्यवस्था (Cash Economy) के कारण UPI उपयोग सीमित है, इनका **{features['Telecom Streak']}** का निर्बाध मोबाइल रिचार्ज रिकॉर्ड और **{features['PM-Kisan Status']}** PM-Kisan भूमि सत्यापन इनकी वित्तीय विश्वसनीयता को प्रमाणित करते हैं। **{features['FASTag Activity']}** गतिविधि इनकी फसल आपूर्ति शृंखला में भागीदारी को दर्शाती है। 
        
        *यह निर्णय भारतीय रिज़र्व बैंक (RBI) के 'सूक्ष्म वित्त ऋण (Microfinance Loans)' मास्टर दिशा-निर्देशों के पूर्ण अनुपालन में लिया गया है।*
        """
    else:
        return f"""
        **निर्णय: अतिरिक्त समीक्षा आवश्यक (Manual Review Required)** इस आवेदक का कृषक विश्वास स्कोर **{score}/900** है।  
        
        यद्यपि इनके पास **{features['Crop Insurance']}** है, परंतु उनके दूरसंचार (Telecom) और परिवहन (FASTag) पदचिह्न अपर्याप्त हैं। RBI के जोखिम प्रबंधन मानकों के अनुसार, ऋण स्वीकृत करने से पूर्व फील्ड अधिकारी (Field Agent) द्वारा भौतिक सत्यापन और आय अनुमान की आवश्यकता है।
        """


# ==========================================
# 3. STREAMLIT UI: SIDEBAR
# ==========================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/869/869114.png", width=50) # Small leaf/agri logo
    st.title("Krishi-Credit AI")
    st.caption("Powered by Databricks Apps")
    
    st.divider()
    
    st.subheader("Branch Manager Portal")
    farmer_id = st.text_input("Enter Farmer ID / Aadhaar", placeholder="e.g., ADHR-9842")
    
    evaluate_btn = st.button("Evaluate Applicant", type="primary", use_container_width=True)
    
    st.divider()
    st.info("🎯 **Notice:** This system bypasses traditional credit bureaus by analyzing alternative digital footprints.")


# ==========================================
# 4. STREAMLIT UI: MAIN DASHBOARD
# ==========================================

st.title("🌾 Applicant Underwriting Dashboard")
st.markdown("Evaluate unbanked/underbanked farmers operating in the cash economy.")
st.divider()

if evaluate_btn:
    if not farmer_id:
        st.warning("⚠️ Please enter a valid Farmer ID to proceed.")
    else:
        # --- ML PIPELINE EXECUTION ---
        with st.spinner("Analyzing alternative digital footprints via Databricks MLflow..."):
            score, features = fetch_ml_score(farmer_id)
            
        # --- TOP HALF: THE HARD DATA ---
        st.subheader("📊 Alternative Credit Profile")
        
        # Determine styling based on score
        if score >= 700:
            risk_tier = "Prime (Low Risk)"
        elif score >= 600:
            risk_tier = "Near Prime (Medium Risk)"
        else:
            risk_tier = "Subprime (High Risk)"
            
        # Layout: Score on the left, Metrics on the right
        score_col, metrics_col = st.columns([1, 2.5])
        
        with score_col:
            st.metric(label="Sovereign Trust Score", value=score, delta=risk_tier)
            
        with metrics_col:
            st.caption("Key Data Footprints")
            # 3 Alternative Data Cards
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric(label="📱 Telecom Stability", value="Verified", delta=features["Telecom Streak"])
            with c2:
                st.metric(label="🚜 Mandi Transport", value="Active", delta=features["FASTag Activity"])
            with c3:
                st.metric(label="🏛️ Gov Welfare", value="Linked", delta=features["PM-Kisan Status"])

        st.write("---") # Visual separator

        # --- BOTTOM HALF: SOVEREIGN REASONING (GenAI) ---
        st.subheader("🤖 AI Underwriting Advisory (RBI Compliant)")
        st.caption("Locally generated rationale explaining the ML model's decision.")
        
        with st.spinner("Drafting compliant rationale via Databricks Foundation Model APIs..."):
            advisory_text = generate_rbi_letter(score, features)
            
        # Display the output in a clean info/success box
        if score >= 600:
            st.success(advisory_text, icon="✅")
        else:
            st.warning(advisory_text, icon="⚠️")

else:
    # --- DEFAULT / WAITING STATE ---
    # Center-aligned welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👈 Please enter an applicant ID in the sidebar and click **Evaluate Applicant** to run the pipeline.")
        st.markdown("""
        **How it works:**
        1. Ingests raw data via Databricks Unity Catalog.
        2. MLflow scores the applicant using non-traditional proxies (Telecom, FASTag, etc.).
        3. Llama-3 (AI Gateway) drafts an RBI-compliant explanation in local languages.
        """)
