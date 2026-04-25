import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
import re
import time

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Krishi-Credit OS", layout="wide")

# Inject Earthy Agricultural Brand Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    /* Earthy Warm Theme */
    [data-testid="stAppViewContainer"] { 
        background-color: #E8E4D8 !important; 
        color: #4A2E1E !important; 
        background-image: radial-gradient(circle, #D6D0C4 1px, transparent 1px) !important;
        background-size: 20px 20px !important;
    }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container { max-width: 95% !important; padding-top: 3rem !important; padding-bottom: 2rem !important; }
    
    /* Sleek Input Styling */
    div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput > div > div, .stSelectbox > div > div {
        background-color: #F0ECE1 !important;
        border: 1px solid #D6D0C4 !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within, .stTextInput > div > div:focus-within, .stSelectbox > div > div:focus-within {
        border-color: #7A7428 !important;
        box-shadow: 0 0 0 1px #7A7428 !important;
    }
    div[data-baseweb="input"] input, .stTextInput input {
        color: #4A2E1E !important;
        background-color: transparent !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
    }
    
    /* Sleek Select Box Styling */
    div[data-baseweb="select"] > div, .stSelectbox div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: #4A2E1E !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 0.9rem !important;
    }
    
    /* Earthy Brand Button */
    div.stButton > button {
        background-color: #0E5A2D !important;
        color: #F0ECE1 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        height: 42px !important;
        font-size: 0.9rem !important;
        transition: opacity 0.2s ease !important;
    }
    div.stButton > button:hover { 
        opacity: 0.85 !important;
    }
    
    /* Clean up input labels */
    .stTextInput label, .stSelectbox label {
        color: #7A7428 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        margin-bottom: 0.25rem !important;
    }

    /* Fix Placeholder Visibility */
    ::placeholder { color: #9A8B7A !important; opacity: 0.7 !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LAYER & VOICE LOGIC
# ==========================================
@st.cache_data
def load_data():
    if os.path.exists("master_hackathon_data_1000000_rows.csv"):
        return pd.read_csv("master_hackathon_data_1000000_rows.csv")
    if os.path.exists("krishi_credit_engine_data.csv"):
        return pd.read_csv("krishi_credit_engine_data.csv")
    return pd.DataFrame()

def fetch_applicant_data(user_id: str, df: pd.DataFrame):
    if df.empty: return None
    if 'farmer_id' in df.columns:
        user_data = df[df['farmer_id'] == user_id]
        if not user_data.empty: return user_data.iloc[0]
    if 'user_id' in df.columns:
        match = re.search(r'\d+', user_id)
        if match:
            numeric_id = int(match.group())
            user_data = df[df['user_id'] == numeric_id]
            if not user_data.empty: return user_data.iloc[0]
    return None

# ==========================================
# 3. NATIVE HEADER & CONTROLS
# ==========================================
# Native header prevents iframe spacing gaps
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #D6D0C4; padding-bottom: 1.5rem; margin-bottom: 2rem;">
        <div>
            <h1 style="color: #4A2E1E; font-size: 1.1rem; font-weight: 700; margin: 0; display: flex; align-items: center; gap: 10px; font-family: 'Inter', sans-serif;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0E5A2D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                Databricks Underwriting Engine
            </h1>
            <p style="color: #7A7428; font-size: 0.8rem; margin: 4px 0 0 0; font-family: 'Inter', sans-serif;">Krishi-Credit OS v2.4 • Unity Catalog Connected</p>
        </div>
        <div>
            <span style="background: #F0ECE1; border: 1px solid #D6D0C4; color: #7A7428; padding: 4px 10px; border-radius: 4px; font-size: 0.7rem; font-weight: 500; display: flex; align-items: center; gap: 6px; font-family: 'Inter', sans-serif;">
                <span style="width: 6px; height: 6px; background: #0E5A2D; border-radius: 50%;"></span>
                System Normal
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

col_search, col_lang, col_btn, col_pad = st.columns([3, 2, 2, 2])
with col_search:
    applicant_id = st.text_input("Applicant Identification", value="ADHR-100004", placeholder="Enter ID", label_visibility="collapsed")
with col_lang:
    selected_language = st.selectbox("Language", ["English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", "Hindi", "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", "Marathi", "Nepali", "Odia", "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", "Telugu", "Urdu"], label_visibility="collapsed")
with col_btn:
    run_engine = st.button("Query Pipeline")

st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# ==========================================
# 4. DASHBOARD RENDERER
# ==========================================
if 'dashboard_active' not in st.session_state:
    st.session_state.dashboard_active = True

if run_engine:
    st.session_state.dashboard_active = True

if st.session_state.dashboard_active:
    df = load_data()
    ui_container = st.empty()
    
    skeleton_html = f"""<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script><style>body {{ background-color: #E8E4D8; margin: 0; }} .skeleton {{ background: linear-gradient(90deg, #E5E0D3 25%, #E0DBCF 50%, #E5E0D3 75%); background-size: 400% 100%; animation: shimmer 1.5s infinite; border-radius: 4px; }} @keyframes shimmer {{ 0% {{ background-position: 200% 0; }} 100% {{ background-position: -200% 0; }} }}</style></head><body><div class="border border-[#D6D0C4] rounded-xl bg-[#F0ECE1] overflow-hidden flex flex-col w-full shadow-lg"><div class="px-6 py-4 border-b border-[#D6D0C4] flex justify-between items-center bg-[#EAE5D9]"><div class="flex items-center gap-3"><div class="w-8 h-8 rounded skeleton"></div><div><div class="h-3 w-24 skeleton mb-2"></div><div class="h-2 w-32 skeleton"></div></div></div><div class="flex items-center gap-2"><div class="h-5 w-20 skeleton rounded-md"></div><div class="h-5 w-16 skeleton rounded-md"></div></div></div><div class="grid grid-cols-3 divide-x divide-[#D6D0C4]"><div class="p-6"><div class="h-3 w-24 skeleton mb-5"></div><div class="space-y-4 mt-2"><div class="flex justify-between items-center"><div class="h-3 w-20 skeleton"></div><div class="h-4 w-12 skeleton"></div></div><div class="flex justify-between items-center"><div class="h-3 w-24 skeleton"></div><div class="h-4 w-14 skeleton"></div></div><div class="flex justify-between items-center"><div class="h-3 w-16 skeleton"></div><div class="h-4 w-12 skeleton"></div></div><div class="flex justify-between items-center"><div class="h-3 w-28 skeleton"></div><div class="h-4 w-10 skeleton"></div></div></div><div class="mt-6 pt-5 border-t border-[#D6D0C4]"><div class="h-3 w-24 skeleton mb-4"></div><div class="h-10 w-full skeleton rounded-sm"></div></div></div><div class="p-6 bg-[#EAE5D9] flex flex-col items-center justify-center relative"><div class="absolute top-6 left-6 h-3 w-20 skeleton"></div><div class="mt-4 relative flex items-center justify-center"><div class="w-32 h-32 rounded-full border-[6px] border-[#E0DBCF]"></div><div class="absolute flex flex-col items-center justify-center"><div class="h-8 w-16 skeleton mb-1"></div><div class="h-2 w-8 skeleton"></div></div></div><div class="h-2 w-32 skeleton mt-5"></div></div><div class="p-6 flex flex-col"><div class="flex items-center justify-between mb-4"><div class="h-3 w-24 skeleton"></div><div class="h-4 w-28 skeleton rounded-md"></div></div><div class="flex-grow space-y-2 mt-2"><div class="h-2 w-full skeleton"></div><div class="h-2 w-full skeleton"></div><div class="h-2 w-5/6 skeleton"></div><div class="h-2 w-4/6 skeleton"></div></div><div class="mt-4 pt-4 border-t border-[#D6D0C4] flex items-center justify-between"><div class="h-3 w-40 skeleton"></div></div></div></div><div class="border-t border-[#D6D0C4] bg-[#EAE5D9] p-6 flex flex-col md:flex-row items-center justify-between"><div class="flex items-center gap-4 w-full md:w-1/2 mb-4 md:mb-0"><div class="w-10 h-10 rounded skeleton"></div><div><div class="h-3 w-32 skeleton mb-2"></div><div class="flex gap-2"><div class="h-6 w-24 skeleton"></div><div class="h-4 w-16 skeleton rounded-md"></div></div></div></div><div class="w-full md:w-1/2 flex flex-col justify-center pl-0 md:pl-6 border-l-0 md:border-l border-[#D6D0C4]"><div class="flex justify-between items-center mb-2"><div class="h-2 w-24 skeleton"></div><div class="h-2 w-6 skeleton"></div></div><div class="w-full h-1.5 skeleton rounded-full"></div></div></div></div></body></html>"""
    
    with ui_container:
        components.html(skeleton_html, height=870, scrolling=False)
        
    time.sleep(1.2) # Allow skeleton UI to be visible during pseudo-loading
    user_row = fetch_applicant_data(applicant_id, df)
        
    if user_row is None:
        ui_container.empty()
        st.error(f"Applicant record '{applicant_id}' could not be located in Unity Catalog.")
    else:
        # Extract features
        score = int(user_row.get("synthetic_agri_cibil_score", user_row.get("krishi_credit_score", 0)))
        telecom = int(user_row.get("telecom_recharge_streak_months", 0))
        fastag = int(user_row.get("fastag_trips_last_6m", 0))
        pm_kisan = int(user_row.get("pmkisan_installments_ytd", 0))
        upi = int(user_row.get("upi_transaction_count_30d", 0))
        
        # New hackathon features
        mandi_vol = float(user_row.get("mandi_revenue_volatility_index", 0.0))
        ndvi_var = float(user_row.get("satellite_ndvi_variance", 0.0))
        dbt_dep = float(user_row.get("dbt_dependence_percentage", 0.0))
        zero_bal = int(user_row.get("days_with_zero_balance_6m", 0))
        
        # Farmer Profile Features
        land_area = float(user_row.get("land_area_hectares", 0.0))
        agristack = int(user_row.get("agristack_id_linked", 0))
        pmfby = int(user_row.get("pmfby_insurance_enrolled", 0))
        aadhaar = int(user_row.get("aadhaar_ekyc_verified", 0))
        
        # Harvest Repayment Data
        rabi_share = int(user_row.get("rabi_crop_share_pct", 50))
        kharif_share = int(user_row.get("kharif_crop_share_pct", 50))
        
        # Extract ML Predicted Credit Limit from Dataset
        recommended_limit = int(user_row.get("predicted_lending_limit", 0))
        max_limit = land_area * 100000
        
        if recommended_limit == 0:
            limit_color = "text-[#9A5A33]" # Rust Brown
            bar_color = "bg-[#9A5A33]"
            limit_status = "Declined"
            limit_percentage = 0
        else:
            limit_color = "text-[#0E5A2D]" if score >= 600 else "text-[#7A7428]"
            bar_color = "bg-[#0E5A2D]" if score >= 600 else "bg-[#7A7428]"
            limit_status = "Pre-Approved" if score >= 600 else "Manual Review"
            limit_percentage = min(100, int((recommended_limit / max_limit) * 100)) if max_limit > 0 else 0
            
        limit_formatted = f"₹{recommended_limit:,.0f}" if recommended_limit > 0 else "₹0"
        
        is_approved = score >= 600
        
        # Simulate 6-month historical UPI volume for the Bar Chart
        import random
        random.seed(int(re.search(r'\d+', applicant_id).group())) # deterministic seed based on numeric ID
        upi_avg_inr_val = float(user_row.get("upi_monthly_avg_inr", 0))
        upi_history = [max(0, upi_avg_inr_val * (1 + random.uniform(-0.4, 0.4))) for _ in range(6)]
        max_upi = max(upi_history) if max(upi_history) > 0 else 1
        
        chart_height = 40
        bar_width = 14
        bar_spacing = 8
        left_margin = 28
        def format_currency_short(val):
            if val >= 100000: return f"{val/100000:.1f}L"
            if val >= 1000: return f"{val/1000:.0f}K"
            return f"{val:.0f}"
            
        svg_bars = f'''
            <!-- Y-Axis Grid Lines & Labels -->
            <text x="{left_margin-6}" y="6" fill="#52525b" font-size="7" font-weight="500" text-anchor="end" font-family="Inter, sans-serif">{format_currency_short(max_upi)}</text>
            <line x1="{left_margin}" y1="4" x2="{left_margin + 132}" y2="4" stroke="#262626" stroke-width="1" stroke-dasharray="2,2" />
            
            <text x="{left_margin-6}" y="{chart_height/2 + 2}" fill="#52525b" font-size="7" font-weight="500" text-anchor="end" font-family="Inter, sans-serif">{format_currency_short(max_upi/2)}</text>
            <line x1="{left_margin}" y1="{chart_height/2}" x2="{left_margin + 132}" y2="{chart_height/2}" stroke="#262626" stroke-width="1" stroke-dasharray="2,2" />
            
            <text x="{left_margin-6}" y="{chart_height}" fill="#52525b" font-size="7" font-weight="500" text-anchor="end" font-family="Inter, sans-serif">0</text>
            <line x1="{left_margin}" y1="{chart_height}" x2="{left_margin + 132}" y2="{chart_height}" stroke="#262626" stroke-width="1" stroke-dasharray="2,2" />
        '''
        
        for i, val in enumerate(upi_history):
            h = max(2, (val / max_upi) * chart_height)
            y_pos = chart_height - h
            x_pos = left_margin + i * (bar_width + bar_spacing)
            delay = 300 + (i * 100)
            color = "#0E5A2D" if val >= upi_avg_inr_val else "#D6D0C4" # Highlight above average
            svg_bars += f'''
                <rect x="{x_pos}" y="{y_pos}" width="{bar_width}" height="{h}" fill="{color}" rx="1.5" class="animate-fade-up" style="animation-delay: {delay}ms; opacity: 0;" />
                <text x="{x_pos + bar_width/2}" y="{chart_height + 14}" fill="#737373" font-size="8" font-weight="600" text-anchor="middle" class="animate-fade-up" style="animation-delay: {delay}ms; opacity: 0;">M{6-i}</text>
            '''
            
        import datetime
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        
        # =========================================
        # RADAR CHART: 5-Signal Risk Dimensions
        # =========================================
        import math
        radar_cx, radar_cy, radar_r = 100, 95, 70
        
        # Normalize each signal to 0-1
        radar_signals = {
            "Mandi Stability": max(0.0, 1.0 - (mandi_vol / 10.0)),
            "Crop Health": max(0.0, 1.0 - ndvi_var),
            "Financial Cushion": max(0.0, 1.0 - (zero_bal / 180.0)),
            "DBT Independence": max(0.0, 1.0 - dbt_dep),
            "UPI Activity": min(1.0, upi / 60.0),
        }
        signal_names = list(radar_signals.keys())
        signal_vals = list(radar_signals.values())
        num_axes = len(signal_names)
        
        def radar_point(i, r_scale, cx, cy, r, n):
            angle = math.pi / 2 + (2 * math.pi * i / n)  # start from top
            x = cx + r * r_scale * math.cos(angle)
            y = cy - r * r_scale * math.sin(angle)
            return x, y

        # Outer grid hexagons (25%, 50%, 75%, 100%)
        radar_grids = ""
        for level in [0.25, 0.5, 0.75, 1.0]:
            pts = " ".join(f"{radar_point(i, level, radar_cx, radar_cy, radar_r, num_axes)[0]:.1f},{radar_point(i, level, radar_cx, radar_cy, radar_r, num_axes)[1]:.1f}" for i in range(num_axes))
            stroke_opacity = "0.2" if level < 1.0 else "0.35"
            radar_grids += f'<polygon points="{pts}" fill="none" stroke="#B8B0A0" stroke-width="{"0.5" if level < 1.0 else "1"}" opacity="{stroke_opacity}" />\n'
        
        # Axis lines from center to each vertex
        radar_axes = ""
        for i in range(num_axes):
            ox, oy = radar_point(i, 1.0, radar_cx, radar_cy, radar_r, num_axes)
            radar_axes += f'<line x1="{radar_cx}" y1="{radar_cy}" x2="{ox:.1f}" y2="{oy:.1f}" stroke="#B8B0A0" stroke-width="0.5" opacity="0.35" />\n'
        
        # Filled polygon from data values
        data_pts = " ".join(f"{radar_point(i, signal_vals[i], radar_cx, radar_cy, radar_r, num_axes)[0]:.1f},{radar_point(i, signal_vals[i], radar_cx, radar_cy, radar_r, num_axes)[1]:.1f}" for i in range(num_axes))
        radar_fill = f'<polygon points="{data_pts}" fill="rgba(14,90,45,0.12)" stroke="#0E5A2D" stroke-width="1.5" stroke-linejoin="round" style="animation: fadeUp 0.8s ease forwards; animation-delay: 600ms; opacity: 0;" />\n'

        # Dots at each vertex
        radar_dots = ""
        radar_labels = ""
        # Monochromatic earthy green scale
        label_colors = ["#0E5A2D", "#2D7A4A", "#4A9668", "#7A7428", "#9A5A33"]
        for i, (name, val) in enumerate(zip(signal_names, signal_vals)):
            dx, dy = radar_point(i, val, radar_cx, radar_cy, radar_r, num_axes)
            radar_dots += f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="2.5" fill="#0E5A2D" stroke="#F0ECE1" stroke-width="1" style="animation: fadeUp 0.4s ease forwards; animation-delay: {700 + i*80}ms; opacity: 0;" />\n'
            # Label at full radius + offset
            lx, ly = radar_point(i, 1.22, radar_cx, radar_cy, radar_r, num_axes)
            anchor = "middle"
            if lx < radar_cx - 5: anchor = "end"
            elif lx > radar_cx + 5: anchor = "start"
            pct = int(val * 100)
            radar_labels += f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#7A7428" font-size="7.5" font-weight="500" text-anchor="{anchor}" font-family="Inter, sans-serif" style="animation: fadeUp 0.4s ease forwards; animation-delay: {700 + i*80}ms; opacity: 0;">{name} {pct}%</text>\n'
        
        if 3 <= current_month <= 5:
            season_1 = f"Rabi ({current_year})"
            season_2 = f"Kharif ({current_year})"
            season_1_share = rabi_share
            season_2_share = kharif_share
        elif 6 <= current_month <= 10:
            season_1 = f"Kharif ({current_year})"
            season_2 = f"Rabi ({current_year + 1})"
            season_1_share = kharif_share
            season_2_share = rabi_share
        else:
            season_1 = f"Rabi ({current_year if current_month < 3 else current_year + 1})"
            season_2 = f"Kharif ({current_year if current_month < 3 else current_year + 1})"
            season_1_share = rabi_share
            season_2_share = kharif_share


        if is_approved:
            score_color_hex = "#0E5A2D" # Deep Green
            tier_badge = '<span class="inline-flex items-center rounded bg-[#E8F5ED] border border-[#C8E0D0] px-2 py-0.5 text-[10px] font-medium text-[#0E5A2D]">Prime Tier</span>'
            decision_text = "Automated Approval Recommended"
            decision_text_class = "text-[#0E5A2D]"
            decision_icon = "check-circle-2"
        else:
            score_color_hex = "#9A5A33" # Rust Brown
            tier_badge = '<span class="inline-flex items-center rounded bg-[#F5EDE8] border border-[#E0D0C8] px-2 py-0.5 text-[10px] font-medium text-[#9A5A33]">Sub-Prime Tier</span>'
            decision_text = "Manual Review Required"
            decision_text_class = "text-[#9A5A33]"
            decision_icon = "alert-circle"

        # ============================================
        # REPAYMENT PROJECTION TIMELINE (12 months)
        # ============================================
        month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        kharif_sow  = {6,7}
        kharif_grow = {8,9,10}
        kharif_harv = {11,12}
        rabi_sow    = {11,12}
        rabi_grow   = {1,2}
        rabi_harv   = {3,4}

        emi_per_harvest = int(recommended_limit * 0.5)  # 50% per harvest window

        tl_months = []
        for offset in range(12):
            m = ((current_month - 1 + offset) % 12) + 1
            label = month_names[m - 1]
            is_today_m = (offset == 0)
            if m in kharif_harv or m in rabi_harv:
                mtype = "harvest"
                emi = emi_per_harvest
            elif m in kharif_sow or m in rabi_sow:
                mtype = "sow"
                emi = 0
            elif m in kharif_grow or m in rabi_grow:
                mtype = "grow"
                emi = 0
            else:
                mtype = "idle"
                emi = 0
            tl_months.append({"label": label, "type": mtype, "emi": emi, "today": is_today_m})

        tl_w, tl_h = 860, 72
        cell_w = tl_w // 12
        tl_svg_blocks = ""
        type_colors = {"harvest": "#0E5A2D", "sow": "#9A5A33", "grow": "#7A7428", "idle": "#E5E0D3"}
        type_labels = {"harvest": "Harvest", "sow": "Sow", "grow": "Grow", "idle": ""}
        for idx, mo in enumerate(tl_months):
            x          = idx * cell_w
            color      = type_colors[mo["type"]]
            delay      = 100 + idx * 60
            opacity    = "0.85" if mo["today"] else "0.22"
            txt_fill   = "#4A2E1E" if mo["today"] else "#9A8B7A"
            txt_weight = "600" if mo["today"] else "400"
            lbl_fill   = "#F0ECE1" if mo["today"] else color
            tl_svg_blocks += f'<rect x="{x+1}" y="28" width="{cell_w-2}" height="30" rx="4" fill="{color}" opacity="{opacity}" style="animation: fadeUp 0.3s ease {delay}ms both;"/>\n'
            if mo["today"]:
                tl_svg_blocks += f'<rect x="{x+1}" y="28" width="{cell_w-2}" height="30" rx="4" fill="none" stroke="#0E5A2D" stroke-width="1.5"/>\n'
            tl_svg_blocks += f'<text x="{x + cell_w//2}" y="22" font-size="8" fill="{txt_fill}" font-weight="{txt_weight}" text-anchor="middle" font-family="Inter,sans-serif">{mo["label"]}</text>\n'
            if mo["type"] != "idle":
                tl_svg_blocks += f'<text x="{x + cell_w//2}" y="47" font-size="7" fill="{lbl_fill}" text-anchor="middle" font-family="Inter,sans-serif" opacity="0.9">{type_labels[mo["type"]]}</text>\n'
            if mo["emi"] > 0:
                emi_val = mo["emi"]
                emi_str = "Rs." + (str(emi_val // 100000) + "L" if emi_val >= 100000 else str(emi_val // 1000) + "K")
                tl_svg_blocks += f'<text x="{x + cell_w//2}" y="67" font-size="7.5" fill="#0E5A2D" font-weight="600" text-anchor="middle" font-family="Inter,sans-serif">{emi_str} due</text>\n'
            
        # ==========================================
        # REAL DATABRICKS DBRX-INSTRUCT INTEGRATION
        # ==========================================
        import requests
        import json
        
        token = os.environ.get("DATABRICKS_TOKEN")
        host = os.environ.get("DATABRICKS_HOST")
        
        # Default mock values if running locally without Databricks env vars
        rationale = f"Profile exhibits high alternative data density. A continuous {telecom}-month telecom payment history indicates reliable liquidity. ML Lending Limit calculated at ₹{recommended_limit:,.0f} with an approval confidence of {limit_percentage}%."
        
        if token and host:
            prompt = f"The applicant has {telecom} months of telecom history, {fastag} FASTag trips, {pm_kisan} PM-Kisan subsidies, and {upi} UPI transactions/month. The system decision is {'APPROVED' if is_approved else 'REJECTED'} with an ML-predicted safe lending limit of ₹{recommended_limit:,.0f} and an approval confidence of {limit_percentage}%. Write a 2-3 sentence professional underwriting rationale explaining this decision and explicitly mentioning the recommended ₹ limit and confidence percentage. Language required: {selected_language}."
            
            system_prompt = f"You are a professional banking underwriter. Return only the professional rationale text. Do not include any formatting, markdown, or JSON. Just the plain text in the requested language."
            
            url = f"https://{host.replace('https://', '')}/serving-endpoints/databricks-dbrx-instruct/invocations"
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            data = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 200,
                "temperature": 0.3
            }
            try:
                resp = requests.post(url, headers=headers, json=data, timeout=10)
                if resp.status_code == 200:
                    rationale = resp.json()["choices"][0]["message"]["content"].strip()
                else:
                    rationale = f"DBRX API Error {resp.status_code}: {resp.text}"
            except Exception as e:
                rationale = f"Databricks Connection Error: {str(e)}"
        else:
            # Fallback to local hardcoded if not deployed on Databricks Apps
            if is_approved:
                approved_map = {
                    "Hindi": f"आवेदक का डिजिटल फुटप्रिंट मजबूत है। {telecom} महीने का टेलीकॉम डेटा और {fastag} फास्टैग लॉग्स एक स्थिर आय का संकेत देते हैं। कृषि ऋण स्वीकृति की सिफारिश की जाती है।",
                    "Tamil": f"விண்ணப்பதாரரின் டிஜிட்டல் தடம் வலுவாக உள்ளது. {telecom} மாத தொலைத்தொடர்பு தரவு மற்றும் {fastag} ஃபாஸ்டேக் பதிவுகள் நிலையான வருமானத்தை குறிக்கின்றன. விவசாய கடன் ஒப்புதல் பரிந்துரைக்கப்படுகிறது.",
                    "Telugu": f"దరఖాస్తుదారు డిజిటల్ ఫుట్‌ప్రింట్ బలంగా ఉంది. {telecom} నెలల టెలికాం డేటా మరియు {fastag} ఫాస్టాగ్ లాగ్‌లు స్థిరమైన ఆదాయాన్ని సూచిస్తాయి. వ్యవసాయ రుణ ఆమోదం సిఫార్సు చేయబడింది.",
                    "Marathi": f"अर्जदाराचा डिजिटल फूटप्रिंट मजबूत आहे. {telecom} महिन्यांचा टेलिकॉम डेटा आणि {fastag} फास्टॅग नोंदी स्थिर उत्पन्नाचे संकेत देतात. कृषी कर्ज मंजुरीची शिफारस केली जाते.",
                    "Bengali": f"আবেদনকারীর ডিজিটাল ফুটপ্রিন্ট শক্তিশালী। {telecom} মাসের টেলিকম ডেটা এবং {fastag} ফাস্ট্যাগ লগ একটি স্থিতিশীল আয়ের ইঙ্গিত দেয়। কৃষি ঋণ অনুমোদনের সুপারিশ করা হচ্ছে।",
                    "Gujarati": f"અરજદારની ડિજિટલ ફૂટપ્રિન્ટ મજબૂત છે. {telecom} મહિનાનો ટેલિકોમ ડેટા અને {fastag} ફાસ્ટેગ લોગ સ્થિર આવક સૂચવે છે. કૃષિ લોન મંજૂરીની ભલામણ કરવામાં આવે છે.",
                    "Kannada": f"ಅರ್ಜಿದಾರರ ಡಿಜಿಟಲ್ ಹೆಜ್ಜೆಗುರುತು ಪ್ರಬಲವಾಗಿದೆ. {telecom} ತಿಂಗಳ ಟೆಲಿಕಾಂ ಡೇಟಾ ಮತ್ತು {fastag} ಫಾಸ್ಟ್‌ಟ್ಯಾಗ್ ಲಾಗ್‌ಗಳು ಸ್ಥಿರ ಆದಾಯವನ್ನು ಸೂಚಿಸುತ್ತವೆ. ಕೃಷಿ ಸಾಲ ಮಂಜೂರಾತಿಯನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ.",
                    "Malayalam": f"അപേക്ഷകന്റെ ഡിജിറ്റൽ ഫുട്പ്രിന്റ് ശക്തമാണ്. {telecom} മാസത്തെ ടെലികോം ഡാറ്റയും {fastag} ഫാസ്ടാഗ് ലോഗുകളും സുസ്ഥിര വരുമാനത്തെ സൂചിപ്പിക്കുന്നു. കാർഷിക വായ്പ അംഗീകാരം ശുപാർശ ചെയ്യുന്നു.",
                    "Punjabi": f"ਬਿਨੈਕਾਰ ਦਾ ਡਿਜੀਟਲ ਫੁੱਟਪ੍ਰਿੰਟ ਮਜ਼ਬੂਤ ​​ਹੈ। {telecom} ਮਹੀਨਿਆਂ ਦਾ ਟੈਲੀਕਾਮ ਡੇਟਾ ਅਤੇ {fastag} ਫਾਸਟੈਗ ਲੌਗ ਸਥਿਰ ਆਮਦਨ ਨੂੰ ਦਰਸਾਉਂਦੇ ਹਨ। ਖੇਤੀਬਾੜੀ ਕਰਜ਼ੇ ਦੀ ਮਨਜ਼ੂਰੀ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ।",
                    "Odia": f"ଆବେଦନକାରୀଙ୍କ ଡିଜିଟାଲ୍ ଫୁଟପ୍ରିଣ୍ଟ ଶକ୍ତିଶାଳୀ ଅଟେ। {telecom} ମାସର ଟେଲିକମ୍ ଡାଟା ଏବଂ {fastag} ଫାଷ୍ଟାଗ୍ ଲଗ୍ ସ୍ଥିର ଆୟର ସୂଚନା ଦେଇଥାଏ | କୃଷି ଋଣ ଅନୁମୋଦନ ସୁପାରିଶ କରାଯାଇଛି |",
                    "Assamese": f"আবেদনকাৰীৰ ডিজিটেল ফুটপ্ৰিণ্ট শক্তিশালী। {telecom} মাহৰ টেলিকম ডেটা আৰু {fastag} ফাষ্টেগ লগে সুস্থিৰ উপাৰ্জনৰ ইংগিত দিয়ে। কৃষি ঋণ অনুমোদনৰ পৰামৰ্শ দিয়া হৈছে।",
                    "Bodo": f"आबेदनगिरिनि डिजिटल फुटप्रिन्ट गोख्रों। {telecom} दाननि टेलिकम डाटा आरो {fastag} फास्टेग लगआ थिरां आय फोरमायो। आबाद लोन गनायथिनि सिफारिस खालामनाय जाबाय।",
                    "Dogri": f"अर्जदार दा डिजिटल फुटप्रिंट मजबूत ऐ। {telecom} म्हीने दा टेलीकॉम डेटा ते {fastag} फास्टैग लॉग स्थिर आमदनी दा संकेत दिंदे न। कृषि कर्ज मंजूरी दी सिफारिश कीती जंदी ऐ।",
                    "Kashmiri": f"درخواست دِوَنوٲلِس چُھ ڈیجیٹل فُٹ پرنٹ مَضبوٗط۔ {telecom} رؠتَن ہُنٛد ٹیلی کام ڈاٹا تہٕ {fastag} فاسٹیگ لاگ چھِ مُستقل آمدنی ہُنٛد اِشارٕ دِوان۔ زَرعی قَرٕز مَنظوٗری ہِنٛز سِفارِش چھِ یِوان کَرنہٕ۔",
                    "Konkani": f"अर्जदाराचो डिजिटल फूटप्रिंट घटसाण आसा. {telecom} म्हयन्यांचो टेलिकॉम डेटा आनी {fastag} फास्टॅग लॉग थीर उत्पन्नाचो संकेत दितात. कृषी रीण मंजुरीची शिफारस केल्ली आसा.",
                    "Maithili": f"आवेदकक डिजिटल फुटप्रिंट मजबूत अछि। {telecom} महिना धरिक टेलीकॉम डेटा आ {fastag} फास्टैग लॉग स्थिर आयक संकेत दैत अछि। कृषि ऋण स्वीकृति केर सिफारिश कएल जाइत अछि।",
                    "Manipuri": f"এপ্লিকেণ্টকী দিজিতেল ফুতপ্রিন্ত মপাঙ্গল কনবা অমা লৈ। থা {telecom}গী তেলিকোম দেতা অমসুং ফাস্তেগ লোগ {fastag}না লেপ্পা লৈতবা ইনকমগী খুদম পীরি। লৌউ-শিংউগী লোন অয়াবা পীনবা রিকমেন্দ তৌরি।",
                    "Nepali": f"आवेदकको डिजिटल फुटप्रिन्ट बलियो छ। {telecom} महिनाको टेलिकम डाटा र {fastag} फास्ट्याग लगहरूले स्थिर आम्दानीको संकेत दिन्छन्। कृषि ऋण स्वीकृतिको सिफारिस गरिन्छ।",
                    "Sanskrit": f"आवेदकस्य डिजिटल-फुटप्रिन्ट् दृढम् अस्ति। {telecom} मासानां टेलिकॉम-दत्तांशः {fastag} फास्टैग-लॉग् च स्थिर-आयस्य सङ्केतं यच्छन्ति। कृषि-ऋण-स्वीकृतेः शिफारशः क्रियते।",
                    "Santali": f"ᱟᱵᱮᱫᱚᱱᱠᱟᱨᱤᱭᱟᱜ ᱰᱤᱡᱤᱴᱟᱞ ᱯᱷᱩᱴᱯᱨᱤᱱᱴ ᱠᱮᱴᱮᱡ ᱜᱮᱭᱟ᱾ {telecom} ᱪᱟᱸᱫᱚ ᱨᱮᱭᱟᱜ ᱴᱮᱞᱤᱠᱚᱢ ᱰᱮᱴᱟ ᱟᱨ {fastag} ᱯᱷᱟᱥᱴᱮᱜᱽ ᱞᱚᱜᱽ ᱛᱷᱤᱨ ᱟᱨᱡᱟᱣ ᱨᱮᱭᱟᱜ ᱤᱥᱟᱨᱟ ᱮᱢᱮᱫᱼᱟ᱾ ᱪᱟᱥ ᱨᱤᱱ ᱮᱢᱚᱜ ᱨᱮᱭᱟᱜ ᱥᱤᱯᱷᱟᱨᱤᱥ ᱦᱩᱭᱩᱜ ᱠᱟᱱᱟ᱾",
                    "Sindhi": f"درخواست ڏيندڙ جو ڊجيٽل فوٽ پرنٽ مضبوط آهي. {telecom} مهينن جو ٽيليڪام ڊيٽا ۽ {fastag} فاسٽيگ لاگ مستحڪم آمدني جو اشارو ڏين ٿا. زرعي قرض جي منظوري جي سفارش ڪئي وئي آهي.",
                    "Urdu": f"درخواست دہندہ کا ڈیجیٹل فٹ پرنٹ مضبوط ہے۔ {telecom} ماہ کا ٹیلی کام ڈیٹا اور {fastag} فاسٹیگ لاگز مستحکم آمدنی کی نشاندہی کرتے ہیں۔ زرعی قرض کی منظوری کی سفارش کی جاتی ہے۔"
                }
                rationale = approved_map.get(selected_language, f"Profile exhibits high alternative data density. A continuous {telecom}-month telecom payment history indicates reliable liquidity. Databricks ML recommends a maximum lending limit of ₹{recommended_limit:,.0f} with a {limit_percentage}% approval confidence based on positive transport and payment logs.")
            else:
                rejected_map = {
                    "Hindi": f"डेटा घनत्व कम है। केवल {telecom} महीने का रिकॉर्ड प्राप्त हुआ है, जो स्वचालित स्वीकृति के लिए अपर्याप्त है। भौतिक क्षेत्र सत्यापन आवश्यक है।",
                    "Tamil": f"தரவு அடர்த்தி குறைவாக உள்ளது. {telecom} மாத பதிவு மட்டுமே பெறப்பட்டுள்ளது, இது தானியங்கி ஒப்புதலுக்கு போதுமானதாக இல்லை. உடல் கள சரிபார்ப்பு அவசியம்.",
                    "Telugu": f"డేటా సాంద్రత తక్కువగా ఉంది. {telecom} నెలల రికార్డ్ మాత్రమే స్వీకరించబడింది, ఇది స్వయంచాలక ఆమోదానికి సరిపోదు. భౌతిక క్షేత్ర ధృవీకరణ అవసరం.",
                    "Marathi": f"डेटा घनता कमी आहे. केवळ {telecom} महिन्यांचा रेकॉर्ड प्राप्त झाला आहे, जो स्वयंचलित मंजुरीसाठी अपुरा आहे. भौतिक क्षेत्र पडताळणी आवश्यक आहे.",
                    "Bengali": f"ডেটার ঘনত্ব কম। মাত্র {telecom} মাসের রেকর্ড পাওয়া গেছে, যা স্বয়ংক্রিয় অনুমোদনের জন্য অপর্যাপ্ত। ম্যানুয়াল যাচাইকরণ প্রয়োজন।",
                    "Gujarati": f"ડેટા ઘનતા ઓછી છે. માત્ર {telecom} મહિનાનો રેકોર્ડ પ્રાપ્ત થયો છે, જે સ્વચાલિત મંજૂરી માટે અપૂરતો છે. ભૌતિક ક્ષેત્રની ચકાસણી જરૂરી છે.",
                    "Kannada": f"ಡೇಟಾ ಸಾಂದ್ರತೆ ಕಡಿಮೆಯಾಗಿದೆ. ಕೇವಲ {telecom} ತಿಂಗಳ ದಾಖಲೆಯನ್ನು ಮಾತ್ರ ಸ್ವೀಕರಿಸಲಾಗಿದೆ, ಇದು ಸ್ವಯಂಚಾಲಿತ ಅನುಮೋದನೆಗೆ ಸಾಕಾಗುವುದಿಲ್ಲ. ಭೌತಿಕ ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ.",
                    "Malayalam": f"ഡാറ്റാ സാന്ദ്രത കുറവാണ്. {telecom} മാസത്തെ റെക്കോർഡ് മാത്രമേ ലഭിച്ചിട്ടുള്ളൂ, ഇത് സ്വയമേവയുള്ള അംഗീകാരത്തിന് പര്യാപ്തമല്ല. നേരിട്ടുള്ള പരിശോധന ആവശ്യമാണ്.",
                    "Punjabi": f"ਡਾਟਾ ਘਣਤਾ ਘੱਟ ਹੈ। ਸਿਰਫ਼ {telecom} ਮਹੀਨਿਆਂ ਦਾ ਰਿਕਾਰਡ ਪ੍ਰਾਪਤ ਹੋਇਆ ਹੈ, ਜੋ ਆਟੋਮੈਟਿਕ ਮਨਜ਼ੂਰੀ ਲਈ ਨਾਕਾਫ਼ੀ ਹੈ। ਦਸਤੀ ਤਸਦੀਕ ਦੀ ਲੋੜ ਹੈ।",
                    "Odia": f"ଡାଟା ସାନ୍ଦ୍ରତା କମ୍ ଅଟେ | କେବଳ {telecom} ମାସର ରେକର୍ଡ ଗ୍ରହଣ କରାଯାଇଛି, ଯାହାକି ସ୍ୱୟଂଚାଳିତ ଅନୁମୋଦନ ପାଇଁ ପର୍ଯ୍ୟାପ୍ତ ନୁହେଁ | ମାନୁଆଲ ଯାଞ୍ଚ ଆବଶ୍ୟକ |",
                    "Assamese": f"ডেটাৰ ঘনত্ব কম। মাত্ৰ {telecom} মাহৰ ৰেকৰ্ড পোৱা গৈছে, যি স্বয়ংক্ৰিয় অনুমোদনৰ বাবে অপৰ্যাপ্ত। মেনুৱেল পৰীক্ষাৰ প্ৰয়োজন।",
                    "Bodo": f"डाटा घनत्व खम। खालि {telecom} दाननि रेकर्ड मोननाय जादों, जाय गावनोगाव गनायथिनि थाखाय थोजासे नङा। मेनुयेल आनजाद गोनांथि दं।",
                    "Dogri": f"डेटा घनत्व घट्ट ऐ। सिर्फ {telecom} म्हीने दा रिकॉर्ड हासल होया ऐ, जड़ा स्वचालित मंजूरी लेई अपर्याप्त ऐ। मैनुअल जांच जरूरी ऐ।",
                    "Kashmiri": f"ڈاٹا گَھنَتو چُھ کَم۔ صِرِف {telecom} رؠتَن ہُنٛد رِکارڈ چُھ مِلیومُت، یُس آٹوٗمیٹِک مَنظوٗری خٲطرٕ ناكافی چُھ۔ مینوٗئل تَصدیٖق چُھ ضۆروٗری۔",
                    "Konkani": f"डेटा घनताय उणी आसा. फकत {telecom} म्हयन्यांचो रेकॉर्ड मेळ्ळा, जो स्वयंचलित मंजुरी खातीर अपुरो आसा. मॅन्युअल तपासणीची गरज आसा.",
                    "Maithili": f"डेटा घनत्व कम अछि। मात्र {telecom} महिना धरिक रिकॉर्ड प्राप्त भेल अछि, जे स्वचालित स्वीकृति लेल अपर्याप्त अछि। मैनुअल सत्यापनक आवश्यकता अछि.",
                    "Manipuri": f"দেতা দেন্সিতি য়াম্না নেম্মী। থা {telecom}খক্কী রেকোর্দ খক্তমক ফংলে, মসি ওতোমেতিক অয়াবা পীনবা মতিক চাদে। মেনুয়েল ওইনা য়েংশিনবা মথৌ তাই।",
                    "Nepali": f"डाटा घनत्व कम छ। मात्र {telecom} महिनाको रेकर्ड प्राप्त भएको छ, जुन स्वचालित स्वीकृतिको लागि अपर्याप्त छ। म्यानुअल प्रमाणिकरण आवश्यक छ।",
                    "Sanskrit": f"दत्तांश-घनत्वं न्यूनम् अस्ति। केवलं {telecom} मासानां अभिलेखः प्राप्तः, यत् स्वचालित-स्वीकृत्यै अपर्याप्तम् अस्ति। हस्तचालित-सत्यापनम् आवश्यकम्।",
                    "Santali": f"ᱰᱮᱴᱟ ᱰᱮᱱᱥᱤᱴᱤ ᱠᱚᱢ ᱜᱮᱭᱟ᱾ ᱠᱷᱟᱹᱞᱤ {telecom} ᱪᱟᱸᱫᱚ ᱨᱮᱭᱟᱜ ᱨᱮᱠᱚᱨᱰ ᱧᱟᱢ ᱟᱠᱟᱱᱟ, ᱡᱟᱦᱟᱸ ᱫᱚ ᱚᱴᱚᱢᱮᱴᱤᱠ ᱮᱯᱨᱩᱵᱷᱟᱞ ᱞᱟᱹᱜᱤᱫ ᱵᱟᱝ ᱯᱩᱨᱟᱹᱜᱼᱟ᱾ ᱢᱮᱱᱩᱣᱮᱞ ᱵᱷᱮᱨᱤᱯᱷᱤᱠᱮᱥᱚᱱ ᱞᱟᱹᱠᱛᱤᱭᱟ᱾",
                    "Sindhi": f"ڊيٽا جي کثافت گھٽ آھي. صرف {telecom} مهينن جو رڪارڊ مليو آهي، جيڪو خودڪار منظوري لاءِ ڪافي نه آهي. دستي تصديق جي ضرورت آهي.",
                    "Urdu": f"ڈیٹا کی کثافت کم ہے۔ صرف {telecom} ماہ کا ریکارڈ موصول ہوا ہے، جو خودکار منظوری کے لیے ناکافی ہے۔ دستی تصدیق درکار ہے۔"
                }
                rationale = rejected_map.get(selected_language, f"Profile lacks sufficient digital footprint density. Minimal {telecom}-month telecom history and low transport data fail to establish a baseline for proxy income assessment. ML prediction sets limit to ₹0 with a {limit_percentage}% approval confidence. Proceed to manual KYC.")

        # ==========================================
        # SARVAM AI TEXT-TO-SPEECH INTEGRATION
        # ==========================================
        sarvam_audio_base64 = ""
        sarvam_api_key = os.environ.get("SARVAM_API_KEY")
        
        sarvam_lang_map = {
            "English": "en-IN",
            "Hindi": "hi-IN",
            "Tamil": "ta-IN",
            "Telugu": "te-IN",
            "Marathi": "mr-IN",
            "Bengali": "bn-IN",
            "Gujarati": "gu-IN",
            "Kannada": "kn-IN",
            "Malayalam": "ml-IN",
            "Punjabi": "pa-IN",
            "Odia": "or-IN"
        }
        
        target_lang = sarvam_lang_map.get(selected_language)
        
        if sarvam_api_key and target_lang and rationale:
            sarvam_url = "https://api.sarvam.ai/text-to-speech"
            payload = {
                "inputs": [rationale],
                "target_language_code": target_lang,
                "speaker": "meera",
                "pitch": 0,
                "pace": 1.0,
                "loudness": 1.0,
                "speech_sample_rate": 8000,
                "enable_preprocessing": True,
                "model": "bulbul:v1"
            }
            headers = {
                "api-subscription-key": sarvam_api_key,
                "Content-Type": "application/json"
            }
            
            try:
                tts_resp = requests.post(sarvam_url, json=payload, headers=headers, timeout=10)
                if tts_resp.status_code == 200:
                    data = tts_resp.json()
                    sarvam_audio_base64 = data.get("audios", [""])[0] if "audios" in data else data.get("audio_base64", "")
            except Exception as e:
                pass

        html_dashboard = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/lucide@latest"></script>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
            <style>
                body {{ 
                    font-family: 'Inter', sans-serif; 
                    background-color: #E8E4D8; 
                    color: #4A2E1E; 
                    margin: 0; 
                    scroll-behavior: smooth; 
                    background-image: radial-gradient(circle, #D6D0C4 1px, transparent 1px); 
                    background-size: 20px 20px;
                }}
                .dot-grid {{ 
                    background-color: #F0ECE1; 
                    background-image: radial-gradient(circle, #E0DBCF 1px, transparent 1px); 
                    background-size: 20px 20px; 
                }}
                @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(15px); }} to {{ opacity: 1; transform: translateY(0); }} }}
                @keyframes fadeLeft {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: translateX(0); }} }}
                @keyframes drawCircle {{ from {{ stroke-dashoffset: 351.8; }} to {{ stroke-dashoffset: {351.8 - (351.8 * score / 900)}; }} }}
                @keyframes pulseGlow {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
                @keyframes ping {{ 0% {{ transform: scale(1); opacity: 1; }} 75%, 100% {{ transform: scale(2); opacity: 0; }} }}
                @keyframes shimmerText {{ 0% {{ background-position: -200% center; }} 100% {{ background-position: 200% center; }} }}
                @keyframes countUp {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
                @keyframes borderPulse {{ 0%, 100% {{ border-color: #D6D0C4; }} 50% {{ border-color: rgba(14,90,45,0.15); }} }}
                @keyframes scaleX {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
                @keyframes floatUp {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-3px); }} }}
                @keyframes glowEdge {{ 0%, 100% {{ box-shadow: 0 0 0 0 rgba(14,90,45,0); }} 50% {{ box-shadow: 0 0 28px 0 rgba(14,90,45,0.06), 0 0 0 1px rgba(14,90,45,0.08); }} }}
                @keyframes tagPop {{ 0% {{ opacity:0; transform: scale(0.85); }} 60% {{ transform: scale(1.05); }} 100% {{ opacity:1; transform: scale(1); }} }}
                @keyframes shimmerSweep {{ 0% {{ background-position: -200% 0; }} 100% {{ background-position: 200% 0; }} }}
                @keyframes iconBob {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
                @keyframes scoreSpring {{ 0% {{ opacity:0; transform: scale(0.5) translateY(10px); }} 70% {{ transform: scale(1.08) translateY(-2px); }} 100% {{ opacity:1; transform: scale(1) translateY(0); }} }}
                @keyframes accentLine {{ from {{ transform: scaleX(0); opacity:0; }} to {{ transform: scaleX(1); opacity:1; }} }}
                .animate-fade-up {{ animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; }}
                .animate-fade-left {{ animation: fadeLeft 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; }}
                .delay-50 {{ animation-delay: 50ms; }}
                .delay-100 {{ animation-delay: 100ms; }}
                .delay-150 {{ animation-delay: 150ms; }}
                .delay-200 {{ animation-delay: 200ms; }}
                .delay-250 {{ animation-delay: 250ms; }}
                .delay-300 {{ animation-delay: 300ms; }}
                .delay-350 {{ animation-delay: 350ms; }}
                .delay-400 {{ animation-delay: 400ms; }}
                .delay-500 {{ animation-delay: 500ms; }}
                .pulse-indicator {{ animation: pulseGlow 2s ease-in-out infinite; }}
                .ping-dot {{ position: relative; }}
                .ping-dot::before {{ content: ''; position: absolute; inset: 0; border-radius: 50%; background: #0E5A2D; animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite; }}
                .score-glow {{ border-radius: 50%; transition: all 0.3s ease; }}
                .animate-scale-x {{ animation: scaleX 1s cubic-bezier(0.16, 1, 0.3, 1) forwards; transform: scaleX(0); transform-origin: left; }}
                .score-count {{ animation: scoreSpring 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; animation-delay: 600ms; opacity: 0; }}
                .border-pulse {{ animation: borderPulse 3s ease-in-out infinite; }}
                .shimmer-row {{ background: linear-gradient(90deg, transparent 0%, rgba(122,116,40,0.04) 50%, transparent 100%); background-size: 200% 100%; animation: shimmerText 3s linear infinite; }}
                .card-glow {{ animation: glowEdge 4s ease-in-out infinite; }}
                .tag-pop {{ animation: tagPop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both; }}
                .icon-bob {{ animation: iconBob 3s ease-in-out infinite; }}
                .float-card {{ animation: floatUp 5s ease-in-out infinite; }}
                /* Gradient progress bars — earthy */
                .bar-gradient-green {{ background: linear-gradient(90deg, #083D1A, #0E5A2D, #2D7A4A); }}
                .bar-gradient-amber {{ background: linear-gradient(90deg, #5C3A1A, #9A5A33, #C4834D); }}
                /* Icon hover */
                [data-lucide]:hover {{ transform: rotate(12deg) scale(1.15); transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); }}
                /* Row hover removed to prevent blur */
                /* Header shimmer badge */
                .shimmer-badge {{ background: linear-gradient(90deg, #EAE5D9 0%, #E8E4D8 50%, #EAE5D9 100%); background-size: 200% 100%; animation: shimmerSweep 2.5s linear infinite; }}
                /* Accent underline on section headers */
                .section-title-accent {{ position: relative; }}
                .section-title-accent::after {{
                    content: '';
                    position: absolute;
                    bottom: -4px; left: 0;
                    width: 24px; height: 2px;
                    background: #0E5A2D;
                    animation: accentLine 0.6s ease 400ms both;
                    transform-origin: left;
                }}
                /* Score ring hover glow removed */
            </style>
        </head>
        <body>
            <div class="border border-[#D6D0C4] rounded-xl overflow-hidden flex flex-col w-full shadow-lg card-glow dot-grid" style="position:relative;">
                
                <!-- Card Header -->
                <div class="px-6 py-4 border-b border-[#D6D0C4] flex justify-between items-center bg-[#EAE5D9] animate-fade-up" style="position:relative;">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded bg-[#E5E0D3] border border-[#D6D0C4] flex items-center justify-center text-[#4A2E1E] font-medium text-sm">
                            {applicant_id[-2:]}
                        </div>
                        <div>
                            <h2 class="text-sm font-semibold text-[#4A2E1E] leading-none">{applicant_id}</h2>
                            <p class="text-[10px] text-[#7A7428] mt-1 uppercase tracking-widest font-medium">AgriStack Verified Profile</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="inline-flex items-center gap-1.5 rounded bg-[#E8F5ED] border border-[#C8E0D0] px-2 py-0.5 text-[10px] font-medium text-[#0E5A2D] shimmer-badge tag-pop" style="animation-delay:300ms;">
                            <i data-lucide="shield-check" class="w-3 h-3 text-[#0E5A2D]"></i> ID Verified
                        </span>
                        {tier_badge}
                    </div>
                </div>
                
                <!-- 3-Column Grid: Farmer Profile | AutoML Score | Risk Radar -->
                <div class="grid grid-cols-3 divide-x divide-[#D6D0C4]">
                    
                    <!-- Column 1: Farmer Profile -->
                    <div class="p-6 relative" style="animation: fadeUp 0.6s cubic-bezier(0.16,1,0.3,1) 80ms both;">
                        <h3 class="text-[10px] font-semibold text-[#7A7428] uppercase tracking-widest mb-5 flex items-center gap-2 section-title-accent" style="animation: fadeUp 0.5s ease 150ms both;">
                            <i data-lucide="user" class="w-3 h-3"></i> Farmer Profile
                        </h3>
                        <dl class="space-y-2">
                            <div class="flex justify-between items-center group hover:bg-[#EAE5D9] p-2 -mx-2 rounded-lg transition-colors duration-200 cursor-default" style="animation: fadeUp 0.45s ease 190ms both;">
                                <dt class="text-xs text-[#6B5D4F] group-hover:text-[#4A2E1E] transition-colors flex items-center gap-2"><i data-lucide="map" class="w-3.5 h-3.5 text-[#9A8B7A] group-hover:text-[#0E5A2D] transition-colors"></i> Land Holding</dt>
                                <dd class="text-xs font-medium text-[#4A2E1E] bg-[#E5E0D3] group-hover:bg-[#E8E4D8] border border-[#D6D0C4] px-1.5 py-0.5 rounded transition-colors">{land_area:.2f} HA</dd>
                            </div>
                            <div class="flex justify-between items-center group hover:bg-[#EAE5D9] p-2 -mx-2 rounded-lg transition-colors duration-200 cursor-default" style="animation: fadeUp 0.45s ease 240ms both;">
                                <dt class="text-xs text-[#6B5D4F] group-hover:text-[#4A2E1E] transition-colors flex items-center gap-2"><i data-lucide="fingerprint" class="w-3.5 h-3.5 text-[#9A8B7A] group-hover:text-[#0E5A2D] transition-colors"></i> Aadhaar eKYC</dt>
                                <dd class="text-[10px] font-medium {'text-[#0E5A2D]' if aadhaar else 'text-[#9A5A33]'} bg-[#E5E0D3] group-hover:bg-[#E8E4D8] border border-[#D6D0C4] px-1.5 py-0.5 rounded uppercase tracking-wider transition-colors">{'Verified' if aadhaar else 'Pending'}</dd>
                            </div>
                            <div class="flex justify-between items-center group hover:bg-[#EAE5D9] p-2 -mx-2 rounded-lg transition-colors duration-200 cursor-default" style="animation: fadeUp 0.45s ease 290ms both;">
                                <dt class="text-xs text-[#6B5D4F] group-hover:text-[#4A2E1E] transition-colors flex items-center gap-2"><i data-lucide="sprout" class="w-3.5 h-3.5 text-[#9A8B7A] group-hover:text-[#0E5A2D] transition-colors"></i> AgriStack ID</dt>
                                <dd class="text-[10px] font-medium {'text-[#0E5A2D]' if agristack else 'text-[#9A5A33]'} bg-[#E5E0D3] group-hover:bg-[#E8E4D8] border border-[#D6D0C4] px-1.5 py-0.5 rounded uppercase tracking-wider transition-colors">{'Linked' if agristack else 'Unlinked'}</dd>
                            </div>
                            <div class="flex justify-between items-center group hover:bg-[#EAE5D9] p-2 -mx-2 rounded-lg transition-colors duration-200 cursor-default" style="animation: fadeUp 0.45s ease 340ms both;">
                                <dt class="text-xs text-[#6B5D4F] group-hover:text-[#4A2E1E] transition-colors flex items-center gap-2"><i data-lucide="shield" class="w-3.5 h-3.5 text-[#9A8B7A] group-hover:text-[#0E5A2D] transition-colors"></i> PMFBY Insurance</dt>
                                <dd class="text-[10px] font-medium {'text-[#0E5A2D]' if pmfby else 'text-[#9A5A33]'} bg-[#E5E0D3] group-hover:bg-[#E8E4D8] border border-[#D6D0C4] px-1.5 py-0.5 rounded uppercase tracking-wider transition-colors">{'Active' if pmfby else 'Inactive'}</dd>
                            </div>
                            <div class="flex justify-between items-center group hover:bg-[#EAE5D9] p-2 -mx-2 rounded-lg transition-colors duration-200 cursor-default" style="animation: fadeUp 0.45s ease 390ms both;">
                                <dt class="text-xs text-[#6B5D4F] group-hover:text-[#4A2E1E] transition-colors flex items-center gap-2"><i data-lucide="signal" class="w-3.5 h-3.5 text-[#9A8B7A] group-hover:text-[#0E5A2D] transition-colors"></i> Telecom Streak</dt>
                                <dd class="text-xs font-medium text-[#4A2E1E] bg-[#E5E0D3] group-hover:bg-[#E8E4D8] border border-[#D6D0C4] px-1.5 py-0.5 rounded transition-colors">{telecom} mo.</dd>
                            </div>
                            <div class="flex justify-between items-center group hover:bg-[#EAE5D9] p-2 -mx-2 rounded-lg transition-colors duration-200 cursor-default" style="animation: fadeUp 0.45s ease 440ms both;">
                                <dt class="text-xs text-[#6B5D4F] group-hover:text-[#4A2E1E] transition-colors flex items-center gap-2"><i data-lucide="truck" class="w-3.5 h-3.5 text-[#9A8B7A] group-hover:text-[#0E5A2D] transition-colors"></i> FASTag Trips</dt>
                                <dd class="text-xs font-medium text-[#4A2E1E] bg-[#E5E0D3] group-hover:bg-[#E8E4D8] border border-[#D6D0C4] px-1.5 py-0.5 rounded transition-colors">{fastag} trips</dd>
                            </div>
                        </dl>
                        
                        <div class="mt-6 pt-5 border-t border-[#D6D0C4]">
                            <div class="flex items-center justify-between mb-4">
                                <h3 class="text-[10px] font-semibold text-[#7A7428] uppercase tracking-widest flex items-center gap-2">
                                    <i data-lucide="bar-chart-3" class="w-3 h-3"></i> 6M UPI Cash Flow
                                </h3>
                                <span class="text-[9px] font-medium text-[#7A7428] bg-[#E5E0D3] px-1.5 py-0.5 rounded">Avg: ₹{upi_avg_inr_val:,.0f}</span>
                            </div>
                            <div class="flex justify-center w-full">
                                <svg width="{left_margin + (bar_width + bar_spacing) * 6}" height="{chart_height + 18}" viewBox="0 0 {left_margin + (bar_width + bar_spacing) * 6} {chart_height + 18}">
                                    {svg_bars}
                                </svg>
                            </div>
                        </div>
                    </div>

                    <!-- Column 2: Trust Score -->
                    <div class="p-6 flex flex-col items-center justify-center relative animate-fade-up delay-200">
                        <h3 class="absolute top-6 left-6 text-[10px] font-semibold text-[#7A7428] uppercase tracking-widest flex items-center gap-2 section-title-accent">
                            <i data-lucide="activity" class="w-3 h-3"></i> AutoML Score
                        </h3>
                        
                        <div class="mt-4 relative flex items-center justify-center">
                            <div class="score-glow">
                                <svg class="w-32 h-32 transform -rotate-90">
                                    <circle cx="64" cy="64" r="56" fill="none" stroke="#E0DBCF" stroke-width="6"></circle>
                                    <circle cx="64" cy="64" r="56" fill="none" stroke="{score_color_hex}" stroke-width="6" stroke-dasharray="351.8" stroke-dashoffset="351.8" stroke-linecap="round" style="animation: drawCircle 1.2s cubic-bezier(0.65, 0, 0.35, 1) forwards; animation-delay: 400ms;"></circle>
                                </svg>
                            </div>
                            <div class="absolute flex flex-col items-center justify-center">
                                <span class="text-4xl font-semibold text-[#4A2E1E] tracking-tight score-count">{score}</span>
                                <span class="text-[9px] font-medium text-[#7A7428] mt-1 uppercase tracking-widest animate-fade-up delay-500">/ 900</span>
                            </div>
                        </div>
                        
                        <p class="text-[10px] text-[#7A7428] mt-5 text-center max-w-[180px] leading-relaxed">
                            Computed securely using <span class="text-[#4A2E1E] font-medium">Databricks AutoML</span>.
                        </p>
                        

                    </div>

                    <!-- Column 3: Risk Signal Radar -->
                    <div class="p-6 flex flex-col relative" style="animation: fadeUp 0.6s ease 280ms both;">
                        <h3 class="text-[10px] font-semibold text-[#7A7428] uppercase tracking-widest mb-4 flex items-center gap-2 section-title-accent">
                            <i data-lucide="radar" class="w-3 h-3"></i> Risk Signal Radar
                            <span class="ml-auto text-[9px] font-medium bg-[#F0ECE1] border border-[#D6D0C4] px-1.5 py-0.5 rounded flex items-center gap-1">
                                <span class="w-1 h-1 rounded-full bg-[#0E5A2D] pulse-indicator"></span> 5D
                            </span>
                        </h3>
                        <!-- Radar SVG -->
                        <div class="flex justify-center">
                            <svg width="190" height="175" viewBox="0 0 200 190">
                                {radar_grids}
                                {radar_axes}
                                {radar_fill}
                                {radar_dots}
                                {radar_labels}
                            </svg>
                        </div>
                        <!-- Signal Bars -->
                        <div class="mt-3 space-y-2">
                            {''.join(f'''<div class="flex items-center gap-2" style="animation: fadeUp 0.4s ease {750 + i*70}ms both;">
                                <span class="w-1.5 h-1.5 rounded-full flex-shrink-0" style="background:{label_colors[i]};"></span>
                                <span class="text-[9px] text-[#6B5D4F] w-16 flex-shrink-0">{signal_names[i]}</span>
                                <div class="flex-1 bg-[#E0DBCF] rounded-full h-1 overflow-hidden">
                                    <div style="width:{int(signal_vals[i]*100)}%; background:{label_colors[i]}; height:100%; border-radius:9999px; animation: scaleX 0.7s ease {820 + i*80}ms both; transform-origin:left;"></div>
                                </div>
                                <span class="text-[9px] text-[#7A7428] w-6 text-right">{int(signal_vals[i]*100)}%</span>
                            </div>''' for i, _ in enumerate(signal_names))}
                        </div>
                    </div>

                </div>
                <!-- END 3-col grid -->

                <!-- GenAI Analysis — Full Width Row -->
                <div class="border-t border-[#D6D0C4] p-6 relative" style="animation: fadeUp 0.6s ease 420ms both;">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-[10px] font-semibold text-[#7A7428] uppercase tracking-widest flex items-center gap-2">
                            <i data-lucide="cpu" class="w-3 h-3"></i> GenAI Analysis
                        </h3>
                        <span class="text-[9px] font-medium text-[#7A7428] bg-[#E5E0D3] border border-[#D6D0C4] px-1.5 py-0.5 rounded flex items-center gap-1.5">
                            <span class="w-1.5 h-1.5 rounded-full bg-[#0E5A2D] pulse-indicator"></span> databricks-dbrx-instruct
                        </span>
                    </div>
                    <div class="text-sm text-[#6B5D4F] leading-relaxed max-w-4xl" style="animation: fadeUp 0.5s ease 520ms both;">
                        {rationale}
                    </div>
                    <div class="mt-5 pt-4 border-t border-[#D6D0C4] flex items-center justify-between">
                        <div class="flex items-center gap-2 text-xs font-medium {decision_text_class}">
                            <i data-lucide="{decision_icon}" class="w-3.5 h-3.5"></i>
                            {decision_text}
                        </div>
                        <div class="flex items-center gap-4 text-[9px] text-[#7A7428]">
                            <span class="flex items-center gap-1.5"><i data-lucide="database" class="w-3 h-3"></i> Unity Catalog</span>
                            <span class="flex items-center gap-1.5"><i data-lucide="zap" class="w-3 h-3"></i> Databricks AutoML</span>
                        </div>
                    </div>
                    {f'''
                    <div class="mt-4 border-t border-[#D6D0C4] pt-4">
                        <div class="text-[10px] font-semibold text-[#7A7428] uppercase tracking-widest mb-2 flex items-center gap-2">
                            <i data-lucide="mic" class="w-3 h-3"></i> Voice Advisory (Sarvam AI)
                        </div>
                        <audio controls style="width: 100%; height: 32px;">
                            <source src="data:audio/wav;base64,{sarvam_audio_base64}" type="audio/wav">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                    ''' if sarvam_audio_base64 else ''}
                </div>
                
                <!-- Repayment Projection Timeline -->
                <div class="border-t border-[#D6D0C4] bg-[#EAE5D9] px-6 py-5" style="animation: fadeUp 0.6s ease 460ms both;">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-[10px] font-semibold text-[#7A7428] uppercase tracking-widest flex items-center gap-2">
                            <i data-lucide="calendar-range" class="w-3 h-3"></i> Repayment Projection — Crop Cycle Aligned
                        </h3>
                        <div class="flex items-center gap-4 text-[9px] text-[#7A7428]">
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-sm" style="background:#9A5A33;opacity:0.7;"></span>Sowing</span>
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-sm" style="background:#7A7428;opacity:0.7;"></span>Growing</span>
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-sm" style="background:#0E5A2D;opacity:0.7;"></span>Harvest + EMI Due</span>
                            <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-sm border border-[#0E5A2D]"></span>Today</span>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <svg width="{tl_w}" height="{tl_h}" viewBox="0 0 {tl_w} {tl_h}" style="width:100%;">
                            {tl_svg_blocks}
                        </svg>
                    </div>
                    <p class="text-[9px] text-[#9A8B7A] mt-2">EMI windows auto-synced to Kharif &amp; Rabi harvest cycles · Credit limit ₹{recommended_limit:,.0f} split 50/50 across seasons</p>
                </div>

                <!-- ML Credit Limit Prediction -->
                <div class="border-t border-[#D6D0C4] bg-[#EAE5D9] p-6 flex flex-col md:flex-row items-center justify-between animate-fade-up delay-400">
                    <div class="flex items-center gap-4 w-full md:w-1/2 mb-4 md:mb-0">
                        <div class="w-10 h-10 rounded bg-[#E5E0D3] border border-[#D6D0C4] flex items-center justify-center">
                            <i data-lucide="wallet" class="w-4 h-4 {limit_color}"></i>
                        </div>
                        <div>
                            <h3 class="text-[10px] font-semibold text-[#7A7428] uppercase tracking-widest flex items-center gap-2 mb-1">
                                ML Recommended Credit Limit
                            </h3>
                            <div class="flex items-baseline gap-2">
                                <span class="text-2xl font-bold {limit_color} tracking-tight">{limit_formatted}</span>
                                <span class="text-[9px] font-medium {limit_color} bg-[#F0ECE1] border border-[#D6D0C4] px-1.5 py-0.5 rounded uppercase tracking-wider">{limit_status}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="w-full md:w-1/2 flex flex-col justify-center pl-0 md:pl-6 border-l-0 md:border-l border-[#D6D0C4]">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-[9px] text-[#6B5D4F] uppercase tracking-widest flex items-center gap-1.5"><i data-lucide="shield-check" class="w-3 h-3 text-[#7A7428]"></i> Approval Confidence</span>
                            <span class="text-[10px] font-medium text-[#4A2E1E]">{limit_percentage}%</span>
                        </div>
                        <div class="w-full bg-[#E0DBCF] rounded-full h-2 border border-[#D6D0C4] overflow-hidden">
                            <div class="{'bar-gradient-green' if is_approved else 'bar-gradient-amber'} h-2 rounded-full animate-scale-x" style="width: {limit_percentage}%; animation-delay: 600ms;"></div>
                        </div>
                    </div>
                </div>
            </div>
            <script>
                lucide.createIcons();
            </script>
        </body>
        </html>
        """
        with ui_container:
            components.html(html_dashboard, height=1120, scrolling=False)
