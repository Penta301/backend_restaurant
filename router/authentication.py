import sys
from model import Restaurant, Payed_service
from fastapi import APIRouter
from database import (
    collection_restaurant, 
    collection_payed_service,
    fetch_one
)

router = APIRouter(
    prefix="/api/authentication",
    tags=['authentication']
)


@router.post('/verify_restaurant/{owner}')
async def verify_restaurant(owner:str):
    authentication_restaurant = await fetch_one(collection_restaurant, {'owner':owner}, model=Restaurant)
    authentication_service = await fetch_one(collection_payed_service, {'owner':owner}, model=Payed_service)

    if authentication_restaurant or authentication_service:
        if not authentication_service.verified:
            pass

        response = {'service':authentication_service, 'restaurant':authentication_restaurant}
        return response

    response = {'service':False, 'restaurant':False}

    return response
