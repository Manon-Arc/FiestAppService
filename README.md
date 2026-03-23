
# <img src="./assets/images/appicon.png" width="40" style="vertical-align: middle; border-radius: 10px"/> AI Recommendation Service – Drink & Food Predictor

Project by [__ARCAS__ Manon](https://github.com/Manon-Arc) and [__MACE__ Léo](https://github.com/LeoMa33)
Welcome to the AI service powering **FiestApp**'s smart food and drink recommendations.  
This repository provides a **from scratch implementation** of a **Random Forest Regressor** in Python to estimate consumption for **beer**, **soft drinks**, and **pizza** during events, based on participant profiles and event context.

<img alt="Python badge" src="https://img.shields.io/badge/Language-Python-green">

---

### 📌 Table of contents:

I. [About the project](#💡-about-the-project)

II. [ML Concepts Used](#🧠-ml-concepts-used)  

III. [Model Inputs & Outputs](#📐-model-input--output)  

IV. [Training Process](#🧪-training-process)  

V. [Architecture Overview](#🧩-architecture-overview)  

VI. [Project Structure](#📁-project-structure)  

VII. [Installation](#📥-install-the-project)  

---

### 💡 About the project :

This AI module is integrated into **[FiestApp](https://github.com/LeoMa33/FiestApp_App)** to provide smart and automatic estimation of party resources. Built without any ML libraries like `scikit-learn`, it demonstrates how to implement:

- A full Random Forest Regressor manually
- Prediction pipeline using dataclasses and JSON input
- Data pre-processing with Pandas
The model recommends quantities:
- **per person**: for example, 2 beers
- **globally**: for example, 3 bottles of soda, 5 pizzas

---

### 🧠 ML Concepts Used :

✅ **Implemented from scratch**:

- `DecisionTreeRegressor` using **MSE-based split**
- `RandomForestRegressor` using **bagging**
- **Bootstrap sampling** for diversity
- **Prediction aggregation** via mean

❌ **No external ML libraries**:

- No `scikit-learn`, `xgboost`, `lightgbm`, etc.

---

### 📐 Model Input & Output

#### 🎯 Input data:

```python
class ProfilParticipant(BaseModel):
    gender: Literal["man", "woman"]
    age: int
    height: int
    weight: int
    alcoholConsumption: Literal["never", "casual", "regular", "seasoned"]
```

Transformed into features with `pandas.get_dummies()`.

#### 📤 Output units:

- **Soft**: Glasses (5 glasses = 1 bottle)
- **Pizza**: Slices (8 slices = 1 pizza)
- **Bière**: Glasses

---

### 🧪 Training Process

```python
model_biere = RandomForestRegressor(n_estimators=10)
model_biere.fit(X.to_numpy(), y_biere.to_numpy())
```

- One model trained per product: **beer**, **soft**, **pizza**
- Models are saved using `joblib`:
  - `model_biere.joblib`
  - `model_soft.joblib`
  - `model_pizza.joblib`

---

### 🧩 Architecture Overview

```plaintext
                         AI SERVICE ARCHITECTURE

┌──────────────┐
│ FiestApp App │  ──▶  HTTPS POST JSON
└────┬─────────┘
     │
     ▼
┌─────────────────────────────────────┐
│       AI Python Service (FastAPI)  │
│                                     │
│ 1. Input JSON → DataFrame           │
│ 2. Predict: beer / soft / pizza     │
│ 3. Output formatted recommendations │
└─────────────────────────────────────┘
```

- Integrated as a **microservice** callable from the Flutter app via REST
- Offers per-participant or global recommendations

---

### 📁 Project Structure

```text
src/
├── api/
│   ├── app.py                     ← FastAPI application & error handling
│   ├── Dtos.py                    ← Pydantic models for API inputs/outputs
│   └── services/
│       ├── model_loader.py        ← Loading shared models
│       ├── prediction_service.py  ← Data normalization and prediction engine
│       └── utils.py               ← Utility functions (unit conversion)
├── shared/
│   └── model/
│       ├── model_biere.joblib     ← Trained model: beer
│       ├── model_soft.joblib      ← Trained model: soft drinks
│       └── model_pizza.joblib     ← Trained model: pizza
└── train/
    ├── train.py                   ← Training script
    ├── model.py                   ← DecisionTree & RandomForest implementation
    └── data/
        ├── generate.py            ← Data generation script
        └── data_soiree_user.csv   ← Training dataset

docker-compose.yml                 ← Docker Compose configuration
Dockerfile                         ← Docker image configuration
requirements.txt                   ← Python dependencies
```


### 📥 Install the project

#### 🐳 Docker Installation (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed

**Steps:**

1. **Clone the repository**
   ```bash
   git clone https://github.com/Manon-Arc/FiestAppService.git
   cd FiestAppService
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access the service**
   - API available at: `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`

**Docker commands:**

```bash
# Stop the service
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up --build -d
```


#### 🛠️ Local Development Installation

**Prerequisites:**
- Python 3.13+
- pip

**Steps:**

1. **Clone the repository**
   ```bash
   git clone https://github.com/Manon-Arc/FiestAppService.git
   cd FiestAppService
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate data file**

   ```bash
   cd src
   python -m train.data.generate 
   ```

4. **Train models (optional if already trained)**
   ```bash
   cd src
   python -m train.train    
   ```
5. **Run the FastAPI server**
   ```bash
   cd src
   python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Access the service**
   - API available at: `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`


#### 🔗 API Usage Example

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '[
            {
                "gender": "man",
                "age": 0,
                "height": 0,
                "weight": 0,
                "alcoholConsumption": "casual"
            }
        ]'
```
---

> Developed with ❤️ for the **[FiestApp](https://github.com/LeoMa33/FiestApp_App.git)** ecosystem.  

