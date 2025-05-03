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
This script contains functions for processing of scraped data from Tata Power.
"""




# #############################################################################
# IMPORTS
# #############################################################################
import re
import requests

import pandas as pd

from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim


# #############################################################################
# MAIN
# #############################################################################
loc = Nominatim(user_agent="Geopy Library")
df = pd.read_csv("../../data/raw_data/company_tata_projects.csv")
projects_info = {
    "Project_Name": [],
    "Location": [],
    "Longitude": [],
    "Latitude": [],
    "Year": [],
    "Project_Size": [],
    "Project_Link": [],
    "Project_Image_Link": []
}
for idx, row in df.iterrows():
    project_name, location, year, project_size = None, None, None, None
    url = row["url"]
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    h2_tags = soup.find_all("h2")
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

    if project_name is None or project_name == "Impact":
        project_name = row["title"]

    projects_info["Project_Name"].append(project_name)
    projects_info["Location"].append(location)
    projects_info["Year"].append(year)
    projects_info["Project_Size"].append(project_size)
    long, lat = None, None
    if location is not None or location != "N/A":
        getLoc = loc.geocode(location)
        # printing address
        # print(getLoc.address)

        try:
            lat, long = getLoc.latitude, getLoc.longitude
        except:
            # This handles the error in geocoding of "village chandarva, gujarat"
            getLoc = loc.geocode(location.split(",")[1])
            lat, long = getLoc.latitude, getLoc.longitude
    projects_info["Latitude"].append(lat)
    projects_info["Longitude"].append(long)
    projects_info["Project_Link"].append(url)
    projects_info["Project_Image_Link"].append(row["img"])

info_df = pd.DataFrame(data=projects_info)
del projects_info

info_df = info_df.rename(
    columns={
        "Project_Name": "name",
        "Location": "state",
        "Longitude": "lon",
        "Latitude": "lat",
        "Year": "year",
        "Project_Size": "capacity",
        "Project_Link": "url",
        "Project_Image_Link": "image_url"
})
info_df["developer"] = "TATA Power"
info_df["source"] = "tata"
info_df.to_csv("../../data/processed_data/company_tata_projects_processed.csv", index=False)
