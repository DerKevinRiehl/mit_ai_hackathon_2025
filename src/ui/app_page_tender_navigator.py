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
    import streamlit as st

    # Fake State filter (hardcoded Indian states)
    fake_states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
        "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
        "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
        "West Bengal"
    ]
    # states = st.multiselect(
    #     "State", fake_states, default=fake_states, key=f"state_{i}"
    # )
    # Single-select State with "All" option (moved here)
    state = st.selectbox(
        "State",
        options=["All", *fake_states],
        index=0,
        key=f"state_{i}"
    )

    # Fake Date of Publication filter (2025)
    fake_dates = [f"2025-{str(month).zfill(2)}" for month in range(1, 13)]
    publication_date = st.selectbox(
        "Date of Publication", fake_dates, key=f"date_{i}"
    )

    # Fake Volume filter
    fake_volumes = [f"Volume [USD] {v}" for v in range(1, 11)]
    volume = st.slider(
        "Volume [USD]", min_value=1, max_value=10, value=5, key=f"volume_{i}"
    )
    # No real filtering, just return the original data
    return data

def generate_map(i, filtered, st_folium):
    m = folium.Map(location=[21.0, 78.0], zoom_start=5)
    for _, row in filtered.iterrows():
        # popup_html = generate_popup_html(row)
        folium.Marker(
            location=[row['lat'], row['lon']],
            # popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
        ).add_to(m)
    st_folium(m, width="100%", height=700, key=f"map_{i}")