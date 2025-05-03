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
This script contains functions for processing of scraped data from renew.
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
df = pd.read_csv("../../data/raw_data/company_renew_projects.csv")
df = df[df["types"].isin(["solar", "Solar/Wind"])]

# Now merge with data_processed
# name,lat,lon,state,capacity,developer,year,
# type,technology,bifacial,grid,manufacturer,offtake,
# financing,performance,irradiance,grid_proximity,image_url
df = df.rename(
    columns={
        "title": "name",
        "location": "state",
        "category": "type",
    }
)
df["developer"] = "ReNew"
df["source"] = "renew"
df["lat"] = pd.NA
df["lon"] = pd.NA

for idx, row in df.iterrows():
    getLoc = loc.geocode(row["state"])
    df.loc[idx, "lat"], df.loc[idx, "lon"] = getLoc.latitude, getLoc.longitude

df.to_csv("../../data/processed_data/company_renew_projects_processed.csv", index=False)