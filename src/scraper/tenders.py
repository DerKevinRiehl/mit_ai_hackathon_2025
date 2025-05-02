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
This script contains functions for the scraping of data from TENDERS:
    https://www.seci.co.in/view/publish/tender?tender=all
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

START_PAGE = "https://www.seci.co.in/view/publish/tender?tender=all"
TARGET_FILE = "../../data/raw_data/gov_tenders.csv"

# #############################################################################
# MAIN CODE
# #############################################################################

driver = webdriver.Chrome()
driver.get(START_PAGE)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
except Exception as e:
    print("Page did not load in time:", e)
    

# ########## DOWNLOAD PAGES
html_pages = []
while True:
    # 1. Wait until the page is loaded (wait for a known element, e.g., the "Next ›" button or any stable element)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        print("Page did not load in time:", e)
        break

    # 2. Get and store the HTML
    html_pages.append(driver.page_source)

    # 3. Try to find the "Next ›" button by its visible text in a <span>
    try:
        next_button = driver.find_element(By.XPATH, "//*[text()='Next']")
        next_button.click()
    except Exception:
        # "Next ›" not found, exit loop
        break

    time.sleep(2)
    
driver.quit()


# ########## PARSE CONTENT

company_data = []
for page in html_pages:
    tbl = page.split("</table>")[0].split("<table")[1]
    parts = tbl.split("<tr ")[2:]
    for part in parts:
        row_parts = part.split("<td>")[1:]
        row_parts = [r.split("</td>")[0].strip() for r in row_parts]
        s_no = row_parts[0]
        tender_id = row_parts[1]
        tender_id2 = row_parts[2]
        tender_ref = row_parts[3]
        tender_title = row_parts[4]
        tender_date = row_parts[5]
        tender_details = row_parts[6]
        tender_corrigendum = "https://www.seci.co.in/"+row_parts[7].split("href=\"")[1].split("\"")[0]
        company_data.append([s_no, tender_id, tender_id2, tender_ref, tender_title, tender_details, tender_date, tender_corrigendum ])

company_data = pd.DataFrame(company_data, columns=["s_no", "tender_id", "tender_id2", "tender_ref", "tender_title", "tender_date", "tender_details", "tender_corrigendum"])
company_data.to_csv(TARGET_FILE, index=False)