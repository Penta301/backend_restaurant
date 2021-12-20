from database import pay_service_mercadopago
import sys
sys.path.append('..')
from fastapi import HTTPException, APIRouter
from backend.model import Service
from backend.database import (
    pay_service_mercadopago,
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
        print(response)
        return response

    raise HTTPException(400, "Something went wrong")

# @router.post('/notification_pay/')
# async def notification_pay(notification):
#     notification