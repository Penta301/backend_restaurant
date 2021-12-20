import sys
sys.path.append('..')
from fastapi import HTTPException, APIRouter, Depends 
from backend.model import Food
from backend.database import (
    collection_food, 
    create_operation,
    fetch_all
)

router = APIRouter(
    prefix="/api",
    tags=['Food']
)

@router.post("/create_food/", response_model = Food)
async def post_todo(food: Food):
    food = food.dict()
    if food['amount'] > 0:
        food['available'] = True
    else:
        food['available'] = False

    response = await create_operation(food, collection_food)    
    if response:
        return response
    raise HTTPException(400, 'Something wet wrong')


@router.get('/get_food/{restaurant}/') 
async def get_food(restaurant:str):
    response = await fetch_all(collection_food, Food, {'restaurant':restaurant})
    return response