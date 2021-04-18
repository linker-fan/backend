import motor.motor_asyncio
import time
import datetime

CONNECTION_STRING = "mongodb://root:password@localhost:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false"

client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)
database = client.linker

users_collection = database.get_collection('users')

async def checkIfUserExists(username: str) -> bool:
    """
    CheckIfUserExists takes username string as an argument
    and queries user from the users collection. If user is not
    found returns False, otherwise True
    """
    user = await users_collection.find_one({"username": username})
    if user is None: return False

    return True

async def checkIfEmailExists(email: str) -> bool:
    """
    CheckIfEmailExists takes email string as an argument
    and queries user from the users collection. If user is not
    found returns False, otherwise True
    """
    user = await users_collection.find_one({"email": email})
    if user is None: return False
    
    return True

async def insertUser(username: str, email: str, hashedPassword: str) -> str:
    ts = time.time()
    time_now = datetime.datetime.fromtimestamp(ts).isoformat()

    user = {
        "username": username,
        "password": hashedPassword,
        "email": email,
        "email_confirmed": False,
        "created": time_now,
        "updated": time_now,
    }

    result = await users_collection.insert_one(user)
    return repr(result.inserted_id)

async def getPasswordByUsername(username: str) -> str:
    password = await users_collection.find_one({"username": username}, {"password": 1, "_id": 0})
    return password["password"]

