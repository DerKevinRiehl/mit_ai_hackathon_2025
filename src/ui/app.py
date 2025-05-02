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
import base64
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from app_marker_generator import generate_popup_html
import app_projects
from app_banner import generate_banner


# #############################################################################
# STREAMLIT PAGE CONFIGRUATION
# #############################################################################

    # Streamlit page config
st.set_page_config(layout="wide")




# #############################################################################
# DATA LOADING
# #############################################################################    
    # Sample dummy data — replace with real data source
@st.cache_data
def load_data():
    return pd.read_csv("dummy_data.csv")
data = load_data()




# #############################################################################
# USER INTERFACE LAYOUT
# #############################################################################    

# ########### BANNER
generate_banner()

# ########### TABS
tab_names = [
    "🗺️ Projects Overview",
    "☀️ Solar Potential Explorer",
    "💰 Investment Navigator",
    "📄 Tender Navigator"
]
tabs = st.tabs(tab_names)

# ########### PROJECTS OVERVIEW
i = 0
with tabs[0]:
    col1, col2 = st.columns([2, 5])  # Adjust the ratio as needed

    # Filter Pane
    with col1:
        st.header(f"🔍 Filter Projects")
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

    # Map
    with col2:
        app_projects.generate_map(i, filtered, st_folium)

# ########### SOLAR POTENTIAL EXPLORER
i = 1
with tabs[1]:
    # Create two columns: left for filters, right for map
    col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed

    with col1:
        st.header(f"🔍 Filter Projects")
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

    with col2:
        m = folium.Map(location=[21.0, 78.0], zoom_start=5)
        for _, row in filtered.iterrows():
            popup_html = generate_popup_html(row)
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
            ).add_to(m)
        st_folium(m, width="100%", height=700, key=f"map_{i}")

# ########### INVESTMENT NAVIGATOR
i = 2
with tabs[2]:
    # Create two columns: left for filters, right for map
    col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed

    with col1:
        st.header(f"🔍 Filter Projects")
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

    with col2:
        m = folium.Map(location=[21.0, 78.0], zoom_start=5)
        for _, row in filtered.iterrows():
            popup_html = generate_popup_html(row)
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
            ).add_to(m)
        st_folium(m, width="100%", height=700, key=f"map_{i}")

# ########### TENDER NAVIGATOR
i = 3
with tabs[3]:
    # Create two columns: left for filters, right for map
    col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed

    with col1:
        st.header(f"🔍 Filter Projects")
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

    with col2:
        m = folium.Map(location=[21.0, 78.0], zoom_start=5)
        for _, row in filtered.iterrows():
            popup_html = generate_popup_html(row)
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
            ).add_to(m)
        st_folium(m, width="100%", height=700, key=f"map_{i}")