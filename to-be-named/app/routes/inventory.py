from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import select
import json
from aiokafka import AIOKafkaProducer

from app.db import get_session, Session
from app.models import Product, ProductCreate, ProductUpdate
from app.kafka.producer import get_kafka_producer

product_router = APIRouter(tags=["product"], prefix="/product")


@product_router.get('/')
def get_all_stock(session:Annotated[Session,Depends(get_session)]):
    stmt = select(Product)
    result = session.exec(stmt).all()
    return result


@product_router.post('/create-product')
async def create_product(product:ProductCreate, session:Annotated[Session,Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    db_product = Product.model_validate(product)

    data = {
        "name":product.name,
        "description":product.description 
    }

    data_json = json.dumps(data).encode('utf-8')
    print("JSON data in Product producer", data_json)
    await producer.send_and_wait("create-product", data_json)

    # session.add(db_product)
    # session.commit()
    # session.refresh(db_product)
    return data_json

@product_router.patch('/update-product/{product_id}')
def update_product(product_id:int, product:ProductUpdate , session:Annotated[Session, Depends(get_session)]):
    db_product = session.get(Product, product_id)
    if not db_product:
        return {"message": "Product not found"}
    product_data = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    return db_product

    