# src/app/api/query.py
from fastapi import APIRouter
from pydantic import BaseModel
from src.util import helpers
import faiss
import json
import numpy as np
from openai import OpenAI
from src.config import OPENAI_API_KEY

router = APIRouter()

# Load FAISS index and chunks mapping once at startup
INDEX_PATH = "/home/rhsieh/rag/data/indices/faiss_index.bin"
CHUNKS_MAPPING_PATH = "/home/rhsieh/rag/data/mapping/chunks_mapping.json"

INDEX= faiss.read_index(INDEX_PATH)

with open(CHUNKS_MAPPING_PATH, "r", encoding="utf-8") as f:
  mapping = json.load(f)
  CHUNKS = mapping["chunks"]
  METADATA = mapping.get("metadata", None)


class QueryRequest(BaseModel):
  query: str

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_text(text: str) -> np.ndarray:
  """
  Get the embedding for a given text using OpenAI's embedding model.
  """
  response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
  )
  embedding = np.array(response.data[0].embedding).astype("float32")
  return embedding


def retrieve_context(query: str, k: int = 3) -> str:
  """
  Embed the query, search the FAISS index, and return concatenated text chunks.
  """
  query_embedding = embed_text(query)
  query_embedding = np.expand_dims(query_embedding, axis=0)

  # Search top-k similar vectors
  distances, indices = INDEX.search(query_embedding, k)

  # get corresponding text chunks
  retrieved_chunks = [CHUNKS[i] for i in indices[0] if i < len(CHUNKS)]

  # combining retrieved chunks with separators
  context = "\n\n".join(retrieved_chunks)
  print(retrieved_chunks)
  return context


def generate_response(prompt: str) -> str:
  """
  Call OpenAI's LLM API with prompt
  """
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "You are a helpful assistant. Be clear and concise in your responses."},
      {
        "role": "user",
        "content": prompt
      }
    ],
    max_tokens=150,
    temperature=0.2
  )
  return response.choices[0].message.content


@router.post("/query")
def query_endpoint(payload: QueryRequest):
  user_query = payload.query

  # Retrieve context
  context = retrieve_context(user_query, k=3)

  prompt = (
    f"Use the following context to answer the query:\n\n"
    f"Context:\n{context}\n\n"
    f"Query: {user_query}\n\n"
    "Answer:"
  )

  try:
    response = generate_response(prompt)
  except Exception as e:
    response = f"Error generating response: {e}"

  return {"response": response}