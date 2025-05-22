# routers.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from middleware import *
import requests
from typing import Optional

router = APIRouter(
    prefix="/exchange",
    tags=["exchange"]
)

API_URL = "https://economia.awesomeapi.com.br/json/last/"

###################################
##### Routers Functions Below #####
###################################

#Default function, change as needed
@router.get("")
async def root_func():
    return {"message": "Root function ran!"}

@router.get("/{currency1}/{currency2}", status_code=200)
async def convert_currency(currency1: str, currency2: str, 
                           cookie: AuthToken = Depends(get_cookie_as_model)):
    try:
        exchange_rate = requests.get(API_URL + f"{currency1}-{currency2}")
        if not exchange_rate:
            raise HTTPException(400, detail="Erro ao realizar request de exchange")
        if exchange_rate.status_code != 200:
            raise HTTPException(status_code=exchange_rate.status_code, detail=exchange_rate.json().get("detail"))
        
        exchange_rate = exchange_rate.json()[f"{currency1}{currency2}"]
        response = {
            "sell": exchange_rate["high"],
            "buy": exchange_rate["low"],
            "date": exchange_rate["create_date"],
            "id_account": cookie.user_id
        }
        return response


    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
