from fastapi import APIRouter, HTTPException, status
from models.basemodel import Macchinari
from utils.utils import plants_collection, machinery_collection
from utils.utils import toString
from bson.objectid import ObjectId

router_macchinari = APIRouter()

@router_macchinari.get("macchinari/{id}")
async def get_macchinari(id_macchinario: str):
    macchinario = machinery_collection.find_one({"_id": ObjectId(id_macchinario)})
    if macchinario:
        macchinario["_id"] = toString(macchinario["_id"])
        return macchinario
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail={"message": "Id non trovato"})
    