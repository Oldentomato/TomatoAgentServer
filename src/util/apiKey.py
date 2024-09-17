from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

def getApiKey(apiName):
    try:
        key = os.getenv(apiName)
    except: 
        Exception("No Api Key")
        
    return key