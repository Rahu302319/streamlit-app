import streamlit as st
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration & Data ---
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

def extract_rto_name(rto_name):
    return rto_name.split()[0]

# --- Main Automation Logic ---
def run_automation(download_path, selected_year, selected_rto_names):
    status_box = st.empty()  # Placeholder for status updates
    
    # Ensure the path exists
    if not os.path.exists(download_path):
        try:
            os.makedirs(download_path)
        except OSError as e:
            st.error(f"Error creating directory: {e}")
            return

    # Set up Chrome options
    chrome_options = Options()
    # Note: If running on a cloud server (headless), uncomment the line below:
    # chrome_options.add_argument("--headless") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    status_box.info("Starting Browser...")

    try:
        url = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"
        driver.get(url)

        # 1. Initial Navigation
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]"))
        ).click()
        time.sleep(2)

        # Select State
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/ul/li[18]"))
        ).click()
        time.sleep(3)

        # Click Dropdown Icon
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/div[3]"))
        ).click()
        time.sleep(2)

        # Open Dropdown Panel
        dropdown_icon = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "selectedRto"))
        )
        dropdown_icon.click()
        time.sleep(2)

        # 2. Iterate through selected RTOs
        progress_bar = st.progress(0)
        total_rtos = len(selected_rto_names)

        for index, rto_name in enumerate(selected_rto_names):
            status_box.info(f"Processing: {rto_name} ({index + 1}/{total_rtos})")
            
            # Re-click dropdown if needed (sometimes DOM refreshes close it)
            try:
                dropdown_icon.click()
                time.sleep(1)
            except:
                pass # Already open or reference stale, continue to find options

            # Find and Click Option
            options = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#selectedRto_items .ui-selectonemenu-item"))
            )
            
            option_found = False
            for option in options:
                if option.text == rto_name:
                    option.click()
                    option_found = True
                    break
            
            if not option_found:
                st.warning(f"RTO '{rto_name}' not found in dropdown. Skipping.")
                continue

            time.sleep(2)

            # Axis Selections
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/div[3]"))).click()
            time.sleep(1)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='yaxisVar_4']"))).click()
            time.sleep(2)
            
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/label"))).click()
            time.sleep(2)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='xaxisVar_7']"))).click()
            time.sleep(2)

            # Year Selection
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/label"))).click()
            time.sleep(2)

            year_mapping = {
                "2025": "//*[@id='selectedYear_1']", "2024": "//*[@id='selectedYear_2']",
                "2023": "//*[@id='selectedYear_3']", "2022": "//*[@id='selectedYear_4']",
                "2021": "//*[@id='selectedYear_5']", "2020": "//*[@id='selectedYear_6']"
            }
            year_xpath = year_mapping.get(selected_year)
            if year_xpath:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, year_xpath))).click()
            else:
                st.error(f"Year {selected_year} mapping not found.")
                continue
            time.sleep(2)

            # Refresh Report
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button"))).click()
            time.sleep(5)

            # Toggle Table View
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[3]/div"))).click()
            except:
                st.warning("Could not click toggler, retrying or checking visibility.")

            time.sleep(2)

            # Checkboxes (LMV, LPV)
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[12]/td/label"))).click()
                time.sleep(1)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div[1]/div/div/div/table/tbody/tr[13]/td/label"))).click()
                time.sleep(1)
                
                # Refresh Table
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[1]/div[1]/span/button"))).click()
                time.sleep(5)
                
                # Download
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a/img"))).click()
                time.sleep(3)
                
                # Handle File Move
                default_download_dir = os.path.expanduser('~/Downloads')
                files = os.listdir(default_download_dir)
                if files:
                    downloaded_file = max([os.path.join(default_download_dir, f) for f in files], key=os.path.getctime)
                    extracted_name = extract_rto_name(rto_name)
                    new_file_name = f"{extracted_name}_{selected_year}.xlsx"
                    new_file_path = os.path.join(download_path, new_file_name)
                    
                    shutil.move(downloaded_file, new_file_path)
                    st.success(f"Downloaded: {new_file_name}")
                else:
                    st.error("No file found in Downloads folder.")

            except Exception as e:
                st.error(f"Error processing RTO table/download: {e}")

            # Reset Toggler for next iteration if needed
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='filterLayout']/div[1]/a"))).click()
                time.sleep(1)
            except:
                pass

            progress_bar.progress((index + 1) / total_rtos)

    except Exception as e:
        st.error(f"Global Automation Error: {e}")
    finally:
        driver.quit()
        status_box.success("Automation Complete!")

# --- Streamlit UI Layout ---
st.set_page_config(page_title="RTO Data Downloader", layout="wide")

st.title("🚗 RTO Data Automation")
st.markdown("This tool automates data extraction from the Vahan Dashboard.")

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    
    # Input for path (Text input instead of Dialog)
    download_path = st.text_input("Download Folder Path", placeholder=r"C:\Users\YourName\Desktop\RTO_Data")
    
    selected_year = st.selectbox("Select Year", ["2025", "2024", "2023", "2022", "2021", "2020"])
    
    # Multiselect is better than 100 checkboxes
    container = st.container()
    all_rtos = st.checkbox("Select All RTOs")
    
    if all_rtos:
        selected_rtos = container.multiselect("Select RTOs", RTO_DATA, default=RTO_DATA)
    else:
        selected_rtos = container.multiselect("Select RTOs", RTO_DATA)
    
    start_btn = st.button("Start Download", type="primary")

# Main Execution Area
if start_btn:
    if not download_path:
        st.error("Please enter a valid download folder path.")
    elif not selected_rtos:
        st.error("Please select at least one RTO.")
    else:
        st.warning("Do not close the browser window that opens. Please wait...")
        run_automation(download_path, selected_year, selected_rtos)
