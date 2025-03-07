# rag

#### Frontend
```chainlit run src/chainlit_app.py -w --port 8000```


#### Backend
```uvicorn src.app.main:app --reload --port 8001```
``` ```

#### TODO:
* fix hardcoded path in src/rag/ingest.py

* Inference pipeline
    * Retrieval
        * Top-k -> other algorithms
        * Prompting
    * Summarization
* Data Ingestion
    * Chunking, embedding
    * Store in database (s3, mongodb)
* Implement MS bot (reach)
    * https://docs.chainlit.io/deploy/teams


#### Functionality:
* frontend ui
* backend api routing
* llm query