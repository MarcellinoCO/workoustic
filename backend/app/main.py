import requests

from fastapi import FastAPI, Cookie, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .utils import spotify

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello world"}
