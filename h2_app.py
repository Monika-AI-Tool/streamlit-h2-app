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
            opex_cogs = st.number_input(f"OPEX COGS ({year})", value=0.0, key=f"cogs_{i}")
            opex_ely = st.number_input(f"OPEX ELY ({year})", value=0.0, key=f"ely_{i}")

        with col3:
            multiplier = st.number_input(f"Credit Multiplier ({year})", key=f"mult_{i}")
            smr_replacement = st.number_input(f"SMR Replacement Benefit ({year})", value=0.0, key=f"smr_{i}")
            h2_revenue = st.number_input(f"H₂ Production Revenue ({year})", value=0.0, key=f"h2rev_{i}")
            working_cap = st.number_input(f"Working Capital ({year})", value=0.0, key=f"wc_{i}")

        # RED Revenue Berechnung
        co2_per_kg = (co2_refinery * energy_density) / 1_000_000
        credits_per_kg = co2_per_kg * multiplier
        revenue_per_kg = credits_per_kg * credit_price
        red_revenue = h2_production * 1_000 * revenue_per_kg

        total_cf = (
            h2_revenue + smr_replacement + red_revenue
            - capex - opex_cogs - opex_ely - taxes - working_cap
        )

        results.append({
            "Jahr": year,
            "H₂ Production": h2_revenue,
            "SMR Replacement": smr_replacement,
            "RED Revenues": red_revenue,
            "CAPEX": capex,
            "OPEX COGS": opex_cogs,
            "OPEX ELY": opex_ely,
            "Taxes": taxes,
            "Working Capital": working_cap,
            "Netto-CF": total_cf
        })

# Ergebnisanzeige
st.header("📊 Cashflow-Tabelle")
df = pd.DataFrame(results)
st.dataframe(df.style.format("{:,.2f}"))

# NPV-Berechnung
npv = sum(row["Netto-CF"] / ((1 + discount_rate) ** i) for i, row in enumerate(results))
st.subheader("💰 NPV-Berechnung")
st.metric(label="Net Present Value (NPV)", value=f"{npv:,.2f} €")
