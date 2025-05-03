"""
"Mr Sunshine India" - "Solar Detective: Mapping Indiaâ€™s Solar Infrastructure Using Agentic AI"
-------------------------------------------
Authors:        Kevin Riehl <kriehl@ethz.ch>, Shaimaa El-Baklish <shaimaa.elbaklish@ivt.baug.ethz.ch>
Organization:   ETH ZÃ¼rich, Institute for Transportation Planning and Systems
Development:    2025
Submitted to:   MIT Global AI Hackathon 2025, 
                Track 01: Agentic AI for Dataset Building
                Challenge 02: "Solar Detective: Mapping Indiaâ€™s Solar Infrastructure Using Agentic AI"
-------------------------------------------
This script contains functions for the scraping of data from Renew:
    https://www.renew.com/global-presence
"""




# #############################################################################
# IMPORTS
# #############################################################################

import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# #############################################################################
# CONSTANTS
# #############################################################################

START_PAGE = "https://www.renew.com/global-presence"
TARGET_FILE = "../../data/raw_data/company_renew_projects.csv"

# #############################################################################
# MAIN CODE
# #############################################################################



# DOWNLOAD SOLAR ONLY

PAGE_SOLAR = ""

driver = webdriver.Chrome()
driver.get(START_PAGE)

time.sleep(1)
element = driver.find_elements(By.CLASS_NAME, "category-drop")[2]
driver.execute_script("arguments[0].scrollIntoView();", element)
time.sleep(1)
#element.click()
#driver.find_element(By.XPATH, '//li[contains(@class, "filter_btn") and (normalize-space(text())="solar")]').click()
#time.sleep(10)

# CLICK MORE
while True:
    # 1. Wait until the page is loaded (wait for a known element, e.g., the "Next ›" button or any stable element)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        print("Page did not load in time:", e)
        break

    # 2. Try to find the "Next ›" button by its visible text in a <span>
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'load_more_button'))
        )
        #next_button = driver.find_element(By.NAME, 'load_more_button')
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", next_button)
    except Exception:
        # "Next ›" not found, exit loop
        break
    time.sleep(5)
PAGE_SOLAR = driver.page_source

driver.quit()





# ########## PARSE CONTENT

company_data = []

parts = PAGE_SOLAR.split("<div class=\"filterDiv")[1:]
for part in parts:
    title = part.split("filter_lg_head\">")[1].split("</span>")[0]
    category = part.split("Category :")[1].split("</p>")[0].split("<p>")[1].strip()
    types = part.split("Type :")[1].split("</p>")[0].split("<p>")[1].strip()
    location = part.split("Location :")[1].split("</p>")[0].split("<p>")[1].strip()
    capacity = part.split("Capacity :")[1].split("</p>")[0].split("<p>")[1].strip()
    company_data.append([title, category, types, location, capacity])
    
company_data = pd.DataFrame(company_data, columns=["title", "category", "types", "location", "capacity"])
company_data.to_csv(TARGET_FILE, index=False)