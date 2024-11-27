from fastapi import APIRouter, HTTPException, status
from models.basemodel import Utente
from utils.utils import users_collection
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/login")
async def login(Utente: Utente):
    utente = users_collection.find_one({"username": Utente.username})
    if utente and utente["password"] == Utente.password:
        return {"message": "Utente autenticato con successo"}
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Utente non trovato, ricontrollare i dati"})