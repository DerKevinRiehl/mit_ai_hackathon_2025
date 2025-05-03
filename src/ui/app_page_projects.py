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
import streamlit as st
import pandas as pd




# #############################################################################
# METHODS
# #############################################################################

def generate_filter_pane(i, data):
    with st.expander("Filters", expanded=True):
        sources = st.multiselect(
            "Operator",  # Changed label here
            data['source'].unique(), 
            default=data['source'].unique(), 
            key=f"source_{i}"
        )
        
        # Produced Energy Slider
        min_energy = float(data['produced_energy'].min()) if 'produced_energy' in data else 0.0
        max_energy = float(data['produced_energy'].max()) if 'produced_energy' in data else 1000.0
        produced_energy = st.slider(
            "Capacity [MWh]",
            min_value=min_energy,
            max_value=max_energy,
            value=(min_energy, max_energy),
            key=f"energy_{i}"
        )

        # Commission Year Slider
        if 'commission_year' in data:
            min_year = int(data['commission_year'].min())
            max_year = int(data['commission_year'].max())
        else:
            min_year, max_year = 2000, 2025
        commission_year = st.slider(
            "Commission Year",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key=f"commission_year_{i}"
        )

        # Single-select State with "All" option (moved here)
        state_options = ["All"] + list(data['state'].unique())
        state = st.selectbox(
            "State",
            options=state_options,
            index=0,
            key=f"state_{i}"
        )

        bifacial = st.multiselect(
            "Bifacial Modules", 
            ["Yes", "No"], 
            default=["Yes", "No"], 
            key=f"bifacial_{i}"
        )
        techs = st.multiselect(
            "Technology", 
            data['technology'].unique(), 
            default=data['technology'].unique(), 
            key=f"tech_{i}"
        )
        types = st.multiselect(
            "Type", 
            data['type'].unique(), 
            default=data['type'].unique(), 
            key=f"type_{i}"
        )

    # Filtering logic
    filtered = data[
        data['type'].isin(types) &
        data['technology'].isin(techs) &
        data['source'].isin(sources)
    ]
    # State filter (only if not "All")
    if state != "All":
        filtered = filtered[filtered['state'] == state]
    # Bifacial filter as multiselect
    if set(bifacial) != set(["Yes", "No"]):
        filtered = filtered[filtered['bifacial'].map(lambda x: "Yes" if x else "No").isin(bifacial)]
    return filtered

def generate_map(i, filtered, st_folium):
    m = folium.Map(location=[21.0, 78.0], zoom_start=5)
    for _, row in filtered.iterrows():
        popup_html = generate_popup_html(row)
        marker_color = get_marker_color(row.get("source", ""))
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=marker_color, icon='bolt', prefix='fa')
        ).add_to(m)
    st_folium(m, width="100%", height=700, key=f"map_{i}")
    
def get_marker_color(source):
    if source == "tata":
        return "black"
    elif source == "renew":
        return "green"
    elif source == "azure":
        return "orange"
    else:
        return "blue"  # default
    
def generate_popup_html(row):
    popup_html = f"<b>{row['name']}</b><br>"
    if pd.notna(row.get('image_url', None)) and row['image_url']:
        popup_html += f'<img src="{row["image_url"]}" width="150"><br><br>'
    popup_html += '<table style="width:100%; font-size:13px;">'
    general_rows = ""
    if pd.notna(row.get('capacity', None)):
        general_rows += f'<tr><td><b>Capacity</b></td><td style="text-align:right;">{row["capacity"]} MW</td></tr>'
    if pd.notna(row.get('lat', None)) and pd.notna(row.get('lon', None)):
        general_rows += f'<tr><td><b>Location</b></td><td style="text-align:right;">{row["lat"]}, {row["lon"]}</td></tr>'
    if pd.notna(row.get('developer', None)):
        general_rows += f'<tr><td><b>Operator</b></td><td style="text-align:right;">{row["developer"]}</td></tr>'
    if pd.notna(row.get('year', None)):
        general_rows += f'<tr><td><b>Commissioned</b></td><td style="text-align:right;">{row["year"]}</td></tr>'
    if pd.notna(row.get('type', None)):
        general_rows += f'<tr><td><b>Type</b></td><td style="text-align:right;">{row["type"]}</td></tr>'
    if general_rows:
        popup_html += '<tr><th colspan="2" style="background-color:#f2f2f2; text-align:left;">General Information</th></tr>' + general_rows
    
    tech_rows = ""
    if pd.notna(row.get('technology', None)) or pd.notna(row.get('bifacial', None)):
        tech_type = row['technology'] if pd.notna(row.get('technology', None)) else ''
        if pd.notna(row.get('bifacial', None)):
            tech_type += f" ({'Bifacial' if row['bifacial'] else 'Monofacial'})"
        tech_rows += f'<tr><td><b>Cell Types</b></td><td style="text-align:right;">{tech_type}</td></tr>'
    if pd.notna(row.get('irradiance', None)):
        tech_rows += f'<tr><td><b>Irradiance</b></td><td style="text-align:right;">{row["irradiance"]}</td></tr>'
    if pd.notna(row.get('performance', None)):
        tech_rows += f'<tr><td><b>Performance</b></td><td style="text-align:right;">{row["performance"]}</td></tr>'
    if pd.notna(row.get('grid', None)):
        tech_rows += f'<tr><td><b>Grid</b></td><td style="text-align:right;">{row["grid"]}</td></tr>'
    if pd.notna(row.get('grid_proximity', None)):
        tech_rows += f'<tr><td><b>Grid Proximity</b></td><td style="text-align:right;">{row["grid_proximity"]}</td></tr>'
    if tech_rows:
        popup_html += '<tr><th colspan="2" style="background-color:#f2f2f2; text-align:left;">Technology</th></tr>' + tech_rows
    
    business_rows = ""
    if pd.notna(row.get('manufacturer', None)):
        business_rows += f'<tr><td><b>Manufacturer</b></td><td style="text-align:right;">{row["manufacturer"]}</td></tr>'
    if pd.notna(row.get('developer', None)):
        business_rows += f'<tr><td><b>Developer</b></td><td style="text-align:right;">{row["developer"]}</td></tr>'
    if pd.notna(row.get('offtake', None)):
        business_rows += f'<tr><td><b>Offtake</b></td><td style="text-align:right;">{row["offtake"]}</td></tr>'
    if pd.notna(row.get('financing', None)):
        business_rows += f'<tr><td><b>Financing</b></td><td style="text-align:right;">{row["financing"]}</td></tr>'
    if business_rows:
        popup_html += '<tr><th colspan="2" style="background-color:#f2f2f2; text-align:left;">Business & Policy</th></tr>' + business_rows
    
    popup_html += '</table>'
    
    return popup_html