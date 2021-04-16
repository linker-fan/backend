import time
from typing import Dict
import jwt
from decouple import config

JWT_SECRET = config("jwt_secret")
JWT_ALGORITHM = config("jwt_algorithm")

def token_response(token: str){
    return {"token": token}
}

def signJWT(user_id: str, username: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "username": username,
        "expires": time.time() + 600 #expire in 10 minutes from this moment
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try