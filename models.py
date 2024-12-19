from enum import Enum

class BlogType(str,Enum):
    news = 'news'
    article = 'article'
    blog = 'blog'
