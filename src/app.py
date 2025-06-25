from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np
from joblib import load
from types_custom import SoireeRequest, PredictionResponse
from utils import to_units

app = FastAPI()

# Chargement des modèlesk
model_biere, cols_biere = load("./model/model_biere.joblib")
model_soft, cols_soft = load("./model/model_soft.joblib")
model_pizza, cols_pizza = load("./model/model_pizza.joblib")

@app.post("/predict", response_model=PredictionResponse)
def predict(soiree: SoireeRequest):
    duree = (soiree.context.heure_fin - soiree.context.heure_debut).total_seconds() / 3600

    df = pd.DataFrame([
        {
            **participant.dict(),
            **soiree.context.dict(),
            "duree": duree

        }
        for participant in soiree.participants
    ])

    # Préparation des features
    def prepare_features(df, cols):
        df_enc = pd.get_dummies(df)
        for c in cols:
            if c not in df_enc.columns:
                df_enc[c] = 0
        df_enc = df_enc[cols]
        return df_enc

    X_biere = prepare_features(df, cols_biere)
    X_soft = prepare_features(df, cols_soft)
    X_pizza = prepare_features(df, cols_pizza)

    preds_biere = model_biere.predict(X_biere.to_numpy())
    preds_soft = model_soft.predict(X_soft.to_numpy())
    preds_pizza = model_pizza.predict(X_pizza.to_numpy())

    # (optionnel) Application du coefficient manuel sur la bière
    COEF_BOIT = {
        "pas du tout": 1,#0.6,
        "peu":  1,#0.8,
        "normal":  1,#1.0,
        "beaucoup":  1,#1.3
    }
    for i, p in enumerate(soiree.participants):
        preds_biere[i] *= COEF_BOIT[p.boit_ce_soir]

    total = {
        "biere": round(float(np.sum(preds_biere)), 2),
        "soft": round(float(np.sum(preds_soft)), 2),
        "pizza": round(float(np.sum(preds_pizza)), 2),
    }

    par_personne = []
    for b, s, p in zip(preds_biere, preds_soft, preds_pizza):
        par_personne.append({
            "biere": int(b),
            "verre_soft": int(s),
            "part_pizza": int(p)
        })

    total_unit = to_units(total)

    return PredictionResponse(total_units=total_unit, par_personne=par_personne)
