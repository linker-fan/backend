from fastapi import FastAPI
from pydantic import BaseModel

class AuthSettings(BaseModel): 
    authjwt

app = FastAPI()

