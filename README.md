# rag

#### Frontend
```chainlit run src/chainlit_app.py -w --port 8000```

#### Backend
```uvicorn src.app.main:app --reload --port 8001```
``` ```

#### TODO:
* fix hardcoded path in src/rag/ingest.py
    * switch to datastore (PostgreSQL, pgvector, ts_rank)
* implement intelligent chunking - spaCy
* compare and contrast embedding models: OpenAI vs tiktoken
* refactor search reranking
* implement retries for calling LLM (tenacity)
    * perhaps host locally if possible
* implement more intelligent prompting pipeline
    * engineer prompts

* research ways to preprocess data efficiently
* research chunking methods
* research search reranking
* research data storage

* Implement MS bot (reach)
    * https://docs.chainlit.io/deploy/teams



#### Tech Stack:
* Frontend: Chainlit
* Backend: FastAPI
* PDF Parsing: PyMuPDF 
* Chunking: custom
* Embedding: OpenAI
* Datastore: local
* Reranking: FAISS
* LLM: OpenAI