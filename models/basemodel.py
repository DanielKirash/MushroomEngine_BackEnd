from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Ruolo(Enum):
    #Ruoli possibili per un utente
    admin = "admin"
    user = "user"

class Utente(BaseModel):
    #Classe per la rappresentazione di un utente
    username: str = Field(...)
    password: str = Field(...)
    # ruolo: Ruolo = Field(...)

class Macchinari(BaseModel):
    #Classe per la rappresentazione di una macchina
    plant_id: str
    name: str
    type: str
    status: str

class Impianti(BaseModel):
    #Classe per la rappresentazione di un impianto
    name: str
    location: str
    description: str
    machinery: List[Macchinari] = []