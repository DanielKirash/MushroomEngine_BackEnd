from fastapi import APIRouter, HTTPException, status
from models.basemodel import Impianti
from utils.utils import plants_collection

router_impianti = APIRouter()
