#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
import joblib

def train():
    # Ensure model folder exists
    model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model")
    os.makedirs(model_dir, exist_ok=True)

    # Generate synthetic dataset
    X = np.random.rand(100, 5)
    y = np.random.randint(0, 2, 100)
    df = pd.DataFrame(X, columns=[f'feature{i+1}' for i in range(5)])
    df['label'] = y

    # Train RandomForest
    clf = RandomForestClassifier()
    clf.fit(df.drop('label', axis=1), df['label'])

    # Train IsolationForest
    iso = IsolationForest(random_state=42)
    iso.fit(df.drop('label', axis=1))

    # Save models
    joblib.dump(clf, os.path.join(model_dir, "random_forest.joblib"))
    joblib.dump(iso, os.path.join(model_dir, "isolation_forest.joblib"))
    print(f"Models trained and saved to {model_dir}")

if __name__ == "__main__":
    train()

