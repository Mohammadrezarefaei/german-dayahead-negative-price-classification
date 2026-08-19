"""Automated Pytest Suite for SMARD Engine."""

import pytest
from src.smard_engine import SMARDEngine


def test_residual_load_calculation():
  engine = SMARDEngine()
  # Demand 50 GW, Wind 25 GW, Solar 15 GW -> Residual Load = 10 GW
  res_load = engine.calculate_residual_load(
      grid_demand_gw=50.0, wind_gw=25.0, solar_gw=15.0
  )
  assert res_load == 10.0


def test_high_negative_price_risk():
  engine = SMARDEngine(residual_load_threshold_gw=12.0)
  # Residual load is 5 GW (Severe surplus regime)
  result = engine.predict_negative_price_risk(
      grid_demand_gw=45.0, wind_gw=30.0, solar_gw=10.0
  )
  assert result["negative_price_flag"] == 1
  assert result["negative_price_probability"] >= 0.50


def test_low_negative_price_risk():
  engine = SMARDEngine(residual_load_threshold_gw=12.0)
  # High demand, low renewables -> Residual load = 35 GW
  result = engine.predict_negative_price_risk(
      grid_demand_gw=60.0, wind_gw=15.0, solar_gw=10.0
  )
  assert result["negative_price_flag"] == 0
  assert result["negative_price_probability"] < 0.20


def test_economic_curtailment_savings():
  engine = SMARDEngine()
  # Price is -€45/MWh, 100 MWh generation -> Avoided loss = €4,500
  savings = engine.calculate_curtailment_savings(
      negative_price_eur=-45.0, solar_gen_mwh=100.0
  )
  assert savings == 4500.0
