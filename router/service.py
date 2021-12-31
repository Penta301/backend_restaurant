import requests
from fastapi import HTTPException, APIRouter
from model import Service, Payed_service
import datetime
from database import (
    pay_service_mercadopago,
    collection_payed_service,
    create_operation
)

router = APIRouter(
    prefix="/api/service",
    tags=['Service']
)

@router.post("/pay_service/")
async def pay_service(service:Service):
    service = service.dict()

    response = await pay_service_mercadopago(service)
    response = response['mercado_pago_response']['id']
    
    if response:
        await create_operation({'owner':service['owner'], 'type_plan':service['title'], 'date':datetime.datetime.now(), 'pay_id':response}, collection_payed_service)
        return response

    raise HTTPException(400, "Something went wrong")

@router.post("/notification_url/{topic}/{id}", status_code=200)
async def handle_ipn(topic, id):
    print(topic, id)
