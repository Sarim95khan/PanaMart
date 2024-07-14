from pydantic import EmailStr
from app.db import get_session,Session, select
from app.routes.auth import verify_password,decode_token, oauth2_scheme,verify_hash_hash_password
from typing import Annotated
from sqlmodel import select
from app.models import UserModel
from fastapi import HTTPException,status, Depends
from jose import JWTError
import json
from passlib.hash import pbkdf2_sha256  



def get_user_by_email(email:EmailStr,session:Session):
    print("Email recieved", email)
    stmt =  select(UserModel).where(UserModel.email == email)
    users = session.exec(stmt).first()
    print("USers", users)
    if not users:
        return False
    return users

def authenticate_user(email:str, password:str, session:Session):
    user = get_user_by_email(email,session)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def payload_data_seperate(payload):
    user_data = payload.get('sub')

    info_dict = {}
    pairs = user_data.split()
    for pair in pairs:
        key, value = pair.split('=')
        value = value.strip("'")
        info_dict[key] = value
    return info_dict


def current_user(token:Annotated[str,Depends(oauth2_scheme)], session:Annotated[Session,Depends(get_session)] ):
    credential = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        data = payload_data_seperate(payload)
           
        print("TYPE", type(data))
        user_email = data['email']
        user_password = data['password']
    except:
        raise JWTError
    
    user = get_user_by_email(user_email, session)
    print(user_password)
    if not user:
        raise credential
    return user

        



# CRUD
def create_user(user:UserModel, session:Session):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


