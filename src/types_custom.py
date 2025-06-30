from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime

class ContexteSoiree(BaseModel):
    saison: Literal["été", "hiver", "printemps", "automne"]
    heure_debut: datetime
    lieu: Literal["intérieur", "extérieur"]
    heure_fin: datetime

class ProfilParticipant(BaseModel):
    biologicalGender: Literal["male", "female"]
    age: int
    height: int
    weight: int
    alcoholConsumption: Literal["occasionally", "regularly", "seasoned"]

class SoireeRequest(BaseModel):
    context: ContexteSoiree
    participants: List[ProfilParticipant]

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
