import redis
import pickle 
redisClient = redis.Redis(host='redis_containerDev', port=6379)

from fastapi import APIRouter, HTTPException, Form
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from router.dbRouter import register, login, logout
from src.util import getApiKey, ControlMongo, password_encrypt, password_decrypt

auth = APIRouter()

@auth.on_event("startup")
def startupEvent():
    global mongo 
    mongo = ControlMongo(username=getApiKey("MONGODB_USERNAME"),password=getApiKey("MONGODB_PASSWORD"),dbName="tomato_server", collName="Users")
    print(mongo)

@auth.post("/register")
def registerUser(userName:str = Form(...), password:str = Form(...)):
    global mongo 
    message = register(mongo, userName, password)
    print(message)
    return message

@auth.post("/login")
def loginUser(userName:str = Form(...), password:str = Form(...)):
    try:
        userInfo = login(mongo, userName, password)
        user_id = f"_id:{userInfo["_id"]}"
        redisClient.hset(user_id, mapping={
                "user_uid": userInfo["userName"],
                "token": userInfo["token"],
                "expireAt": userInfo["expireAt"]
            })

    except redis.RedisError as e:
        print(f"Redis error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    # userRedisKey = f"{userInfo}"
    
    # print(userRedisKey)
    # try:
    #     redisClient.set(userRedisKey, pickle.dumps(userInfo))
    #     return {"success": True}
    # except error as e:
    #     return {"success": False, "error":e}
        
    

    # objectData = redisClient.get(userRedisKey)
    # if objectData:
    #     print("get from redis")
    #     return pickle.loads(objectData)
    # return userInfo