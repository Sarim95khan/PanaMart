from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from typing import AsyncGenerator, Annotated, Optional
from sqlmodel import SQLModel, Field
import asyncio

# from app.kafka.consumers.create_inventory import consume_message



from app.db import create_db_and_tables
from app.routes.payment import payment_router
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer




@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    # create_db_and_tables()
    print('Life Span')
    # task = asyncio.create_task(consume_messages('product-passed', 'broker:19092'))
    yield


app= FastAPI(
    lifespan=lifespan,
       servers=[
        {
            "url": "http://127.0.0.1:8004", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ]
)



app.include_router(payment_router)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get('/')
def index():
    return {'message': 'Hello Payment'}




