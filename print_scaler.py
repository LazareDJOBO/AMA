import pickle
import numpy as np

# Create a dummy class if scaler is custom, though it seems standard
try:
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    print("M:", scaler.mean_)
    print("S:", scaler.scale_)
except Exception as e:
    print("Error:", e)
