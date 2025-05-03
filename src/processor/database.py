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
This script converts the tables into a PostGresSQL Database.
"""




# #############################################################################
# IMPORTS
# #############################################################################

import psycopg2
import pandas as pd
from sqlalchemy import create_engine



# #############################################################################
# Conversion
# #############################################################################

# Create Database
conn = psycopg2.connect(database="postgres", user="postgres", password="password", host="localhost", port="5432")
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE DATABASE mydb")
conn.close()

# Get Database Running
engine = create_engine('postgresql://postgres:password@localhost:5432/mydb')

# Project Explorer Data
df = pd.read_csv('../../data/data_processed.csv')
df.to_sql('project_overview', engine, if_exists='replace', index=False)

# Investment Navigator Data
df = pd.read_excel('../../data/data_processed/national_statistics.xlsx')
df.to_sql('national_data', engine, if_exists='replace', index=False)

# Tender Data
df = pd.read_csv('../../data/tender_processed.csv')
df.to_sql('tender_navigator', engine, if_exists='replace', index=False)