from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime


class ProfilParticipant(BaseModel):
    gender: Literal["man", "woman"]
    age: int
    height: int
    weight: int
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
