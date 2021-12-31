import sys
sys.path.append('..')
from fastapi import HTTPException, APIRouter, Depends 
from backend.model import Food
from backend.database import (
    collection_food, 
    create_operation,
    fetch_all,
    remove_operation,
    fetch_one
)
from cloudinaryBackend import uploader
router = APIRouter(
    prefix="/api",
    tags=['Food']
)

@router.post("/create_food/", response_model = Food)
async def post_todo(food: Food):
    food = food.dict()
    food['type_food'] = food['type_food'].strip().casefold()
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

@router.delete("/delete_food/{restaurant}/{food_name}")
async def delete_food(restaurant:str, food_name:str):
    remove_model = {'restaurant':restaurant, 'name':food_name}
    food = await fetch_one(collection_food, remove_model)
    response = await remove_operation(collection_food, remove_model=remove_model)
    
    if response:
        print(food)
        uploader.destroy(food['img'])
        return response
    raise HTTPException(404, 'Food not found')
