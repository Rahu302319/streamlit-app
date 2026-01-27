import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import shutil
import zipfile
import tempfile

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
    chrome_options.add_argument("--headless")  # MUST be headless for Streamlit Cloud
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Set default download directory for the browser
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def extract_rto_name(rto_name):
    return rto_name.split()[0]

def scrape_vahan(selected_rtos, selected_year, progress_bar, status_text):
    # Create a temporary directory for this session
    temp_dir = tempfile.mkdtemp()
    
    driver = None
    downloaded_files = []

    try:
        driver = get_driver(temp_dir)
        driver.set_page_load_timeout(600)
        
        url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"
        driver.get(url)
        
        status_text.text("Navigating to dashboard...")
        
        # Click Dashboard
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]"))).click()
        time.sleep(2)

        # Select State (Assuming Kerala from your original code index 18)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/ul/li[18]"))).click()
        time.sleep(3)

        # Loop through RTOs
        total_rtos = len(selected_rtos)
        
        for idx, rto_name in enumerate(selected_rtos):
            try:
                status_text.text(f"Processing ({idx+1}/{total_rtos}): {rto_name}")
                progress_bar.progress((idx) / total_rtos)

                # Open Dropdown
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "selectedRto"))).click()
                time.sleep(1)

                # Select Specific RTO
                options = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#selectedRto_items .ui-selectonemenu-item")))
                for option in options:
                    if option.text.strip() == rto_name:
                        option.click()
                        break
                time.sleep(2)

                # Click Y Axis -> Maker
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[3]"))).click()
                time.sleep(1)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='yaxisVar_4']"))).click()
                time.sleep(1)

                # Click X Axis -> Month
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/label"))).click()
                time.sleep(1)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='xaxisVar_7']"))).click()
                time.sleep(1)

                # Select Year
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/label"))).click()
                time.sleep(1)
                
                year_mapping = {
                    "2025": "//*[@id='selectedYear_1']",
                    "2024": "//*[@id='selectedYear_2']",
                    "2023": "//*[@id='selectedYear_3']",
                    "2022": "//*[@id='selectedYear_4']",
                    "2021": "//*[@id='selectedYear_5']",
                    "2020": "//*[@id='selectedYear_6']"
                }
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, year_mapping[selected_year]))).click()
                time.sleep(2)

                # Refresh 1
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button"))).click()
                time.sleep(4)

                # Open Filter Toggle
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[3]/div"))).click()
                time.sleep(2)

                # Select LMV and LPV
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[12]/td/label"))).click()
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[13]/td/label"))).click()
                time.sleep(1)

                # Refresh 2
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[1]/span/button"))).click()
                time.sleep(4)

                # Download
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a/img"))).click()
                
                # Wait for download to complete
                time.sleep(5) 

                # Rename and Move
                files = os.listdir(temp_dir)
                xlsx_files = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]
                
                # Sort by creation time to get the newest
                if xlsx_files:
                    full_paths = [os.path.join(temp_dir, f) for f in xlsx_files]
                    latest_file = max(full_paths, key=os.path.getctime)
                    
                    short_name = extract_rto_name(rto_name)
                    new_name = f"{short_name}_{selected_year}.xlsx"
                    new_path = os.path.join(temp_dir, new_name)
                    
                    # If we haven't already renamed this specific file
                    if latest_file != new_path:
                        os.rename(latest_file, new_path)
                        downloaded_files.append(new_path)
                
                # Clean up UI (Toggle Hide) for next loop
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='filterLayout']/div[1]/a"))).click()
                time.sleep(1)

            except Exception as e:
                st.error(f"Error processing {rto_name}: {str(e)}")
                continue

        progress_bar.progress(100)
        status_text.text("Scraping Completed!")
        
        return downloaded_files, temp_dir

    except Exception as e:
        st.error(f"Critical Error: {str(e)}")
        return [], temp_dir
    finally:
        if driver:
            driver.quit()

# --- STREAMLIT UI ---
st.title("🚗 Vahan RTO Data Downloader")

# Sidebar inputs
st.sidebar.header("Configuration")
selected_year = st.sidebar.selectbox("Select Year", ["2025", "2024", "2023", "2022", "2021", "2020"])

select_all = st.sidebar.checkbox("Select All RTOs")
if select_all:
    selected_rtos = st.sidebar.multiselect("Select RTOs", RTO_DATA, default=RTO_DATA)
else:
    selected_rtos = st.sidebar.multiselect("Select RTOs", RTO_DATA)

# Main Area
st.write(f"You have selected **{len(selected_rtos)}** RTOs for the year **{selected_year}**.")

if st.button("Start Scraping", type="primary"):
    if not selected_rtos:
        st.warning("Please select at least one RTO.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        files, temp_dir = scrape_vahan(selected_rtos, selected_year, progress_bar, status_text)
        
        if files:
            # Create a ZIP file of all downloaded data
            zip_filename = f"RTO_Data_{selected_year}.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in files:
                    zipf.write(file, os.path.basename(file))
            
            # Read Zip file into memory for download button
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📥 Download All Files (ZIP)",
                    data=f,
                    file_name=zip_filename,
                    mime="application/zip"
                )
            
            st.success(f"Successfully scraped {len(files)} files!")
        else:
            st.error("No files were downloaded. Please check the logs.")
        
        # Cleanup is tricky in web apps, usually temp dirs are cleaned by OS, 
        # but we can try to clean up if we want, strictly after the download button is generated.
