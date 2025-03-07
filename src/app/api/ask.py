# src/app/api/ask.py
from fastapi import APIRouter
from pydantic import BaseModel
from src.util.helpers import *

router = APIRouter()

class QueryRequest(BaseModel):
  query: str

@router.post("/ask")
def ask_question(payload: QueryRequest):
  user_query = payload.query
  return {"answer": f"You asked: {user_query}"}