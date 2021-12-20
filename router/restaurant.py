from database import pay_service_mercadopago
import sys
sys.path.append('..')
from fastapi import HTTPException, APIRouter
from backend.model import Restaurant, Show_Restaurant
from backend.database import (
    collection_restaurant, 
    create_operation,
    update_operation,
    remove_operation,
)

router = APIRouter(
    prefix="/api",
    tags=['Restaurant']
)

@router.post("/restaurant_create/", response_model = Show_Restaurant)
async def post_todo(restaurant: Restaurant):
    restaurant = restaurant.dict()
    response = await create_operation(restaurant, collection_restaurant, 'owner', 'owner')
    if response == "error_name":
        raise HTTPException(400, "That username exist")
    if response:
        return response

    raise HTTPException(400, "Something went wrong")

@router.put("/restaurant_edit/{name}/{where}")
async def edit_operation(name:str, where:str ,restaurant:Restaurant ):
    response = await update_operation(collection_restaurant, name, restaurant.dict(), where)
    if response:
        return "Succesfully edited"
    raise HTTPException(404, f"That restaurant with the name: {name}, doesn't exist")

@router.delete("/restaurant_delete/{name}/")
async def delete_operation(name ):
    response = await remove_operation(collection_restaurant, name)
    if response:
        return "Succesfully deleted operation"
    raise HTTPException(404, f"That restaurant with the name: {name}, doesn't exist")