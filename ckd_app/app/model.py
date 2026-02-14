import pickle
import pandas as pd
import numpy as np
import os
from .schemas import PatientInput

MODEL_PATH = os.path.join(os.path.dirname(__file__), "xgb_model_6features.pkl")
model = None

def load_model():
    global model
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

def calcul_dfg_ckd_epi(sexe: str, age: int, creatinine_mg_L: float) -> float:
    """
    Calcule le DFG selon la formule CKD-EPI 2021.
    """
    if creatinine_mg_L <= 0 or age <= 0:
        return np.nan

    # Conversion mg/L -> mg/dL
    creatinine_mg_dL = creatinine_mg_L / 10.0
    
    sexe_str = sexe.upper()
    if sexe_str == 'F':
        kappa = 0.7
        alpha = -0.241
        facteur_sexe = 1.012
    elif sexe_str == 'M':
        kappa = 0.9
        alpha = -0.302
        facteur_sexe = 1.0
    else:
        return np.nan

    dfg = (
        142
        * min(creatinine_mg_dL / kappa, 1) ** alpha
        * max(creatinine_mg_dL / kappa, 1) ** -1.200
        * (0.9938 ** age)
        * facteur_sexe
    )
    return round(dfg, 2)

def predict_stage(data: PatientInput):
    if model is None:
        load_model()
    
    # 1. Calculate DFG
    dfg = calcul_dfg_ckd_epi(data.sexe, data.age, data.creatinine)
    
    # 2. Encode categorical variables
    # Mapping: {"Réduit":0, "Normal":1, "Normale":1, "Augmenté":2}
    cholesterol_map = {"Réduit": 0, "Normal": 1, "Augmenté": 2}
    
    ldl_encoded = cholesterol_map.get(data.cholesterol_ldl, 1)
    total_encoded = cholesterol_map.get(data.cholesterol_total, 1)
    
    # 3. Prepare Feature Vector
    # Order: ["dfg", "Créatinine (mg/L)", "Urée (g/L)", "Température (C°)", "Cholestérol LDL_Encoded", "Cholestérol Total_Encoded"]
    
    # Normalization Parameters (extracted from scaler.pkl)
    # Mapping based on numeric_vars order in analyze_scaler.py/notebook:
    # Index 7: Créatinine (mg/L) -> Mean: 43.36, Scale: 69.30
    # Index 8: Urée (g/L) -> Mean: 1.40, Scale: 10.84
    # Index 6: Température (C°) -> Mean: 36.63, Scale: 2.86
    # Index 14: Cholestérol LDL_Encoded -> Mean: 1.07, Scale: 0.44
    # Index 12: Cholestérol Total_Encoded -> Mean: 1.12, Scale: 0.40
    # Note: 'dfg' was NOT in the scaler as it is a calculated feature added LATER in the notebook.
    # HOWEVER, the model expects 'dfg' as the first feature. 
    # Let's check if 'dfg' was scaled in the notebook.
    # In the notebook: 
    #   df_ml[existing_numeric_vars] = scaler.fit_transform(...)
    #   X = df_ml[feature_cols] ...
    #   X["dfg"] = ...
    # It seems 'dfg' was added to X AFTER the scaler was applied to other columns.
    # So 'dfg' is likely UNSCALED.
    
    features = pd.DataFrame([{
        "dfg": dfg,
        "Créatinine (mg/L)": (data.creatinine - 43.3625) / 69.2978,
        "Urée (g/L)": (data.uree - 1.4017) / 10.8385,
        "Température (C°)": (data.temperature - 36.6318) / 2.8613,
        "Cholestérol LDL_Encoded": (ldl_encoded - 1.0714) / 0.4429,
        "Cholestérol Total_Encoded": (total_encoded - 1.1169) / 0.4021
    }])
    
    # 4. Predict
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    # Map class index to probabilities
    probs_dict = {i: float(prob) for i, prob in enumerate(probabilities)}
    
    return int(prediction), probs_dict
