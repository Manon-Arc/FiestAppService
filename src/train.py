import pandas as pd
import numpy as np
from model import RandomForestRegressor
from joblib import dump

data = pd.read_csv('/data/data_soiree_train.csv')

# Préparation des données
X = pd.get_dummies(data.drop(columns=["biere", "soft", "pizza"]))
y_biere = data["biere"]
y_soft = data["soft"]
y_pizza = data["pizza"]

# Entraînement
model_biere = RandomForestRegressor(n_estimators=10)
model_biere.fit(X.to_numpy(), y_biere.to_numpy())

model_soft = RandomForestRegressor(n_estimators=10)
model_soft.fit(X.to_numpy(), y_soft.to_numpy())

model_pizza = RandomForestRegressor(n_estimators=10)
model_pizza.fit(X.to_numpy(), y_pizza.to_numpy())

# Sauvegarde des modèles et colonnes
dump((model_biere, X.columns.tolist()), "model/model_biere.joblib")
dump((model_soft, X.columns.tolist()), "model/model_soft.joblib")
dump((model_pizza, X.columns.tolist()), "model/model_pizza.joblib")
