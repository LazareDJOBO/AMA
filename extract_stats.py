import pandas as pd
import numpy as np

# Load original data to re-calculate stats if needed
path = "C:/Users/poste/Desktop/Master1/Data AI4CKD.xlsx"
# Note: I don't have access to the Excel file directly here, but I can check the notebook's output in the comments or assume standard scaler values if the file is missing.
# Wait, I can try to load the excel file if it exists.

if os.path.exists(path):
    print("Found Excel file. Calculating stats...")
    df = pd.read_excel(path)
    # ... logic to reproduce notebook filtering ...
else:
    print("Excel file not found.")

# Let's try to load the scaler with a different protocol or just dump content
import pickle
try:
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    print("Mean:", scaler.mean_)
    print("Scale:", scaler.scale_)
except Exception as e:
    print("Scaler load failed:", e)
