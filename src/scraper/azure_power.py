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
This script contains functions for the scraping of data from Azurepower:
    https://www.azurepower.com/project-overview?view_all=on&field_project_category_target_id%5B9%5D=9&field_project_category_target_id%5B10%5D=10&field_project_category_target_id%5B11%5D=11&field_project_locations_target_id%5B1%5D=1&field_project_locations_target_id%5B2%5D=2&field_project_locations_target_id%5B15%5D=15&field_project_locations_target_id%5B14%5D=14&field_project_locations_target_id%5B12%5D=12&field_project_locations_target_id%5B3%5D=3&field_project_locations_target_id%5B4%5D=4&field_project_locations_target_id%5B13%5D=13&field_project_locations_target_id%5B5%5D=5&field_project_locations_target_id%5B6%5D=6&field_project_locations_target_id%5B7%5D=7&field_project_locations_target_id%5B8%5D=8
"""




# #############################################################################
# IMPORTS
# #############################################################################

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# #############################################################################
# CONSTANTS
# #############################################################################

START_PAGE = "https://www.azurepower.com/project-overview?view_all=on&field_project_category_target_id%5B9%5D=9&field_project_category_target_id%5B10%5D=10&field_project_category_target_id%5B11%5D=11&field_project_locations_target_id%5B1%5D=1&field_project_locations_target_id%5B2%5D=2&field_project_locations_target_id%5B15%5D=15&field_project_locations_target_id%5B14%5D=14&field_project_locations_target_id%5B12%5D=12&field_project_locations_target_id%5B3%5D=3&field_project_locations_target_id%5B4%5D=4&field_project_locations_target_id%5B13%5D=13&field_project_locations_target_id%5B5%5D=5&field_project_locations_target_id%5B6%5D=6&field_project_locations_target_id%5B7%5D=7&field_project_locations_target_id%5B8%5D=8"
TARGET_FILE = "../../data/raw_data/company_azure_power_projects.csv"

# #############################################################################
# MAIN CODE
# #############################################################################

driver = webdriver.Chrome()
driver.get(START_PAGE)

html_pages = []

# ########## DOWNLOAD PAGES
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
        next_button = driver.find_element(By.XPATH, '//span[text()="Next ›"]')
        # Click the parent element (likely an <a> or <button>)
        parent = next_button.find_element(By.XPATH, './..')
        parent.click()
    except Exception:
        # "Next ›" not found, exit loop
        break

driver.quit()


# ########## PARSE CONTENT

company_data = []

for page in html_pages:
    parts = page.split("field-content")[1:]
    for part in parts:
        # GET IMG URL
        img_url = part.split("img src=\"")[1].split("\"")[0]

        # GET TITLE
        title = part.split("<h3 class=\"title\">")[1].split("</h3>")[0]

        # Get DETAILS
        rel_part = part.split("portfolio-lists list-unstyled mb-0")[1].split("</ul>")[0]
        project_size = rel_part.split("Project Size :")[1].split("</li>")[0].split("\">")[1].split("</")[0]
        commissioned = rel_part.split("Commissioned :")[1].split("</li>")[0].split("\">")[1].split("</")[0]
        offtaker = rel_part.split("Offtaker :")[1].split("</li>")[0].split("\">")[1].split("</")[0]
        location = rel_part.split("Project Location :")[1].split("</li>")[0].split("\">")[1].split("</")[0]
        if "Highlights :" in rel_part:
            highlights = rel_part.split("Highlights :")[1].split("</li>")[0].split("\">")[1].split("</")[0]
        else:
            highlights = None
        company_data.append([title, "AzurePower", img_url, project_size, commissioned, offtaker, location, highlights])
        
company_data = pd.DataFrame(company_data, columns=["title", "company", "img_url", "project_size", "commissioned", "offtaker", "location", "highlights"])
company_data.to_csv(TARGET_FILE, index=False)