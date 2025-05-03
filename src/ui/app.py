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
import pandas as pd
import json

import streamlit as st
from streamlit_folium import st_folium

from app_banner import generate_banner

import app_page_projects
import app_page_potential_explorer
import app_page_investment_navigator
import app_page_tender_navigator




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
    dummy_data = pd.read_csv("../../data/dummy_data.csv")
    # Investment Data
    investment_data = pd.read_excel("../../data/geography/india_climate_energy_dashboard/IndiaClimateEnergyDashboard_Complete.xlsx", header=1)
    return dummy_data, investment_data
data, investment_data = load_data()

    # Load Shapes
with open("../../data/geography/Indian_States.json", "r", encoding="utf-8") as f:
    state_geo = json.load(f)


investment_data_columns = ['Installed Capacity [loc]', 'Installed Capacity [dec]',
       'Hydro', 'Nuclear', 'RES', 'Thermal', 'Central', 'Private', 'State.1',
       'Rooftop Solar Capacity', 'Generation', 'Peak Demand',
       'Electricity Sales', 'AT&C Losses', 'ACS-ARR (Electricity Sales) Gap',
       'GDP [ConstPrice]', 'GDP [CurrPrice]', 'SectoralGVA [ConstPrice]',
       'SectoralGVA [CurrPrice]', 'Population', 'IncomePerCapita [CurrPrice]',
       'IncomePerCapita [ConstPrice]', 'NO2', 'SO2', 'PMO', 'PM25']
investment_data = investment_data.iloc[2:]
for col in investment_data_columns:
    investment_data[col] = investment_data[col].astype(float)
    
# import sys
# sys.exit(0)

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
        st.markdown("#### 🔍 Filter Projects")
        with st.container(height=600):  # Adjust height as needed
            filtered = app_page_projects.generate_filter_pane(i, data)

    # Map
    with col2:
        app_page_projects.generate_map(i, filtered, st_folium)

# ########### SOLAR POTENTIAL EXPLORER
i = 1
with tabs[1]:
    col1, col2 = st.columns([2, 5])  # Adjust the ratio as needed

    # Filter Pane
    with col1:
        st.markdown("#### 🔍 Filter Factors")
        with st.container(height=600):  # Adjust height as needed
            filtered = app_page_potential_explorer.generate_filter_pane(i, data)

    # Map
    with col2:
        app_page_potential_explorer.generate_map(i, filtered, st_folium)

# ########### INVESTMENT NAVIGATOR
i = 2
with tabs[2]:
    col1, col2, col3 = st.columns([2, 5, 2])  # Adjust the ratio as needed

    # Filter Pane
    with col1:
        st.markdown("#### 🔍 Your Company Details")
        with st.container(height=600):  # Adjust height as needed
            filtered = app_page_investment_navigator.generate_filter_pane(i, data, investment_data)
        
    # Map
    with col2:
        app_page_investment_navigator.generate_map(i, filtered, st_folium, state_geo)

    # Calculator
    with col3:
        st.markdown("#### 🔍 Projected Business Statement")
        #with st.container(height=600):  # Adjust height as needed
        #    app_page_investment_navigator.generate_filter_pane(i, data)
        
# ########### TENDER NAVIGATOR
i = 3
with tabs[3]:
    col1, col2 = st.columns([2, 5])  # Adjust the ratio as needed

    with col1:
        # Filter Pane (top 50%)
        st.markdown("#### 🔍 Find Tenders")
        with st.container(height=250):  # Adjust height as needed
            filtered = app_page_tender_navigator.generate_filter_pane(i, data)

        # Scrollable Results (bottom 50%)
        st.markdown("#### 📋 Tenders")
        with st.container(height=250):  # Adjust height as needed
            if filtered.empty:
                st.info("No tenders match the selected filters.")
            else:
                for idx, row in filtered.iterrows():
                    st.markdown(
                        f"""
                        <div style="padding:8px 0; border-bottom:1px solid #eee;">
                            <b>{row['name']}</b> <br>
                            <span style="color: #888;">{row['state']}, {row['year']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    with col2:
        app_page_tender_navigator.generate_map(i, filtered, st_folium)