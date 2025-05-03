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
import pandas as pd



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
    if top_choice == "Electricity":
        sub_selected = st.radio("Select Aspect:", [
                                          "Installed Capacity [loc]", "Installed Capacity [dec]", "Hydro",
                                          "Nuclear", "RES", "Thermal", "Central", "Private", 
                                          "State", "Rooftop Solar Capacity", "Generation", "Peak Demand", "Electricity Sales", "AT&C Losses",  "ACS-ARR (Electricity Sales) Gap"
                                          ])
    elif top_choice=="Economy & Demographics":
        sub_selected = st.radio("Select Aspect:", [
                                            "GDP [ConstPrice]", "GDP [CurrPrice]", "SectoralGVA [ConstPrice]", "SectoralGVA [CurrPrice]", "Population", "IncomePerCapita [CurrPrice]", "IncomePerCapita [ConstPrice]"
                                          ])
    elif top_choice=="Emissions":
        sub_selected = st.radio("Select Aspect:", [
                                            "NO2", "SO2", "PMO", "PM25"
                                          ])
    elif top_choice=="Investment Potential Score":
        sub_selected = "Installed Capacity [loc]"
    else:
        sub_selected = "Population"
        
    # Filtering must be done outside the columns (so both columns can use the result)
    if sub_selected in investment_data.columns:
        filtered = investment_data[["State", sub_selected]]
    else:
        sub_selected = "Population"
    filtered = investment_data[["State", sub_selected]]
    filtered = filtered.rename(columns={sub_selected: "value"})
    return filtered

def generate_company_details(i, data):
    # ROI Slider
    roi = st.slider(
          "Expected ROI (%)",
          min_value=0,
          max_value=100,
          value=10,
          step=1,
          help="Select your target Return on Investment percentage."
    )
    # Investment Volume Slider
    investment_volume = st.slider(
          "Investment Volume ($k)",
          min_value=0,
          max_value=10000,
          value=500,
          step=100,
          help="Select your planned investment volume in thousands of dollars."
    )
    # Desired Marketshare Slider
    marketshare = st.slider(
          "Desired Marketshare (%)",
          min_value=0,
          max_value=100,
          value=5,
          step=1,
          help="Select your desired market share percentage."
    )
    # Growth Potential Slider
    growth_potential = st.slider(
          "Growth Potential (%)",
          min_value=0,
          max_value=100,
          value=20,
          step=1,
          help="Estimate the growth potential for your project."
    )
    
    # Optionally, display the selected values
    st.markdown(f"**ROI:** {roi}%")
    st.markdown(f"**Investment Volume:** ${investment_volume * 1000:,}")
    st.markdown(f"**Desired Marketshare:** {marketshare}%")
    st.markdown(f"**Growth Potential:** {growth_potential}%")

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
    
    # 3. Add colored polygons with click event
    geojson = folium.GeoJson(
       state_geo,
       name="State Borders",
       style_function=lambda feature: {
           "fillColor": colormap(state_value_dict.get(feature["properties"]["NAME_1"])) 
                        if state_value_dict.get(feature["properties"]["NAME_1"]) is not None else "#ffffff00",
           "color": "#333333",
           "weight": 1.5,
           "fillOpacity": 0.7 if state_value_dict.get(feature["properties"]["NAME_1"]) is not None else 0,
       },
       tooltip=folium.GeoJsonTooltip(fields=["NAME_1"], aliases=["State:"]),
   )
    geojson.add_to(m)

    # 4. Add color legend
    colormap.caption = 'Value'
    colormap.add_to(m)
    
    # 5. Display in Streamlit and capture click
    map_data = st_folium(m, width="100%", height=700, key=f"map_{i}")

    # 6. Display selected state name
    if map_data and map_data.get("last_active_drawing"):
        props = map_data["last_active_drawing"]["properties"]
        state_name = props.get("NAME_1")
    else:
        state_name = None
    return state_name


def business_calculator_pane(i, state_name, data, investment_data):
    if state_name is None:
        st.write(f"#### Calculation For Selected State: **-**")
        return
    st.write(f"#### Calculation For Selected State: **{state_name}**")
    
    # Filter for the selected state
    row = investment_data[investment_data["State"] == state_name]
    if row.empty:
        st.warning("No data available for the selected state.")
        return
    
    # Select and rename relevant columns for display
    display_cols = {
        "calc_AirPollutionFactor": "Air Pollution Factor",
        "calc_land": "Land Investment",
        "calc_material": "Material Investment",
        "calc_installation": "Installation Investment",
        "calc_grid_connection": "Grid Connection Investment",
        "calc_invest": "Total Investment",
        "calc_operation": "Operation Cost",
        "calc_equipment": "Equipment Cost",
        "calc_staff": "Staff Cost",
        "calc_cost": "Total Operating Cost",
        "calc_efficiency": "Efficiency Factor",
        "calc_prices": "Electricity Price (Adjusted)",
        "calc_sales": "Electricity Sales (Adjusted)",
        "calc_revenue": "Total Revenue",
        "calc_profit": "Profit (Clipped)",
        "calc_interest_rate": "Interest Rate",
        "calc_ebit": "EBIT"
    }
    
    # Prepare a DataFrame for display
    df_display = row[list(display_cols.keys())].rename(columns=display_cols).T
    df_display.columns = ["Value"]
    df_display.reset_index(inplace=True)
    df_display.columns = ["Metric", "Value"]
    
    # Format numbers nicely
    def format_value(val):
        if isinstance(val, (int, float)):
            if abs(val) >= 1e6:
                return f"{val:,.2f}"
            elif abs(val) >= 1e3:
                return f"{val:,.2f}"
            else:
                return f"{val:.2f}"
        return val

    df_display["Value"] = df_display["Value"].apply(lambda x: format_value(x.values[0]) if isinstance(x, pd.Series) else format_value(x))
    
    # Bold specific rows and insert separator rows
    bold_metrics = ["Total Investment", "Total Operating Cost", "Total Revenue", "Profit (Clipped)"]
    new_rows = []
    for idx, row in df_display.iterrows():
        metric = row["Metric"]
        value = row["Value"]
        if metric in bold_metrics:
            new_rows.append({"Metric": f"<b>{metric}</b>", "Value": f"<b>{value}</b>"})
            # Add empty separator row
            new_rows.append({"Metric": "", "Value": ""})
        else:
            new_rows.append({"Metric": metric, "Value": value})
    df_display = pd.DataFrame(new_rows)
    
    # Add custom CSS for right-aligning numbers and table style
    st.markdown("""
        <style>
        .dataframe {
            border-collapse: collapse;
            width: 100%;
        }
        .dataframe th, .dataframe td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .dataframe td:last-child {
            text-align: right !important;
            font-family: monospace;
        }
        .dataframe tr:nth-child(even){background-color: #f9f9f9;}
        .dataframe tr:hover {background-color: #f1f1f1;}
        b {
            color: #2c3e50;
            font-weight: 700;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Display as HTML table with unsafe_allow_html=True to render bold tags
    st.write(
        df_display.to_html(
            index=False, 
            escape=False,  # Important to render <b> tags
            justify="left", 
            border=0, 
            classes="dataframe"
        ), 
        unsafe_allow_html=True
    )


