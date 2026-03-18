"""
FiestApp Service API
REST API for party consumption predictions using Machine Learning models.

Architecture:
  - Layer 1 (API): Routes and request handling (this file)
  - Layer 2 (Services): Business logic, normalization, and model inference (services/)
"""

import logging
from typing import List

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.Dtos import PredictionResponse, ProfilParticipant
from api.services import PredictionService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# FastAPI Application Configuration
# ============================================================================

app = FastAPI(
    title="FiestApp Service API",
    description="""
## 🍻 Party Consumption Prediction API

This API uses **Machine Learning** models to predict the consumption of beer, soft drinks, 
and pizzas based on participant profiles.

### Features

- **Personalized predictions**: Based on age, gender, weight, height, and consumption habits
- **ML models**: Random Forest Regressors
- **Detailed results**: Per-person and total consumption with purchase units
- **Clean Architecture**: Separated API and business logic layers
""",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"},
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
    },
)


# ============================================================================
# Exception Handlers
# ============================================================================


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Handle validation errors with 400 (Bad Request) instead of 422.
    Returns structured error details for the client.
    """
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(loc) for loc in error["loc"][1:]),  # Skip "body"
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Invalid request format",
            "errors": errors,
        },
    )


# ============================================================================
# Service Initialization
# ============================================================================

prediction_service = PredictionService()
logger.info("✓ Prediction service initialized")


# ============================================================================
# API Endpoints
# ============================================================================


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict party consumption",
    description="""
Predicts the consumption of beer, soft drinks, and pizza slices for a list of participants.

**Input:** List of participant profiles
- `age`: Age in years (integer)
- `gender`: "man" or "woman"
- `height`: Height in centimeters (integer)  
- `weight`: Weight in grammes (integer)
- `alcoholConsumption`: "never", "casual", "regular", or "seasoned"

**Output:** 
- `total_units`: Aggregate quantities with purchase units (cases/bottles/pizzas)
- `par_personne`: Per-participant consumption breakdown

**Note:** Participants under 18 years will automatically have alcohol consumption set to "never".
""",
    tags=["Predictions"],
)
def predict(participants: List[ProfilParticipant]) -> PredictionResponse:
    """
    Endpoint to generate consumption predictions for party participants.

    Delegates to PredictionService which handles:
    1. Input normalization and validation
    2. Feature engineering (one-hot encoding)
    3. Model inference
    4. Result aggregation and formatting
    """
    logger.info(f"📊 Received prediction request for {len(participants)} participants")

    return prediction_service.generate_predictions(participants)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "FiestApp Prediction API"}
