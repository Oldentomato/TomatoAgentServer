from fastapi import FastAPI
import uvicorn

import pymongo

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

client = pymongo.MongoClient("mongodb://mongodb:27017/")

# from auth.auth import auth

app = FastAPI()
# app.include_router(auth, prefix='/auth')

@app.get("/")
def root():
    return {"message" : "Hello World"}
