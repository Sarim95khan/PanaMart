from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends, HTTPException
from app.models import UserSignUp, UserModel, UserUpdateName, UserUpdatePassword
from app.routes.auth import hash_password,verify_password
from app.routes.service import get_user_by_email, create_user, current_user    
from app.db import Session, get_session


user_router = APIRouter(tags=["user"], prefix="/auth")


@user_router.get("/user/{user_id}")
async def get_user(user_id: int, session:Annotated[Session, Depends(get_session)]):
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/user/")
async def get_user(current_user:Annotated[UserModel, Depends(current_user)], session:Annotated[Session, Depends(get_session)]):
    return current_user

@user_router.post("/sign-up")
async def sign_up(user_data: UserSignUp, session:Annotated[Session,Depends(get_session)]):
    user = get_user_by_email(user_data.email,session)
    print("function get user", user_data)
    if not user:
        db_obj = UserModel.model_validate(
        user_data
    )
        db_obj.password = hash_password(db_obj.password)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return {"user":db_obj} 
    raise HTTPException(status_code=400, detail="User already exists")


@user_router.patch('/update-username')
async def update_user(current_user: Annotated[UserModel, Depends(current_user)], user_update: UserUpdateName, session:Annotated[Session, Depends(get_session)]):
    current_user_email = current_user.email
    existing_user = get_user_by_email(current_user_email, session)
    if existing_user and existing_user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Email already exists")
    user_data = user_update.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

    
@user_router.patch('/update-password')
async def update_password(current_user: Annotated[UserModel, Depends(current_user)], user_update: UserUpdatePassword, session:Annotated[Session, Depends(get_session)]):
    print("Current User passwprd", user_update.current_password)
    if  not verify_password(user_update.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if user_update.current_password == user_update.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_pwd = hash_password(user_update.new_password)
    current_user.password = hashed_pwd
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@user_router.delete("/delete-user")
def delete_user(current_user: Annotated[UserModel, Depends(current_user)], session:Annotated[Session, Depends(get_session)]):
    session.delete(current_user)
    session.commit()
    return {"message":"User deleted successfully"}
