from model import filter_model_id, Quest_table
from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from database import (
collection_quest,
create_operation,
fetch_all,
fetch_one,
remove_operation,
replace_many_operation,
collection_order
)

router = APIRouter(
    prefix="/api/quest_tables",
    tags=['Quests']
)


@router.post('/new_quest/')
async def new_quest(quest:Quest_table):
    quest = quest.dict()
    verification = await fetch_one(collection_quest, quest)

    if verification:
        remove = await remove_operation(collection_quest, remove_model = verification)

    response = await create_operation(quest, collection_quest)
    if response:
        response_id = str(response['_id'])
        return response_id
    raise HTTPException(400, "Something went wrong")

@router.get('/get_quest/{restaurant}')
async def get_quest(restaurant:str):
    response = await fetch_all(collection_quest, Quest_table, exclude = False)
    if response:
        procesed_response = filter_model_id(response)
        return procesed_response
    return []

@router.post('/complete_quest/')
async def complete_quest(quest:Quest_table):
    quest = quest.dict()
    response = await remove_operation(collection_quest, remove_model=quest)
    if response:
        return {'response':'Updated sucessfully'}
    raise HTTPException(404, "Order not found")

@router.post('/complete_bill/')
async def complete_bill(quest:Quest_table):
    quest = quest.dict()
    filter_model = {'table':{'$eq':quest['table']}, 'restaurant':{'$eq':quest['restaurant']}, 'payed':{'$eq': False}}
    replace_model = {"$set": {'completed':True, 'payed':True}}
    update = await replace_many_operation(collection_order, filter_model, replace_model)
    if update:
        response = await remove_operation(collection_quest, remove_model=quest)
        if response:
            return {'response':'Updated sucessfully'}
        raise HTTPException(404, "Order not found")
    raise HTTPException(400, "Something went wrong")
