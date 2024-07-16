from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional


class Inventory(SQLModel,table=True):
    id : int|None = Field(default=None, primary_key=True)
    name: str
    description :str
    price:int |None= Field(default=None)



    
