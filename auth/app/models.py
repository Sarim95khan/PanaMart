from sqlmodel import SQLModel,Field
from pydantic import EmailStr, BaseModel

class UserModel(SQLModel,table=True):
    id: int|None = Field(default=None,primary_key=True)
    username :str= Field(min_length=3)
    email:EmailStr
    password : str


class UserSignUp(BaseModel):
    username: str
    email:str
    password:str

class UserUpdateName(BaseModel):
    username: str

class UserUpdatePassword(BaseModel):
    current_password: str
    new_password:str
