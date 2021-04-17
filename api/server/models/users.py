from pydantic import BaseModel

class LoginUser(BaseModel):
    username: str
    password: str

class NewUser(BaseModel):
    username: str
    email: str
    password1: str
    password2: str