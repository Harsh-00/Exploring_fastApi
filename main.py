from fastapi import FastAPI,status,Response
from models import BlogType
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root() -> dict:  # type hinting, tell the return type of this function
    return {'message': "I am Noob"}


# get method -> path parameter, query parameter, predefined values
# tags -> categorize the api on swagger ui (shows well structured documentation)
# summary,description -> short and long description of the api, there are 2 ways to write description,one by using triple quotes and other by using variable
#response description -> used to describe the response of the api



# query parameter (THOSE VALUES THAT ARE NOT SHOWN IN THE URL)
# description -> used variable to write long description
# response description  
@app.get('/blog/all',
         tags=['Blogs'],
         summary='Get all Blogs',
         description='Get all blogs with per page limit',
         response_description='All blogs fetched successfully')
def all_blogs(pages:int ,limit: int=10 , published: bool=True, verified:Optional[bool]=None) -> dict: 
    return {'data': 'All blogs', 'Total Pages': pages, 'Limit': limit, 'Published': published, 'Verified': verified}



# combining path and query params
# tags -> used 2 here (will shown in both categories)
# description -> used triple quotes to write long description
@app.get('/blog/{id}/comments/{comment_id}',
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
@app.get('/blog/type/{type}',
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
@app.get('/blog/{id}',
         tags=['Blogs']) 
def read_blog(id: int,res:Response) -> dict: # type checking (behind the scenes, it uses pydantic library to check)
    if id>=10: 
        res.status_code=status.HTTP_404_NOT_FOUND
        return {'message': 'Blog not found'}
    else:
        res.status_code=status.HTTP_200_OK
        return {'message':"Blog found",'blog_id': id} 
 