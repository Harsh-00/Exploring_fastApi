from fastapi import FastAPI,Request
from routers import blog,user
from auth import authentication
from models import TestException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List


app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)

@app.get("/")
def read_root() -> dict:  # type hinting, tell the return type of this function
    return {'message': "I am Noob"}

# exception handler
# @app.exception_handler(TestException)
# def test_exception_handler(request:Request, exc:TestException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} is testing."}
#     )




# CORS
origins=[
    "http://localhost:8000",
    "http://localhost"
]
# Note : http://localhost:8000/ (slash at the end, Not Valid) is different from http://localhost:8000 (no slash at the end, Valid)

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods= ["*"],
    allow_headers= ["*"],
) 