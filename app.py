import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
import base64

# Remove packages.txt file (not needed anymore)

# RTO Data - Simplified version for demonstration
rto_data = [
    "ADOOR SRTO - KL26", "ALAPPUZHA RTO - KL4",
    "ALATHUR SRTO - KL49", "ALUVA SRTO - KL41",
    "ANGAMALI SRTO - KL63", "ATTINGAL RTO - KL16",
    "ERNAKULAM RTO - KL7", "IDUKKI RTO - KL6",
    "KANNUR RTO - KL13", "KASARGODE RTO - KL14",
    "KOLLAM RTO - KL2", "KOTTAYAM RTO - KL5",
    "KOZHIKODE RTO - KL11", "MALAPPURAM RTO - KL10",
    "PALAKKAD RTO - KL9", "PATHANAMTHITTA RTO - KL3",
    "THRISSUR RTO - KL8", "TRIVANDRUM RTO - KL1",
    "WAYANAD RTO - KL12"
]

def generate_sample_data(rto_name, year):
    """Generate sample data for demonstration"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Create sample data
    data = {
        'Month': months,
        'Vehicle_Type': ['LMV'] * 6 + ['LPV'] * 6,
        'Registration_Count': [100 + i*10 for i in range(12)],
        'RTO': [rto_name] * 12,
        'Year': [year] * 12
    }
    
    return pd.DataFrame(data)

def get_rto_code(rto_name):
    """Extract RTO code from name"""
    parts = rto_name.split()
    for part in parts:
        if part.startswith('KL'):
            return part
    return ''

def create_download_link(df, filename):
    """Create a download link for Excel file"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='RTO Data')
    
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def main():
    st.set_page_config(
        page_title="RTO Data Downloader",
        page_icon="🚗",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .success-box {
            background-color: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            border: 1px solid #c3e6cb;
            margin: 1rem 0;
        }
        .info-box {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 1rem;
            border-radius: 5px;
            border: 1px solid #bee5eb;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🚗 RTO Data Downloader")
    st.markdown("Download vehicle registration data for Kerala RTOs")
    st.markdown("---")
    
    # Create columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Settings")
        
        # Year selection
        year = st.selectbox(
            "Select Year:",
            ["2025", "2024", "2023", "2022", "2021", "2020"],
            index=0
        )
        
        # Data type selection
        data_type = st.selectbox(
            "Select Data Type:",
            ["Vehicle Registrations", "Tax Collections", "Fines Collected"]
        )
        
        # Select all checkbox
        select_all = st.checkbox("Select All RTOs", value=False)
        
        # Download button
        if st.button("📥 Generate Data Files", type="primary", use_container_width=True):
            st.session_state.download_triggered = True
        else:
            st.session_state.download_triggered = False
            
        # Information
        with st.expander("ℹ️ About this App"):
            st.markdown("""
            This application generates sample RTO data for demonstration purposes.
            
            **Features:**
            - Generate data for multiple RTOs
            - Select different years
            - Download as Excel files
            - Bundle download as ZIP
            
            **Note:** This is a demo version. In production, this would connect to the actual Parivahan portal API.
            """)
    
    with col2:
        st.subheader("📍 Select RTOs")
        
        # RTO selection
        if select_all:
            selected_rtos = st.multiselect(
                "RTO List:",
                rto_data,
                default=rto_data,
                label_visibility="collapsed"
            )
        else:
            selected_rtos = st.multiselect(
                "RTO List:",
                rto_data,
                label_visibility="collapsed"
            )
        
        # Selection info
        if selected_rtos:
            st.markdown(f"""
            <div class="info-box">
            ✅ Selected <strong>{len(selected_rtos)} RTO(s)</strong> for year <strong>{year}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Show selected RTOs
            with st.expander(f"👁️ Selected RTOs ({len(selected_rtos)})"):
                cols = st.columns(2)
                for idx, rto in enumerate(selected_rtos):
                    with cols[idx % 2]:
                        st.write(f"• {rto}")
    
    st.markdown("---")
    
    # Download section
    if st.session_state.get('download_triggered', False):
        if not selected_rtos:
            st.error("❌ Please select at least one RTO.")
        else:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Generate data
            all_dataframes = []
            
            for idx, rto in enumerate(selected_rtos):
                # Update progress
                progress = (idx + 1) / len(selected_rtos)
                progress_bar.progress(progress)
                status_text.text(f"Processing: {rto} ({idx + 1}/{len(selected_rtos)})")
                
                # Generate sample data
                df = generate_sample_data(rto, year)
                all_dataframes.append((rto, df))
                
                # Small delay for realistic feel
                import time
                time.sleep(0.1)
            
            # Show success message
            status_text.empty()
            progress_bar.empty()
            
            st.markdown(f"""
            <div class="success-box">
            ✅ Successfully generated data for <strong>{len(selected_rtos)} RTO(s)</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Individual file downloads
            st.subheader("📄 Individual Files")
            file_cols = st.columns(3)
            
            for idx, (rto_name, df) in enumerate(all_dataframes):
                with file_cols[idx % 3]:
                    # Extract RTO code for filename
                    rto_code = get_rto_code(rto_name)
                    filename = f"{rto_code}_{year}_data.xlsx"
                    
                    # Create download button
                    st.download_button(
                        label=f"⬇️ {rto_code}",
                        data=df.to_csv(index=False).encode('utf-8'),
                        file_name=f"{rto_code}_{year}.csv",
                        mime="text/csv",
                        key=f"individual_{idx}"
                    )
            
            # Combined download option
            st.subheader("📦 Combined Download")
            
            if len(all_dataframes) > 1:
                # Create a single dataframe with all data
                combined_df = pd.concat([df for _, df in all_dataframes], ignore_index=True)
                
                # Download as CSV
                csv = combined_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download All as CSV",
                    data=csv,
                    file_name=f"all_rto_data_{year}.csv",
                    mime="text/csv",
                    key="combined_csv"
                )
                
                # Download as Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    combined_df.to_excel(writer, index=False, sheet_name='All RTO Data')
                output.seek(0)
                
                st.download_button(
                    label="📥 Download All as Excel",
                    data=output,
                    file_name=f"all_rto_data_{year}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="combined_excel"
                )
            
            # Data preview
            with st.expander("👁️ Preview Data"):
                if all_dataframes:
                    preview_df = all_dataframes[0][1].head()
                    st.dataframe(preview_df, use_container_width=True)
                    st.caption(f"Sample data for {all_dataframes[0][0]} ({year})")
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center; color: gray;'>
            <p>RTO Data Generator v1.0</p>
            <p>Data sourced from sample dataset</p>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
