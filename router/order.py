import sys
from model import Order, filter_model_id
from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from database import (
collection_order,
create_operation,
fetch_all,
replace_operation,
replace_many_operation
)

router = APIRouter(
    prefix="/api/orders",
    tags=['Orders']
)


@router.post('/create_order/')
async def verify_restaurant(order:Order):
    order = order.dict()
    response = await create_operation(order, collection_order)
    if response:
        response_id = str(response['_id'])
        return response_id
    raise HTTPException(400, "Something went wrong")

@router.get('/get_order/{restaurant}')
async def get_order(restaurant:str):
    response = await fetch_all(collection_order, Order, {'restaurant':restaurant, 'payed':False}, False)
    if response:
        procesed_response = filter_model_id(response)
        return procesed_response
    return []

@router.post('/complete_order/{id}')
async def complete_order(id:str, update_order:Order):
    update_order = update_order.dict()
    update_order['completed'] = True
    response = await replace_operation(collection_order, {'_id':ObjectId(id)}, update_order)
    if response.matched_count:
        return {'response':'Updated sucessfully'}
    raise HTTPException(404, "Order not found")

@router.post('/uncomplete_order/{id}')
async def uncomplete_order(id:str, update_order:Order):
    update_order = update_order.dict()
    update_order['completed'] = False
    response = await replace_operation(collection_order, {'_id':ObjectId(id)}, update_order)
    if response.matched_count:
        return {'response':'Updated sucessfully'}
    raise HTTPException(404, "Order not found")

@router.post('/pay_table/')
async def pay_table(update_order:Order):
    update_order = update_order.dict()
    filter_model = {'table':{'$eq':update_order['table']}, 'restaurant':{'$eq':update_order['restaurant']}, 'payed':{'$eq':False}}
    replace_model = {"$set": {'completed':True, 'payed':True}}
    update = await replace_many_operation(collection_order, filter_model, replace_model)
    if update:
        return {'response':'Updated sucessfully'}
    raise HTTPException(404, "Order not found")

