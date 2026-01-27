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
    
    # --- CRITICAL FIX: HARDCODE PATHS FOR STREAMLIT CLOUD ---
    chrome_options.binary_location = "/usr/bin/chromium"
    
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Set default download directory
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Use system installed chromedriver
    service = Service("/usr/bin/chromedriver")
    
    return webdriver.Chrome(service=service, options=chrome_options)

def extract_rto_name(rto_name):
    # Extract the first part of the RTO name before "SRTO" or "RTO"
    return rto_name.split()[0]

def scrape_vahan(selected_rtos, selected_year, progress_bar, status_text):
    temp_dir = tempfile.mkdtemp()
    driver = None
    downloaded_files = []

    try:
        driver = get_driver(temp_dir)
        driver.set_page_load_timeout(600)
        
        url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"
        driver.get(url)
        
        status_text.text("Navigating to dashboard...")
        
        # Wait for page to load - Click Dashboard
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]"))
        ).click()
        time.sleep(2)

        # Select State (KL)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/ul/li[18]"))
        ).click()
        time.sleep(3)

        total_rtos = len(selected_rtos)
        
        for idx, rto_name in enumerate(selected_rtos):
            try:
                status_text.text(f"Processing ({idx+1}/{total_rtos}): {rto_name}")
                progress_bar.progress((idx) / total_rtos)
                
                # --- RTO Selection Logic ---
                
                # 1. Click Dropdown Arrow
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/div[3]"))
                ).click()
                time.sleep(2)

                # 2. Click The RTO Input Field to open panel
                dropdown_trigger = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "selectedRto"))
                )
                dropdown_trigger.click()
                time.sleep(2)

                # 3. Find specific RTO in list
                options = WebDriverWait(driver, 60).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#selectedRto_items .ui-selectonemenu-item"))
                )
                
                option_found = False
                for option in options:
                    if option.text.strip() == rto_name:
                        option.click()
                        option_found = True
                        break
                
                if not option_found:
                    st.warning(f"RTO {rto_name} not found in list.")
                    continue
                    
                time.sleep(2)

                # --- CONFIGURATION LOGIC ---

                # Y Axis -> Maker
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[3]"))
                ).click()
                time.sleep(1)
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='yaxisVar_4']"))
                ).click()
                time.sleep(1)

                # X Axis -> Month
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/label"))
                ).click()
                time.sleep(1)
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='xaxisVar_7']"))
                ).click()
                time.sleep(1)

                # Year Selection
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/label"))
                ).click()
                time.sleep(1)

                year_mapping = {
                    "2025": "//*[@id='selectedYear_1']",
                    "2024": "//*[@id='selectedYear_2']",
                    "2023": "//*[@id='selectedYear_3']",
                    "2022": "//*[@id='selectedYear_4']",
                    "2021": "//*[@id='selectedYear_5']",
                    "2020": "//*[@id='selectedYear_6']"
                }
                
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, year_mapping[selected_year]))
                ).click()
                time.sleep(2)

                # Refresh Button
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button"))
                ).click()
                time.sleep(5)

                # Toggle Filters
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

                # Refresh Table
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[1]/span/button"))
                ).click()
                time.sleep(5)

                # Download Excel
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a/img"))
                ).click()
                time.sleep(3)

                # --- FILE HANDLING ---
                # Check for new file in temp_dir
                files = os.listdir(temp_dir)
                xlsx_files = [f for f in files if f.endswith('.xlsx') or f.endswith('.xls')]
                
                if xlsx_files:
                    # Get the most recently created file
                    full_paths = [os.path.join(temp_dir, f) for f in xlsx_files]
                    latest_file = max(full_paths, key=os.path.getctime)
                    
                    # Rename logic
                    extracted_name = extract_rto_name(rto_name)
                    new_file_name = f"{extracted_name}_{selected_year}.xlsx"
                    new_file_path = os.path.join(temp_dir, new_file_name)
                    
                    # Avoid renaming if already renamed (in case of re-runs)
                    if latest_file != new_file_path:
                        shutil.move(latest_file, new_file_path)
                        downloaded_files.append(new_file_path)
                
                # Toggle Hide Filter (Clean up for next loop)
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='filterLayout']/div[1]/a"))
                ).click()
                time.sleep(1)

            except Exception as e:
                st.error(f"Error processing {rto_name}: {str(e)}")
                # Attempt to recover by reloading page? Or just continue
                continue

        progress_bar.progress(100)
        status_text.text("Scraping Completed!")
        return downloaded_files, temp_dir

    except Exception as e:
        st.error(f"Critical System Error: {str(e)}")
        return [], temp_dir
    finally:
        if driver:
            driver.quit()

# --- STREAMLIT UI ---
st.title("Vahan Data Scraper (Headless)")

st.sidebar.header("Configuration")
selected_year = st.sidebar.selectbox("Select Year", ["2025", "2024", "2023", "2022", "2021", "2020"])

select_all = st.sidebar.checkbox("Select All RTOs")
if select_all:
    selected_rtos = st.sidebar.multiselect("Select RTOs", RTO_DATA, default=RTO_DATA)
else:
    selected_rtos = st.sidebar.multiselect("Select RTOs", RTO_DATA)

st.write(f"Selected **{len(selected_rtos)}** RTOs for Year **{selected_year}**")

if st.button("Start Scraping", type="primary"):
    if not selected_rtos:
        st.warning("Please select at least one RTO.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        files, temp_dir = scrape_vahan(selected_rtos, selected_year, progress_bar, status_text)
        
        if files:
            # Zip the files
            zip_filename = f"RTO_Data_{selected_year}.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in files:
                    zipf.write(file, os.path.basename(file))
            
            # Create Download Button
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📥 Download All Files (ZIP)",
                    data=f,
                    file_name=zip_filename,
                    mime="application/zip"
                )
            st.success(f"Successfully downloaded {len(files)} files.")
        else:
            st.error("No files were downloaded. Please check the logs.")
