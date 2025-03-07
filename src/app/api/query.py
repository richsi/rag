# src/app/api/query.py
from fastapi import APIRouter
from pydantic import BaseModel
from src.util import helpers
import faiss
import json

router = APIRouter()

# Load FAISS index and chunks mapping once at startup
INDEX_PATH = "/home/rhsieh/data/indices/faiss_index.bin"
CHUNKS_MAPPING_PATH = "/home/rhsieh/data/mapping/chunks_mapping.json"

index = faiss.read_index(INDEX_PATH)
with open(CHUNKS_MAPPING_PATH, "r", encoding="utf-8") as f:
  chunks = json.load(f)


class QueryRequest(BaseModel):
  query: str

@router.post("/query")
def query_llm(payload: QueryRequest):
  user_query = payload.query
  model_response = helpers.inference(user_query)
  return {"response": f"{model_response}"}