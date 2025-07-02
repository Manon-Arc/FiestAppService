from fastapi import FastAPI
import pandas as pd
import numpy as np
from joblib import load
from typing import List
from types_custom import PredictionResponse, ProfilParticipant
from utils import to_units

app = FastAPI(
    title="FiestApp Service API",
    description="""
## 🍻 Party Consumption Prediction API

This API uses **Machine Learning** models to predict the consumption of beer, soft drinks, and pizzas based on participant profiles.

### Features

- **Personalized prediction**: Based on age, gender, weight, height, and consumption habits
- **ML models**: Random Forest
- **Detailed results**: Per person and totals
""",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"},  # Dark and modern theme
        "defaultModelsExpandDepth": -1,  # Hide the Models section
        "displayRequestDuration": True,  # Show request duration
    },
)


# Chargement des modèles
model_biere, cols_biere = load("./model/model_biere.joblib")
model_soft, cols_soft = load("./model/model_soft.joblib")
model_pizza, cols_pizza = load("./model/model_pizza.joblib")



@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict party consumption",
    description="""
Predicts the consumption of beer, soft drinks, and pizza slices for a list of participants.

- **Input:** A list of participant profiles (age, gender, weight, height, alcoholConsumption)
- **Output:** Predicted consumption per participant and totals, with purchase units.
""",
    tags=["Prediction"],
)

def predict(participants: List[ProfilParticipant] ):
    """
    Prédit la consommation pour une liste de participants.
    """
    print("===== PROFILS DES PARTICIPANTS =====")
    for i, p in enumerate(participants):
        print(
            f"Participant {i+1}: {p.gender}, {p.age} ans, {p.height}m, {p.weight}kg, {p.alcoholConsumption}"
        )

    # Convertir la liste de participants en DataFrame
    df = pd.DataFrame([participant.dict() for participant in participants])

    # Vérifier le DataFrame généré
    print("===== DATAFRAME GÉNÉRÉ =====")
    print(df.head())

    # Préparation des features
    def prepare_features(df, cols):
        # One-hot encoding
        df_enc = pd.get_dummies(df, columns=["gender", "alcoholConsumption"])

        print(f"Colonnes après encoding: {df_enc.columns.tolist()}")
        print(f"Colonnes attendues: {cols}")

        # S'assurer que toutes les colonnes requises sont présentes
        missing_cols = set(cols) - set(df_enc.columns)
        if missing_cols:
            print(f"Colonnes manquantes: {missing_cols}")
            for c in missing_cols:
                df_enc[c] = 0

        # Réorganiser les colonnes dans le bon ordre
        df_enc = df_enc[cols]
        return df_enc

    X_biere = prepare_features(df.copy(), cols_biere)
    X_soft = prepare_features(df.copy(), cols_soft)
    X_pizza = prepare_features(df.copy(), cols_pizza)

    print("===== FEATURES PRÉPARÉES =====")
    print("X_biere shape:", X_biere.shape)
    print("X_biere head:")
    print(X_biere.head())

    # Prédictions
    preds_biere = model_biere.predict(X_biere.to_numpy())
    preds_soft = model_soft.predict(X_soft.to_numpy())
    preds_pizza = model_pizza.predict(X_pizza.to_numpy())

    # Log des prédictions brutes
    print("===== PRÉDICTIONS BRUTES =====")
    for i, (b, s, p) in enumerate(zip(preds_biere, preds_soft, preds_pizza)):
        print(f"Participant {i+1}: Bière={b:.2f}, Soft={s:.2f}, Pizza={p:.2f}")

    # Arrondir les prédictions négatives à 0
    preds_biere = np.maximum(0, preds_biere)
    preds_soft = np.maximum(0, preds_soft)
    preds_pizza = np.maximum(0, preds_pizza)

    total = {
        "beer": round(float(np.sum(preds_biere)), 2),
        "soft": round(float(np.sum(preds_soft)), 2),
        "pizza": round(float(np.sum(preds_pizza)), 2),
    }

    par_personne = []
    for b, s, p in zip(preds_biere, preds_soft, preds_pizza):
        par_personne.append(
            {
                "beer": int(round(b)),
                "softDrink": int(round(s)),
                "pizzaSlice": int(round(p)),
            }
        )

    print("===== RÉSULTATS FINAUX PAR PERSONNE =====")
    for i, pp in enumerate(par_personne):
        print(f"Participant {i+1}: {pp}")

    total_unit = to_units(total)
    print(f"Total units: {total_unit}")

    return PredictionResponse(total_units=total_unit, par_personne=par_personne)
