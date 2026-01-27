import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
import shutil
import zipfile
import tempfile
import pandas as pd
from datetime import datetime
import socket

# --- CONFIGURATION ---
PAGE_TITLE = "Vahan RTO Scraper"
PAGE_ICON = "🚗"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- RTO DATA ---
RTO_DATA = [
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

# --- HELPER FUNCTIONS ---
def get_driver(download_dir):
    chrome_options = Options()
    
    # 1. HARDCODED PATH FOR STREAMLIT CLOUD
    chrome_options.binary_location = "/usr/bin/chromium"
    
    # 2. STRATEGY: Eager (Don't wait for all resources)
    chrome_options.page_load_strategy = 'eager'
    
    # 3. CRITICAL PERFORMANCE FIX: DISABLE IMAGES
    # This prevents the browser from downloading heavy images, 
    # saving memory and preventing timeouts.
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    # 4. SPOOF USER AGENT
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    # 5. HEADLESS & RESOURCE SAVING ARGS
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # 6. DOWNLOAD PREFERENCES
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2  # Block images
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service("/usr/bin/chromedriver")
    
    # Create driver with increased socket timeout
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set script timeout to prevent hangs
    driver.set_script_timeout(120)
    driver.set_page_load_timeout(120)
    
    return driver

def extract_rto_name(rto_name):
    return rto_name.split()[0]

def log_message(log_placeholder, messages, new_msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    messages.append(f"[{timestamp}] {new_msg}")
    log_placeholder.code("\n".join(messages[-10:]), language="bash")

def scrape_vahan(selected_rtos, selected_year, progress_bar, status_text, log_placeholder, final_report_placeholder):
    temp_dir = tempfile.mkdtemp()
    driver = None
    downloaded_files = []
    messages = []
    report_data = []

    try:
        log_message(log_placeholder, messages, "Initializing Chrome (No Images Mode)...")
        driver = get_driver(temp_dir)
        
        url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"
        log_message(log_placeholder, messages, "Connecting to Vahan Dashboard...")
        
        # Try/Except block specifically for the initial load
        try:
            driver.get(url)
        except Exception as e:
            log_message(log_placeholder, messages, "Initial load timeout (ignoring if DOM ready)...")
        
        # Initial Dashboard Click
        log_message(log_placeholder, messages, "Clicking Dashboard...")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]"))).click()
        
        # State Selection (KL)
        log_message(log_placeholder, messages, "Selecting State: Kerala...")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/ul/li[18]"))).click()
        time.sleep(3)

        total_rtos = len(selected_rtos)
        
        for idx, rto_name in enumerate(selected_rtos):
            try:
                status_text.write(f"**Processing ({idx+1}/{total_rtos}):** `{rto_name}`")
                progress_bar.progress((idx) / total_rtos)
                
                log_message(log_placeholder, messages, f"Setting RTO: {rto_name}")
                
                # 1. Click Dropdown Arrow
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/div[3]"))).click()
                time.sleep(1)

                # 2. Click Input
                dropdown_trigger = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "selectedRto")))
                dropdown_trigger.click()
                time.sleep(1)

                # 3. Find RTO
                options = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#selectedRto_items .ui-selectonemenu-item")))
                
                option_found = False
                for option in options:
                    if option.text.strip() == rto_name:
                        option.click()
                        option_found = True
                        break
                
                if not option_found:
                    report_data.append({"RTO": rto_name, "Status": "Failed", "Reason": "RTO Not Found"})
                    log_message(log_placeholder, messages, f"Error: {rto_name} skipped.")
                    # Close dropdown
                    try: dropdown_trigger.click()
                    except: pass
                    continue
                    
                time.sleep(1)

                # Configurations
                log_message(log_placeholder, messages, "Applying Filters...")
                
                # Y Axis
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[3]"))).click()
                time.sleep(0.5)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='yaxisVar_4']"))).click()
                
                # X Axis
                time.sleep(0.5)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/label"))).click()
                time.sleep(0.5)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='xaxisVar_7']"))).click()
                
                # Year
                time.sleep(0.5)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/label"))).click()
                time.sleep(0.5)

                year_mapping = {"2025": "//*[@id='selectedYear_1']", "2024": "//*[@id='selectedYear_2']", "2023": "//*[@id='selectedYear_3']", "2022": "//*[@id='selectedYear_4']", "2021": "//*[@id='selectedYear_5']", "2020": "//*[@id='selectedYear_6']"}
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, year_mapping[selected_year]))).click()
                
                # Refresh
                time.sleep(1)
                log_message(log_placeholder, messages, "Refreshing...")
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button"))).click()
                time.sleep(3)

                # Filter Toggle
                log_message(log_placeholder, messages, "Selecting Vehicle Types...")
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[3]/div"))).click()
                time.sleep(1)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[12]/td/label"))).click()
                time.sleep(0.5)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[13]/td/label"))).click()
                
                # Refresh Table
                time.sleep(1)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[1]/span/button"))).click()
                time.sleep(3)

                # Download
                log_message(log_placeholder, messages, "Downloading...")
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a/img"))).click()
                time.sleep(3)

                # File Management
                files = os.listdir(temp_dir)
                xlsx_files = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]
                
                if xlsx_files:
                    full_paths = [os.path.join(temp_dir, f) for f in xlsx_files]
                    latest_file = max(full_paths, key=os.path.getctime)
                    extracted_name = extract_rto_name(rto_name)
                    new_file_name = f"{extracted_name}_{selected_year}.xlsx"
                    new_file_path = os.path.join(temp_dir, new_file_name)
                    
                    if latest_file != new_file_path:
                        shutil.move(latest_file, new_file_path)
                        downloaded_files.append(new_file_path)
                    
                    report_data.append({"RTO": rto_name, "Status": "Success", "File": new_file_name})
                    log_message(log_placeholder, messages, f"Saved: {new_file_name}")
                else:
                    report_data.append({"RTO": rto_name, "Status": "Failed", "Reason": "No file downloaded"})
                    log_message(log_placeholder, messages, "Error: File missing.")

                # Cleanup Filter
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='filterLayout']/div[1]/a"))).click()
                except:
                    pass # Ignore if filter close fails
                time.sleep(1)

            except Exception as e:
                report_data.append({"RTO": rto_name, "Status": "Failed", "Reason": "Timeout/Error"})
                log_message(log_placeholder, messages, f"Failed: {str(e)[:50]}...")
                # Refresh page to reset state for next RTO
                try:
                    driver.refresh()
                    time.sleep(3)
                except:
                    pass
                continue

        progress_bar.progress(100)
        status_text.write("**Scraping Completed!**")
        log_message(log_placeholder, messages, "Process Finished.")
        
        df = pd.DataFrame(report_data)
        final_report_placeholder.dataframe(df, use_container_width=True)
        
        return downloaded_files, temp_dir

    except Exception as e:
        st.error(f"Critical System Error: {str(e)}")
        return [], temp_dir
    finally:
        if driver:
            driver.quit()

# --- STREAMLIT UI ---
st.title("🚗 Vahan RTO Data Scraper (Lite Mode)")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Configuration")
    selected_year = st.selectbox("Select Year", ["2025", "2024", "2023", "2022", "2021", "2020"])
    
    st.info("⚡ **Lite Mode Active:** Images are disabled to prevent timeouts on the cloud server.")

    select_all = st.checkbox("Select All RTOs")
    if select_all:
        selected_rtos = st.multiselect("Select RTOs", RTO_DATA, default=RTO_DATA)
    else:
        selected_rtos = st.multiselect("Select RTOs", RTO_DATA)
    
    start_btn = st.button("Start Scraping", type="primary", use_container_width=True)

with col2:
    st.subheader("Live Status Monitor")
    
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    st.markdown("**System Logs:**")
    log_placeholder = st.empty()
    log_placeholder.code("Ready...", language="bash")
    
    st.markdown("**Final Report:**")
    final_report_placeholder = st.empty()

if start_btn:
    if not selected_rtos:
        st.warning("Please select at least one RTO.")
    else:
        files, temp_dir = scrape_vahan(
            selected_rtos, 
            selected_year, 
            progress_bar, 
            status_text, 
            log_placeholder,
            final_report_placeholder
        )
        
        if files:
            zip_filename = f"RTO_Data_{selected_year}.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in files:
                    zipf.write(file, os.path.basename(file))
            
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📥 Download Result (ZIP)",
                    data=f,
                    file_name=zip_filename,
                    mime="application/zip",
                    type="secondary",
                    use_container_width=True
                )
            st.success(f"Successfully scraped {len(files)} files!")
