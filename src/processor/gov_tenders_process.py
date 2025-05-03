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
import os
import sys
import re
import random
import requests

import pandas as pd

from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim


# #############################################################################
# FUNCTIONS
# #############################################################################
def get_random_location_in_india():
    # India is roughly between latitudes 6°N and 37°N, and longitudes 68°E and 97°E
    latitude_min, latitude_max = 6, 37
    longitude_min, longitude_max = 68, 97
    
    # Generate random latitude and longitude within the defined bounds
    random_lat = random.uniform(latitude_min, latitude_max)
    random_lon = random.uniform(longitude_min, longitude_max)
    
    return random_lat, random_lon

# #############################################################################
# MAIN
# #############################################################################
loc = Nominatim(user_agent="Geopy Library")
df = pd.read_csv("../../data/raw_data/gov_tenders.csv")
print(df.columns)

df["location"] = pd.NA
df["lat"] = pd.NA
df["lon"] = pd.NA
df["drop"] = 0
for idx, row in df.iterrows():
    if "solar" not in row["tender_details"].lower():
        df.loc[idx, "drop"] = 1
        continue

    location_match = re.search(
        r'(?:at|in)\s+([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*(?:,\s*[A-Z][a-zA-Z]*)?)',
        row["tender_details"]
    )
    location = location_match.group(1).strip() if location_match else "N/A"
    # Handle the case of New Delhi
    if location.split(", ")[-1] == "New":
        location_match = re.search(
            r'(?:at|in)\s+([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*(?:,\s*New\s+[A-Z][a-zA-Z]*)(?:,\s*[A-Z][a-zA-Z]*)?)',
            row["tender_details"]
        )
        location = location_match.group(1).strip() if location_match else "N/A"
    if location != "N/A" and location != "India":
        try:
            getLoc = loc.geocode(location)
            lat, long = getLoc.latitude, getLoc.longitude
        except:
            # handle case of "SECI, New Delhi"
            try:
                getLoc = loc.geocode(location.split(", ")[-1])
                lat, long = getLoc.latitude, getLoc.longitude
            except:
                # handle case of "NDRF Academy Nagpur Campus"
                try:
                    getLoc = loc.geocode(location.split(" ")[2])
                    lat, long = getLoc.latitude, getLoc.longitude
                except:
                    # if fail, random location
                    location = "India"
                    lat, long = get_random_location_in_india()
    else:
        # random location
        location = "India"
        lat, long = get_random_location_in_india()
    df.loc[idx, "location"] = location
    df.loc[idx, "lat"] = lat
    df.loc[idx, "lon"] = long

df = df[df["drop"] == 0]
df = df.drop(columns="drop")
df.to_csv("../../data/processed_data/gov_tenders_processed.csv", index=False)