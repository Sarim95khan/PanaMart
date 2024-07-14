from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from typing import AsyncGenerator, Annotated, Optional
from sqlmodel import SQLModel, Field



from app.db import create_db_and_tables
from app.routes.product import product_router
from aiokafka import AIOKafkaProducer

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    yield

app= FastAPI(
    lifespan=lifespan,
       servers=[
        {
            "url": "http://127.0.0.1:8001", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ]
)

app.include_router(product_router)

app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    
    await producer.send_and_wait('sarim',b'OK Sarim')
    return todo

@app.get('/')
def index():
    return {'message': 'Hello Product'}




