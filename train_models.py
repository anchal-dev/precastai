import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

df = pd.read_csv('precast_dataset.csv')

TARGETS = ['strength_gain_time_hr', 'total_cycle_time_hr', 'cost_per_cycle_inr']
CATS = ['cement_type','admixture_type','curing_method','element_type','region','automation_level','season']
NUMS = [c for c in df.columns if c not in TARGETS + CATS]

def add_features(df):
    df = df.copy()
    df['maturity_proxy']    = (df['curing_temperature_C'] + 10) * df['curing_duration_hr']
    df['cement_efficiency'] = df['cement_content_kgm3'] / df['water_cement_ratio']
    df['climate_stress']    = df['ambient_temperature_C'] * (1 - df['relative_humidity_pct'] / 100)
    return df

X = add_features(df.drop(columns=TARGETS))
y_time = df['total_cycle_time_hr']
y_cost = df['cost_per_cycle_inr']

X_tr, X_te, yt_tr, yt_te, yc_tr, yc_te = train_test_split(
    X, y_time, y_cost, test_size=0.2, random_state=42)

NUMS_ENG = NUMS + ['maturity_proxy', 'cement_efficiency', 'climate_stress']
preprocessor = ColumnTransformer([
    ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())]), NUMS_ENG),
    ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                      ('enc', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))]), CATS),
])
X_tr_t = preprocessor.fit_transform(X_tr)
X_te_t  = preprocessor.transform(X_te)

xgb_time = XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.05,
                         subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1)
xgb_time.fit(X_tr_t, yt_tr)

xgb_cost = XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.05,
                         subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1)
xgb_cost.fit(X_tr_t, yc_tr)

def evaluate(model, X, y, name):
    p = model.predict(X)
    print(f'{name}: MAE={mean_absolute_error(y,p):.2f}  RMSE={mean_squared_error(y,p,squared=False):.2f}  R2={r2_score(y,p):.4f}')

evaluate(xgb_time, X_te_t, yt_te, 'Cycle Time Model')
evaluate(xgb_cost, X_te_t, yc_te, 'Cost Model     ')

cv = cross_val_score(xgb_time, X_tr_t, yt_tr, cv=KFold(5, shuffle=True, random_state=42), scoring='r2')
print(f'CV R2 (Time): {cv.mean():.4f} +/- {cv.std():.4f}')

joblib.dump(xgb_time,     'model_cycle_time.pkl')
joblib.dump(xgb_cost,     'model_cost.pkl')
joblib.dump(preprocessor, 'preprocessor.pkl')
print('\nModels saved!')