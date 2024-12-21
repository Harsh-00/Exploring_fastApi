from fastapi import FastAPI
from routers import blog


app = FastAPI()

app.include_router(blog.router)


@app.get("/")
def read_root() -> dict:  # type hinting, tell the return type of this function
    return {'message': "I am Noob"}
