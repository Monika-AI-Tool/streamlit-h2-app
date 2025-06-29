import streamlit as st
import pandas as pd

st.set_page_config(page_title="H₂-Projektmodell", layout="wide")
st.title("🧪 H₂-Projekt: Szenariorechnung & NPV")

# Projektparameter
st.sidebar.header("🔧 Projektkonfiguration")
start_year = st.sidebar.number_input("Startjahr", min_value=2000, value=2026)
project_years = st.sidebar.number_input("Projektlaufzeit (in Jahren)", min_value=1, value=10)
discount_rate = st.sidebar.number_input("Diskontierungszins [%]", min_value=0.0, value=8.0) / 100

# Ergebnisliste
results = []

st.header("📥 Eingaben & Berechnungen pro Jahr")

for i in range(project_years):
    year = start_year + i
    with st.expander(f"📆 Jahr {year}"):
        col1, col2, col3 = st.columns(3)

        with col1:
            h2_production = st.number_input(f"Green H₂ Production Vol in Tonnen ({year})", key=f"h2_{i}")
            credit_price = st.number_input(f"Credit Price [€/Credit] ({year})", key=f"cp_{i}")
            capex = st.number_input(f"CAPEX ({year})", value=0.0, key=f"capex_{i}")
            taxes = st.number_input(f"Taxes ({year})", value=0.0, key=f"tax_{i}")

        with col2:
            co2_refinery = st.number_input(f"CO₂ Abatement [gCO₂e/MJ] ({year})", key=f"co2_{i}")
            energy_density = st.number_input(f"Energy Density H₂ [MJ/kg] ({year})", key=f"ed_{i}")
            opex_cogs = st.number_input(f"OPEX COG
