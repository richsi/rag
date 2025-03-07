# src/rag/ingest.py

import os
import numpy as np
import faiss
import pymupdf
import json
from openai import OpenAI
from src.config import OPENAI_API_KEY

def read_pdf_document(file_path: str) -> list:
  """
  Reads a PDF file using PyMuPDF and returns a list of texts, one per page.
  """
  doc = pymupdf.open(file_path)
  page_texts = []
  for page in doc:
    text = page.get_text("text")
    page_texts.append(text)
  return page_texts


def chunk_text(text: str, max_length: int = 500) -> list:
  """
  Splits text into chunks of a maximum number of characterse.
  TODO: Improve splitting on sentence boundaries
  """
  return [text[i:i+max_length] for i in range(0, len(text), max_length)]


def embed_text(text: str) -> list:
  """
  Uses OpenAI's embedding API to generate an embedding for a given text chunk.
  """
  client = OpenAI(api_key=OPENAI_API_KEY)
  response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
  )
  return response.data[0].embedding


def build_index_from_docs(directory: str) -> tuple[faiss.IndexFlatL2, list, list]:
  """
    Processes all PDF files in the given directory, extracts text from every page,
    further chunks the text if needed, and builds a FAISS index from the embeddings.
    
    Returns:
      - index: a FAISS index with all embeddings
      - all_chunks: list of text chunks corresponding to the embeddings
      - all_metadata: list of metadata dictionaries (document name, page, chunk index)
  """
  # create directory if it does nto exist
  os.makedirs(directory, exist_ok=True)

  all_embeddings = []
  all_chunks = []
  all_metadata = []     # extra infor (e.g., filename, chunk index)

  for file_name in os.listdir(directory): # iterate over all docs in dir
    if file_name.lower().endswith(".pdf"): # only process pdf files
      file_path = os.path.join(directory, file_name)
      pages = read_pdf_document(file_path) # get a list of text for each page 
      for page_idx, page_text in enumerate(pages): # chunk the pages by idx
        chunks = chunk_text(page_text, max_length=500) 
        for chunk_idx, chunk in enumerate(chunks): # embed the chunks by idx
          embedding = embed_text(chunk)
          all_embeddings.append(embedding)
          all_chunks.append(chunk)
          all_metadata.append({
            "documents": file_name,
            "page": page_idx,
            "chunk_idx": chunk_idx
          })

  # convert embeddings list to np array with type float32
  all_embeddings = np.array(all_embeddings).astype("float32")
  dimension = all_embeddings.shape[1]
  # create FAISS index using L2 distance
  index = faiss.IndexFlatL2(dimension)
  index.add(all_embeddings)
  return index, all_chunks, all_metadata


if __name__ == "__main__":
  local_path = "/home/rhsieh/rag/data" # TODO: fix hardcode
  documents_dir = f"{local_path}/docs"

  # process PDFs and build index
  index, chunks, metadata = build_index_from_docs(documents_dir)

  # save FAISS index to disk
  index_path = f"{local_path}/indices"
  os.makedirs(index_path, exist_ok=True)
  faiss.write_index(index, f"{index_path}/faiss_index.bin")

  # save the mapping of chunks and meta data to a JSON file
  chunk_metadata_mapping_path = f"{local_path}/mapping"
  os.makedirs(chunk_metadata_mapping_path, exist_ok=True)
  mapping = {"chunks": chunks, "metadata": metadata}
  with open(f"{chunk_metadata_mapping_path}/chunks_mapping.json", "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)
  
  print("Ingestion complete.")