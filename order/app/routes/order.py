from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import select
from aiokafka import AIOKafkaProducer
import json

from app.db import get_session, Session
from app.models import Order, OrderCreate,OrderUpdate
from app.kafka.producer import get_kafka_producer
order_router = APIRouter(tags=["order"], prefix="/order")


@order_router.get('/')
def get_all_product(session:Annotated[Session,Depends(get_session)]):
    stmt = select(Order)
    result = session.exec(stmt).all()
    return result


@order_router.post('/create-order')
async def create_order(order:OrderCreate, session:Annotated[Session,Depends(get_session)],producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    db_order = Order.model_validate(order) 
    kafka_order = {
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity
    }
    json_data = json.dumps(kafka_order).encode('utf-8')
    print("Encoded Kafka ORDER", json_data)

    await producer.send_and_wait('create-order', json_data)

    # Creating order producer
    

    # session.add(db_order)
    # session.commit()
    # session.refresh(db_order)
    return json_data

# @product_router.patch('/update-order/{order_id}')
# def update_order(order_id:int, order:OrderUpdate , session:Annotated[Session, Depends(get_session)]):
#     db_order = session.get(Order, order_id)
#     if not db_order:
#         return {"message": "Product not found"}
#     order_data = order.model_dump(exclude_unset=True)
#     db_order.sqlmodel_update(order_data)
#     session.add(db_order)
#     session.commit()
#     return db_order

    