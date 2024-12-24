
from fastapi import APIRouter


router=APIRouter(prefix='/user',tags=['User'],)


@router.post('/signup')
def signup(username:str,password:str):
    return {'username':username,'password':password}

@router.post('/login')
def login(username:str,password:str):
    return {'username':username,'password':password}