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




# #############################################################################
# STREAMLIT PAGE CONFIGRUATION
# #############################################################################
# Streamlit page config
st.set_page_config(layout="wide")
st.title("🌞 Mr Sunshine India: Mapping India’s Solar Infrastructure 🌞")


# Sample dummy data — replace with real data source
"""
data = pd.DataFrame([
    {
        'name': 'Solar Park A',
        'lat': 28.7041,
        'lon': 77.1025,
        'state': 'Delhi',
        'capacity': 100,
        'developer': 'ABC Solar Ltd.',
        'year': 2020,
        'type': 'Utility-scale',
        'technology': 'c-Si',
        'bifacial': True,
        'grid': '132kV Substation A',
        'manufacturer': 'XYZ Panels Co.',
        'offtake': 'PPA',
        'financing': 'ADB loan (public)',
        'performance': '95% avg CUF',
        'irradiance': '5.2 kWh/m²/day',
        'grid_proximity': '1.2 km',
        'image_url': 'https://via.placeholder.com/150'
    },
    {
        'name': 'Rooftop B',
        'lat': 19.0760,
        'lon': 72.8777,
        'state': 'Maharashtra',
        'capacity': 2,
        'developer': 'GreenHomes',
        'year': 2022,
        'type': 'Rooftop',
        'technology': 'CdTe',
        'bifacial': False,
        'grid': 'Low-voltage net meter',
        'manufacturer': 'ThinFilmTech',
        'offtake': 'Net Metering',
        'financing': 'Private Equity',
        'performance': '88% CUF',
        'irradiance': '4.8 kWh/m²/day',
        'grid_proximity': 'Direct',
        'image_url': 'https://via.placeholder.com/150'
    },
    {
        'name': 'Floating Solar C',
        'lat': 13.0827,
        'lon': 80.2707,
        'state': 'Tamil Nadu',
        'capacity': 10,
        'developer': 'SunFloat Energy',
        'year': 2021,
        'type': 'Floating',
        'technology': 'c-Si',
        'bifacial': True,
        'grid': '220kV Transmission',
        'manufacturer': 'SunTech',
        'offtake': 'Merchant Market',
        'financing': 'World Bank-backed',
        'performance': '90% CUF',
        'irradiance': '5.5 kWh/m²/day',
        'grid_proximity': '0.5 km',
        'image_url': 'https://via.placeholder.com/150'
    }
])
"""
@st.cache_data
def load_data():
    return pd.read_csv("dummy_data.csv")

data = load_data()


# Sidebar filters
st.sidebar.header("🔍 Filter Projects")
states = st.sidebar.multiselect("State", data['state'].unique(), default=data['state'].unique())
types = st.sidebar.multiselect("Type", data['type'].unique(), default=data['type'].unique())
techs = st.sidebar.multiselect("Technology", data['technology'].unique(), default=data['technology'].unique())
bifacial = st.sidebar.radio("Bifacial Modules", ["All", "Yes", "No"], index=0)

# Apply filters
filtered = data[
    data['state'].isin(states) &
    data['type'].isin(types) &
    data['technology'].isin(techs)
]

if bifacial != "All":
    filtered = filtered[filtered['bifacial'] == (bifacial == "Yes")]


# Create folium map
m = folium.Map(location=[21.0, 78.0], zoom_start=5)

# Add markers
for _, row in filtered.iterrows():
    popup_html = f"""
    <b>{row['name']}</b><br>
    <img src="{row['image_url']}" width="150"><br><br>
    <b>Capacity:</b> {row['capacity']} MW<br>
    <b>Developer:</b> {row['developer']}<br>
    <b>Commissioned:</b> {row['year']}<br>
    <b>Type:</b> {row['type']}<br>
    <b>Technology:</b> {row['technology']} ({'Bifacial' if row['bifacial'] else 'Monofacial'})<br>
    <b>Grid:</b> {row['grid']}<br>
    <b>Manufacturer:</b> {row['manufacturer']}<br>
    <b>Offtake:</b> {row['offtake']}<br>
    <b>Financing:</b> {row['financing']}<br>
    <b>Performance:</b> {row['performance']}<br>
    <b>Irradiance:</b> {row['irradiance']}<br>
    <b>Grid Proximity:</b> {row['grid_proximity']}<br>
    """
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
    ).add_to(m)

# Display map
st_data = st_folium(m, width=900, height=600)
