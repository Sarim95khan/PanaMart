from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from typing import AsyncGenerator, Annotated, Optional
from sqlmodel import SQLModel, Field
import asyncio
# from app.kafka.consumer import consume_messages




from app.db import create_db_and_tables
from app.routes.product import product_router
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer


async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product-group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()



@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    # print("Creating tables..")
    # create_db_and_tables()
    print('Life Span')
    task = asyncio.create_task(consume_messages('create-product', 'broker:19092'))
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


@app.get('/')
def index():
    return {'message': 'Hello Product'}




