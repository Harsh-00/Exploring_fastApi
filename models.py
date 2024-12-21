from enum import Enum
from pydantic import BaseModel
from typing import Optional


class BlogType(str,Enum):
    news = 'news'
    article = 'article'
    blog = 'blog'

class Image(BaseModel):
    url: str
    name: str

class BlogModel(BaseModel):
    title: str
    content: str
    type: BlogType
    published: bool
    verified: Optional[bool]=False
    img: Optional[Image]=None