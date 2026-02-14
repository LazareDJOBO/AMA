from pydantic import BaseModel, Field
from typing import Literal

class PatientInput(BaseModel):
    age: int = Field(..., gt=0, description="Age in years")
    sexe: Literal['M', 'F'] = Field(..., description="Sex (M/F)")
    creatinine: float = Field(..., gt=0, description="Creatinine (mg/L)")
    uree: float = Field(..., gt=0, description="Urea (g/L)")
    temperature: float = Field(..., gt=30, lt=45, description="Temperature (C)")
    cholesterol_ldl: Literal['Réduit', 'Normal', 'Augmenté'] = Field(..., description="LDL Cholesterol level")
    cholesterol_total: Literal['Réduit', 'Normal', 'Augmenté'] = Field(..., description="Total Cholesterol level")

class PredictionOutput(BaseModel):
    stage: int
    probabilities: dict[int, float]
