import streamlit as st
import folium
from streamlit_folium import st_folium
import json

# Page config
st.set_page_config(layout="wide")
st.title("🗺️ Solar Detective: India Map with State Borders")

# Create folium map
m = folium.Map(location=[22.5, 78.0], zoom_start=5)

# Load GeoJSON (adjust filename if needed)
with open("Indian_States.json", "r", encoding="utf-8") as f:
    state_geo = json.load(f)

# Add state boundaries to map
folium.GeoJson(
    state_geo,
    name="State Borders",
    style_function=lambda x: {
        "fillColor": "#ffffff00",  # transparent fill
        "color": "#333333",
        "weight": 1.5,
    },
    tooltip=folium.GeoJsonTooltip(fields=["NAME_1"], aliases=["State:"])
).add_to(m)

# Render map inside Streamlit
st_data = st_folium(m, width=1000, height=600)