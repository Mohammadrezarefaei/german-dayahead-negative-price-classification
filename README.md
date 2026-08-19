# ⚡ German Day-Ahead Electricity Market & Negative Price Classifier

[![SMARD Pipeline CI](https://github.com/Mohammadrezarefaei/german-dayahead-negative-price-classification/actions/workflows/ci.yml/badge.svg)](https://github.com/Mohammadrezarefaei/german-dayahead-negative-price-classification/actions)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://german-dayahead-negative-price-classification.streamlit.app/)

An automated quantitative pipeline and interactive risk-management tool for the **German EPEX Spot Day-Ahead Market**. Ingests regulatory grid and generation metrics (**SMARD / Bundesnetzagentur**), predicts negative price events driven by renewable feed-in spikes, and models economic curtailment under **EEG §51**.

---

## 🚀 Live Interactive Demo
👉 **[Access the Live Streamlit Web App](https://german-dayahead-negative-price-classification.streamlit.app/)**

---

## 📌 Market Physics & Merit-Order Dynamics

Negative electricity prices occur when non-dispatchable generation (Wind + Solar) exceeds national load, coupled with thermal plant inflexibility:
* **Residual Load Formulation:**
  $$\text{Residual Load} = P_{\text{Demand}} - (P_{\text{Wind}} + P_{\text{Solar}})$$
* **Renewable Cannibalization:** Inflection points occur when renewable penetration exceeds $75\%$ of real-time demand, compressing marginal clearing prices below €0/MWh.
* **EEG §51 Curtailment Shield:** Calculates financial balancing penalties avoided by executing economic curtailment during consecutive negative market hours.

---

## 🔍 Model Validation & Regime Boundary Analysis

The classifier and risk framework were stress-tested across distinct German wholesale market regimes:

* **High Renewable Influx (Surplus Regime):** When Residual Load drops below **10.0 GW**, negative price risk escalates rapidly ($>80\%$), triggering automated curtailment signals.
* **Tight Baseload Regime (High Demand / Dunkelflaute):** When Residual Load exceeds **35.0 GW**, price risks remain $<5\%$, ensuring standard merit-order dispatch.
* **Boundary Limitation:** In borderline regimes (10–14 GW Residual Load), price formation is highly sensitive to cross-border interconnector flows (imports/exports with France, Austria, and Scandinavia), which can mitigate local negative price events.

---

## 🛠️ Software Architecture & Automated Testing
* **CI/CD Pipeline:** Fully automated testing via **GitHub Actions** (`pytest` test suite covering residual load balance, classification flags, and curtailment calculations).
* **Modular Core Engine:** Located in `src/smard_engine.py`.
* **Tech Stack:** Python 3.11, NumPy, Pandas, Matplotlib, Streamlit, Pytest.
