from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import Optional
from typing import AsyncGenerator, Annotated
from starlette.middleware.cors import CORSMiddleware
from app.routes import user, login
from sqlmodel import SQLModel,Field
import json



from aiokafka import AIOKafkaProducer



from app.db import create_db_and_tables 


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="User Auth API with DB",
               servers=[
        {
            "url": "http://127.0.0.1:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        },
        ]  )

app.include_router(router = user.user_router)
app.include_router(router = login.login_router)


app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],    
        allow_headers=["*"],
        
    )


@app.get('/')
def root():
    return {'message': 'Hello Auth Sairm ok??    '}





