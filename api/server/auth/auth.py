import re
import bcrypt
from validate_email import validate_email

def validateUsername(username: str) -> bool:
    if len(username) > 40: return False
    if len(username) < 3: return False
    if not re.match("^[a-zA-Z0-9_.-]+$", username): return False

    return True

def validateEmail(email: str) -> bool:
   if len(email) < 4 : return False
   return validate_email(email)

def encryptPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")

def comparePasswordAndHash(password: str, hashedPassword: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashedPassword)
