from pydantic import BaseModel
from typing import Optional
import datetime


class Service(BaseModel):
    owner:str
    title:str    
    quantity: Optional[int] = 1
    unit_price:int

class Payed_service(BaseModel):
    pay_id = int
    owner:str
    type_plan:str
    date: datetime.datetime
    verified: Optional[bool] = False

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
    color_configuration: Optional[dict] = {
        'main_text':'#ffffff',
        'brigth_color':'#4f46e5',
        'cancel_color':'#d62328',
        'background_color':'#1b2532',
        'structure':'modern'
            }
            

class Show_Restaurant(BaseModel):
    name:str
    color_configuration: Optional[dict] = {
        'main_text':'#ffffff',
        'brigth_color':'#4f46e5',
        'cancel_color':'#d62328',
        'background_color':'#1b2532',
            }
    tables: Optional[int] = 0
    food: Optional[list] = []
    requests: Optional[list] = []

def filter_model_id(array_of_models):
    filtered_arr = []
    for body in array_of_models:
        body['_id'] = str(body['_id']) 
        filtered_arr.append(body)
    return filtered_arr
