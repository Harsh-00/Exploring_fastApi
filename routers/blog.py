from fastapi import APIRouter, status, Response,Query,Body,Path,HTTPException,Header,Cookie,Form,Depends
from models import BlogType,TestException
from typing import Optional,List,Dict  
from models import BlogModel
from auth.oauth2 import oauth2_schema



# router=APIRouter(prefix='/blog',tags=['Blogs'],) # can add tag here for all the apis in this file
router=APIRouter(prefix='/blog')



# get method -> path parameter, query parameter, predefined values
# tags -> categorize the api on swagger ui (shows well structured documentation)
# summary,description -> short and long description of the api, there are 2 ways to write description,one by using triple quotes and other by using variable
#response description -> used to describe the response of the api



# query parameter (THOSE VALUES THAT ARE NOT SHOWN IN THE URL)
# description -> used variable to write long description
# response description  
@router.get('/all',
         tags=['Blogs'],
         summary='Get all Blogs',
         description='Get all blogs with per page limit',
         response_description='All blogs fetched successfully')
def all_blogs(pages:int ,limit: int=10 , published: bool=True, verified:Optional[bool]=None) -> dict: 
    return {'data': 'All blogs', 'Total Pages': pages, 'Limit': limit, 'Published': published, 'Verified': verified}


#custom response
#custom header ( can see on UI threw inspect element)
#cookie 
@router.get('/allTypes',tags=['Blogs']) # token is used to authenticate the user
def all_types(res:Response,
              custom_header: Optional[List[str]]=Header(None),
              my_cookie: Optional[str]=Cookie(None), # get cookie (that is stored on client side with key as 'my_cookie')
              token:str=Depends(oauth2_schema)):  
    types = [type.name for type in BlogType]
    # converting list to string
    data=" ".join(types)
    response=Response(content=data,media_type='text/plain')
    response.set_cookie(key="Name",value="Harsh") #set cookie
    return response # response type is text
    # various media_types are : xml, text/plain, htmlfiles, streaming, etc



# combining path and query params
# tags -> used 2 here (will shown in both categories)
# description -> used triple quotes to write long description
@router.get('/{id}/comments/{comment_id}',
         tags=['Blogs','Comments'],
         summary='Get a comment') 
def read_comment(id:int, comment_id:int,valid:bool=False, username:Optional[str]=None )->dict:
    """ 
    **Parameters**
    - **id** : int : Blog id
    - **comment_id** : int : Comment id
    - **valid** : bool : Valid comment or not
    - **username** : str : Username of the commenter
    """
    return {'blog_id': id, 'comment_id': comment_id, 'valid': valid, 'username': username}



#predefined values
@router.get('/type/{type}',
         tags=['Blogs']) 
def blog_type(type: BlogType) -> dict:
    if type == BlogType.news:
        return {'data': 'News'}
    if type == BlogType.article:
        return {'data': 'Article'}
    if type == BlogType.blog:
        return {'data': 'Blog'}



# status code concept
# path parameter
# custom exception
@router.get('/{id}',
         tags=['Blogs']) 
def read_blog(id: int,res:Response) -> dict: # type checking (behind the scenes, it uses pydantic library to check)
    if id>=10: 
        res.status_code=status.HTTP_404_NOT_FOUND
        return {'message': 'Blog not found'}
    elif id==0: 
        raise TestException(name='Harsh') 
    else:
        res.status_code=status.HTTP_200_OK
        return {'message':"Blog found",'blog_id': id} 

 


# --------------------Post Method---------------------
# pydantic BaseModel is used to validate the request body
# I have implemented BlogModel in models.py file ( check out )



# req body converted from JSON to pydantic type -> data validation automatic, data conversion automatic
@router.post('/create',tags=['Blogs'])
def create_blog( blog:BlogModel)->dict:
    return {'data':blog}

# combined multiple things
@router.post('/create/{id}',tags=['Blogs'])
def create_blog_with_id(blog:BlogModel,id:int,res:Response,verified:Optional[bool]=None)->dict:
    if id<0:
        res.status_code=status.HTTP_400_BAD_REQUEST
        return {'message':'Invalid id'}
    
    if id>10: # similar as above
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invaliddd id')
    else:
        res.status_code=status.HTTP_201_CREATED
        return{'data':blog,'id':id,'verified':verified}



# parameter metadata -> information about the parameter (data about the data) (using Query)
# multiple value of same query parameter variable
# variable for Body
# number validators -> gt (greater than), ge (greater than or equal), lt, le
# used submodels in BlogModel
# used subtypes of data types ( list, dict)
@router.post('/create/{id}/comments/{num_valid}',tags=['Blogs'])
def create_comment(blog:BlogModel,id:int,
                   comment_id:int=Query(None,description='ID of comment',alias='CommentIdddd'),
                   username: str=Body(...,min_length=3,max_length=50,description='Username of the commenter'),
                   num_valid:int=Path(...,gt=10,le=20),
                   names:List[str]=[],
                   metadata:Dict[str,str]={'Harsh':'Good','Rohan':'Bad'},
                   version:Optional[List[float]]=Query(None)) : 
    return {'blog_id':id , 'comment_id':comment_id}




# Form -> type: application/x-www-form-urlencoded 
# pip install python-multipart
@router.post('/createForm',tags=['Blogs'])
def form_creation(name:str=Form(...),age:int=Form(...)):
    return {'name':name,'age':age} # return type is dict and content type is application/json