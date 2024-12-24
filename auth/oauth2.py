from fastapi.security import OAuth2PasswordBearer
from fastapi.param_functions import Depends
from fastapi import HTTPException,status 
from datetime import timedelta,datetime
from typing import Optional
from jose import jwt,JWTError

oauth2_schema=OAuth2PasswordBearer(tokenUrl='tokennn') # tokenUrl is the endpoint where the token is generated

SECURITY_KEY='harsh'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES= 30

def create_access_token(data: dict,expire_delta: Optional[timedelta]=None): 
    to_encode=data.copy() # Copy the data to be encoded in the token
    if expire_delta:
        expire= datetime.utcnow()+expire_delta
    else:
        expire= datetime.utcnow()+timedelta(minutes=15)
    
    to_encode.update({'exp':expire}) # Add the expiration time to the data
    encoded_jwt=jwt.encode(to_encode,SECURITY_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token:str=Depends(oauth2_schema)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Token',
        headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload=jwt.decode(token,SECURITY_KEY,algorithms=[ALGORITHM])
        username: str= payload.get('sub')
        message: str= payload.get('message')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user={'username':username,'message':message}
    
    return user



