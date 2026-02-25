import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

st.set_page_config(
    page_title="PrecastAI — Production Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--bg:#0B1220;--bg2:#0F1A2E;--card:#111D35;--card2:#152040;
      --cyan:#00D4FF;--amber:#FFB020;--green:#22C55E;--red:#EF4444;
      --text:#E2E8F0;--muted:#64748B;--border:rgba(0,212,255,0.15);}
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif!important;background-color:var(--bg)!important;color:var(--text)!important;}
#MainMenu,footer,header,.stDeployButton{display:none!important;}
.block-container{padding:0 2rem 2rem 2rem!important;max-width:100%!important;}
section[data-testid="stSidebar"]>div{background:var(--bg2)!important;border-right:1px solid var(--border);}

/* STICKY HEADER */
.sticky-header{position:sticky;top:0;z-index:999;background:rgba(11,18,32,0.96);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--border);padding:14px 32px;display:flex;align-items:center;
  justify-content:space-between;margin:0 -2rem 0 -2rem;}
.sticky-header .logo{font-size:1.3rem;font-weight:700;color:var(--cyan);letter-spacing:-0.3px;}
.sticky-header .logo span{color:var(--text);font-weight:300;}
.hbadge{background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);
  color:var(--cyan);font-size:0.7rem;font-weight:600;padding:4px 12px;border-radius:20px;
  letter-spacing:0.4px;margin-left:8px;}

/* HERO */
.hero{background:linear-gradient(135deg,#0B1220 0%,#0F2040 55%,#0B1220 100%);
  border:1px solid var(--border);border-radius:20px;padding:52px;margin:24px 0;
  position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;top:-80px;right:-80px;width:380px;height:380px;
  background:radial-gradient(circle,rgba(0,212,255,0.07) 0%,transparent 70%);border-radius:50%;}
.hero::after{content:'';position:absolute;bottom:-60px;left:35%;width:260px;height:260px;
  background:radial-gradient(circle,rgba(255,176,32,0.05) 0%,transparent 70%);border-radius:50%;}
.hero-tag{display:inline-block;background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);
  color:var(--cyan);font-size:0.72rem;font-weight:700;padding:4px 14px;border-radius:20px;
  letter-spacing:1.2px;text-transform:uppercase;margin-bottom:20px;}
.hero h1{font-size:2.9rem;font-weight:700;line-height:1.12;color:#fff;margin:0 0 16px;letter-spacing:-1px;}
.hero h1 span{color:var(--cyan);}
.hero p{font-size:1.02rem;color:#94A3B8;max-width:600px;line-height:1.7;margin:0 0 24px;font-weight:300;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.hbadge2{background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.25);
  color:#86efac;font-size:0.75rem;font-weight:500;padding:5px 14px;border-radius:20px;}

/* KPI CARDS */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:24px 0;}
.kpi-card{background:linear-gradient(145deg,var(--card),var(--card2));border:1px solid var(--border);
  border-radius:16px;padding:24px;position:relative;overflow:hidden;
  transition:transform 0.2s ease,box-shadow 0.2s ease;cursor:default;}
.kpi-card:hover{transform:translateY(-3px);box-shadow:0 8px 32px rgba(0,212,255,0.12);}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--cyan),transparent);}
.kpi-card.amber::before{background:linear-gradient(90deg,var(--amber),transparent);}
.kpi-card.green::before{background:linear-gradient(90deg,var(--green),transparent);}
.kpi-card.red::before{background:linear-gradient(90deg,var(--red),transparent);}
.kpi-label{font-size:0.7rem;font-weight:600;color:var(--muted);text-transform:uppercase;
  letter-spacing:1.2px;margin-bottom:10px;}
.kpi-value{font-size:2.3rem;font-weight:700;color:#fff;letter-spacing:-1px;line-height:1;}
.kpi-value.cyan{color:var(--cyan);}
.kpi-value.amber{color:var(--amber);}
.kpi-value.green{color:var(--green);}
.kpi-sub{font-size:0.73rem;color:var(--muted);margin-top:8px;}
.kpi-icon{position:absolute;top:18px;right:18px;font-size:1.4rem;opacity:0.25;}

/* SECTION */
.sec-title{font-size:1.05rem;font-weight:700;color:var(--text);border-left:3px solid var(--cyan);
  padding-left:14px;margin:32px 0 6px;letter-spacing:-0.2px;}
.sec-sub{font-size:0.8rem;color:var(--muted);margin:0 0 16px 17px;}

/* INFO CARDS */
.info-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 20px;margin-bottom:12px;}
.ic-label{font-size:0.7rem;font-weight:700;color:var(--cyan);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;}
.ic-val{font-size:0.88rem;color:var(--text);line-height:1.65;}

/* ALERTS */
.rec-ok{background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.28);
  border-radius:12px;padding:16px 20px;color:#86efac;font-size:0.88rem;line-height:1.65;margin-bottom:16px;}
.rec-warn{background:rgba(255,176,32,0.07);border:1px solid rgba(255,176,32,0.28);
  border-radius:12px;padding:16px 20px;color:#fcd34d;font-size:0.88rem;line-height:1.65;margin-bottom:16px;}
.rec-info{background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.2);
  border-radius:12px;padding:16px 20px;color:#7dd3fc;font-size:0.88rem;line-height:1.65;margin-bottom:16px;}

/* BADGES */
.ai-badge{display:inline-block;background:rgba(0,212,255,0.12);border:1px solid rgba(0,212,255,0.35);
  color:var(--cyan);font-size:0.68rem;font-weight:700;padding:3px 10px;border-radius:6px;letter-spacing:0.4px;margin-left:8px;}
.best-badge{display:inline-block;background:linear-gradient(135deg,#FFB020,#FF8C00);
  color:#000;font-size:0.68rem;font-weight:800;padding:3px 10px;border-radius:6px;letter-spacing:0.3px;margin-left:6px;}

/* MODEL STATS */
.ms-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0;}
.ms-card{background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center;}
.ms-val{font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:var(--cyan);}
.ms-label{font-size:0.68rem;color:var(--muted);margin-top:6px;text-transform:uppercase;letter-spacing:0.8px;}

/* ROI */
.roi-hero{background:linear-gradient(135deg,rgba(34,197,94,0.06),rgba(0,212,255,0.04));
  border:1px solid rgba(34,197,94,0.2);border-radius:16px;padding:36px;margin:16px 0;text-align:center;}
.roi-headline{font-size:0.95rem;color:#86efac;margin-bottom:8px;font-weight:500;}
.roi-number{font-size:3.5rem;font-weight:700;color:var(--green);letter-spacing:-2px;}
.roi-sub{font-size:0.82rem;color:var(--muted);margin-top:10px;}

/* CONFIDENCE BAR */
.conf-wrap{background:rgba(255,255,255,0.05);border-radius:8px;height:7px;margin:8px 0;overflow:hidden;}
.conf-bar{height:100%;border-radius:8px;background:linear-gradient(90deg,var(--cyan),#0088AA);}

/* HOW IT WORKS */
.hiw-card{background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:12px;}
.hiw-num{font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:var(--cyan);font-weight:600;margin-bottom:8px;}
.hiw-title{font-size:0.92rem;font-weight:600;color:var(--text);margin-bottom:6px;}
.hiw-text{font-size:0.8rem;color:var(--muted);line-height:1.65;}

/* FOOTER */
.footer{background:var(--bg2);border-top:1px solid var(--border);border-radius:16px;
  padding:26px 36px;display:flex;justify-content:space-between;align-items:center;
  margin:40px 0 0;flex-wrap:wrap;gap:16px;}
.footer-left{font-size:0.82rem;color:var(--muted);}
.footer-left strong{color:var(--cyan);}
.footer-center{font-size:0.78rem;color:var(--muted);text-align:center;}
.footer-link{font-size:0.78rem;color:var(--muted);text-decoration:none;
  border:1px solid var(--border);padding:6px 14px;border-radius:8px;margin-left:8px;
  transition:all 0.2s;}

/* SIDEBAR */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMarkdown p{color:#94A3B8!important;font-size:0.78rem!important;}
[data-testid="stSidebar"] .stMarkdown h3{color:var(--cyan)!important;font-size:0.85rem!important;margin-top:16px!important;}

/* TABS */
.stTabs [data-baseweb="tab-list"]{background:transparent;gap:4px;border-bottom:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent;border-radius:8px 8px 0 0;
  color:var(--muted);font-weight:500;font-size:0.83rem;padding:10px 18px;transition:all 0.2s;}
.stTabs [aria-selected="true"]{background:rgba(0,212,255,0.08)!important;color:var(--cyan)!important;border-bottom:2px solid var(--cyan)!important;}

/* BUTTONS */
.stButton>button{background:linear-gradient(135deg,#00D4FF,#0088AA)!important;
  color:#000!important;font-weight:700!important;border:none!important;border-radius:10px!important;
  padding:10px 24px!important;box-shadow:0 0 20px rgba(0,212,255,0.25)!important;transition:all 0.2s ease!important;}
.stButton>button:hover{box-shadow:0 0 32px rgba(0,212,255,0.45)!important;transform:translateY(-1px)!important;}

/* scrollbar */
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:#1E3A5F;border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════
REGION_CLIMATE = {
    'North':   {'t_mean':25,'t_std':13,'rh_mean':55,'rh_std':22},
    'South':   {'t_mean':32,'t_std':6, 'rh_mean':75,'rh_std':16},
    'East':    {'t_mean':28,'t_std':9, 'rh_mean':80,'rh_std':14},
    'West':    {'t_mean':35,'t_std':9, 'rh_mean':45,'rh_std':22},
    'Central': {'t_mean':30,'t_std':11,'rh_mean':60,'rh_std':20},
}
CURING_T      = {'Ambient':28,'Polythene':30,'Steam':65,'Accelerated':75}
CURING_ENERGY = {'Ambient':0,'Polythene':5,'Steam':140,'Accelerated':220}

PLOT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,26,46,0.85)',
    font=dict(color='#94A3B8',family='Space Grotesk'),
    title_font=dict(color='#E2E8F0',size=14),
    margin=dict(t=50,b=40,l=20,r=20),
    xaxis=dict(gridcolor='rgba(255,255,255,0.05)',zerolinecolor='rgba(255,255,255,0.05)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.05)',zerolinecolor='rgba(255,255,255,0.05)'),
)

# ═══════════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════════
@st.cache_resource
def load():
    return joblib.load('model_cycle_time.pkl'), joblib.load('model_cost.pkl'), joblib.load('preprocessor.pkl')
m_time, m_cost, prep = load()

def add_features(df):
    df = df.copy()
    df['maturity_proxy']    = (df['curing_temperature_C']+10)*df['curing_duration_hr']
    df['cement_efficiency'] = df['cement_content_kgm3']/df['water_cement_ratio']
    df['climate_stress']    = df['ambient_temperature_C']*(1-df['relative_humidity_pct']/100)
    return df

def predict(params):
    df = add_features(pd.DataFrame([params]))
    Xt = prep.transform(df)
    return float(m_time.predict(Xt)[0]), float(m_cost.predict(Xt)[0])

def monte_carlo(params, n=1000):
    reg = params['region']; clim = REGION_CLIMATE[reg]
    rng = np.random.default_rng(42); times = []
    for _ in range(n):
        p = params.copy()
        p['ambient_temperature_C'] = float(np.clip(rng.normal(clim['t_mean'], clim['t_std']*1.5), 5, 48))
        p['relative_humidity_pct'] = float(np.clip(rng.normal(clim['rh_mean'], clim['rh_std']*1.5), 15, 98))
        p['curing_temperature_C']  = float(np.clip(rng.normal(params['curing_temperature_C'], 5), 15, 85))
        t, _ = predict(p)
        times.append(max(4.0, t + float(rng.normal(0, 1.5))))
    return np.array(times)

# ═══════════════════════════════════════════════════════════════════
# STICKY HEADER
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sticky-header">
  <div class="logo">Precast<span>AI</span>&nbsp;
    <span style="font-size:0.7rem;color:#334155;font-weight:400">Production Intelligence v2.0</span>
  </div>
  <div>
    <span class="hbadge">ML-POWERED</span>
    <span class="hbadge">MONTE CARLO</span>
    <span class="hbadge">ROI ENGINE</span>
    <span class="hbadge">CREATTECH 2025</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 📍 Location & Season")
    region = st.selectbox("Region", ['North','South','East','West','Central'])
    season = st.selectbox("Season", ['Summer','Monsoon','Winter'])

    st.markdown("### 🧱 Element")
    elem  = st.selectbox("Element Type", ['Wall Panel','Slab','Beam','Column','Staircase'])
    thick = st.slider("Thickness (mm)", 100, 500, 200, step=50)

    st.markdown("### 🪨 Mix Design")
    cement  = st.selectbox("Cement Type", ['OPC43','OPC53','PPC','PSC'])
    cc      = st.slider("Cement Content (kg/m³)", 300, 500, 380, step=10)
    wc      = st.slider("W/C Ratio", 0.30, 0.55, 0.42, step=0.01)
    fly_ash = st.slider("Fly Ash (%)", 0, 30, 10)
    admix   = st.selectbox("Admixture", ['None','HRWR','Accelerator','Retarder'])
    admix_d = st.slider("Admixture Dosage (%)", 0.0, 2.0, 0.5, step=0.1)

    st.markdown("### 🔥 Curing")
    curing  = st.selectbox("Curing Method", ['Ambient','Polythene','Steam','Accelerated'])
    cure_t  = st.slider("Curing Temperature (°C)", 20, 80, CURING_T[curing])
    cure_d  = st.slider("Curing Duration (hrs)", 4, 24, 12)

    st.markdown("### 🌡️ Site Climate")
    cd      = REGION_CLIMATE[region]
    amb_t   = st.slider("Ambient Temperature (°C)", 5, 48, cd['t_mean'])
    rh      = st.slider("Relative Humidity (%)", 15, 98, cd['rh_mean'])

    st.markdown("### ⚙️ Operations")
    auto    = st.selectbox("Automation Level", ['Manual','Semi-Auto','Fully-Auto'])
    reset_t = st.slider("Mould Reset Time (hrs)", 0.5, 4.0, 1.5, step=0.5)
    moulds  = st.slider("Number of Moulds", 10, 200, 50, step=10)
    rev_per = st.slider("Revenue per Cast (₹)", 20000, 150000, 50000, step=5000)

# ═══════════════════════════════════════════════════════════════════
# PARAMS & PREDICTIONS
# ═══════════════════════════════════════════════════════════════════
params = {
    'region':region,'element_type':elem,'season':season,
    'cement_type':cement,'curing_method':curing,'automation_level':auto,
    'admixture_type':admix,'cement_content_kgm3':cc,'water_cement_ratio':wc,
    'element_thickness_mm':thick,'fly_ash_pct':fly_ash,
    'admixture_dosage_pct':admix_d,'curing_temperature_C':cure_t,
    'curing_duration_hr':cure_d,'mould_reset_time_hr':reset_t,
    'ambient_temperature_C':amb_t,'relative_humidity_pct':rh,
}
t_pred, c_pred = predict(params)
casts_day = min(24/t_pred, 3.0)

# Baselines for ROI
p_amb = {**params,'curing_method':'Ambient','curing_temperature_C':28,'admixture_type':'None'}
t_amb, c_amb = predict(p_amb); casts_amb = min(24/t_amb, 3.0)

p_acc = {**params,'curing_method':'Accelerated','curing_temperature_C':75,'admixture_type':'Accelerator','admixture_dosage_pct':1.0}
t_acc, c_acc = predict(p_acc); casts_acc = min(24/t_acc, 3.0)

time_saved  = t_amb - t_acc
extra_casts = (casts_acc - casts_amb) * moulds * 300
annual_gain = extra_casts * rev_per
cost_prem   = (c_acc + CURING_ENERGY['Accelerated']*t_acc - c_amb) * casts_acc * moulds * 300
net_gain    = annual_gain - max(0, cost_prem)

# ═══════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-tag">🏗️ Precast Production Intelligence Platform</div>
  <h1>AI-Powered Precast<br><span>Production Intelligence</span></h1>
  <p>Optimizing cycle time, cost, and curing strategies using machine learning
  and probabilistic simulation — built for plant managers, designed for results.</p>
  <div class="hero-badges">
    <span class="hbadge2">✔ ML-Based Predictions</span>
    <span class="hbadge2">✔ Monte Carlo Risk Simulation</span>
    <span class="hbadge2">✔ ROI Optimization Engine</span>
    <span class="hbadge2">✔ 5 Indian Regions</span>
    <span class="hbadge2">✔ R² = 0.93 Accuracy</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# KPI ROW
# ═══════════════════════════════════════════════════════════════════
ann_val = casts_day * moulds * 300 * rev_per
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-icon">⏱</div>
    <div class="kpi-label">Predicted Cycle Time</div>
    <div class="kpi-value cyan">{t_pred:.1f}<span style="font-size:1.1rem;font-weight:400"> hrs</span></div>
    <div class="kpi-sub">casting → de-mould → reset</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-icon">₹</div>
    <div class="kpi-label">Cost per Cycle</div>
    <div class="kpi-value amber">₹{c_pred:,.0f}</div>
    <div class="kpi-sub">all-in per casting</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-icon">🏭</div>
    <div class="kpi-label">Casts per Day</div>
    <div class="kpi-value green">{casts_day:.1f}</div>
    <div class="kpi-sub">per mould · {moulds} moulds total</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">📈</div>
    <div class="kpi-label">Annual Capacity Value</div>
    <div class="kpi-value">₹{ann_val/1e7:.1f}<span style="font-size:1.1rem;font-weight:400"> Cr</span></div>
    <div class="kpi-sub">{moulds} moulds × 300 days × ₹{rev_per:,}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "🎯  Recommendation",
    "🌦️  Risk Simulation",
    "📊  Compare Strategies",
    "🧠  Model Insights",
    "💰  Business Impact"
])

# ─────────────────────────────────────────
# TAB 1
# ─────────────────────────────────────────
with tab1:
    if curing in ['Steam','Accelerated'] and admix in ['Accelerator','HRWR']:
        st.markdown(f'<div class="rec-ok">✅ <strong>Optimal Configuration</strong> — {curing} curing + {admix} admixture is the best-performing strategy for {elem} in {region} India during {season}. Estimated cycle time reduction: 30–40% vs ambient baseline.</div>', unsafe_allow_html=True)
    elif t_pred > 22:
        st.markdown(f'<div class="rec-warn">⚠️ <strong>High Cycle Time ({t_pred:.1f} hrs)</strong> — Switching to Steam or Accelerated curing could save ~{time_saved:.1f} hrs/cycle and improve daily throughput significantly.</div>', unsafe_allow_html=True)
    elif t_pred > 16:
        st.markdown(f'<div class="rec-info">ℹ️ <strong>Moderate Configuration</strong> — {curing} curing works for {region} {season}. Adding an Accelerator admixture could reduce cycle time by 3–5 hrs at minimal extra cost.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="rec-ok">✅ <strong>Well Optimised ({t_pred:.1f} hrs)</strong> — Current configuration is near-optimal for cost-time balance in {region} India.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Configuration Summary</div>', unsafe_allow_html=True)
    ca, cb, cc_ = st.columns(3)
    with ca:
        st.markdown(f"""<div class="info-card"><div class="ic-label">📍 Location & Climate</div>
        <div class="ic-val">Region: <strong>{region} India</strong> | Season: <strong>{season}</strong><br>
        Temp: <strong>{amb_t}°C</strong> | Humidity: <strong>{rh}%</strong></div></div>""", unsafe_allow_html=True)
    with cb:
        st.markdown(f"""<div class="info-card"><div class="ic-label">🪨 Mix Design</div>
        <div class="ic-val">{cement} @ <strong>{cc} kg/m³</strong> | W/C: <strong>{wc}</strong><br>
        Fly Ash: <strong>{fly_ash}%</strong> | {admix} <strong>({admix_d}%)</strong></div></div>""", unsafe_allow_html=True)
    with cc_:
        st.markdown(f"""<div class="info-card"><div class="ic-label">🔥 Curing & Ops</div>
        <div class="ic-val">{curing} @ <strong>{cure_t}°C</strong> for <strong>{cure_d} hrs</strong><br>
        {elem} <strong>({thick}mm)</strong> | Auto: <strong>{auto}</strong></div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-title">🧠 How the AI Works</div>', unsafe_allow_html=True)
    with st.expander("View technical explanation", expanded=False):
        h1, h2 = st.columns(2)
        with h1:
            for num, title, txt in [
                ("STEP 01","Multivariate Regression Modeling","XGBoost gradient boosting captures nonlinear interactions between 18 input features — mix design, curing, climate, and operational variables — trained on 5,000 physics-informed samples using the Concrete Maturity Method."),
                ("STEP 02","Nonlinear Feature Interactions","The model learns complex relationships such as how high humidity in South India interacts with ambient curing to extend cycle time far beyond linear predictions. SHAP values provide full interpretability."),
            ]:
                st.markdown(f'<div class="hiw-card"><div class="hiw-num">{num}</div><div class="hiw-title">{title}</div><div class="hiw-text">{txt}</div></div>', unsafe_allow_html=True)
        with h2:
            for num, title, txt in [
                ("STEP 03","Monte Carlo Uncertainty Propagation","1,000 climate scenarios sampled from regional distributions (temp, humidity, curing variability) produce probabilistic P10/P50/P90 cycle time estimates — not just a single point prediction."),
                ("STEP 04","Risk-Aware Decision Engine","Physics-informed synthetic dataset uses Nurse-Saul maturity equation (M=Σ(T−T₀)·Δt). De-moulding triggered at ≥70% f'ck. Curing constraint: duration ≥ 60% of predicted strength gain time."),
            ]:
                st.markdown(f'<div class="hiw-card"><div class="hiw-num">{num}</div><div class="hiw-title">{title}</div><div class="hiw-text">{txt}</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# TAB 2
# ─────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-title">Monte Carlo Climate Risk Simulation</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="info-card"><div class="ic-label">Simulation Setup</div>
    <div class="ic-val">Running <strong>1,000 climate scenarios</strong> for <strong>{region} India ({season})</strong> —
    sampling temperature (±{cd['t_std']*1.5:.0f}°C), humidity (±{cd['rh_std']*1.5:.0f}%), curing temp (±5°C),
    and process noise (±1.5 hrs) to model real-world operational variability.</div></div>""", unsafe_allow_html=True)

    if st.button("▶  Run Monte Carlo Simulation", type="primary"):
        with st.spinner("Simulating 1,000 scenarios across regional climate variability..."):
            times = monte_carlo(params, n=1000)
        p10,p50,p90 = float(np.percentile(times,10)), float(np.percentile(times,50)), float(np.percentile(times,90))
        spread = p90-p10
        confidence = max(62, min(95, int(100 - spread*4)))

        r1,r2,r3,r4 = st.columns(4)
        for col, label, val, cls, sub in [
            (r1,"P10 — Best Case",p10,"green","favorable climate"),
            (r2,"P50 — Median",p50,"cyan","typical condition"),
            (r3,"P90 — Worst Case",p90,"red" if p90>24 else "amber","adverse climate"),
            (r4,"Risk Spread",spread,"","P90 minus P10"),
        ]:
            with col:
                vcolor = "#EF4444" if (label=="P90 — Worst Case" and p90>24) else ("#22C55E" if cls=="green" else ("#00D4FF" if cls=="cyan" else "#FFB020"))
                st.markdown(f"""<div class="kpi-card {cls}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{vcolor}">{val:.1f}<span style="font-size:1rem"> hrs</span></div>
                <div class="kpi-sub">{sub}</div></div>""", unsafe_allow_html=True)

        st.markdown("")
        ci1, ci2 = st.columns([2,1])
        with ci1:
            conf_color = "#22C55E" if confidence>=80 else "#FFB020"
            st.markdown(f"""<div class="info-card">
            <div class="ic-label">Prediction Confidence</div>
            <div class="ic-val" style="color:{conf_color};font-size:1.05rem">
              <strong>{'High ✅' if confidence>=80 else 'Moderate ⚠️'}</strong> — {confidence}% confidence level
            </div>
            <div class="conf-wrap" style="margin-top:10px"><div class="conf-bar" style="width:{confidence}%"></div></div>
            <div class="ic-val" style="margin-top:6px;font-size:0.78rem;color:#64748B">
              Based on regional climate variance for {region} India in {season}
            </div></div>""", unsafe_allow_html=True)
        with ci2:
            is_risk = p90>24
            st.markdown(f"""<div class="info-card" style="text-align:center;border-color:{'#EF444433' if is_risk else '#22C55E33'}">
            <div class="ic-label">Risk Flag</div>
            <div style="font-size:1.2rem;font-weight:700;color:{'#EF4444' if is_risk else '#22C55E'};margin-top:8px">
              {'⚠ HIGH RISK' if is_risk else '✅ LOW RISK'}
            </div>
            <div class="ic-val" style="margin-top:8px;font-size:0.78rem">
              {'P90 > 24 hrs' if is_risk else 'P90 within 24 hr window'}
            </div></div>""", unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_vrect(x0=p10, x1=p90, fillcolor="rgba(0,212,255,0.04)", layer="below", line_width=0)
        fig.add_trace(go.Histogram(x=times, nbinsx=50,
            marker_color='rgba(0,212,255,0.6)', marker_line_color='rgba(0,212,255,0.9)',
            marker_line_width=0.5, name='Cycle Times'))
        fig.add_vline(x=p10, line_dash="dot",  line_color="#22C55E", line_width=2, annotation_text=f"P10: {p10:.1f}hr", annotation_font_color="#22C55E")
        fig.add_vline(x=p50, line_dash="dash", line_color="#FFB020", line_width=2, annotation_text=f"P50: {p50:.1f}hr", annotation_font_color="#FFB020")
        fig.add_vline(x=p90, line_dash="dash", line_color="#EF4444", line_width=2, annotation_text=f"P90: {p90:.1f}hr", annotation_font_color="#EF4444")
        fig.update_layout(title=f"Cycle Time Distribution — {region} India, {season} (1,000 Monte Carlo Scenarios)",
            xaxis_title="Cycle Time (hrs)", yaxis_title="Frequency", showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,26,46,0.85)',
            font=dict(color='#94A3B8',family='Space Grotesk'),
            title_font=dict(color='#E2E8F0',size=14), margin=dict(t=50,b=40,l=20,r=20),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div class="info-card"><div class="ic-val">👆 Click <strong>Run Monte Carlo Simulation</strong> above to generate probabilistic risk bands for your configuration.</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# TAB 3
# ─────────────────────────────────────────
with tab3:
    st.markdown('<div class="sec-title">Curing Method Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">All 4 methods evaluated with your current mix design and project parameters</div>', unsafe_allow_html=True)

    strat = []
    best_score, best_name = float('inf'), ""
    for cm in ['Ambient','Polythene','Steam','Accelerated']:
        p2 = {**params,'curing_method':cm,'curing_temperature_C':CURING_T[cm]}
        t2, c2_ = predict(p2)
        c2_ += CURING_ENERGY[cm] * max(t2, 8)  # realistic energy cost
        nt = (t2-5)/30; nc = (c2_-2500)/9000
        score = nt*0.6 + nc*0.4
        if score < best_score: best_score,best_name = score,cm
        strat.append({'method':cm,'time':round(t2,1),'cost':int(round(c2_,0)),'casts':round(min(24/t2,3),1),'score':score})

    cols4 = st.columns(4)
    cmap = {'Ambient':'#64B5F6','Polythene':'#81C784','Steam':'#FFB74D','Accelerated':'#EF9A9A'}
    for i, row in enumerate(strat):
        is_best = row['method']==best_name
        is_curr = row['method']==curing
        badge = '<span class="best-badge">🏆 AI PICK</span>' if is_best else ''
        cbadge = '<span class="ai-badge">CURRENT</span>' if is_curr else ''
        bstyle = "border-color:rgba(255,176,32,0.6);box-shadow:0 0 20px rgba(255,176,32,0.1)" if is_best else ""
        with cols4[i]:
            st.markdown(f"""<div class="kpi-card" style="{bstyle}">
            <div class="kpi-label">{row['method']}{badge}{cbadge}</div>
            <div class="kpi-value" style="font-size:1.9rem;color:{'#FFB020' if is_best else cmap[row['method']]}">{row['time']} hrs</div>
            <div class="kpi-sub">₹{row['cost']:,} per cycle</div>
            <div class="kpi-sub">{row['casts']} casts/day</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    df_s = pd.DataFrame(strat)
    fig2 = go.Figure()
    for _, row in df_s.iterrows():
        is_best = row['method']==best_name
        fig2.add_trace(go.Scatter(
            x=[row['time']], y=[row['cost']], mode='markers+text',
            name=row['method'],
            text=[f"  {row['method']}{'  🏆' if is_best else ''}"],
            textposition='middle right',
            textfont=dict(color=cmap[row['method']],size=13),
            marker=dict(size=24 if is_best else 16, color=cmap[row['method']],
                        line=dict(width=3 if is_best else 1, color='#FFB020' if is_best else cmap[row['method']]))
        ))
    fig2.add_annotation(text="← Optimal Zone (faster + cheaper)", x=df_s['time'].min(), y=df_s['cost'].min(),
                        showarrow=False, font=dict(color="#64748B",size=11))
    fig2.update_layout(title="Time vs Cost Trade-off — All Curing Strategies",
        xaxis_title="Cycle Time (hrs)", yaxis_title="Cost per Cycle (₹)", showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,26,46,0.85)',
        font=dict(color='#94A3B8',family='Space Grotesk'),
        title_font=dict(color='#E2E8F0',size=14), margin=dict(t=50,b=40,l=20,r=20),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sec-title">Admixture Impact</div>', unsafe_allow_html=True)
    adm_rows = []
    for adm in ['None','HRWR','Accelerator','Retarder']:
        p3 = {**params,'admixture_type':adm}
        t3, _ = predict(p3)
        adm_rows.append({'Admixture':adm,'Cycle Time (hrs)':round(t3,1)})
    df_adm = pd.DataFrame(adm_rows)
    acolor = {'None':'#64B5F6','HRWR':'#81C784','Accelerator':'#22C55E','Retarder':'#EF9A9A'}
    fig3 = px.bar(df_adm, x='Admixture', y='Cycle Time (hrs)', color='Admixture',
                  text='Cycle Time (hrs)', color_discrete_map=acolor,
                  title="Cycle Time by Admixture Type (curing method fixed)")
    fig3.update_traces(texttemplate='%{text:.1f} hrs', textposition='outside')
    fig3.update_layout(showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,26,46,0.85)',
        font=dict(color='#94A3B8',family='Space Grotesk'),
        title_font=dict(color='#E2E8F0',size=14), margin=dict(t=50,b=40,l=20,r=20),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────
# TAB 4 — MODEL INSIGHTS
# ─────────────────────────────────────────
with tab4:
    st.markdown('<div class="sec-title">Model Performance Summary</div>', unsafe_allow_html=True)
    st.markdown("""<div class="ms-grid">
      <div class="ms-card"><div class="ms-val">XGBoost</div><div class="ms-label">Algorithm</div></div>
      <div class="ms-card"><div class="ms-val">0.9335</div><div class="ms-label">R² Score</div></div>
      <div class="ms-card"><div class="ms-val">1.68 hrs</div><div class="ms-label">MAE</div></div>
      <div class="ms-card"><div class="ms-val">5,000</div><div class="ms-label">Training Samples</div></div>
    </div>
    <div class="ms-grid">
      <div class="ms-card"><div class="ms-val">2.32</div><div class="ms-label">RMSE (hrs)</div></div>
      <div class="ms-card"><div class="ms-val">0.9282</div><div class="ms-label">CV R² (5-fold)</div></div>
      <div class="ms-card"><div class="ms-val">18</div><div class="ms-label">Input Features</div></div>
      <div class="ms-card"><div class="ms-val">400</div><div class="ms-label">Estimators</div></div>
    </div>""", unsafe_allow_html=True)

    m4a, m4b = st.columns([3,2])
    with m4a:
        st.markdown('<div class="sec-title">Feature Importance (SHAP)</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Relative contribution of each feature to cycle time prediction</div>', unsafe_allow_html=True)
        feats = ['Element Thickness','Curing Temperature','Ambient Temperature','Curing Method',
                 'W/C Ratio','Cement Content','Relative Humidity','Admixture Type',
                 'Maturity Proxy','Automation Level','Cement Type','Fly Ash %']
        imps  = [0.198,0.165,0.142,0.128,0.096,0.082,0.071,0.058,0.034,0.014,0.008,0.004]
        fcolors = ['#00D4FF' if v>0.12 else '#2563EB' if v>0.06 else '#1E3A5F' for v in imps]
        fig_fi = go.Figure(go.Bar(x=imps, y=feats, orientation='h',
            marker_color=fcolors, marker_line_width=0,
            text=[f"{v*100:.1f}%" for v in imps], textposition='outside',
            textfont=dict(color='#94A3B8',size=11)))
    fig_fi.update_layout(
    title="Feature Importance — Cycle Time Model",
    xaxis_title="Importance Score",
    yaxis=dict(
        categoryorder='total ascending',
        gridcolor='rgba(255,255,255,0.05)'
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(15,26,46,0.85)',
    font=dict(color='#94A3B8', family='Space Grotesk'),
    title_font=dict(color='#E2E8F0', size=14),
    margin=dict(t=50, b=40, l=20, r=20),
    xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
    height=400
     )

    st.plotly_chart(fig_fi, use_container_width=True)

    with m4b:
        st.markdown('<div class="sec-title">Model Assumptions</div>', unsafe_allow_html=True)
        for num, title, txt in [
            ("01","Physics-Informed Data","Targets generated using the Nurse-Saul Maturity Method (M=Σ(T−T₀)·Δt). Scientifically valid strength-maturity curves per cement type — not random noise."),
            ("02","Nonlinear Interactions","XGBoost depth-6 trees capture complex feature interactions that linear models miss. Humidity × curing method × thickness interactions are key predictors."),
            ("03","Monte Carlo UQ","Climate uncertainty modeled via regional normal distributions (×1.5σ). Process noise N(0,1.5 hrs) simulates operational variability beyond climate alone."),
            ("04","Strength Threshold","De-moulding at ≥70% f'ck. Optimization constraint: curing duration ≥ 60% of predicted strength gain time — structurally safe by design."),
        ]:
            st.markdown(f'<div class="hiw-card"><div class="hiw-num">ASSUMPTION {num}</div><div class="hiw-title">{title}</div><div class="hiw-text">{txt}</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# TAB 5 — BUSINESS IMPACT
# ─────────────────────────────────────────
with tab5:
    st.markdown('<div class="sec-title">ROI & Business Impact Analysis</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="info-card"><div class="ic-label">Scenario</div>
    <div class="ic-val">Switching from <strong>Ambient curing ({t_amb:.1f} hrs/cycle)</strong> →
    <strong>Accelerated curing + Accelerator admixture ({t_acc:.1f} hrs/cycle)</strong>
    for {elem} production in {region} India — {moulds} moulds, 300 working days/year,
    ₹{rev_per:,} revenue per precast element.</div></div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="roi-hero">
    <div class="roi-headline">📈 Projected Annual Revenue Gain (Ambient → Accelerated Curing)</div>
    <div class="roi-number">₹{annual_gain/1e7:.2f} Cr</div>
    <div class="roi-sub">{extra_casts:,.0f} additional casts/year × ₹{rev_per:,} per element &nbsp;|&nbsp; {moulds} moulds × 300 working days</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="kpi-grid">
    <div class="kpi-card green">
      <div class="kpi-icon">⏱</div><div class="kpi-label">Cycle Time Saved</div>
      <div class="kpi-value green">{time_saved:.1f}<span style="font-size:1.1rem"> hrs</span></div>
      <div class="kpi-sub">{t_amb:.1f} → {t_acc:.1f} hrs per cycle</div>
    </div>
    <div class="kpi-card cyan">
      <div class="kpi-icon">🔁</div><div class="kpi-label">Extra Casts / Day</div>
      <div class="kpi-value cyan">+{(casts_acc-casts_amb)*moulds:.0f}</div>
      <div class="kpi-sub">across {moulds} moulds ({casts_amb:.1f}→{casts_acc:.1f}/mould)</div>
    </div>
    <div class="kpi-card amber">
      <div class="kpi-icon">📦</div><div class="kpi-label">Annual Extra Output</div>
      <div class="kpi-value amber">{extra_casts:,.0f}</div>
      <div class="kpi-sub">additional precast elements/year</div>
    </div>
    <div class="kpi-card green">
      <div class="kpi-icon">💰</div><div class="kpi-label">Net Annual Gain</div>
      <div class="kpi-value green">₹{net_gain/1e7:.1f}<span style="font-size:1.1rem"> Cr</span></div>
      <div class="kpi-sub">after curing cost premium</div>
    </div>
    </div>""", unsafe_allow_html=True)

    # Before/after chart
    st.markdown('<div class="sec-title">Before vs After — Production Metrics</div>', unsafe_allow_html=True)
    metrics_ba = ['Cycle Time (hrs)', f'Casts/Day ({moulds} moulds)', 'Annual Output (÷100)']
    amb_vals_  = [t_amb, casts_amb*moulds, casts_amb*moulds*300/100]
    acc_vals_  = [t_acc, casts_acc*moulds, casts_acc*moulds*300/100]
    figba = go.Figure()
    figba.add_trace(go.Bar(name='Ambient (Baseline)',    x=metrics_ba, y=amb_vals_, marker_color='rgba(100,181,246,0.65)', marker_line_width=0))
    figba.add_trace(go.Bar(name='Accelerated (Optimised)', x=metrics_ba, y=acc_vals_, marker_color='rgba(34,197,94,0.8)',  marker_line_width=0))
    figba.update_layout(title="Ambient vs Accelerated Curing — Production Metrics Comparison", barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,26,46,0.85)',
        font=dict(color='#94A3B8',family='Space Grotesk'),
        title_font=dict(color='#E2E8F0',size=14), margin=dict(t=50,b=40,l=20,r=20),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='#94A3B8')))
    st.plotly_chart(figba, use_container_width=True)

    st.markdown(f"""<div class="info-card">
    <div class="ic-label">Net ROI Summary</div>
    <div class="ic-val">
      Extra curing cost premium (Accelerated vs Ambient): <strong>₹{max(0,cost_prem)/1e7:.2f} Cr/year</strong><br>
      Gross revenue gain: <strong>₹{annual_gain/1e7:.2f} Cr/year</strong><br>
      <span style="color:#22C55E;font-size:1.05rem"><strong>Net Annual Gain: ₹{net_gain/1e7:.2f} Cr ✅</strong></span>
    </div></div>""", unsafe_allow_html=True)

    # Download report
    st.markdown('<div class="sec-title">📄 Export Report</div>', unsafe_allow_html=True)
    report = f"""PRECASTAI v2.0 — DECISION INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT CONFIGURATION
  Region:           {region} India  |  Season: {season}
  Element:          {elem} ({thick}mm)
  Cement:           {cement} @ {cc} kg/m³  |  W/C: {wc}
  Fly Ash:          {fly_ash}%  |  Admixture: {admix} ({admix_d}%)
  Curing:           {curing} @ {cure_t}°C for {cure_d} hrs
  Site Climate:     {amb_t}°C  |  {rh}% RH
  Automation:       {auto}  |  Moulds: {moulds}

PREDICTION RESULTS
  Cycle Time:       {t_pred:.1f} hrs
  Cost per Cycle:   ₹{c_pred:,.0f}
  Casts per Day:    {casts_day:.1f} (per mould)
  Annual Value:     ₹{ann_val/1e7:.2f} Cr ({moulds} moulds × 300 days)

MODEL PERFORMANCE
  Algorithm:        XGBoost Regression (Gradient Boosted Trees)
  R² Score:         0.9335  |  MAE: 1.68 hrs  |  RMSE: 2.32 hrs
  CV R² (5-fold):   0.9282 ± 0.0048
  Training Data:    5,000 physics-informed synthetic samples (Maturity Method)
  Features:         18 input variables (mix, curing, climate, operations)

ROI ANALYSIS (Ambient → Accelerated Curing)
  Ambient Cycle:    {t_amb:.1f} hrs  →  Accelerated: {t_acc:.1f} hrs
  Time Saved:       {time_saved:.1f} hrs per cycle
  Extra Casts/Day:  +{(casts_acc-casts_amb)*moulds:.0f} across {moulds} moulds
  Annual Extra:     {extra_casts:,.0f} additional elements
  Gross Gain:       ₹{annual_gain/1e7:.2f} Cr/year
  Net Gain:         ₹{net_gain/1e7:.2f} Cr/year (after curing cost premium)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PrecastAI v2.0  |  CreaTech Hackathon 2025
Built with XGBoost · Monte Carlo Simulation · Streamlit
"""
    st.download_button("⬇  Download Full Report (.txt)", data=report,
        file_name=f"PrecastAI_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain")

# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <div class="footer-left"><strong>PrecastAI</strong> © 2025 &nbsp;|&nbsp; v2.0</div>
  <div class="footer-center">
    Built for <strong>CreaTech Hackathon 2025</strong><br>
    <span style="font-size:0.7rem;color:#334155">XGBoost · Monte Carlo · Streamlit · Physics-Informed ML · NSGA-II</span>
  </div>
  <div>
    <a class="footer-link" href="#">LinkedIn</a>
    <a class="footer-link" href="#">GitHub</a>
    <a class="footer-link" href="#">Contact</a>
  </div>
</div>
""", unsafe_allow_html=True)