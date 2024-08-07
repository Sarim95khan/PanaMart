from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import select

import json
from aiokafka import AIOKafkaProducer

from app.db import get_session, Session,Inventory

from app.models import InventoryUpdate, InventoryDelete, InventoryCreate
from app.kafka.producer import get_kafka_producer

inventory_router = APIRouter(tags=["inventory"], prefix="/inventory")


@inventory_router.get('/')
def get_all_stock(session:Annotated[Session,Depends(get_session)]):
    stmt = select(Inventory)
    result = session.exec(stmt).all()
    return result


@inventory_router.post('/create-inventory')
async def create_inventory(inventory:InventoryCreate, session:Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    db_inventory = Inventory.model_validate(inventory)
    
    data = {
        "product_id":db_inventory.product_id,
        "stock":db_inventory.stock
    }

    data_json = json.dumps(data).encode('utf-8')
    print("JSON data in add-stock topic producer", data_json)
    await producer.send_and_wait('add-stock',data_json)

    # session.add(db_inventory)
    # session.commit()
    # session.refresh(db_inventory)
    return db_inventory

@inventory_router.patch('/update-inventory/{inventory_id}')
def update_product(inventory_id:int, inventory:InventoryUpdate , session:Annotated[Session, Depends(get_session)]):
    db_inventory = session.get(Inventory, inventory_id)
    if not db_inventory:
        return {"message": "Inventory not found"}
    inventory_data = inventory.model_dump(exclude_unset=True)
    db_inventory.sqlmodel_update(inventory_data)
    session.add(db_inventory)
    session.commit()
    return db_inventory

    