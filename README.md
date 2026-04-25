**Krishi Command Center** is a high-performance, 100% native Databricks application designed to automate rural credit risk assessment. It eliminates traditional lending bottlenecks by using GenAI to analyze 1-million-row datasets in real-time.

---

## 🏗️ 100% Native Databricks Tech Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend UI** | **Streamlit (v1.32.0)** | Fast, Python-native interactive dashboard for loan officers. |
| **Hosting** | **Databricks Apps (Serverless)** | Secure, internal hosting within the Databricks perimeter. |
| **Data Engine** | **Databricks Delta Lake** | Optimized storage for 1M+ scoring records (`default.agri_credit_features_1m`). |
| **Compute** | **Databricks SQL Warehouse** | Decoupled compute for high-speed concurrent user lookups. |
| **AI Engine** | **Databricks AI Gateway** | Direct access to Foundation Model APIs (Llama 3 / DBRX) for underwriting. |

---

## 🛠️ Application Flow (Real-Time Pipeline)

1.  **User Input:** Loan officer enters a unique Farmer ID (e.g., ADHR-100042) into the Streamlit UI.
2.  **Secure Query:** Streamlit sends a `SELECT` query to the **Databricks SQL Warehouse** via the secure `databricks-sql-connector`.
3.  **Data Extraction:** The SQL Warehouse scans the 1-Million row **Delta Table**, returning weighted feature data (UPI, Assets, SHG history).
4.  **Prompt Construction:** The system injects this data into a specialized "Underwriter Prompt."
5.  **GenAI Underwriting:** The prompt hits the **Databricks AI Gateway**. The LLM applies rural risk logic and streams back a human-readable analysis.
6.  **Final Render:** The dashboard outputs the raw data (Left) and the AI Copilot Analysis (Right) simultaneously.

---

## 🚀 Deployment Guide

### 1. Data Preparation (Notebook)
Run `databricks_notebook.py` to generate the `default.agri_credit_features_1m` Delta Table. This ensures the backend exists.

### 2. Environment Variables
In your Databricks App settings, configure:
- `DATABRICKS_SERVER_HOSTNAME`: Your workspace URL.
- `DATABRICKS_HTTP_PATH`: The path to your SQL Warehouse.
- `DATABRICKS_TOKEN`: Your Personal Access Token.

### 3. Deploy Streamlit
1.  Upload `streamlit_app.py` to your Databricks Workspace.
2.  Click **"Apps"** in the sidebar → **"Create App"**.
3.  Point the App to `streamlit_app.py` and hit **Deploy**.

---

## ⚖️ Proprietary Scoring (35/25/20/20)
The underwriter calculates the **Agri-Trust Score** using four prioritized pillars:
- **35% - Repayment History:** Performance in SHG/FPO micro-loans.
- **25% - Financial Discipline:** UPI merchant transaction density and bill pay history.
- **20% - Asset Equity:** Land verification status and hectare valuation.
- **20% - Identity & Compliance:** Aadhaar eKYC and AgriStack ID linkage.

---

## 🛠️ Developer Info
- **Project:** KrishiCRED Command Center
- **Framework:** Databricks Mosaic AI & Streamlit
- **Model:** Llama 3 / DBRX via Databricks Foundation Model APIs
