from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime


class ProfilParticipant(BaseModel):
    gender: Literal["Male", "Female"]
    age: int
    height: int
    weight: int
    alcoholConsumption: Literal["Occasional", "Regular", "Veteran"]


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
