from pydantic import BaseModel
from typing import Optional

class Service(BaseModel):
    owner:str
    title:str    
    quantity: Optional[int] = 1
    unit_price:int
    
class Show_Service(BaseModel):
    title:str    
    quantity:int
    unit_price:int

class Quest_table(BaseModel):
    type_quest:str
    restaurant:str
    table:int
    completed:bool

class Food(BaseModel):
    img:str
    name:str
    price:int
    restaurant: str
    type_food:str
    available:Optional[bool] = True
    amount:Optional[int] = 0
    delay:Optional[int] = 0
    desc:Optional[str] = ''

class Order(BaseModel):
    restaurant:str
    table:int
    total:int
    food:list
    completed:bool
    payed:bool

class Restaurant(BaseModel):
    owner:str
    name:str
    tables: Optional[int] = 0 

class Show_Restaurant(BaseModel):
    name:str
    tables: Optional[int] = 0
    food: Optional[list] = []
    requests: Optional[list] = []

def filter_model_id(array_of_models):
    filtered_arr = []
    for body in array_of_models:
        body['_id'] = str(body['_id']) 
        filtered_arr.append(body)
    return filtered_arr
