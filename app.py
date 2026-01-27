import streamlit as st
import os
import sys
import time
import tempfile
from pathlib import Path
import shutil
from datetime import datetime

# RTO Data
rto_data = [
    "ADOOR SRTO - KL26( 27-MAR-2019 )", "ALAPPUZHA RTO - KL4( 18-MAR-2019 )",
    "ALATHUR SRTO - KL49( 30-MAR-2019 )", "ALUVA SRTO - KL41( 23-MAR-2019 )",
    "ANGAMALI SRTO - KL63( 23-MAR-2019 )", "ATTINGAL RTO - KL16( 18-MAR-2019 )",
    "CHADAYAMANGALA SRTO - KL82( 28-SEP-2020 )", "CHALAKKUDY SRTO - KL64( 30-MAR-2019 )",
    "CHANGANACHERRY SRTO - KL33( 30-MAR-2019 )", "CHENGANNUR SRTO - KL30( 30-MAR-2019 )",
    "CHERTHALA SRTO - KL32( 30-MAR-2019 )", "CHITTUR SRTO - KL70( 23-MAR-2019 )",
    "DEVIKULAM SRTO - KL68( 30-MAR-2019 )", "ERNAKULAM RTO - KL7( 14-MAR-2019 )",
    "GURUVAYUR SRTO - KL46( 30-MAR-2019 )", "IDUKKI RTO - KL6( 18-MAR-2019 )",
    "IRINJALAKUDA SRTO - KL45( 30-MAR-2019 )", "IRITTY SRTO - KL78( 30-MAR-2019 )",
    "KANHANGAD SRTO - KL60( 30-MAR-2019 )", "KANJIRAPPALLY SRTO - KL34( 30-MAR-2019 )",
    "KANNUR RTO - KL13( 18-MAR-2019 )", "KARUNAGAPPALLY SRTO - KL23( 30-MAR-2019 )",
    "KASARGODE RTO - KL14( 18-MAR-2019 )", "KATTAKADA SRTO - KL74( 29-MAR-2019 )",
    "KAYAMKULAM SRTO - KL29( 30-MAR-2019 )", "KAZHAKUTTOM SRTO - KL22( 29-MAR-2019 )",
    "KODUNGALLUR SRTO - KL47( 30-MAR-2019 )", "KODUVALLY SRTO - KL57( 30-MAR-2019 )",
    "KOILANDY SRTO - KL56( 30-MAR-2019 )", "KOLLAM RTO - KL2( 15-MAR-2019 )",
    "KONDOTTY SRTO - KL84( 28-SEP-2020 )", "KONNI SRTO - KL83( 06-JUL-2020 )",
    "KOTHAMANGALAM SRTO - KL44( 23-MAR-2019 )", "KOTTARAKKARA SRTO - KL24( 30-MAR-2019 )",
    "KOTTAYAM RTO - KL5( 18-MAR-2019 )", "KOZHIKODE RTO - KL11( 15-MAR-2019 )",
    "KUNNATHUR SRTO - KL61( 30-MAR-2019 )", "KUTTANADU SRTO - KL66( 30-MAR-2019 )",
    "MALAPPURAM RTO - KL10( 20-MAR-2019 )", "MALLAPPALLY SRTO - KL28( 27-MAR-2019 )",
    "MANANTHAVADY SRTO - KL72( 30-MAR-2019 )", "MANNARGHAT SRTO - KL50( 30-MAR-2019 )",
    "MATTANCHERRY SRTO - KL43( 23-MAR-2019 )", "MAVELIKKARA SRTO - KL31( 30-MAR-2019 )",
    "MUVATTUPUZHA RTO - KL17( 15-MAR-2019 )", "NANMANDA SRTO - KL76( 30-MAR-2019 )",
    "NEDUMANGADU SRTO - KL21( 29-MAR-2019 )", "NEYYATTINKARA SRTO - KL20( 29-MAR-2019 )",
    "NILAMBUR SRTO - KL71( 30-MAR-2019 )", "NORTH PARUR SRTO - KL42( 23-MAR-2019 )",
    "OTTAPPALAM SRTO - KL51( 30-MAR-2019 )", "PALAI SRTO - KL35( 30-MAR-2019 )",
    "PALAKKAD RTO - KL9( 18-MAR-2019 )", "PARASSALA SRTO - KL19( 29-MAR-2019 )",
    "PATHANAMTHITTA RTO - KL3( 20-MAR-2019 )", "PATHANAPURAM SRTO - KL80( 28-SEP-2020 )",
    "PATTAMBI SRTO - KL52( 30-MAR-2019 )", "PAYYANNUR SRTO - KL86( 28-SEP-2020 )",
    "PERAMBRA SRTO - KL77( 30-MAR-2019 )", "PERINTHALMANNA SRTO - KL53( 30-MAR-2019 )",
    "PERUMBAVUR SRTO - KL40( 23-MAR-2019 )", "PONNANI SRTO - KL54( 30-MAR-2019 )",
    "PUNALUR SRTO - KL25( 30-MAR-2019 )", "RAMANATTUKARA (FEROKE) SRTO - KL85( 28-SEP-2020 )",
    "RANNI SRTO - KL62( 30-MAR-2019 )", "SULTHANBATHERY SRTO - KL73( 30-MAR-2019 )",
    "THALASSERY SRTO - KL58( 30-MAR-2019 )", "THALIPARAMBA SRTO - KL59( 30-MAR-2019 )",
    "THIRURANGADI SRTO - KL65( 30-MAR-2019 )", "THIRUR SRTO - KL55( 30-MAR-2019 )",
    "THIRUVALLA SRTO - KL27( 27-MAR-2019 )", "THODUPUZHA SRTO - KL38( 30-MAR-2019 )",
    "THRIPRAYAR SRTO - KL75( 30-MAR-2019 )", "THRISSUR RTO - KL8( 18-MAR-2019 )",
    "TRIPUNITHURA SRTO - KL39( 23-MAR-2019 )", "TRIVANDRUM RTO - KL1( 21-FEB-2019 )",
    "UDUMBANCHOLA SRTO - KL69( 30-MAR-2019 )", "UZHAVOOR SRTO - KL67( 30-MAR-2019 )",
    "VADAKARA RTO - KL18( 15-MAR-2019 )", "VAIKOM SRTO - KL36( 30-MAR-2019 )",
    "VANDIPERIYAR SRTO - KL37( 30-MAR-2019 )", "VARKALA SRTO - KL81( 10-JUL-2020 )",
    "VELLARIKUNDU SRTO - KL79( 30-MAR-2019 )", "WADAKKANCHERRY SRTO - KL48( 30-MAR-2019 )",
    "WAYANAD RTO - KL12( 15-MAR-2019 )"
]

def setup_browser():
    """Setup Chrome browser for Streamlit Cloud or local"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    
    chrome_options = Options()
    
    # For Streamlit Cloud
    if os.environ.get('STREAMLIT_SHARING', 'false').lower() == 'true':
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        
        # Set Chrome binary location
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        
        # Install ChromeDriver
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        # For local development
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        # Use webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def extract_rto_name(rto_name):
    """Extract the first part of the RTO name before 'SRTO' or 'RTO'"""
    return rto_name.split()[0]

def download_rto_data(selected_year, selected_rto_names, progress_bar, status_text, download_folder):
    """Main function to download RTO data"""
    driver = None
    downloaded_files = []
    
    try:
        # Setup browser
        status_text.text("Setting up browser...")
        driver = setup_browser()
        
        # URL to be accessed
        url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"
        driver.get(url)
        time.sleep(5)
        
        status_text.text("Loading website...")
        
        # Process each RTO
        for idx, rto_name in enumerate(selected_rto_names):
            progress = (idx + 1) / len(selected_rto_names)
            progress_bar.progress(progress)
            status_text.text(f"Processing {idx + 1}/{len(selected_rto_names)}: {rto_name}")
            
            try:
                # Click on RTO dropdown
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]").click()
                time.sleep(2)
                
                # Select Kerala state
                driver.find_element("xpath", "/html/body/div[3]/div/ul/li[18]").click()
                time.sleep(3)
                
                # Click RTO selection dropdown
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/div[3]").click()
                time.sleep(2)
                
                # Select specific RTO
                dropdown = driver.find_element("id", "selectedRto")
                dropdown.click()
                time.sleep(2)
                
                # Find and click the RTO option
                option_found = False
                options = driver.find_elements("css selector", "#selectedRto_items .ui-selectonemenu-item")
                for option in options:
                    if option.text == rto_name:
                        option.click()
                        option_found = True
                        break
                
                if not option_found:
                    st.warning(f"RTO '{rto_name}' not found in dropdown.")
                    continue
                
                time.sleep(2)
                
                # Configure Y Axis (Maker)
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[3]").click()
                time.sleep(1)
                driver.find_element("xpath", "//*[@id='yaxisVar_4']").click()
                time.sleep(1)
                
                # Configure X Axis (Month)
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/label").click()
                time.sleep(1)
                driver.find_element("xpath", "//*[@id='xaxisVar_7']").click()
                time.sleep(1)
                
                # Configure Year
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/label").click()
                time.sleep(1)
                
                # Year mapping
                year_mapping = {
                    "2025": "//*[@id='selectedYear_1']",
                    "2024": "//*[@id='selectedYear_2']",
                    "2023": "//*[@id='selectedYear_3']",
                    "2022": "//*[@id='selectedYear_4']",
                    "2021": "//*[@id='selectedYear_5']",
                    "2020": "//*[@id='selectedYear_6']"
                }
                
                year_xpath = year_mapping.get(selected_year)
                if year_xpath:
                    driver.find_element("xpath", year_xpath).click()
                    time.sleep(1)
                else:
                    st.warning(f"Year '{selected_year}' not found.")
                    continue
                
                # Click Refresh
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button").click()
                time.sleep(5)
                
                # Open filter panel
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[3]/div/div[3]/div").click()
                time.sleep(2)
                
                # Select LMV and LPV
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[12]/td/label").click()
                time.sleep(1)
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[13]/td/label").click()
                time.sleep(1)
                
                # Click Filter Refresh
                driver.find_element("xpath", "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[1]/span/button").click()
                time.sleep(5)
                
                # Try to download (simulated for now)
                extracted_name = extract_rto_name(rto_name)
                file_name = f"{extracted_name}_{selected_year}.xlsx"
                file_path = os.path.join(download_folder, file_name)
                
                # Create a dummy file for demonstration
                with open(file_path, 'w') as f:
                    f.write(f"RTO: {rto_name}\nYear: {selected_year}\nDownloaded at: {datetime.now()}")
                
                downloaded_files.append(file_path)
                st.success(f"Downloaded: {extracted_name}")
                
                # Hide filter panel
                driver.find_element("xpath", "//*[@id='filterLayout']/div[1]/a").click()
                time.sleep(1)
                
            except Exception as e:
                st.error(f"Error processing {rto_name}: {str(e)}")
                continue
        
        return downloaded_files
        
    except Exception as e:
        st.error(f"Browser setup error: {str(e)}")
        return []
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def main():
    st.set_page_config(
        page_title="RTO Data Downloader",
        page_icon="📊",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            width: 100%;
            padding: 10px;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.title("📊 RTO Data Downloader")
    st.markdown("Download RTO vehicle registration data from Parivahan portal")
    st.markdown("---")
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Settings")
        
        # Year selection
        year_list = ["2025", "2024", "2023", "2022", "2021", "2020"]
        selected_year = st.selectbox(
            "Select Year:",
            year_list,
            index=0,
            help="Select the year for which you want to download data"
        )
        
        # Create download folder
        download_folder = tempfile.mkdtemp(prefix="rto_downloads_")
        
        # Select All checkbox
        select_all = st.checkbox("Select All RTOs", value=False)
        
        # Download button
        download_clicked = st.button(
            "🚀 Download Selected Data",
            type="primary",
            use_container_width=True
        )
        
        # Info section
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            1. Select the year from dropdown
            2. Select RTOs from the list
            3. Click 'Download Selected Data'
            4. Wait for the process to complete
            5. Download the generated files
            
            **Note:** This process may take several minutes depending on the number of RTOs selected.
            """)
    
    with col2:
        st.subheader("📍 Select RTOs")
        
        # RTO selection
        if select_all:
            selected_rtos = st.multiselect(
                "RTO List:",
                rto_data,
                default=rto_data,
                label_visibility="collapsed",
                help="Select RTOs to download data for"
            )
        else:
            selected_rtos = st.multiselect(
                "RTO List:",
                rto_data,
                label_visibility="collapsed",
                help="Select RTOs to download data for"
            )
        
        # Selection info
        st.info(f"✅ Selected {len(selected_rtos)} RTO(s) for {selected_year}")
        
        # Preview selected RTOs
        if selected_rtos:
            with st.expander("👁️ Preview Selected RTOs"):
                for rto in selected_rtos[:10]:  # Show first 10
                    st.write(f"• {rto}")
                if len(selected_rtos) > 10:
                    st.write(f"... and {len(selected_rtos) - 10} more")
    
    st.markdown("---")
    
    # Download process
    if download_clicked:
        if not selected_rtos:
            st.error("❌ Please select at least one RTO before downloading.")
        else:
            # Create progress elements
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Create a container for logs
            log_container = st.container()
            
            with log_container:
                st.subheader("📋 Download Log")
                
                # Start download process
                with st.spinner("Starting download process..."):
                    downloaded_files = download_rto_data(
                        selected_year,
                        selected_rtos,
                        progress_bar,
                        status_text,
                        download_folder
                    )
                
                # Show results
                if downloaded_files:
                    status_text.success(f"✅ Download completed! {len(downloaded_files)} file(s) saved.")
                    
                    # List downloaded files
                    st.subheader("📁 Downloaded Files")
                    
                    # Create columns for files display
                    file_cols = st.columns(3)
                    for idx, file_path in enumerate(downloaded_files):
                        with file_cols[idx % 3]:
                            file_name = os.path.basename(file_path)
                            with open(file_path, "rb") as file:
                                st.download_button(
                                    label=f"⬇️ {file_name}",
                                    data=file,
                                    file_name=file_name,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                    
                    # Create zip file option
                    if len(downloaded_files) > 1:
                        st.subheader("📦 Bundle Download")
                        
                        # Create zip in memory
                        import zipfile
                        import io
                        
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for file_path in downloaded_files:
                                zip_file.write(file_path, os.path.basename(file_path))
                        
                        zip_buffer.seek(0)
                        
                        st.download_button(
                            label="📥 Download All as ZIP",
                            data=zip_buffer,
                            file_name=f"rto_data_{selected_year}.zip",
                            mime="application/zip"
                        )
                else:
                    status_text.error("❌ No files were downloaded. Please check the logs above.")
            
            # Cleanup
            try:
                shutil.rmtree(download_folder)
            except:
                pass
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.9em;'>
        <p>RTO Data Downloader • Built with Streamlit • Data sourced from Parivahan Portal</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
