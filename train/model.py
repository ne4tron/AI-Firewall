from sklearn.ensemble import IsolationForest, RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import pandas as pd
import numpy as np
import os


def generate_synthetic(n_normal=1000, n_anom=50):
rng = np.random.RandomState(42)
normal = rng.normal(0, 1, (n_normal,6))
anom = rng.normal(4, 1.5, (n_anom,6))
X = np.vstack([normal, anom])
y = np.hstack([np.zeros(n_normal), np.ones(n_anom)])
cols = ['pkt_len','tcp_flags','src_port','dst_port','flow_bytes','pkt_per_sec']
return pd.DataFrame(X, columns=cols), y


def train(output_path='model/model.joblib'):
X, y = generate_synthetic()
iso = IsolationForest(contamination=0.02, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
ensemble = VotingClassifier([('iso', iso), ('rf', rf)], voting='soft')
pipeline = Pipeline([('scaler', StandardScaler()), ('model', ensemble)])
pipeline.fit(X, y)
os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
joblib.dump(pipeline, output_path)
print(f"Saved ensemble model to {output_path}")


if __name__ == "__main__":
train()
