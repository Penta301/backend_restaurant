import motor.motor_asyncio 
from mercadopago_config import create_mercadopago_items
import random

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.Restaurant
collection_payed_service = database.payed_service
collection_restaurant = database.restaurant
collection_food = database.restaurant_food 
collection_order = database.order
collection_quest = database.quest

async def fetch_all(collection, model, filter_model = False, exclude = True):
    if not filter_model:
        cursor = collection.find({})

    else:
        cursor = collection.find(filter_model)

    if not cursor:
        return cursor
    
    operations=[]
    if exclude:
        async for document in cursor:
            operations.append(model(**document))
        return operations

    async for document in cursor:
        operations.append(document)
    return operations

async def fetch_one(collection, filter_model, model=False):
    cursor = await collection.find_one(filter_model)
    if model:
        if cursor:
            return model(**cursor) 
    return cursor 

async def create_operation(model, collection):
    document = model
    await collection.insert_one(document)
    return document

async def update_operation(collection, model={}, filter_model=False):
    result = await collection.update_one(filter_model, {"$set":model})
    return result.matched_count

async def update_many_operation(collection, model, filter_model):
    result = await collection.update_many(filter_model, model)
    return result.matched_count

async def remove_operation(collection, remove_model = False):
    result = await collection.delete_one(remove_model)
    return result.deleted_count

async def replace_operation(collection, find_model, replace_model):
    result = await collection.replace_one(find_model, replace_model)
    return result

async def replace_many_operation(collection, find_model, replace_model):
    result = await collection.update_many(find_model, replace_model)
    return result

async def authenticate_operation(collection, where, name, specific):
    verification_name = await collection.find_one({where:name,})
    if verification_name:
        return verification_name[specific]
    
    return False

async def pay_service_mercadopago(model_pay):
    document = model_pay
    mercado_pago_response = create_mercadopago_items([document])

    response = {
        'mercado_pago_response':mercado_pago_response,
                }

    return response
