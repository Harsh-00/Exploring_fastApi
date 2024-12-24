from fastapi import APIRouter ,HTTPException,status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth import oauth2

router = APIRouter( tags=['authentication'],)

# for now,
USERNAME= 'harsh'
PASSWORD= 'harsh123'


# tokenURL must be same as the endpoint where the token is generated ( same as defined in oauth2.py)
@router.post('/tokennn')
def get_token(request:OAuth2PasswordRequestForm=Depends()):
    if not request.username==USERNAME or not request.password==PASSWORD: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid credentials')

    access_token=oauth2.create_access_token(data={'sub':request.username,'message':"All Good"})

    return {'access_token':access_token,'token_type':'bearer','message':'Login Successful'}


@router.get('/get_user')
def get_current_user(user:dict=Depends(oauth2.get_current_user)):
    return user