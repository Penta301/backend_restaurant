import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import authentication, restaurant, food, service, order, quests_tables

app = FastAPI()

origins = ['https://localhost:3000',]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(app)

app.include_router(food.router)
app.include_router(authentication.router)
app.include_router(restaurant.router)
app.include_router(service.router)
app.include_router(order.router)
app.include_router(quests_tables.router)

if __name__ == '__main__':
    uvicorn.run(app,
                host="0.0.0.0",
                port=8432,
                ssl_keyfile="./localhost+4-key.pem", 
                ssl_certfile="./localhost+4.pem"
                )
