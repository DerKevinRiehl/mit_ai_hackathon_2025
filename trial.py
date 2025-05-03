import sys

"""
from geopy.geocoders import Nominatim


loc = Nominatim(user_agent="Geopy Library")
getLoc = loc.geocode("Chengmari, West Bengal")

# printing address
print(getLoc.address)

# printing latitude and longitude
print("Latitude = ", getLoc.latitude, "\n")
print("Longitude = ", getLoc.longitude)
"""

import requests
from bs4 import BeautifulSoup
import re

import pandas as pd


df = pd.read_csv("./data/raw_data/company_tata_projects.csv")
project_name, location, year, project_size = None, None, None, None
for idx, row in df.iterrows():
    url = row["url"]
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    h2_tags = soup.find_all("h2")

    # Print the text inside each h2 tag
    #for tag in h2_tags:
    #    print(tag.get_text(strip=True))

    try:
        project_name = h2_tags[2].get_text(strip=True)
        location = h2_tags[3].get_text(strip=True)
        year = h2_tags[4].get_text(strip=True)
        project_size = h2_tags[5].get_text(strip=True)
    except:
        # Get project description
        desc_block = soup.find("div", class_="container")
        paragraphs = desc_block.find_all("p") if desc_block else []
        full_text = " ".join(p.get_text(strip=True) for p in paragraphs)
        # Extract data using regex
        project_size = re.search(r'(\d+)\s*MW', full_text)
        year = re.search(r'(\d{4})', full_text)
        location_matches = re.findall(
            r'(?:at|in)\s+([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*(?:,\s*[A-Z][a-zA-Z]*)?)',
            full_text
        )

        # Choose the longest match from the list
        location = max(location_matches, key=len) if location_matches else "N/A"


        # Clean results
        project_size = project_size.group(1) + " MW" if project_size else "N/A"
        year = year.group(1) if year else "N/A"
        #location = location_match.group(1).strip() if location_match else "N/A"

    if project_name is None or project_name == "Impact":
        project_name = row["title"]
    
    print("Project Name:", project_name)
    print("Location:", location)
    print("Year:", year)
    print("Project Size:", project_size)
    print()

    project_name, location, year, project_size = None, None, None, None

    #sys.exit(1)

sys.exit(1)

START_PAGE = "https://www.tatapower.com/renewables/solar-energy#tabs-9975c704ed-item-2a3f25ad7e-tab"

PAGE_SOLAR = ""

driver = webdriver.Chrome()
driver.get(START_PAGE)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
except Exception as e:
    print("Page did not load in time:", e)

PAGE = driver.page_source

driver.quit()

company_data = []
parts = PAGE.split("leadership-card")[2:14]
for part in parts:
    title = part.split("leadership-person-name\">")[1].split("</p>")[0]
    img = "https://www.tatapower.com/"+part.split("src=\"")[1].split("\"")[0]
    url = "https://www.tatapower.com/"+part.split("href=\"")[1].split("\"")[0]

    company_data.append([title, img, url])