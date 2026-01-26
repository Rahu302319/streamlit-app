import streamlit as st
import requests
import json
import uuid
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import time

# ---------------- CONFIG ----------------
API_KEY = "k_5726942c2615.Ru4o2RnRMhojD1vr497bDFPuTPM5_1Cnjn5xc0qZvytZFBTLNPFzrA"
URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"
MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

# ---- DATABASE CONFIG ----
# NOTE: If running on Streamlit Cloud, 'localhost' will not work. 
# You need the public IP of your database server.
DB_HOST = "localhost" 
DB_USER = "eramsale_Stock_Tracker"
DB_PASSWORD = "Rahul@302319"
DB_NAME = "eramsale_Stock_Tracker"
NETSALE_TABLE = "net_sales_report"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- CUSTOM CSS ----------------
st.set_page_config(
    page_title="J.A.R.V.I.S AI Sales Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .main-header {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stChatMessage {
        padding: 15px 20px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stChatMessage[data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stChatMessage[data-testid="chat-message-assistant"] {
        background: linear-gradient(135deg, #2c3e50 0%, #4a6491 100%);
        color: white;
    }
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
        text-align: center;
        color: white;
    }
    .welcome-card {
        display: inline-block;
        margin: 10px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        width: 100%;
        vertical-align: top;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    h1, h2, h3 { color: white !important; }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1 style='text-align: center;'>🤖 J.A.R.V.I.S - Intelligent Sales Assistant</h1>
    <p style="text-align: center; color: rgba(255,255,255,0.8); font-size: 1.2rem;">
    Just A Rather Very Intelligent System | v3.0 | Advanced Sales Analytics
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- DB FUNCTIONS ----------------

def test_db_connection():
    """Test database connection with detailed error reporting"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
            connection_timeout=5
        )
        
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{NETSALE_TABLE}'")
        table_exists = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if table_exists:
            return True, "✅ Connection successful and table exists!"
        else:
            return False, f"⚠️ Table '{NETSALE_TABLE}' not found in database"
            
    except Error as e:
        return False, f"🚨 Database Error: {str(e)}"

def get_db_connection():
    """Establish database connection with retry logic"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
            connection_timeout=10
        )
        return conn
    except Error as e:
        st.error(f"Connection Error: {e}")
        return None

def load_netsale_df():
    """Load entire sales data from database"""
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        # Load data
        query = f"SELECT * FROM {NETSALE_TABLE}"
        df = pd.read_sql(query, conn)
        
        if df.empty:
            st.warning(f"⚠️ Table '{NETSALE_TABLE}' exists but is empty!")
            conn.close()
            return None
        
        # Clean Numeric Columns
        numeric_cols = ['InvoiceTotal', 'SaleValueBeforeDisc', 'Discount', 'DealerDiscount', 
                       'SaleValueAfterDisc', 'PurchaseValue', 'Margin', 'Percentage']
        
        for col in numeric_cols:
            if col in df.columns:
                # Only clean if it's object/string type
                if df[col].dtype == 'object':
                    try:
                        df[col] = df[col].astype(str).str.replace('[^\d.-]', '', regex=True)
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except Exception:
                        pass
        
        conn.close()
        return df
        
    except Exception as e:
        st.error(f"🚨 Error loading data: {str(e)}")
        if conn:
            conn.close()
        return None

# ---------------- SESSION INIT ----------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = {
        "title": "New Session",
        "messages": [{"role": "system", "content": "You are J.A.R.V.I.S, an advanced sales data analyst AI."}],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if "netsale_df" not in st.session_state:
    st.session_state.netsale_df = None

if "db_connected" not in st.session_state:
    st.session_state.db_connected = False

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 🚀 Quick Actions")
    
    # Test Connection
    if st.button("🔍 Test Connection", use_container_width=True):
        with st.spinner("Testing..."):
            success, message = test_db_connection()
            if success:
                st.success(message)
                st.session_state.db_connected = True
            else:
                st.error(message)
                st.session_state.db_connected = False

    # Load Data
    if st.button("🔄 Load Data", use_container_width=True):
        with st.spinner("Loading sales data..."):
            df = load_netsale_df()
            if df is not None:
                st.session_state.netsale_df = df
                st.success(f"✅ Loaded {len(df)} records")
                time.sleep(1) 
                st.rerun() # FORCE RERUN TO UPDATE MAIN PANEL
            else:
                st.error("Failed to load data")

    if st.button("🧹 Clear Data", use_container_width=True):
        st.session_state.netsale_df = None
        st.rerun()

    st.divider()
    
    # Status
    if st.session_state.netsale_df is not None:
        st.success("✅ Data Loaded")
        st.metric("Records", len(st.session_state.netsale_df))
    else:
        st.warning("❌ No data loaded")

    st.divider()

    # Chat Management
    if st.button("➕ New Chat Session", use_container_width=True):
        chat_id = str(uuid.uuid4())
        st.session_state.chats[chat_id] = {
            "title": f"Session {len(st.session_state.chats) + 1}",
            "messages": [{"role": "system", "content": "You are J.A.R.V.I.S."}],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.current_chat = chat_id
        st.rerun()

# ---------------- MAIN LAYOUT ----------------
col_chat, col_data = st.columns([2, 1])

# ---------------- CHAT PANEL ----------------
with col_chat:
    current_chat = st.session_state.chats[st.session_state.current_chat]
    
    # Display messages
    for msg in current_chat["messages"]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
                st.markdown(msg["content"])
    
    # Input
    if user_input := st.chat_input("Ask about sales data..."):
        # 1. User Message
        current_chat["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # 2. Assistant Response
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            
            if st.session_state.netsale_df is None:
                full_response = "Please load the data using the sidebar button first."
                response_placeholder.markdown(full_response)
            else:
                # Prepare Context for AI
                df = st.session_state.netsale_df
                # Simple keyword check for demo speed, fall back to AI for complex
                if "branch" in user_input.lower() and "sales" in user_input.lower():
                    if 'Branch' in df.columns and 'SaleValueAfterDisc' in df.columns:
                        data = df.groupby('Branch')['SaleValueAfterDisc'].sum().sort_values(ascending=False).head(5)
                        full_response = "### Top Branch Sales\n" + data.to_markdown()
                    else:
                        full_response = "Relevant columns not found."
                    response_placeholder.markdown(full_response)
                else:
                    # Call External API
                    try:
                        sample = df.head(3).to_dict()
                        context = f"Data Sample: {sample}. Question: {user_input}"
                        
                        payload = {
                            "model": MODEL,
                            "messages": [
                                {"role": "system", "content": "You are a data analyst helper. Be concise."},
                                {"role": "user", "content": context}
                            ]
                        }
                        
                        with st.spinner("Thinking..."):
                            response = requests.post(URL, headers=headers, json=payload, timeout=20)
                            if response.status_code == 200:
                                full_response = response.json()['choices'][0]['message']['content']
                            else:
                                full_response = f"AI Error: {response.status_code}"
                            response_placeholder.markdown(full_response)
                    except Exception as e:
                        full_response = f"Error communicating with AI: {e}"
                        response_placeholder.markdown(full_response)
            
            # Save response
            current_chat["messages"].append({"role": "assistant", "content": full_response})

# ---------------- DATA DASHBOARD PANEL ----------------
with col_data:
    st.markdown("### 📊 Live Dashboard")
    
    if st.session_state.netsale_df is not None:
        df = st.session_state.netsale_df
        
        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            if 'SaleValueAfterDisc' in df.columns:
                total_sales = df['SaleValueAfterDisc'].sum()
                st.markdown(f"""<div class="metric-card"><h3>Sales</h3><h2>₹{total_sales:,.0f}</h2></div>""", unsafe_allow_html=True)
            else:
                st.info("Sales col missing")
        
        with col2:
            st.markdown(f"""<div class="metric-card"><h3>Records</h3><h2>{len(df)}</h2></div>""", unsafe_allow_html=True)

        # Data Preview
        st.markdown("#### Preview")
        st.dataframe(df.head(50), use_container_width=True, height=400)
        
        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "sales_data.csv", "text/csv", key='download-csv')

    else:
        st.info("👋 Welcome! Please click 'Load Data' in the sidebar to begin.")
        st.markdown("""
        <div class="welcome-card">
            <h4>Steps:</h4>
            1. Ensure Database is running
            2. Click 'Test Connection'
            3. Click 'Load Data'
        </div>
        """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption(f"J.A.R.V.I.S v3.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")