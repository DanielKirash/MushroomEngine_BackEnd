from fastapi import APIRouter, HTTPException, status
from models.basemodel import Impianti
from utils.utils import plants_collection, machinery_collection
from utils.utils import toString
from bson.objectid import ObjectId

router_impianti = APIRouter()

@router_impianti.post("/impianti")
async def create_impianto(impianto: Impianti):
    response = plants_collection.insert_one(impianto.model_dump())
    return {"_id": toString(response.inserted_id)}

@router_impianti.get("/impianti")
async def get_impianti():
    impianti = list(plants_collection.find())
    for impianto in impianti:
        impianto["_id"] = toString(impianto["_id"])
    return impianti

@router_impianti.get("/impianti/{id}/")
async def get_impianto(id: str):
    impianto = plants_collection.find_one({"_id": ObjectId(id)})
    if impianto:
        impianto["_id"]=toString(impianto["_id"])
        return impianto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail={"message": "Id non trovato"})
    
@router_impianti.delete("/impianti/{id}")
async def delete_impianto(id: str):
    da_eliminare = plants_collection.find_one({"_id": ObjectId(id)})
    if da_eliminare:
        plants_collection.delete_one({"_id": ObjectId(id)})
        return {"message": "Eliminato con successo"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "Id non trovato"})

@router_impianti.put("/impianti/{id}")
async def update_impianto(id: str, impianto: Impianti):
    # Trova l'impianto da aggiornare
    existing_impianto = plants_collection.find_one({"_id": ObjectId(id)})
    
    if not existing_impianto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "Id non trovato"})

    updated_data = impianto.model_dump()

    plants_collection.update_one({"_id": ObjectId(id)},
                                 {"$set": updated_data})
    updated_impianto = plants_collection.find_one({"_id": ObjectId(id)})
    updated_impianto["_id"] = toString(updated_impianto["_id"])
    
    return updated_impianto

@router_impianti.get("/impianti_con_macchinari")
async def get_impianti_con_macchinari():
    impianti = list(plants_collection.find())
    for impianto in impianti:
        impianto["_id"] = toString(impianto["_id"])
        macchinari = list(machinery_collection.find({"plant_id": impianto["_id"]}))
        for macchinario in macchinari:
            macchinario["_id"] = toString(macchinario["_id"])
        impianto["macchinari"] = macchinari
    return impianti