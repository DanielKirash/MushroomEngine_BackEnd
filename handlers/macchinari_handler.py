from fastapi import APIRouter, HTTPException, status
from models.basemodel import Macchinari
from utils.utils import plants_collection, machinery_collection
from utils.utils import toString
from bson.objectid import ObjectId

router_macchinari = APIRouter()

@router_macchinari.get("/macchinari/{id}")
async def get_macchinaro(id_macchinario: str):
    macchinario = machinery_collection.find_one({"_id": ObjectId(id_macchinario)})
    if macchinario:
        macchinario["_id"] = toString(macchinario["_id"])
        return macchinario
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail={"message": "Id non trovato"})
    

@router_macchinari.get("/macchinari")
async def get_macchinari():
    macchinari = list(machinery_collection.find())
    for macchinario in macchinari:
        macchinario["_id"] = toString(macchinario["_id"])
        return macchinari

    
@router_macchinari.post("/impianti/{id}/macchinari")
async def create_macchinari(id_impianto: str, macchinario: Macchinari):
    macchinario.plant_id = id_impianto
    response = machinery_collection.insert_one(macchinario.model_dump())
    macchinario_dict = macchinario.model_dump()
    macchinario_dict["_id"] = toString(response.inserted_id)
    plants_collection.update_one({"_id": ObjectId(id_impianto)},
                                 {"$push": {"macchinari": macchinario_dict}})
    return macchinario_dict

@router_macchinari.delete("/macchinari/{id}")
async def delete_macchinario(id_macchinario: str):
    da_eliminare = machinery_collection.find_one({"_id": ObjectId(id_macchinario)})
    if da_eliminare:
        machinery_collection.delete_one({"_id": ObjectId(id_macchinario)})
        id = da_eliminare["plant_id"]
        plants_collection.update_one({"_id": ObjectId(id)},
                                     {"$pull": {"macchinari": str(id_macchinario)}})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "Id non trovato"})