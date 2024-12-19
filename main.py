from fastapi import FastAPI
from models import BlogType 
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root() -> dict:  # type hinting, tell the return type of this function
    return {'message': "I am Noob"}

# get method -> path parameter, query parameter, predefined values

@app.get('/blog/all')
def all_blogs(pages:int ,limit: int=10 , published: bool=True, verified:Optional[bool]=None) -> dict: 
    # query parameter (THOSE VALUES THAT ARE NOT SHOWN IN THE URL)
    return {'data': 'All blogs', 'Total Pages': pages, 'Limit': limit, 'Published': published, 'Verified': verified}

# combining path and query params
@app.get('/blog/{id}/comments/{comment_id}')
def read_comment(id:int, comment_id:int,valid:bool=False, username:Optional[str]=None )->dict:
    return {'blog_id': id, 'comment_id': comment_id, 'valid': valid, 'username': username}

@app.get('/blog/type/{type}') #predefined values
def blog_type(type: BlogType) -> dict:
    if type == BlogType.news:
        return {'data': 'News'}
    if type == BlogType.article:
        return {'data': 'Article'}
    if type == BlogType.blog:
        return {'data': 'Blog'}
    
@app.get('/blog/{id}') # path parameter
def read_blog(id: int) -> dict: # type checking (behind the scenes, it uses pydantic library to check)
    return {'blog_id': id} 
