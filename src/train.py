import pandas as pd
import numpy as np
from model import RandomForestRegressor
from joblib import dump

np.random.seed(35)  # 🔒 REND LES TIRAGES ALÉATOIRES REPRODUCTIBLES

data = pd.read_csv("./data/data_soiree_user.csv")

# Préparation des données - GARDER toutes les colonnes nécessaires
df_encoded = pd.get_dummies(data, columns=["gender", "alcoholConsumption"])

# Séparer les features et les targets
X = df_encoded.drop(columns=["beer", "softDrink", "pizzaSlice"])
y_biere = df_encoded["beer"]
y_soft = df_encoded["softDrink"]
y_pizza = df_encoded["pizzaSlice"]

print(f"Forme de X après one-hot encoding: {X.shape}")
print(f"Colonnes dans X: {X.columns.tolist()}")
print(f"Nombre de caractéristiques: {X.shape[1]}")

# Vérifier les statistiques des targets
print(f"\nStatistiques des targets:")
print( f"Bière - Min: {y_biere.min()}, Max: {y_biere.max()}, Moyenne: {y_biere.mean():.2f}")
print(f"Soft - Min: {y_soft.min()}, Max: {y_soft.max()}, Moyenne: {y_soft.mean():.2f}")
print(f"Pizza - Min: {y_pizza.min()}, Max: {y_pizza.max()}, Moyenne: {y_pizza.mean():.2f}")

# Entraînement avec des paramètres plus robustes
model_biere = RandomForestRegressor(n_estimators=100, max_depth=8, min_samples=5)
model_biere.fit(X.to_numpy(), y_biere.to_numpy())

model_soft = RandomForestRegressor(n_estimators=100, max_depth=8, min_samples=5)
model_soft.fit(X.to_numpy(), y_soft.to_numpy())

model_pizza = RandomForestRegressor(n_estimators=100, max_depth=8, min_samples=5)
model_pizza.fit(X.to_numpy(), y_pizza.to_numpy())

# Test sur les données d'entraînement
y_pred_biere = model_biere.predict(X.to_numpy())
y_pred_soft = model_soft.predict(X.to_numpy())
y_pred_pizza = model_pizza.predict(X.to_numpy())

print(f"\nTest sur données d'entraînement:")
print(f"Bière - Prédictions: {y_pred_biere[:5]}")
print(f"Bière - Vraies valeurs: {y_biere.to_numpy()[:5]}")
print(f"Soft - Prédictions: {y_pred_soft[:5]}")
print(f"Soft - Vraies valeurs: {y_soft.to_numpy()[:5]}")
print(f"Pizza - Prédictions: {y_pred_pizza[:5]}")
print(f"Pizza - Vraies valeurs: {y_pizza.to_numpy()[:5]}")

# Sauvegarde des modèles et colonnes
dump((model_biere, X.columns.tolist()), "./model/model_biere.joblib")
dump((model_soft, X.columns.tolist()), "./model/model_soft.joblib")
dump((model_pizza, X.columns.tolist()), "./model/model_pizza.joblib")

print("Modèles entraînés et sauvegardés avec succès!")
