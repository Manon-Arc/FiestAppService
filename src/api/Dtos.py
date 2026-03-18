from pydantic import BaseModel, Field
from typing import Literal, List
from datetime import datetime


class ProfilParticipant(BaseModel):
    gender: Literal["man", "woman"]
    age: int = Field(..., gt=0, description="The age must be greater than 0")
    height: int = Field(
        ..., gt=0, description="The height (in centimeters) must be greater than 0"
    )
    weight: int = Field(
        ..., gt=0, description="The weight (in grammes) must be greater than 0"
    )
    alcoholConsumption: Literal["never", "casual", "regular", "seasoned"]


class ProduitConsommation(BaseModel):
    beer: int
    softDrink: int
    pizzaSlice: int


class ProduitConsommationUnit(BaseModel):
    beer: int
    softBottle: int
    pizza: int


class PredictionResponse(BaseModel):
    total_units: ProduitConsommationUnit
    par_personne: List[ProduitConsommation]
