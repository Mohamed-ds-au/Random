import streamlit as st

st.title("Dashboard")

st.markdown("This page embeds the Power BI dashboard using an iframe.")

POWER_BI_URL = (
    "https://app.powerbi.com/view?r=eyJrIjoiNjFkMTBjMDktZTI2Ni00YTE5LWI2OTktOTRlMWZjZmY4NWI2IiwidCI6ImVhZjYyNGM4LWEwYzQtNDE5NS04N2QyLTQ0M2U1ZDc1MTZjZCIsImMiOjh9"
)

import streamlit.components.v1 as components

components.iframe(POWER_BI_URL, width=1200, height=400)
