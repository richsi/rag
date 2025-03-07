# src/app/main.py
from fastapi import FastAPI
from src.app.api.ask import router

app = FastAPI()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
  import uvicorn
  uvicorn("app.main:app", host="", port=8001, reload=True)