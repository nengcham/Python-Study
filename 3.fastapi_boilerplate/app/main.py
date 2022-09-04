from typing import Optional
from fastapi import FastAPI
import datetime
from app.services import agent

app = FastAPI()

@app.get("/")
def now():
    return {"Now": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
