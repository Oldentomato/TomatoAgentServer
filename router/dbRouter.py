from fastapi import APIRouter, HTTPException, Form
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.util import getApiKey, ControlMongo, password_encrypt, password_decrypt
import random
from datetime import datetime
import string
import uuid

dbRoute = APIRouter()

def __generateToken():
    n = 20
    randStr = ""
    for _ in range(n):
        randStr += str(random.choice(string.ascii_uppercase + string.digits))

    return randStr

# @dbRoute.on_event("startup")
# def startupEvent():
#     global mongo 
#     mongo = ControlMongo(username=getApiKey("MONGODB_USERNAME"),password=getApiKey("MONGODB_PASSWORD"),dbName="tomato_server", collName="Users")


# @dbRoute.post("/register")
# def registerUser(userName:str = Form(...), password:str = Form(...)):
#     global mongo 

def register(mongo, userName:str, password:str):
    if len(mongo.selectDB({"userName":userName})) != 0:
        return {"success": False, "msg": "already userName"}
    else:
        randomChoice = random.choice(['a', 'b', 'c', 'd'])
        user_uid = str(uuid.uuid4())
        encryptPassword = password_encrypt(password.encode(), randomChoice)
        # mongo.insertDB({"userName": userName, "password": encryptPassword, "key":randomChoice, "user_uid": user_uid, "token":"", "expireAt":"","chatHistory":[]})
        user_data = {
            "_id" : user_uid,
            "userName": userName,
            "password": encryptPassword,
            "key": randomChoice,
            # "token": "",
            # "expireAt": "",
            "chatHistory": []
        }
        mongo.insertDB(user_data)
        return {"success": True,"user_data": user_data}
    
    
def login(mongo, userName:str, password:str):
    if len(result := mongo.selectDB({"userName":userName})) == 0:
        return {"success": False, "msg": "No ID"}
    else:
        userInfo = result[0]
        print(userInfo)
        userInfo["_id"] = str(userInfo["_id"])
        key = userInfo["key"]
        encryptPassword = userInfo["password"]
        decryptPassword = password_decrypt(encryptPassword, key).decode()
        if password == decryptPassword:
            token = __generateToken()
            expireAt = int(datetime.now().timestamp()) + 3600
            return  {
                        "success": True, 
                        "userName": userInfo["userName"], 
                        "_id":  userInfo["_id"], 
                        "token": token, 
                        "expireAt": expireAt
                    }
        else: 
            return {"success": False, "msg":"Wrong password"}

def logout(mongo, userName:str):
    token = mongo.selectDB({"userName":userName})[0]["token"]
    if token != "":
        mongo.updateDB({"userName":userName}, {"token":""})
        return {"success": True}
    else:
        return {"success": False, "msg":"token Error"}

def __auth(mongo, userName, token):
    if len(mongo.selectDB({"userName": userName, "token":token})) != 0:
        return True
    else:
        return False

def __autoLogout(mongo):
    pass


if __name__ == "__main__":
    mongo = ControlMongo(username=getApiKey("MONGODB_USERNAME"),password=getApiKey("MONGODB_PASSWORD"),dbName="tomato_server", collName="Users")
    # registerResult = register(mongo, "test","qwer1234")
    # print(f"register success: {registerResult}")
    # loginResult = login(mongo, "test","qwer1234")
    # print(f"login: {loginResult}")
    logoutResult = logout(mongo, "test")
    print(f"logout: {logoutResult}")