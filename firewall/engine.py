#!/usr/bin/env python3

import os
import argparse
import joblib
import numpy as np

def load_model(model_path):
    """
    Load a trained ML model using an absolute path.
    """
    model_path = os.path.abspath(model_path)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    clf = joblib.load(model_path)
    return clf

def main(model_path):
    # Load the RandomForest model
    clf = load_model(model_path)
    print(f"RandomForest model loaded from {os.path.abspath(model_path)}")

    # Try to load IsolationForest from the same folder
    iso_model_path = os.path.join(os.path.dirname(os.path.abspath(model_path)), "isolation_forest.joblib")
    if os.path.exists(iso_model_path):
        iso = joblib.load(iso_model_path)
        print(f"IsolationForest model loaded from {iso_model_path}")
    else:
        iso = None
        print("IsolationForest model not found, skipping anomaly detection.")

    # Example: simulate incoming data
    sample = np.random.rand(1, 5)
    pred = clf.predict(sample)
    print(f"RandomForest prediction for sample {sample}: {pred}")

    if iso:
        anomaly = iso.predict(sample)
        print(f"IsolationForest anomaly prediction for sample {sample}: {anomaly}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Firewall Engine")
    parser.add_argument("--model", required=True, help="Path to RandomForest model")
    args = parser.parse_args()
    main(args.model)

