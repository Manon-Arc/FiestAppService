# 🎯 Algorithme de Prédiction pour Soirées (Random Forest From Scratch)

## Objectif

Ce projet implémente **from scratch** un modèle de type **Random Forest Regressor** en Python (sans utiliser `sklearn`) pour prédire les besoins en **bière**, **boissons softs** et **pizza** lors d’une soirée, à partir :
- du **profil des participants**,
- du **contexte de la soirée**.

---

## 🧠 Concepts ML utilisés

### ✅ Implémentés manuellement :
- `DecisionTreeRegressor` : arbre de décision pour la régression
- `RandomForestRegressor` : combinaison de plusieurs arbres via bagging
- Sélection de la meilleure variable de split via **minimisation de la MSE**
- Gestion de l’**échantillonnage aléatoire** (bootstrapping)
- **Agrégation des prédictions** via moyenne

### ❌ Non utilisés :
Aucune dépendance à `scikit-learn`, `xgboost`, `lightgbm`, etc.

---

## 🗂️ Structure du projet

```
/model/
    └── model.py              ← Arbre + Forêt codés manuellement
    └── model_biere.joblib    ← Modèle sauvegardé (joblib)
    └── model_soft.joblib
    └── model_pizza.joblib

/data/
    └── data_soiree_train.csv ← Données d'entraînement

/train/
    └── train_model.py        ← Entraînement des 3 modèles
```

---

## 🧾 Données d’entrée

Les données sont basées sur des profils typés :

```python
class ContexteSoiree(BaseModel):
    saison: Literal["été", "hiver", "printemps", "automne"]
    heure_debut: datetime
    heure_fin: datetime
    lieu: Literal["intérieur", "extérieur"]

class ProfilParticipant(BaseModel):
    genre: Literal["homme", "femme"]
    age: int
    taille: float
    poids: int
    conso_level: Literal["occasionnel", "régulier", "aguerri"]
    boit_ce_soir: Literal["pas du tout", "peu", "normal", "beaucoup"]
```

> Ces données sont transformées via `pandas.get_dummies()` pour l’entraînement.

---

## 🧪 Entraînement

Script : `train_model.py`

```python
model_biere = RandomForestRegressor(n_estimators=10)
model_biere.fit(X.to_numpy(), y_biere.to_numpy())
```

Le modèle est entraîné pour chaque produit (`biere`, `soft`, `pizza`) séparément, puis sauvegardé avec `joblib`.

---

## 📦 Prédictions

- En production, les features sont générées depuis les `ProfilParticipant` et `ContexteSoiree`
- Une requête JSON est transformée en `pandas.DataFrame` d’entrée pour le modèle
- Le modèle renvoie les prédictions par personne ou globalement

---

## 📐 Unité de sortie

Les prédictions sont fournies :
- en **unités individuelles** : verre soft, part de pizza
- en **unités regroupées** :
    - 1 bouteille = 5 verres
    - 1 pizza = 8 parts

---

## 🧩 À améliorer

- Implémentation d’un système de **feature importance**
- Ajout de **cross-validation** ou tuning de paramètres
- Ajout d’un backend Python (FastAPI/gRPC) pour servir le modèle

---

## 🔧 Dépendances minimales

```bash
pip install numpy pandas joblib
```

---

## 👤 Auteur

Ce projet est une **implémentation originale d’un algorithme d’intelligence artificielle** pour prédire la consommation lors de soirées, dans le cadre d’un projet personnel complexe.