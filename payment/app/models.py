from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional


# class Inventory(SQLModel,table=True):
#     id : int|None = Field(default=None, primary_key=True)
#     product_id : int
#     stock : Optional[int] =None
    

class InventoryUpdate(BaseModel):
    stock : int

class InventoryCreate(BaseModel):
    product_id : int
    stock : Optional[int] =None

class InventoryDelete(BaseModel):
    id : int



    
