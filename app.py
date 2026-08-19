"""Interactive Streamlit App: German Electricity Market Negative Price Forecaster."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="German Day-Ahead & Negative Price Analyzer",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ German Power Market & Negative Price Risk Predictor")
st.markdown(
    "Automated ingestion & modeling tool for **EPEX Spot Day-Ahead auctions,"
    " SMARD residual load analytics, and EEG §51 curtailment risks**."
)

st.sidebar.header("⚙️ Grid & Generation Simulation")
grid_demand = st.sidebar.slider(
    "National Electricity Demand (GW)", 35.0, 75.0, 52.0, 1.0
)
solar_feedin = st.sidebar.slider("Solar PV Feed-in (GW)", 0.0, 45.0, 24.0, 1.0)
wind_feedin = st.sidebar.slider(
    "Wind Onshore + Offshore (GW)", 0.0, 50.0, 22.0, 1.0
)
spot_price_manual = st.sidebar.slider(
    "Current EPEX Spot Price (€/MWh)", -120.0, 150.0, -18.5, 2.5
)

# Residual load calculation
tot_renewables = solar_feedin + wind_feedin
res_load = grid_demand - tot_renewables
re_penetration = (tot_renewables / grid_demand) * 100.0

col1, col2 = st.columns([2, 1])

with col1:
  st.subheader("📊 Merit-Order Supply/Demand & Residual Load Balance")

  labels = [
      "Total Demand",
      "Solar Generation",
      "Wind Generation",
      "Residual Grid Load",
  ]
  values = [grid_demand, solar_feedin, wind_feedin, max(0.0, res_load)]
  colors = ["#3B82F6", "#F59E0B", "#10B981", "#6366F1"]

  fig, ax = plt.subplots(figsize=(9, 4.5))
  bars = ax.bar(labels, values, color=colors, width=0.55)
  ax.axhline(
      0, color="black", linewidth=0.8, linestyle="--"
  )  # Visual baseline
  ax.set_ylabel("Power Capacity [GW]", fontweight="bold")
  ax.grid(axis="y", linestyle=":", alpha=0.6)

  for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + 0.8,
        f"{yval:.1f} GW",
        ha="center",
        va="bottom",
        fontweight="bold",
    )

  st.pyplot(fig)

with col2:
  st.subheader("⚠️ Market Risk Diagnostics")

  # Logistic Risk Proxy
  if res_load <= 10.0:
    risk_pct = min(98.0, 100.0 / (1.0 + np.exp(0.4 * (res_load - 4.0))))
  else:
    risk_pct = max(2.0, 100.0 / (1.0 + np.exp(0.3 * (res_load - 8.0))))

  st.metric(
      label="Residual Load (Net Grid Deficit)",
      value=f"{res_load:.1f} GW",
      delta="Severe Surplus" if res_load < 12 else "Normal Dispatch",
  )
  st.metric(
      label="Renewable Penetration",
      value=f"{re_penetration:.1f} %",
      delta="Merit-Order Cannibalization"
      if re_penetration > 75
      else "Balanced",
  )
  st.metric(
      label="Negative Price Probability",
      value=f"{risk_pct:.1f} %",
      delta="High Risk Level" if risk_pct > 50 else "Low Risk",
  )

st.markdown("---")
st.subheader("💡 Economic Curtailment Calculator (EEG §51 Compliance)")

c1, c2, c3 = st.columns(3)
with c1:
  plant_mw = st.number_input("Renewable Asset Capacity (MW)", 1.0, 500.0, 50.0)
with c2:
  hours_negative = st.number_input("Consecutive Negative Hours", 1, 24, 4)
with c3:
  if spot_price_manual < 0:
    avoided_loss = abs(spot_price_manual) * plant_mw * hours_negative
    st.metric(
        label="Avoided Balancing Penalty (via Curtailment)",
        value=f"€{avoided_loss:,.2f}",
        delta="Economic Shield Active",
    )
  else:
    st.metric(
        label="Avoided Balancing Penalty",
        value="€0.00",
        delta="Market Price is Positive",
    )
