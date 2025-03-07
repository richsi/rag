# src/app/api/query.py
from fastapi import APIRouter
from pydantic import BaseModel
from src.util import helpers

router = APIRouter()

class QueryRequest(BaseModel):
  query: str

@router.post("/query")
def query_llm(payload: QueryRequest):
  user_query = payload.query
  model_response = helpers.inference(user_query)
  return {"response": f"{model_response}"}