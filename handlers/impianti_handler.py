from fastapi import APIRouter, HTTPException, status
from models.basemodel import Impianti
from utils.utils import plants_collection
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

@router_impianti.get("/impianti/{id}")
async def get_impianto(id_impianto: str):
    impianto = plants_collection.find_one({"_id": ObjectId(id_impianto)})
    if impianto:
        impianto["_id"]=toString(impianto["_id"])
        return impianto
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail={"message": "Id non trovato"})