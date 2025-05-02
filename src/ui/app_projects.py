"""
"Mr Sunshine India" - "Solar Detective: Mapping India’s Solar Infrastructure Using Agentic AI"
-------------------------------------------
Authors:        Kevin Riehl <kriehl@ethz.ch>, Shaimaa El-Baklish <shaimaa.elbaklish@ivt.baug.ethz.ch>
Organization:   ETH Zürich, Institute for Transportation Planning and Systems
Development:    2025
Submitted to:   MIT Global AI Hackathon 2025, 
                Track 01: Agentic AI for Dataset Building
                Challenge 02: "Solar Detective: Mapping India’s Solar Infrastructure Using Agentic AI"
-------------------------------------------
This script contains functions for the markers.
"""




# #############################################################################
# IMPORTS
# #############################################################################
import pandas as pd
import folium
from app_marker_generator import generate_popup_html





# #############################################################################
# METHODS
# #############################################################################

def generate_map(i, filtered, st_folium):
    m = folium.Map(location=[21.0, 78.0], zoom_start=5)
    for _, row in filtered.iterrows():
        popup_html = generate_popup_html(row)
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
        ).add_to(m)
    st_folium(m, width="100%", height=700, key=f"map_{i}")