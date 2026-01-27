import streamlit as st
import os
import time
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tempfile

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

def extract_rto_name(rto_name):
    # Extract the first part of the RTO name before "SRTO" or "RTO"
    return rto_name.split()[0]

def download_rto_data(download_path, selected_year, selected_rto_names, progress_bar, status_text):
    # Ensure the path exists or create it
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # Set up Chrome options for downloading files
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set download directory
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Start Chrome driver using WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    downloaded_files = []
    
    try:
        # URL to be accessed
        url = "https://vahan.parivaharan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"
        driver.get(url)
        
        # Wait for the page to load and click the required element
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]"))
        ).click()
        
        time.sleep(2)
        
        # Select state option
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/ul/li[18]"))
        ).click()
        
        time.sleep(3)
        
        # Process each selected RTO
        for idx, rto_name in enumerate(selected_rto_names):
            # Update progress
            progress_bar.progress((idx + 1) / len(selected_rto_names))
            status_text.text(f"Processing: {rto_name} ({idx + 1}/{len(selected_rto_names)})")
            
            # Click dropdown icon
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/div[3]"))
            ).click()
            
            time.sleep(2)
            
            # Open the dropdown panel
            dropdown_icon = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "selectedRto"))
            )
            dropdown_icon.click()
            
            time.sleep(2)
            
            # Wait for options to be visible
            options = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#selectedRto_items .ui-selectonemenu-item"))
            )
            
            # Select the option from the dropdown
            option_found = False
            for option in options:
                if option.text == rto_name:
                    option.click()
                    option_found = True
                    break
            
            if not option_found:
                st.warning(f'RTO "{rto_name}" not found in dropdown.')
                continue
            
            time.sleep(2)
            
            # Click Y Axis after selecting RTO
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[3]"))
            ).click()
            time.sleep(2)
            
            # Maker Select
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='yaxisVar_4']"))
            ).click()
            time.sleep(2)
            
            # Click X Axis after selecting RTO
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/label"))
            ).click()
            time.sleep(2)
            
            # Month Select
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='xaxisVar_7']"))
            ).click()
            time.sleep(2)
            
            # Year Select after selecting RTO
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/label"))
            ).click()
            time.sleep(2)
            
            # Define the year mapping
            year_mapping = {
                "2025": "//*[@id='selectedYear_1']",
                "2024": "//*[@id='selectedYear_2']",
                "2023": "//*[@id='selectedYear_3']",
                "2022": "//*[@id='selectedYear_4']",
                "2021": "//*[@id='selectedYear_5']",
                "2020": "//*[@id='selectedYear_6']"
            }
            
            # Select the correct year based on the combobox value
            year_xpath = year_mapping.get(selected_year)
            if year_xpath:
                year_dropdown = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, year_xpath))
                )
                year_dropdown.click()
                time.sleep(2)
            else:
                st.warning(f'Year "{selected_year}" not found.')
                time.sleep(2)
                continue
            
            # Click Refresh
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button"))
            ).click()
            time.sleep(5)
            
            # Click toggler
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[3]/div"))
            ).click()
            time.sleep(2)
            
            # Select LMV
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[12]/td/label"))
            ).click()
            time.sleep(1)
            
            # Select LPV
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[13]/td/label"))
            ).click()
            time.sleep(1)
            
            # Click Refresh
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[1]/span/button"))
            ).click()
            time.sleep(5)
            
            # Download file
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a/img"))
            ).click()
            time.sleep(3)
            
            # Toggle Hide
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='filterLayout']/div[1]/a"))
            ).click()
            time.sleep(1)
            
            # Wait for download to complete
            time.sleep(5)
            
            # Check for downloaded file
            files = os.listdir(download_path)
            # Look for the most recent .xlsx file
            excel_files = [f for f in files if f.endswith('.xlsx')]
            if excel_files:
                # Get the most recently modified Excel file
                latest_file = max([os.path.join(download_path, f) for f in excel_files], key=os.path.getmtime)
                
                # Extract the RTO name for file renaming
                extracted_name = extract_rto_name(rto_name)
                new_file_name = f"{extracted_name}.xlsx"
                new_file_path = os.path.join(download_path, new_file_name)
                
                # Rename the file
                os.rename(latest_file, new_file_path)
                downloaded_files.append(new_file_path)
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
    
    return downloaded_files

def main():
    st.set_page_config(page_title="RTO Data Downloader", layout="wide")
    
    # Custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            width: 100%;
        }
        .stSelectbox, .stTextInput {
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📥 RTO Data Downloader")
    st.markdown("---")
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Settings")
        
        # Year selection
        year_list = ["2025", "2024", "2023", "2022", "2021", "2020"]
        selected_year = st.selectbox("Select Year:", year_list, index=0)
        
        # Download path
        download_path = st.text_input("Download Path:", value=os.getcwd())
        
        # Select All checkbox
        select_all = st.checkbox("Select All RTOs")
        
        # Download button
        download_button = st.button("🚀 Download Selected Data", type="primary")
    
    with col2:
        st.subheader("Select RTOs")
        
        # Create checkboxes for RTOs
        selected_rtos = []
        
        # Use multiselect for better UX with many options
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
        
        # Show selection count
        st.info(f"Selected: {len(selected_rtos)} RTO(s)")
    
    st.markdown("---")
    
    # Download functionality
    if download_button:
        if not selected_rtos:
            st.error("Please select at least one RTO before downloading.")
        else:
            # Create progress bar and status text
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Start download process
            with st.spinner("Starting download process..."):
                downloaded_files = download_rto_data(
                    download_path, 
                    selected_year, 
                    selected_rtos,
                    progress_bar,
                    status_text
                )
            
            # Show completion message
            if downloaded_files:
                status_text.success(f"✅ Download completed! {len(downloaded_files)} file(s) saved.")
                
                # Show downloaded files
                st.subheader("Downloaded Files:")
                for file in downloaded_files:
                    st.write(f"• {os.path.basename(file)}")
                
                # Option to download all files as zip
                if st.button("📦 Download All as ZIP"):
                    import zipfile
                    import io
                    
                    # Create zip file in memory
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for file in downloaded_files:
                            zip_file.write(file, os.path.basename(file))
                    
                    # Provide download button for zip
                    st.download_button(
                        label="Download ZIP",
                        data=zip_buffer.getvalue(),
                        file_name=f"rto_data_{selected_year}.zip",
                        mime="application/zip"
                    )
            else:
                status_text.error("❌ No files were downloaded.")

if __name__ == '__main__':
    main()
