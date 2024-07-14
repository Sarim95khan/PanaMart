from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import pbkdf2_sha256  
from app import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "Iam batman"
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_token(subject: str, expire_delta:timedelta):
    expire_time = datetime.utcnow() + expire_delta
    to_encode = {"exp":expire_time,"sub":str(subject)}
    jwt_encoded = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_encoded

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def verify_hash_hash_password(hash_pass1, hash_pass2):
    is_valid = pbkdf2_sha256.verify(hash_pass1, hash_pass2)
    return is_valid


def hash_password(password):
    return pwd_context.hash(password)
