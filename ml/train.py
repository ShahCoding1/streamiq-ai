"""Train an offline, reproducible bandwidth forecasting model on independent synthetic traces."""
import json
from pathlib import Path
import numpy as np
import joblib
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from backend.app.engine import trace_for, features

MODEL=Path(__file__).resolve().parent/'models'/'bandwidth.joblib'

def dataset(seeds=range(1,101), segments=100):
    X=[]; y=[]; groups=[]
    for seed in seeds:
        for profile in ('stable','mobile','congested','variable','drop','recovery','extreme'):
            trace=trace_for(profile,segments,seed)
            for t in range(5,len(trace)):
                X.append(features(trace[max(0,t-5):t],buffer=12,last_bitrate=1200))
                y.append(trace[t]); groups.append((seed,profile))
    return np.asarray(X),np.asarray(y),groups

def train():
    X,y,groups=dataset()
    # Split by independent trace seeds: adjacent windows never cross train/test.
    train_idx=np.array([g[0]<=70 for g in groups]); val_idx=np.array([70<g[0]<=85 for g in groups]); test_idx=np.array([g[0]>85 for g in groups])
    model=HistGradientBoostingRegressor(max_iter=110,max_leaf_nodes=18,l2_regularization=10,random_state=42)
    model.fit(X[train_idx],y[train_idx]); validation=model.predict(X[val_idx]); test=model.predict(X[test_idx])
    baseline=np.array([X[i][0] for i in np.where(test_idx)[0]])
    metrics={'validation_mae_kbps':round(float(mean_absolute_error(y[val_idx],validation)),2),'test_mae_kbps':round(float(mean_absolute_error(y[test_idx],test)),2),'test_rmse_kbps':round(float(np.sqrt(mean_squared_error(y[test_idx],test))),2),'persistence_baseline_mae_kbps':round(float(mean_absolute_error(y[test_idx],baseline)),2),'train_samples':int(train_idx.sum()),'validation_samples':int(val_idx.sum()),'test_samples':int(test_idx.sum()),'dataset':'Synthetic traces; disjoint trace seeds across splits','model':'HistGradientBoostingRegressor'}
    MODEL.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump({'estimator':model,'metrics':metrics,'feature_names':['last','mean3','mean5','std5','trend','buffer','last_bitrate']},MODEL)
    (MODEL.parent/'metrics.json').write_text(json.dumps(metrics,indent=2))
    print(json.dumps(metrics,indent=2))
    return metrics
if __name__=='__main__':train()
