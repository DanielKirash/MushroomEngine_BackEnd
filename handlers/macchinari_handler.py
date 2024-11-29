from fastapi import APIRouter, HTTPException, status
from models.basemodel import Macchinari
from utils.utils import plants_collection, machinery_collection
from utils.utils import toString
from bson.objectid import ObjectId

router_macchinari = APIRouter()

@router_macchinari.get("/macchinari/{id}")
async def get_macchinaro(id: str):
    macchinario = machinery_collection.find_one({"_id": ObjectId(id)})
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
async def create_macchinari(id: str, macchinario: Macchinari):
    macchinario.plant_id = id
    response = machinery_collection.insert_one(macchinario.model_dump())
    plants_collection.update_one({"_id": ObjectId(id)},
                                 {"$push": {"macchinari": str(response.inserted_id)}})
    return {"_id": toString(response.inserted_id)}

@router_macchinari.delete("/macchinari/{id}")
async def delete_macchinario(id: str):
    da_eliminare = machinery_collection.find_one({"_id": ObjectId(id)})
    if da_eliminare:
        plant_id = da_eliminare["plant_id"]
        machinery_collection.delete_one({"_id": ObjectId(id)})
        plants_collection.update_one({"_id": ObjectId(plant_id)},
                                     {"$pull": {"macchinari": str(id)}})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "Id non trovato"})
    
@router_macchinari.put("/machinery/{machinery_id}")
async def update_macchinario(machinery_id: str, macchinario: Macchinari):
    # Trova il macchinario da aggiornare
    existing_macchinario = machinery_collection.find_one({"_id": ObjectId(machinery_id)})
    
    if not existing_macchinario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "Id non trovato"})
    updated_data = macchinario.model_dump()

    machinery_collection.update_one({"_id": ObjectId(machinery_id)},
                                    {"$set": updated_data})

    updated_macchinario = machinery_collection.find_one({"_id": ObjectId(machinery_id)})
    updated_macchinario["_id"] = toString(updated_macchinario["_id"])
    
    return updated_macchinario