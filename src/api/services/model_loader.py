"""
Model Loader Service
Manages loading and caching of ML models from joblib files.
"""

from joblib import load
from typing import Tuple, Any, Dict
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DEFAULT_MODEL_DIR = os.path.join(BASE_DIR, "shared", "model")


class ModelLoader:
    """Loads and manages ML models for predictions."""

    _instance = None
    _models_cache = {}

    def __new__(cls):
        """Singleton pattern to ensure only one loader instance."""
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def load_models(
        self, model_dir: str = DEFAULT_MODEL_DIR
    ) -> Dict[str, Tuple[Any, list]]:
        """
        Load all ML models from directory.

        Args:
            model_dir: Directory containing model files

        Returns:
            Dictionary with model names as keys and (model, columns) tuples as values
        """
        if self._models_cache:
            return self._models_cache

        try:
            self._models_cache["beer"] = load(
                os.path.join(model_dir, "model_biere.joblib")
            )
            self._models_cache["soft"] = load(
                os.path.join(model_dir, "model_soft.joblib")
            )
            self._models_cache["pizza"] = load(
                os.path.join(model_dir, "model_pizza.joblib")
            )

            print("✓ Models loaded successfully")
            return self._models_cache

        except FileNotFoundError as e:
            raise RuntimeError(f"Model file not found: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading models: {e}")

    def get_model(self, model_name: str) -> Tuple[Any, list]:
        """Get a specific model by name."""
        if not self._models_cache:
            self.load_models()

        if model_name not in self._models_cache:
            raise ValueError(
                f"Model '{model_name}' not found. Available: {list(self._models_cache.keys())}"
            )

        return self._models_cache[model_name]


# Global loader instance
_loader = ModelLoader()


def get_models() -> Dict[str, Tuple[Any, list]]:
    """Get all loaded models."""
    return _loader.load_models()


def get_model(name: str) -> Tuple[Any, list]:
    """Get a specific model."""
    return _loader.get_model(name)
