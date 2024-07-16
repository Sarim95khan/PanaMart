from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from app.routes.service import authenticate_user
from app.routes.auth import create_token
from fastapi import HTTPException,Depends
from app.db import get_session,Session
from datetime import timedelta  
import json

from aiokafka import AIOKafkaProducer

from app.kafka.producer import get_kafka_producer

login_router = APIRouter(tags=["login"], prefix="/auth")




@login_router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], session:Annotated[Session,Depends(get_session)],producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]  ):
    user = authenticate_user(form_data.username, form_data.password,session)
    print(user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    expire_time = timedelta(minutes=15)
    access_token = create_token(subject = user, expire_delta=expire_time)

    jwt_data = {
        "access_token": access_token
    }
    jwt_json = json.dumps(jwt_data).encode('utf-8')
    print("JWT_JSON", jwt_json)
    print("SENDING PRODUCER")
    await producer.send_and_wait('jwt', jwt_json)


    return {"access_token": 2321, "token_type": "bearer"}


