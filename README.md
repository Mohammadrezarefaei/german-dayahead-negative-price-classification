# ⚡ Negative Electricity Price Prediction & Risk Classification (Germany Day-Ahead Market)

An end-to-end machine learning pipeline analyzing and classifying negative spot price events ($Price < 0 \text{ EUR/MWh}$) on the German Day-Ahead power exchange (**EPEX Spot / SMARD**) driven by renewable oversupply and inelastic grid demand.

---

## 📌 Project Overview
As renewable generation scales across the German grid, hours with high wind and solar feed-in combined with low residual demand increasingly trigger negative electricity prices (the "cannibalization effect"). 

This project formulates negative spot pricing as a **supervised classification problem**, providing day-ahead risk probabilities for trading desks, battery storage operators (BESS), and renewable asset managers.

* **Market Domain:** German Day-Ahead Bidding Zone (LU/DE)
* **Data Sources:** Bundesnetzagentur / SMARD.de (Renewable Generation & Market Fundamentals)
* **Target Variable:** Binary Flag `is_negative_price` ($1 \text{ if } \text{Price} < 0 \text{ EUR/MWh else } 0$)
* **Core Physics/Market Drivers:** Net Residual Load, Renewable Penetration Share, and Diurnal/Weekend Cyclicality.

---

## 📊 Classification Benchmark Results

Evaluated on an out-of-sample test split (last 20% time horizon):

| Classifier | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | **0.9583** | **0.9167** | **0.9429** | **0.9296** | **0.9810** |
| **Hist Gradient Boosting** | 0.9479 | 0.9091 | 0.9143 | 0.9117 | 0.9745 |
| **Logistic Regression** | 0.8958 | 0.8205 | 0.9143 | 0.8649 | 0.9320 |

---

## 📈 Visualizations & Market Dynamics

### Merit-Order Curve & Model ROC Curves
![Merit-Order & ROC Curves](negative_price_benchmark.png)

### Key Drivers (Permutation Feature Importance)
![Feature Importance](negative_price_feature_importance.png)

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Data Processing:** `pandas`, `numpy`
* **Machine Learning:** `scikit-learn` (`RandomForestClassifier`, `HistGradientBoostingClassifier`, `LogisticRegression`)
* **Visualization:** `matplotlib`, `seaborn`

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone [https://github.com/](https://github.com/)<YOUR_USERNAME>/german-dayahead-negative-price-classification.git
cd german-dayahead-negative-price-classification

# 2. Install dependencies
pip install pandas numpy scikit-learn matplotlib

# 3. Launch Jupyter Notebook
jupyter notebook negative_price_classification.ipynb
