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
import streamlit as st




# #############################################################################
# METHODS
# #############################################################################

def generate_banner():
    st.markdown("""
        <style>
        /* Reduce top padding/margin for the main block container */
        .block-container {
            padding-top: 0.5rem !important;
        }
        /* Banner styling */
        .solar-banner {
            background: linear-gradient(90deg, #ffea00 0%, #ff9800 100%);
            color: #222;
            padding: 0.7rem 2rem 0.7rem 2rem;
            border-radius: 0.5rem;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.7rem;
            font-weight: 700;
            box-shadow: 0 2px 12px rgba(0,0,0,0.07);
            letter-spacing: 0.01em;
        }
        .solar-banner .flag {
            font-size: 2rem;
            margin: 0 0.7rem;
        }
        .solar-banner .left-space {{
            display: inline-block;
            width: {left_margin_px}px;
            height: 100px;
        }}
        </style>
        
        <div class="solar-banner">
            <br />
        </div>
        
        <div class="solar-banner">
            <br />
            <hr/>
            <hr/>
            <br />
            <hr/>
            <hr/>
            <img src="https://polybox.ethz.ch/index.php/apps/files_sharing/publicpreview/yJMxFnKMSBizZfF?file=/&fileId=4056358333&x=1920&y=1200&a=true&etag=c11127f2c9eb26aa0a959403172392a8" width="150px" />
            <span class="flag"> &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; 🌞</span>
            Mr Sunshine India <span class="flag">🇮🇳</span> Mapping India’s Solar Infrastructure
            <span class="flag">🌞 &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp;  </span>
            <img src="https://polybox.ethz.ch/index.php/apps/files_sharing/publicpreview/yJMxFnKMSBizZfF?file=/&fileId=4056358333&x=1920&y=1200&a=true&etag=c11127f2c9eb26aa0a959403172392a8" width="150px" />
        </div>
    """, unsafe_allow_html=True)