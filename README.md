🏗️ PrecastAI – Production Intelligence System

PrecastAI is a machine learning–powered web application that predicts:

⏱️ Total Cycle Time (hours)

💰 Cost per Cycle (INR)

for precast concrete production using material mix, curing conditions, region, and automation level.

Built using XGBoost + Scikit-Learn + Streamlit and deployed on Streamlit Cloud.

🚀 Live Demo

🔗 https://precastai.streamlit.app

🧠 Features

ML-powered predictions

Monte Carlo simulation (risk analysis)

ROI analysis engine

Smart feature engineering

Interactive UI with Plotly visualizations

Production-ready deployment

🏗️ Tech Stack
Layer	Technology
Frontend	Streamlit
ML Models	XGBoost 3.2.0
Preprocessing	Scikit-learn 1.3.2
Data Handling	Pandas, NumPy
Visualization	Plotly
Deployment	Streamlit Cloud
Python Version	3.11
📂 Project Structure
precastai/
│
├── app.py                  # Main Streamlit app
├── train_models.py         # Model training script
├── generate_data.py        # Synthetic dataset generator
├── precast_dataset.csv     # Dataset
├── model_cycle_time.pkl    # Trained cycle time model
├── model_cost.pkl          # Trained cost model
├── preprocessor.pkl        # Saved preprocessing pipeline
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version config
└── README.md
🔬 Model Details
Targets:

total_cycle_time_hr

cost_per_cycle_inr

Feature Engineering:

Maturity Proxy

Cement Efficiency

Climate Stress

Algorithms Used:

XGBRegressor (Gradient Boosting)

Cross-validation used to validate model robustness.

⚙️ Installation (Local Setup)
1️⃣ Clone Repository
git clone https://github.com/anchal-dev/precastai.git
cd precastai
2️⃣ Create Virtual Environment
conda create -n precast_env python=3.11
conda activate precast_env
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run App
streamlit run app.py
🧪 Train Models (Optional)

If you want to retrain:

python train_models.py

This will regenerate:

model_cycle_time.pkl

model_cost.pkl

preprocessor.pkl

🌍 Deployment

Deployed on Streamlit Cloud with:

Python 3.11

Version-matched XGBoost & Scikit-learn

Auto redeploy on Git push

📊 Use Case

This system helps:

Precast manufacturers

Construction planners

Production engineers

to optimize:

Curing cycles

Material costs

Automation investment decisions

🏆 Future Improvements

Feature importance dashboard

Model explainability (SHAP)

Production API endpoint

Database integration

Real industrial dataset support

👩‍💻 Author

Anchal Gupta
Electronics & Communication Engineering [IOT]
Madan Mohan Malviya University of Technology

GitHub: https://github.com/anchal-dev
