from database import pay_service_mercadopago
from fastapi import HTTPException, APIRouter
from model import Restaurant, Show_Restaurant
from database import (
    collection_restaurant, 
    create_operation,
    update_operation,
    remove_operation,
    fetch_one,
    update_many_operation,
    collection_food,
    collection_order,
    collection_payed_service
)

router = APIRouter(
    prefix="/api",
    tags=['Restaurant']
)

@router.post("/restaurant_create/")
async def post_todo(restaurant: Restaurant):
    restaurant = restaurant.dict()
    restaurant['name'] = restaurant['name'].strip().casefold()
    verification = await fetch_one(collection_restaurant, {'name':restaurant['name']})
    verification_service = await fetch_one(collection_payed_service, {'owner':restaurant['owner']})
    verification_owner_restaurants = await fetch_one(collection_restaurant, {'owner':restaurant['owner']}) 
    print('init verification')
    if verification:
        return {'message':'That restaurant name exist'} 
    if not verification_service:
        return {'message':'pay the service before create a Restaurant'}
    if verification_owner_restaurants:
        return {'message': 'There are more restaurants with that email asociated'}
    print('all verified')
    response = await create_operation(restaurant, collection_restaurant)
    if response:
        return {'message':'The restaurant was created'}

    raise HTTPException(400, "Something went wrong")

@router.put("/restaurant_edit/{name}")
async def edit_operation(name:str, restaurant:Restaurant):
    restaurant = restaurant.dict()
    restaurant['name'] = restaurant['name'].strip().casefold()
    filter_model_restaurant = {'owner': restaurant['owner'], 'name': name}
    filter_model = {'restaurant': name}
    response_food_edit = await update_many_operation(collection_food, {"$set": {'restaurant': restaurant['name']}}, filter_model)
    response_order_edit = await update_many_operation(collection_order, {"$set": {'restaurant': restaurant['name']}}, filter_model)
    response = await update_operation(collection_restaurant, filter_model=filter_model_restaurant, model = restaurant)
    if response:
        return "Succesfully edited"
    raise HTTPException(404, f"That restaurant with the name: {name}, doesn't exist")

@router.delete("/restaurant_delete/")
async def delete_operation(restaurant:Restaurant):
    restaurant = restaurant.dict()
    response = await remove_operation(collection_restaurant, remove_model=restaurant)
    if response:
        return "Succesfully deleted operation"
    raise HTTPException(404, f"That restaurant with the name: {name}, doesn't exist")

@router.get("/restaurant_color_scheme/{restaurant}")
async def get_color_scheme(restaurant:str):
    response = await fetch_one(collection_restaurant, {'name':restaurant}, Restaurant)
    if response:
        return response.dict()['color_configuration'] 
    raise HTTPException(404, f"That restaurant with the name: {name}, doesn't exist")
