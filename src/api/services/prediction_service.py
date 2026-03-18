"""
Prediction Service
Core business logic for predictions: data normalization, feature engineering, and model inference.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from api.Dtos import ProfilParticipant, PredictionResponse
from api.services.utils import to_units
from api.services.model_loader import get_models
import logging

logger = logging.getLogger(__name__)


class DataNormalizer:
    """Handles input data normalization and validation."""

    VALID_GENDERS = {"man", "woman"}
    VALID_ALCOHOL_LEVELS = {"never", "casual", "regular", "seasoned"}
    GENDER_VARIANTS = {
        "male": "man",
        "m": "man",
        "homme": "man",
        "female": "woman",
        "f": "woman",
        "femme": "woman",
    }
    ALCOHOL_VARIANTS = {
        "never": "never",
        "non": "never",
        "casual": "casual",
        "occasionnel": "casual",
        "regular": "regular",
        "régulier": "regular",
        "seasoned": "seasoned",
        "veteran": "seasoned",
    }

    @staticmethod
    def normalize_gender(value: str) -> str:
        """Normalize gender to canonical form (man/woman)."""
        value_clean = value.strip().lower()
        return DataNormalizer.GENDER_VARIANTS.get(value_clean, value_clean)

    @staticmethod
    def normalize_alcohol(value: str, age: int) -> str:
        """Normalize alcohol consumption level. Enforces 'never' for minors < 18."""
        if age < 18:
            return "never"

        value_clean = value.strip().lower()
        return DataNormalizer.ALCOHOL_VARIANTS.get(value_clean, value_clean)

    @classmethod
    def normalize_participants(
        cls, participants: List[ProfilParticipant]
    ) -> pd.DataFrame:
        """
        Normalize a list of participant profiles.

        Returns:
            DataFrame with normalized data
        """
        normalized = []

        for p in participants:
            normalized_gender = cls.normalize_gender(p.gender)
            normalized_alcohol = cls.normalize_alcohol(p.alcoholConsumption, p.age)

            normalized.append(
                {
                    "age": p.age,
                    "gender": normalized_gender,
                    "height": p.height,
                    "weight": p.weight,
                    "alcoholConsumption": normalized_alcohol,
                }
            )

        df = pd.DataFrame(normalized)
        logger.debug(f"Normalized {len(df)} participants")

        return df


class FeatureEngineer:
    """Handles feature preparation and encoding."""

    @staticmethod
    def prepare_features(df: pd.DataFrame, expected_columns: List[str]) -> pd.DataFrame:
        """
        Prepare features with one-hot encoding.

        Args:
            df: DataFrame with raw features
            expected_columns: List of expected columns after encoding

        Returns:
            Encoded DataFrame with correct column order
        """
        # One-hot encoding for categorical features
        df_encoded = pd.get_dummies(
            df, columns=["gender", "alcoholConsumption"], drop_first=False
        )

        # Ensure all expected columns exist
        missing_cols = set(expected_columns) - set(df_encoded.columns)
        if missing_cols:
            logger.warning(f"Missing columns: {missing_cols}. Adding with value 0.")
            for col in missing_cols:
                df_encoded[col] = 0

        # Select and reorder columns
        df_encoded = df_encoded[expected_columns]
        logger.debug(f"Features prepared: {df_encoded.shape}")

        return df_encoded


class PredictionEngine:
    """Handles model inference and prediction aggregation."""

    def __init__(self):
        """Initialize prediction engine with loaded models."""
        self.models = get_models()
        self.model_beer, self.cols_beer = self.models["beer"]
        self.model_soft, self.cols_soft = self.models["soft"]
        self.model_pizza, self.cols_pizza = self.models["pizza"]

    def predict(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Run predictions on prepared features.

        Args:
            df: Normalized DataFrame with participant data

        Returns:
            Tuple of (beer_pred, soft_pred, pizza_pred) arrays
        """
        engineer = FeatureEngineer()

        # Prepare features for each model
        X_beer = engineer.prepare_features(df.copy(), self.cols_beer)
        X_soft = engineer.prepare_features(df.copy(), self.cols_soft)
        X_pizza = engineer.prepare_features(df.copy(), self.cols_pizza)

        # Get predictions
        preds_beer = self.model_beer.predict(X_beer.to_numpy())
        preds_soft = self.model_soft.predict(X_soft.to_numpy())
        preds_pizza = self.model_pizza.predict(X_pizza.to_numpy())

        # Ensure no negative predictions
        preds_beer = np.maximum(0, preds_beer)
        preds_soft = np.maximum(0, preds_soft)
        preds_pizza = np.maximum(0, preds_pizza)

        logger.debug(
            f"Predictions: beer={preds_beer.sum():.2f}, soft={preds_soft.sum():.2f}, pizza={preds_pizza.sum():.2f}"
        )

        return preds_beer, preds_soft, preds_pizza


class PredictionService:
    """
    Main service coordinating the entire prediction workflow.
    Coordinates: Data Normalization → Feature Engineering → Model Inference → Result Formatting
    """

    def __init__(self):
        """Initialize with prediction engine."""
        self.engine = PredictionEngine()

    def generate_predictions(
        self, participants: List[ProfilParticipant]
    ) -> PredictionResponse:
        """
        Generate predictions for a list of participants.

        Args:
            participants: List of participant profiles

        Returns:
            PredictionResponse with totals and per-person predictions
        """
        logger.info(f"Generating predictions for {len(participants)} participants")

        # Step 1: Normalize input data
        df_normalized = DataNormalizer.normalize_participants(participants)

        # Step 2: Run predictions
        preds_beer, preds_soft, preds_pizza = self.engine.predict(df_normalized)

        # Step 3: Aggregate results
        totals = {
            "beer": round(float(np.sum(preds_beer)), 2),
            "soft": round(float(np.sum(preds_soft)), 2),
            "pizza": round(float(np.sum(preds_pizza)), 2),
        }

        # Step 4: Format per-person results
        per_person = [
            {
                "beer": int(round(b)),
                "softDrink": int(round(s)),
                "pizzaSlice": int(round(p)),
            }
            for b, s, p in zip(preds_beer, preds_soft, preds_pizza)
        ]

        # Step 5: Convert to purchase units
        total_units = to_units(totals)

        logger.info(f"Predictions complete. Total: {totals}")

        return PredictionResponse(total_units=total_units, par_personne=per_person)
