import pickle
import sys

try:
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    
    with open("scaler_params.txt", "w") as out:
        out.write(f"Mean: {list(scaler.mean_)}\n")
        out.write(f"Scale: {list(scaler.scale_)}\n")
    
    print("Done writing to scaler_params.txt")

except Exception as e:
    with open("scaler_error.txt", "w") as out:
        out.write(str(e))
    print("Error:", e)
