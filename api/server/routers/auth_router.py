import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from server.models.users import LoginUser, NewUser
from server.database.users import checkIfUserExists, checkIfEmailExists, insertUser, getPasswordByUsername
from server.auth.auth import validateUsername, validateEmail, encryptPassword, comparePasswordAndHash

class Settings(BaseModel):
    authjwt_secret_key: str = "some-secret-jwt-key"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False


auth_router = APIRouter()

@AuthJWT.load_config
def get_config():
    return Settings()

# auth functions
@auth_router.post('/sign_up')
async def sign_up(newUser: NewUser) -> dict:
    # 1. Validate input data:
    # 1.1 Regex username and email + validate host
    if not validateUsername(newUser.username):
        raise HTTPException(status_code=400, detail="Username not valid")
    if not validateEmail(newUser.email):
        raise HTTPException(status_code=400, detail="Email not valid")
    # 2 Check if username and email are already taken
    if await checkIfUserExists(newUser.username):
        raise HTTPException(status_code=400, detail="Username is already taken")
    if await checkIfEmailExists(newUser.email):
        raise HTTPException(status_code=400, detail="Email is already taken")
    # 3 Compare passwords
    if newUser.password1 != newUser.password2:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    # 4 If match, create hash
    hashedPassword = encryptPassword(newUser.password1)
    # 5 Insert user
    result = await insertUser(newUser.username, newUser.email, hashedPassword)
    # 6 Send confirmation email as a background task: TODO
    return {"id": result}
    

@auth_router.post('/login')
async def login(user: LoginUser, Authorize: AuthJWT = Depends()):
    # 1. Check if username exists in the database
    # 2. Get user from the database
    # 3. Check if password is matching with the stored passwordhash
    # 4. If everything is ok, return token, if not throw an exception
    exists = await checkIfUserExists(user.username)
    if not exists:
        raise HTTPException(status_code=401, detail="Wrong username or password") #if user does not exists
    hashedPassword = await getPasswordByUsername(user.username)
    if hashedPassword is None or hashedPassword == "":
        raise HTTPException(status_code=500, detail="Error while getting password")

    if comparePasswordAndHash(user.password, hashedPassword) == False:
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return {"message": "Successfully logged in"}

@auth_router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    
    return {"message": "Successfully logged out"}


@auth_router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    Authorize.set_access_cookies(new_access_token)
    
    return {"message":"The token has been refresh"}