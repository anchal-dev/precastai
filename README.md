<div align="center">

<img src="https://img.shields.io/badge/PrecastAI-Production%20Intelligence-1a1a2e?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTV6TTIgMTdsOSA1IDktNVYybC05IDV6Ii8+PC9zdmc+" alt="PrecastAI Banner"/>

# 🏗️ PrecastAI — Production Intelligence System

**Machine Learning–powered predictions for precast concrete manufacturing**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-precastai.streamlit.app-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://precastai.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.2.0-009688?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.2-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

> Predict **cycle time** and **production cost** for precast concrete operations using advanced ML, Monte Carlo simulation, and ROI analysis — all in an interactive web interface.

<br/>

</div>

---

## 📌 Overview

**PrecastAI** is a production-ready machine learning application that helps precast concrete manufacturers, construction planners, and production engineers make data-driven decisions. By analyzing material mix, curing conditions, regional factors, and automation level, PrecastAI delivers accurate predictions for:

| Metric | Description |
|---|---|
| ⏱️ **Total Cycle Time** | Predicted production duration in hours |
| 💰 **Cost per Cycle** | Estimated production cost in INR |

---

## ✨ Features

- 🤖 **ML-Powered Predictions** — XGBoost regressors trained with cross-validation for robust accuracy
- 🎲 **Monte Carlo Simulation** — Probabilistic risk analysis across thousands of scenarios
- 📈 **ROI Analysis Engine** — Evaluate automation and material investment trade-offs
- 🧮 **Smart Feature Engineering** — Maturity Proxy, Cement Efficiency, Climate Stress indices
- 📊 **Interactive Visualizations** — Dynamic Plotly charts for deep insight
- ☁️ **Production Deployment** — Hosted on Streamlit Cloud with auto-redeploy on push

---

## 🚀 Live Demo

> **Try it now →** [precastai.streamlit.app](https://precastai.streamlit.app)

No setup required. Input your production parameters and get instant predictions with risk analysis.

---

## 🧠 Model Details

### Prediction Targets
- `total_cycle_time_hr` — Total hours from preparation to demoulding
- `cost_per_cycle_inr` — Total cost per production cycle in Indian Rupees

### Feature Engineering
| Engineered Feature | Description |
|---|---|
| **Maturity Proxy** | Temperature × Time index simulating concrete maturity |
| **Cement Efficiency** | Strength-to-cement-ratio optimisation metric |
| **Climate Stress** | Environmental load factor for regional curing conditions |

### Algorithm
- **XGBRegressor** (Gradient Boosting) for both targets
- **Cross-validation** to ensure generalizability and prevent overfitting
- **Scikit-learn pipelines** for reproducible preprocessing

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **ML Models** | XGBoost 3.2.0 |
| **Preprocessing** | Scikit-learn 1.3.2 |
| **Data Handling** | Pandas, NumPy |
| **Visualization** | Plotly |
| **Deployment** | Streamlit Cloud |
| **Python Version** | 3.11 |

---

## 📂 Project Structure

```
precastai/
│
├── app.py                  # 🖥️  Main Streamlit application
├── train_models.py         # 🧪  Model training script
├── generate_data.py        # 🔧  Synthetic dataset generator
│
├── precast_dataset.csv     # 📊  Training dataset
├── model_cycle_time.pkl    # 💾  Trained cycle time model
├── model_cost.pkl          # 💾  Trained cost model
├── preprocessor.pkl        # ⚙️   Saved preprocessing pipeline
│
├── requirements.txt        # 📦  Python dependencies
├── runtime.txt             # 🐍  Python version config
└── README.md               # 📖  You are here
```

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11
- Conda (recommended) or pip

### 1. Clone the Repository
```bash
git clone https://github.com/anchal-dev/precastai.git
cd precastai
```

### 2. Create a Virtual Environment
```bash
conda create -n precast_env python=3.11
conda activate precast_env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎉

---

## 🔁 Retrain Models (Optional)

To regenerate models from scratch using the dataset:

```bash
python train_models.py
```

This will recreate:
- `model_cycle_time.pkl`
- `model_cost.pkl`
- `preprocessor.pkl`

---

## 🌍 Deployment

PrecastAI is deployed on **Streamlit Cloud** with:

- ✅ Python 3.11 runtime (`runtime.txt`)
- ✅ Version-pinned dependencies (`requirements.txt`)
- ✅ XGBoost & Scikit-learn version matching
- ✅ **Auto-redeploy** triggered on every `git push`

---

## 📊 Use Cases

PrecastAI is built for:

| User | Use Case |
|---|---|
| 🏭 **Precast Manufacturers** | Optimize curing cycles and reduce downtime |
| 🏗️ **Construction Planners** | Forecast production timelines with confidence intervals |
| 👷 **Production Engineers** | Justify automation investment with ROI analysis |

---

## 🔮 Roadmap

- [ ] 📉 Feature importance dashboard (SHAP values)
- [ ] 🔍 Model explainability layer
- [ ] 🌐 Production REST API endpoint
- [ ] 🗄️ Database integration for production logging
- [ ] 🏭 Real industrial dataset support
- [ ] 📱 Mobile-optimized interface

---

## 👩‍💻 Author

<div align="center">

**Anchal Gupta**
*Electronics & Communication Engineering*
*Madan Mohan Malviya University of Technology*

[![GitHub](https://img.shields.io/badge/GitHub-anchal--dev-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/anchal-dev)

</div>

---

<div align="center">

*Built with ❤️ for smarter precast concrete manufacturing*

⭐ **Star this repo if you find it useful!**

</div>
