import sys
sys.path.append('..')
from backend.model import Restaurant
from fastapi import APIRouter
from backend.database import (
    collection_restaurant, 
    collection_service,
    fetch_one
)

router = APIRouter(
    prefix="/api/authentication",
    tags=['authentication']
)


@router.post('/verify_restaurant/{owner}')
async def verify_restaurant(owner:str):
    authentication_restaurant = await fetch_one(collection_restaurant, {'owner':owner})

    if authentication_restaurant:
        authentication_restaurant.pop('_id')
    
        Restaurant(**authentication_restaurant)

        response = {'service':{'title':'plan1'}, 'restaurant':authentication_restaurant}

        return response

    response = {'service':False, 'restaurant':False}

    return response