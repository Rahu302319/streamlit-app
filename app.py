# streamlit_automation.py
import streamlit as st
import pandas as pd
import requests
import json
import os
from datetime import datetime, date
import pytz
import openpyxl
from io import BytesIO
import time

st.set_page_config(
    page_title="Robin Automation Dashboard",
    page_icon="⚡",
    layout="wide"
)

# --- CONFIGURATION ---
PHP_API_URLS = {
    "stock": "https://eramsales.ct.ws/dailysalesreport.com/upload/stock_api.php",
    "delivery": "https://eramsales.ct.ws/dailysalesreport.com/upload/delivery_api.php",
    "retail": "https://eramsales.ct.ws/dailysalesreport.com/upload/retail_api.php",
    "ftd_retail": "https://eramsales.ct.ws/dailysalesreport.com/upload/ftd_retail_api.php",
    "booking": "https://eramsales.ct.ws/dailysalesreport.com/upload/booking_api.php",
    "billing": "https://eramsales.ct.ws/dailysalesreport.com/upload/billing_api.php",
    "shield": "https://eramsales.ct.ws/dailysalesreport.com/upload/shield_api.php"
}

UPLOAD_LOCATION_NAME = "Stock_Report_Update"

# --- HELPER FUNCTIONS ---
def get_current_ist_time():
    """Get current IST time"""
    ist_timezone = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist_timezone)

def validate_data_structure(df, report_type):
    """Validate data structure before upload"""
    if df.empty:
        return False, "No data found"
    
    # Required columns for each report type
    required_columns = {
        "delivery": ["Customer GSTIN No", "Invoice No.", "Invoice Date", "Chassis No."],
        "retail": ["Invoice Number", "Invoice Date and Time", "Chassis Number", "Customer Name"],
        "ftd_retail": ["Invoice Number", "Invoice Date and Time", "Chassis Number", "Customer Name"],
        "booking": ["Booking Number", "Booking Date", "Booking Customer Name", "Model Description"],
        "shield": ["SCHEME REGISTRATION ID", "Customer Name", "Invoice Number", "VIN Number"],
        "billing": ["OEM Invoice No", "Chassis Number"],
        "stock": ["Chassis Number", "Model", "Color", "Vehicle Status"]
    }
    
    if report_type not in required_columns:
        return True, "No validation required"
    
    required = required_columns[report_type]
    missing_columns = []
    
    for column in required:
        column_found = False
        for df_column in df.columns:
            if column.lower() in df_column.lower() or df_column.lower() in column.lower():
                column_found = True
                break
        if not column_found:
            missing_columns.append(column)
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, "Data structure validated successfully"

def upload_to_server(df, report_type):
    """Upload data to server"""
    if df.empty:
        st.warning(f"No data found to upload for {report_type}")
        return False
    
    # Validate data structure
    is_valid, validation_message = validate_data_structure(df, report_type)
    if not is_valid:
        st.error(f"Validation failed for {report_type}: {validation_message}")
        return False
    
    # Add upload timestamp
    upload_time = get_current_ist_time()
    
    # Prepare rows
    rows = []
    for _, row in df.iterrows():
        row_dict = {}
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                row_dict[col] = ""
            elif isinstance(val, (datetime, date)):
                row_dict[col] = val.strftime("%Y-%m-%d %H:%M:%S") if isinstance(val, datetime) else val.strftime("%Y-%m-%d")
            else:
                row_dict[col] = str(val)
        rows.append(row_dict)
    
    payload = {
        "location": UPLOAD_LOCATION_NAME,
        "report_type": report_type,
        "rows": rows,
        "clear_previous": True,
        "upload_timestamp": upload_time.strftime("%Y-%m-%d %H:%M:%S"),
        "upload_timezone": "IST"
    }
    
    try:
        api_url = PHP_API_URLS.get(report_type)
        if not api_url:
            st.error(f"No API URL configured for {report_type}")
            return False
        
        response = requests.post(api_url, json=payload, timeout=120)
        
        if response.status_code == 200:
            try:
                resp_json = response.json()
                if resp_json.get("status") in ["success", "partial"]:
                    count = resp_json.get("inserted_count", 0)
                    error_count = resp_json.get("error_count", 0)
                    
                    if error_count > 0:
                        st.warning(f"Upload partially successful: {count} records saved, {error_count} errors")
                    else:
                        st.success(f"✅ UPLOAD SUCCESS: {count} Records Saved to {report_type} table.")
                    return True
                else:
                    err = resp_json.get("message", "Unknown error")
                    st.warning(f"Server Response: {err}")
                    return False
            except json.JSONDecodeError:
                st.warning(f"Invalid JSON response: {response.text[:200]}")
                return False
        else:
            st.error(f"HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        return False

# --- STREAMLIT UI ---
def main():
    # Custom CSS
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        margin-top: 10px;
    }
    .report-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("⚡ Robin Automation Dashboard")
        st.markdown("**Automated Report Uploader to Server**")
    with col2:
        st.markdown(f"**IST Time:** {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.markdown("---")
    
    # Tab Layout
    tab1, tab2, tab3 = st.tabs(["📤 Upload Reports", "📊 Manual Upload", "⚙️ Settings"])
    
    with tab1:
        st.header("📤 Upload Excel Reports")
        
        # File Uploader
        uploaded_file = st.file_uploader(
            "Upload Excel File",
            type=['xlsx', 'xls'],
            help="Upload your Excel report file"
        )
        
        if uploaded_file is not None:
            # Report Type Selection
            report_type = st.selectbox(
                "Select Report Type",
                options=list(PHP_API_URLS.keys()),
                format_func=lambda x: x.replace('_', ' ').title(),
                help="Select the type of report you're uploading"
            )
            
            # Preview Data
            try:
                df = pd.read_excel(uploaded_file)
                st.subheader("📋 Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
                # Show file info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Total Columns", len(df.columns))
                with col3:
                    st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
                
                # Upload Button
                if st.button("🚀 Upload to Server", type="primary", use_container_width=True):
                    with st.spinner("Uploading data to server..."):
                        success = upload_to_server(df, report_type)
                        if success:
                            st.balloons()
                            st.success("✅ Upload completed successfully!")
                        else:
                            st.error("❌ Upload failed. Check the error messages above.")
                
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        
        else:
            st.info("👆 Please upload an Excel file to begin")
    
    with tab2:
        st.header("📊 Manual Data Entry")
        
        report_type_manual = st.selectbox(
            "Select Report Type",
            options=list(PHP_API_URLS.keys()),
            format_func=lambda x: x.replace('_', ' ').title(),
            key="manual_report_type"
        )
        
        # Manual data input
        st.subheader("Enter Data Manually")
        
        # Simple form for manual entry
        with st.form("manual_upload_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                data_input = st.text_area(
                    "Enter data as JSON",
                    height=200,
                    help='Enter data as JSON array of objects. Example: [{"column1": "value1", "column2": "value2"}]'
                )
            
            with col2:
                st.markdown("""
                **Example Format:**
                ```json
                [
                    {
                        "Chassis Number": "ABC123",
                        "Model": "XUV700",
                        "Color": "Red",
                        "Vehicle Status": "In Stock"
                    },
                    {
                        "Chassis Number": "DEF456",
                        "Model": "Scorpio",
                        "Color": "White",
                        "Vehicle Status": "Sold"
                    }
                ]
                ```
                """)
            
            submit_manual = st.form_submit_button("📤 Upload Manual Data", type="primary")
            
            if submit_manual:
                try:
                    if data_input:
                        data = json.loads(data_input)
                        df_manual = pd.DataFrame(data)
                        
                        st.subheader("Preview")
                        st.dataframe(df_manual, use_container_width=True)
                        
                        with st.spinner("Uploading manual data..."):
                            success = upload_to_server(df_manual, report_type_manual)
                            if success:
                                st.success("✅ Manual upload successful!")
                            else:
                                st.error("❌ Manual upload failed.")
                    else:
                        st.warning("Please enter data in JSON format.")
                except json.JSONDecodeError:
                    st.error("Invalid JSON format. Please check your input.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab3:
        st.header("⚙️ Settings")
        
        # API URLs Configuration
        st.subheader("API Configuration")
        with st.expander("View/Edit API URLs"):
            for report_type, url in PHP_API_URLS.items():
                st.text_input(
                    f"{report_type.replace('_', ' ').title()} API",
                    value=url,
                    disabled=True,
                    key=f"api_{report_type}"
                )
        
        # Upload History
        st.subheader("📜 Upload History")
        
        # Initialize session state for history
        if 'upload_history' not in st.session_state:
            st.session_state.upload_history = []
        
        if st.button("Clear History"):
            st.session_state.upload_history = []
            st.success("History cleared!")
        
        if st.session_state.upload_history:
            history_df = pd.DataFrame(st.session_state.upload_history)
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("No upload history yet.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        ⚡ Robin Automation v1.0 | Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

# --- MULTIPLE FILE UPLOAD FEATURE (Optional) ---
def batch_upload_section():
    st.header("📦 Batch Upload Multiple Reports")
    
    uploaded_files = st.file_uploader(
        "Upload multiple Excel files",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="Upload multiple report files at once"
    )
    
    if uploaded_files:
        # Create a mapping for each file
        file_mappings = {}
        
        for uploaded_file in uploaded_files:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**File:** {uploaded_file.name}")
            with col2:
                report_type = st.selectbox(
                    "Report Type",
                    options=list(PHP_API_URLS.keys()),
                    format_func=lambda x: x.replace('_', ' ').title(),
                    key=f"type_{uploaded_file.name}"
                )
                file_mappings[uploaded_file.name] = (uploaded_file, report_type)
        
        if st.button("🚀 Upload All Files", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            success_count = 0
            total_files = len(uploaded_files)
            
            for idx, (filename, (file_obj, report_type)) in enumerate(file_mappings.items()):
                status_text.text(f"Processing {filename}... ({idx+1}/{total_files})")
                
                try:
                    df = pd.read_excel(file_obj)
                    success = upload_to_server(df, report_type)
                    
                    if success:
                        success_count += 1
                        st.success(f"✅ {filename} uploaded successfully")
                    else:
                        st.error(f"❌ {filename} upload failed")
                
                except Exception as e:
                    st.error(f"❌ Error processing {filename}: {str(e)}")
                
                progress_bar.progress((idx + 1) / total_files)
            
            status_text.text("Batch upload completed!")
            st.success(f"✅ {success_count} out of {total_files} files uploaded successfully!")

if __name__ == "__main__":
    main()
