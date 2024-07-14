from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional


class Product(SQLModel,table=True):
    id : int|None = Field(default=None, primary_key=True)
    name: str
    description :str
    price:int |None= Field(default=None)
    SKU:str|None= Field(default=None)
    qty:int|None = Field(default=None)


class ProductCreate(BaseModel):
    name: str
    description :str

class ProductUpdate(BaseModel):
    name:Optional[str] = None
    description : Optional[str] = None
    price:Optional[int]= None
    SKU:Optional[str]= None
    qty : Optional[int]= None
    
