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
This script contains functions for the markers.
"""




# #############################################################################
# IMPORTS
# #############################################################################
import pandas as pd





# #############################################################################
# METHODS
# #############################################################################

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