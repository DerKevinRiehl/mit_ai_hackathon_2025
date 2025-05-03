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
This script contains functions for processing of scraped data from Tata Power.
"""




# #############################################################################
# IMPORTS
# #############################################################################
import pandas as pd



# #############################################################################
# MAIN
# #############################################################################

main_df = pd.read_csv("../../processed_data/data/template_data.csv")
df1 = pd.read_csv("../../data/processed_data/company_azure_power_projects_processed.csv")
df2 = pd.read_csv("../../data/processed_data/company_renew_projects_processed.csv")
df3 = pd.read_csv("../../data/processed_data/company_tata_projects_processed.csv")
main_df = pd.concat([main_df, df1, df2, df3], ignore_index=True)
main_df.to_csv("../../data/processed_data/data_processed.csv", index=False)
