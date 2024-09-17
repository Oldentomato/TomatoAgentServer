import redis
import pickle 
redisClient = redis.Redis(host='redis_containerDev', port=6379)

from fastapi import APIRouter, HTTPException, Form
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from router.dbRouter import register, login, logout
from src.util import getApiKey, ControlMongo, password_encrypt, password_decrypt

chat = APIRouter()

@chat.post("/chat")
def chat(q:str = Form(...)):
    global mongo 
    message = register(mongo, userName, password)
    return message