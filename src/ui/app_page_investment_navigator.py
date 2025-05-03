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
import branca




# #############################################################################
# METHODS
# #############################################################################

def generate_filter_pane(i, data, investment_data):
    # states = st.multiselect("State", data['state'].unique(), default=data['state'].unique(), key=f"state_{i}")
    # types = st.multiselect("Type", data['type'].unique(), default=data['type'].unique(), key=f"type_{i}")
    # techs = st.multiselect("Technology", data['technology'].unique(), default=data['technology'].unique(), key=f"tech_{i}")
    # bifacial = st.radio("Bifacial Modules", ["All", "Yes", "No"], index=0, key=f"bifacial_{i}")

    # Top-level selection
    top_choice = st.radio("Select Factor:", ["Investment Potential Score", "Electricity", "Economy & Demographics", "Emissions"], index=0)
    selected = None

    if top_choice == "Electricity":
        sub_selected = st.radio("Select Aspect:", [
                                          "Installed Capacity [loc]", "Installed Capacity [dec]", "Hydro",
                                          "Nuclear", "RES", "Thermal", "Central", "Private", 
                                          "State", "Rooftop Solar Capacity", "Generation", "Peak Demand", "Electricity Sales", "AT&C Losses",  "ACS-ARR (Electricity Sales) Gap"
                                          ])
        selected = "electricity"
        st.write(f"Selected: {selected}, Sub-selection: {sub_selected}")
    elif top_choice=="Economy & Demographics":
        sub_selected = st.radio("Select Aspect:", [
                                            "GDP [ConstPrice]", "GDP [CurrPrice]", "SectoralGVA [ConstPrice]", "SectoralGVA [CurrPrice]", "Population", "IncomePerCapita [CurrPrice]", "IncomePerCapita [ConstPrice]"
                                          ])
        selected = "economy"
        st.write(f"Selected: {selected}, Sub-selection: {sub_selected}")
    elif top_choice=="Emissions":
        sub_selected = st.radio("Select Aspect:", [
                                            "NO2", "SO2", "PMO", "PM25"
                                          ])
        selected = "emissions"
        st.write(f"Selected: {selected}, Sub-selection: {sub_selected}")
    else:
        selected = "total"
        sub_selected = "total_score"
        st.write("No selection.")
        
    # Filtering must be done outside the columns (so both columns can use the result)
    # st.write(investment_data.columns)
    if sub_selected in investment_data.columns:
        filtered = investment_data[["State", sub_selected]]
    else:
        sub_selected = "Population"
    filtered = investment_data[["State", sub_selected]]
    filtered = filtered.rename(columns={sub_selected: "value"})
    return filtered

def generate_map(i, filtered, st_folium, state_geo):
    # Drop NaNs
    filtered = filtered.dropna(subset=["value"])

    # 1. Prepare mapping
    state_value_dict = dict(zip(filtered["State"], filtered["value"]))
    if filtered["value"].nunique() == 1:
        min_val = filtered["value"].iloc[0] - 1
        max_val = filtered["value"].iloc[0] + 1
    else:
        min_val = filtered["value"].min()
        max_val = filtered["value"].max()
    colormap = branca.colormap.linear.YlOrRd_09.scale(min_val, max_val)

    # 2. Create Map
    m = folium.Map(location=[21.0, 78.0], zoom_start=5)
    
    # 3. Add colored polygons
    folium.GeoJson(
       state_geo,
       name="State Borders",
       style_function=lambda feature: {
           "fillColor": colormap(state_value_dict.get(feature["properties"]["NAME_1"])) 
                        if state_value_dict.get(feature["properties"]["NAME_1"]) is not None else "#ffffff00",
           "color": "#333333",
           "weight": 1.5,
           "fillOpacity": 0.7 if state_value_dict.get(feature["properties"]["NAME_1"]) is not None else 0,
       },
       tooltip=folium.GeoJsonTooltip(fields=["NAME_1"], aliases=["State:"])
    ).add_to(m)

    # 4. Add color legend
    colormap.caption = 'Value'
    colormap.add_to(m)
    
    # 5. Display in Streamlit
    st_folium(m, width="100%", height=700, key=f"map_{i}")