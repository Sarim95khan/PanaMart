from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id : int
    product_id :int
    quantity : int

    
class OrderCreate(BaseModel):
    user_id : int
    product_id :int
    quantity : int

class OrderUpdate(BaseModel):
    product_id :Optional[int]= None
    quantity : Optional[int]= None