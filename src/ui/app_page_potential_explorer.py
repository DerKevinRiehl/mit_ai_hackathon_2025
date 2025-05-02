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
This script contains functions for the markers.
"""




# #############################################################################
# IMPORTS
# #############################################################################
import folium
from app_marker_generator import generate_popup_html
import streamlit as st





# #############################################################################
# METHODS
# #############################################################################

def generate_filter_pane(i, data):
    states = st.multiselect("State", data['state'].unique(), default=data['state'].unique(), key=f"state_{i}")
    types = st.multiselect("Type", data['type'].unique(), default=data['type'].unique(), key=f"type_{i}")
    techs = st.multiselect("Technology", data['technology'].unique(), default=data['technology'].unique(), key=f"tech_{i}")
    bifacial = st.radio("Bifacial Modules", ["All", "Yes", "No"], index=0, key=f"bifacial_{i}")

    # Filtering must be done outside the columns (so both columns can use the result)
    filtered = data[
        data['state'].isin(states) &
        data['type'].isin(types) &
        data['technology'].isin(techs)
    ]
    if bifacial != "All":
        filtered = filtered[filtered['bifacial'] == (bifacial == "Yes")]
    return filtered

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