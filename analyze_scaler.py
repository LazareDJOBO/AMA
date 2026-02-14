import pickle
import numpy as np

try:
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    
    print(f"n_features_in_: {scaler.n_features_in_}")
    if hasattr(scaler, "feature_names_in_"):
        print("feature_names_in_ found:")
        for i, name in enumerate(scaler.feature_names_in_):
            print(f"{i}: {name} | Mean: {scaler.mean_[i]} | Scale: {scaler.scale_[i]}")
    else:
        print("feature_names_in_ NOT found. Dumping raw arrays:")
        print("Mean:", scaler.mean_)
        print("Scale:", scaler.scale_)

except Exception as e:
    print(f"Error: {e}")
