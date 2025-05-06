# rag

#### Frontend
```chainlit run src/chainlit_app.py -w --port 8000```

#### Backend
```uvicorn src.app.main:app --reload --port 8001```

#### Usage
1. `pip install -r requirements.txt`
2. Put your pdf documents into `docs/`
3. Set API key secrets in `.env`
4. Generate binary file using: `python3 -m src.rag.ingest`. Stored in `indices/`
5. Start frontend and backend
6.

#### TODO:
* fix hardcoded path in src/rag/ingest.py
    * switch to datastore (PostgreSQL, pgvector, ts_rank)
* ~~implement intelligent chunking - spaCy~~
* refactor search reranking
* implement retries for calling LLM (tenacity)
    * perhaps host locally if possible
* implement more intelligent prompting pipeline
    * engineer prompts

* research ways to preprocess data efficiently
* research chunking methods
* research search reranking
* research permanent data storage with incremental file adding

* add memory
* add agent functionality
* add reasoning.. (deepseek)

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