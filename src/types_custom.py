from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime

class ContexteSoiree(BaseModel):
    saison: Literal["été", "hiver", "printemps", "automne"]
    heure_debut: datetime
    lieu: Literal["intérieur", "extérieur"]
    heure_fin: datetime

class ProfilParticipant(BaseModel):
    genre: Literal["homme", "femme"]
    age: int
    taille: float
    poids: int
    conso_level: Literal["occasionnel", "régulier", "aguerri"]
    boit_ce_soir: Literal["pas du tout", "peu", "normal", "beaucoup"]

class SoireeRequest(BaseModel):
    context: ContexteSoiree
    participants: List[ProfilParticipant]

class ProduitConsommation(BaseModel):
    biere: int
    verre_soft: int
    part_pizza: int

class ProduitConsommationUnit(BaseModel):
    biere: int
    bouteille_soft: int
    pizza: int

class PredictionResponse(BaseModel):
    total: ProduitConsommation
    total_units: ProduitConsommationUnit
    par_personne: List[ProduitConsommation]
