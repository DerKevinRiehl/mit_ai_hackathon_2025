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
import pandas as pd

from geopy.geocoders import Nominatim


# #############################################################################
# MAIN
# #############################################################################

loc = Nominatim(user_agent="Geopy Library")
df = pd.read_csv("../../data/raw_data/company_azure_power_projects.csv")

# Now merge with data_processed
# name,lat,lon,state,capacity,developer,year,
# type,technology,bifacial,grid,manufacturer,offtake,
# financing,performance,irradiance,grid_proximity,image_url

df = df.rename(
    columns={
        "title": "name",
        "company": "developer",
        "offtaker": "offtake",
        "project_size": "capacity",
        "img_url": "image_url",
        "commissioned": "year",
    }
)
df["str_split"] = df["location"].str.split(",")
df["state"] = df["str_split"].apply(lambda x: x[-1] if len(x) > 1 else x[0])
df = df.drop(columns=["str_split"])

for idx, row in df.iterrows():
    location = row["location"]
    location = location.replace("Dist: ", "").replace("(", "").replace(")", "")
    location_splits = location.split(", ")
    if len(location_splits) > 2:
        location = location_splits[-2] + ", " + location_splits[-1]
    try:
        getLoc = loc.geocode(location)
        df.loc[idx, "lat"], df.loc[idx, "lon"] = getLoc.latitude, getLoc.longitude
    except:
        # This is error handling for Semaliya, Gujarat and Sabarkatha, Gujarat and West Champaran Bettiah, Bihar
        # make location to that of state
        getLoc = loc.geocode(row["state"])
        df.loc[idx, "lat"], df.loc[idx, "lon"] = getLoc.latitude, getLoc.longitude

df = df.drop(columns=["location"])
df["developer"] = "Azure Power"
df["source"] = "azure"
df.to_csv("../../data/processed_data/company_azure_power_projects_processed.csv", index=False)