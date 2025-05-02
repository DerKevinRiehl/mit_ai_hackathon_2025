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
This runnable Python script & streamlit application renders the UI for our prototype in your browser.
You can run it in the terminal as follows:
    streamlit run app.py
"""




# #############################################################################
# IMPORTS
# #############################################################################
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from app_marker_generator import generate_popup_html




# #############################################################################
# STREAMLIT PAGE CONFIGRUATION
# #############################################################################
    # Streamlit page config
st.set_page_config(layout="wide")
st.title("🌞 Mr Sunshine India 🇮🇳: Mapping India’s Solar Infrastructure 🌞")




# #############################################################################
# DATA LOADING
# #############################################################################    
    # Sample dummy data — replace with real data source
@st.cache_data
def load_data():
    return pd.read_csv("dummy_data.csv")
data = load_data()




# #############################################################################
# VISUAL ELEMENTS
# #############################################################################    

# Define tab names
tab_names = [
    "Overview",
    "Current Projects",
    "Opportunities"
]
tabs = st.tabs(tab_names)

# Example: create a different map for each tab
for i, tab in enumerate(tabs):
    with tab:
        # Sidebar-like filters per tab
        st.header(f"🔍 Filter Projects ({tab_names[i]})")
        # You can customize filters per tab if needed
        states = st.multiselect("State", data['state'].unique(), default=data['state'].unique(), key=f"state_{i}")
        types = st.multiselect("Type", data['type'].unique(), default=data['type'].unique(), key=f"type_{i}")
        techs = st.multiselect("Technology", data['technology'].unique(), default=data['technology'].unique(), key=f"tech_{i}")
        bifacial = st.radio("Bifacial Modules", ["All", "Yes", "No"], index=0, key=f"bifacial_{i}")

        # Filter data for each tab (optional: filter by tab type)
        filtered = data[
            data['state'].isin(states) &
            data['type'].isin(types) &
            data['technology'].isin(techs)
        ]
        if bifacial != "All":
            filtered = filtered[filtered['bifacial'] == (bifacial == "Yes")]

        # Optionally, further filter by tab (e.g., only show utility-scale in tab 0)
        # Example:
        # if i == 0:
        #     filtered = filtered[filtered['project_category'] == "utility"]
        # elif i == 1:
        #     filtered = filtered[filtered['project_category'] == "rooftop"]
        # elif i == 2:
        #     filtered = filtered[filtered['project_category'] == "park"]

        # Create a map for each tab
        m = folium.Map(location=[21.0, 78.0], zoom_start=5)

        # Add markers
        for _, row in filtered.iterrows():
            popup_html = generate_popup_html(row)

            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
            ).add_to(m)

        # Display map for this tab
        st_data = st_folium(m, width="100%", height=800, key=f"map_{i}")
