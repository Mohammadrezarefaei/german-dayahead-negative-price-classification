"""SMARD Regulatory API Ingestion & Negative Price Risk Predictor."""

from typing import Dict, List
import numpy as np


class SMARDEngine:

  def __init__(
      self, residual_load_threshold_gw: float = 12.0, negative_price_cutoff: float = 0.0
  ):
    self.threshold_gw = residual_load_threshold_gw
    self.cutoff = negative_price_cutoff

  def calculate_residual_load(
      self, grid_demand_gw: float, wind_gw: float, solar_gw: float
  ) -> float:
    """Calculates residual load: Demand minus non-dispatchable variable renewable generation."""
    res_load = grid_demand_gw - (wind_gw + solar_gw)
    return round(res_load, 2)

  def predict_negative_price_risk(
      self, grid_demand_gw: float, wind_gw: float, solar_gw: float
  ) -> Dict[str, float]:
    """Evaluates probability and flag of negative price occurrence on EPEX Day-Ahead auction."""
    res_load = self.calculate_residual_load(grid_demand_gw, wind_gw, solar_gw)

    # Logistic risk proxy based on German merit-order inflection
    if res_load <= self.threshold_gw:
      # Severe surplus generation regime
      risk_prob = min(0.98, round(1.0 / (1.0 + np.exp(0.4 * (res_load - 5.0))), 3))
      predicted_negative = True
    else:
      risk_prob = max(0.02, round(1.0 / (1.0 + np.exp(0.3 * (res_load - 8.0))), 3))
      predicted_negative = False

    return {
        "residual_load_gw": res_load,
        "negative_price_probability": float(risk_prob),
        "negative_price_flag": int(predicted_negative),
    }

  def calculate_curtailment_savings(
      self, negative_price_eur: float, solar_gen_mwh: float
  ) -> float:
    """Calculates avoided balance penalty when executing economic curtailment under EEG §51 rules."""
    if negative_price_eur >= self.cutoff:
      return 0.0
    avoided_penalty = abs(negative_price_eur) * solar_gen_mwh
    return round(avoided_penalty, 2)
