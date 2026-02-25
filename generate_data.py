import numpy as np, pandas as pd
np.random.seed(42); N=5000

REGION_CLIMATE = {
    'North':{'t_mean':25,'t_std':12,'rh_mean':55,'rh_std':20},
    'South':{'t_mean':32,'t_std':5, 'rh_mean':75,'rh_std':15},
    'East': {'t_mean':28,'t_std':8, 'rh_mean':80,'rh_std':12},
    'West': {'t_mean':35,'t_std':8, 'rh_mean':45,'rh_std':20},
    'Central':{'t_mean':30,'t_std':10,'rh_mean':60,'rh_std':18}}

CURING_COST={'Ambient':0,'Polythene':5,'Steam':120,'Accelerated':200}
CURING_T   ={'Ambient':28,'Polythene':30,'Steam':65,'Accelerated':75}
CURING_EFF ={'Ambient':1.0,'Polythene':0.92,'Steam':0.55,'Accelerated':0.45}
ADMIX_EFF  ={'None':1.0,'HRWR':0.92,'Accelerator':0.70,'Retarder':1.30}
CEMENT_F   ={'OPC43':1.0,'OPC53':0.88,'PPC':1.12,'PSC':1.18}

def strength_gain_time(row):
    T = row['curing_temperature_C']
    base_mat = 500 + (row['water_cement_ratio']-0.35)*2000 + (400-row['cement_content_kgm3'])*2
    t = (base_mat/max(T+10,1) * CEMENT_F[row['cement_type']]
         * ADMIX_EFF[row['admixture_type']] * CURING_EFF[row['curing_method']]
         * (1 + 0.15*row['element_thickness_mm']/200))
    return max(4, t + np.random.normal(0,0.8))

def cycle_cost(row, sgt):
    auto_mult = {'Manual':1.5,'Semi-Auto':1.0,'Fully-Auto':0.5}[row['automation_level']]
    return (row['cement_content_kgm3']*7 + row['admixture_dosage_pct']*row['cement_content_kgm3']*0.05
            + CURING_COST[row['curing_method']]*sgt + sgt*auto_mult*80 + np.random.normal(0,50))

data=[]
for _ in range(N):
    reg=np.random.choice(list(REGION_CLIMATE)); clim=REGION_CLIMATE[reg]
    cm=np.random.choice(['Ambient','Polythene','Steam','Accelerated'],p=[.35,.25,.25,.15])
    row={'region':reg,'cement_type':np.random.choice(['OPC43','OPC53','PPC','PSC']),
         'cement_content_kgm3':np.random.randint(300,500),
         'water_cement_ratio':round(np.random.uniform(.30,.55),2),
         'fly_ash_pct':np.random.randint(0,30),
         'admixture_type':np.random.choice(['None','HRWR','Accelerator','Retarder'],p=[.30,.25,.30,.15]),
         'admixture_dosage_pct':round(np.random.uniform(0,2),2),
         'curing_method':cm,'curing_temperature_C':CURING_T[cm]+np.random.normal(0,3),
         'curing_duration_hr':np.random.randint(6,24),
         'element_thickness_mm':np.random.choice([100,150,200,250,300,400,500]),
         'element_type':np.random.choice(['Wall Panel','Slab','Beam','Column','Staircase']),
         'ambient_temperature_C':np.random.normal(clim['t_mean'],clim['t_std']),
         'relative_humidity_pct':np.clip(np.random.normal(clim['rh_mean'],clim['rh_std']),15,98),
         'season':np.random.choice(['Summer','Monsoon','Winter']),
         'automation_level':np.random.choice(['Manual','Semi-Auto','Fully-Auto'],p=[.40,.35,.25]),
         'mould_reset_time_hr':round(np.random.uniform(.5,4.0),1)}
    sgt=strength_gain_time(row)
    row.update({'strength_gain_time_hr':round(sgt,2),
                'total_cycle_time_hr':round(sgt+row['mould_reset_time_hr']+0.5,2),
                'cost_per_cycle_inr':round(cycle_cost(row,sgt),2)})
    data.append(row)

df=pd.DataFrame(data); df.to_csv('precast_dataset.csv',index=False)
print(df[['strength_gain_time_hr','total_cycle_time_hr','cost_per_cycle_inr']].describe())
