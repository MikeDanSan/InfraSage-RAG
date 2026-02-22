# Phase 1 Implementation Guide

This is your roadmap for building the core RAG MVP. Work through each module in order. For each one, read the relevant concept doc first, then implement.

## Step 1: Set Up Your Environment

Before writing any code:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Verify FAISS installed correctly:
```bash
python3 -c "import faiss; print(faiss.__version__)"
```

## Step 2: config.py

**Read first**: No concept doc needed -- this is standard Python configuration.

**What to build**:
- Load environment variables from `.env`
- Create a Pydantic `Settings` class (using `pydantic-settings`) with fields for:
  - `openai_api_key: str`
  - `embedding_model: str` (default: "text-embedding-3-small")
  - `llm_model: str` (default: "gpt-4o-mini")
  - `chunk_size: int` (default: 1000)
  - `chunk_overlap: int` (default: 200)
  - `top_k: int` (default: 5)
  - `index_dir: str` (default: "index")
  - `data_dir: str` (default: "data")
- Export a single `settings` instance that other modules import

**Why Pydantic Settings**: It validates types automatically, reads from `.env` files, and gives you a single source of truth for configuration. This pattern is standard in FastAPI projects.

**Hint**: Look at `pydantic_settings.BaseSettings` and its `model_config` for env file loading.

## Step 3: ingestion.py

**Read first**: `docs/concepts/02-chunking.md`

**What to build** (three functions):

### Function 1: `extract_text_from_pdf(pdf_path: str) -> str`
- Open the PDF using pdfplumber
- Extract text from each page
- Join all page text into a single string
- Return the full text

### Function 2: `clean_text(text: str) -> str`
- Replace multiple consecutive newlines with a single newline
- Replace multiple consecutive spaces with a single space
- Strip leading/trailing whitespace
- Return cleaned text

### Function 3: `chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]`
- Split the text into chunks of `chunk_size` characters
- Each chunk overlaps with the previous by `chunk_overlap` characters
- Return a list of chunk strings

**Think about**: What happens if `chunk_overlap >= chunk_size`? What if the text is shorter than `chunk_size`?

## Step 4: embeddings.py

**Read first**: `docs/concepts/01-embeddings.md`

**What to build**:

### Function: `generate_embeddings(texts: list[str], model: str) -> list[list[float]]`
- Initialize the OpenAI client
- Call the embeddings API with the list of texts
- Extract the embedding vectors from the response
- Return them as a list of lists of floats

**Think about**: The OpenAI API accepts batches of texts. Sending all chunks in one call is more efficient than calling one at a time. But what if you have thousands of chunks? You might want to batch in groups of ~100.

## Step 5: retrieval.py

**Read first**: `docs/concepts/03-vector-search.md`

**What to build**:

### Function 1: `create_index(dimension: int) -> faiss.Index`
- Create a FAISS IndexFlatL2 (or IndexFlatIP) with the given dimension
- Return the index

### Function 2: `add_to_index(index: faiss.Index, embeddings: list[list[float]])`
- Convert embeddings to a numpy array (float32)
- Add them to the index

### Function 3: `search_index(index: faiss.Index, query_embedding: list[float], top_k: int) -> tuple`
- Convert query to numpy array (float32), reshape to (1, dimension)
- Search the index
- Return distances and indices

### Function 4: `save_index(index, chunks, index_dir)` and `load_index(index_dir)`
- Save/load the FAISS index file and a JSON file mapping indices to chunk text

## Step 6: llm.py

**Read first**: `docs/concepts/04-rag-pipeline.md` and `docs/concepts/05-prompt-engineering.md`

**What to build**:

### Function 1: `build_prompt(question: str, context_chunks: list[str]) -> list[dict]`
- Construct the messages list for the OpenAI chat API
- System message with grounding instructions
- User message with context chunks and the question
- Return the messages list

### Function 2: `query_llm(messages: list[dict], model: str) -> dict`
- Call the OpenAI chat completion API
- Extract the answer text
- Extract token usage from the response
- Return a dict with: answer, prompt_tokens, completion_tokens, total_tokens

## Step 7: main.py

**Read first**: `docs/concepts/04-rag-pipeline.md` (the "Full Data Flow" section)

**What to build**:

### POST /ingest
- Accept a PDF file upload
- Run: extract_text -> clean_text -> chunk_text -> generate_embeddings -> create_index -> add_to_index -> save_index
- Return: chunk count, success status

### POST /query
- Accept a JSON body with a question string
- Run: load_index -> generate_embeddings(question) -> search_index -> build_prompt -> query_llm
- Return: answer, token usage, chunk count used

## Testing Your MVP

Once everything is wired up:

1. Place a PDF in the `data/` folder
2. Start the server: `uvicorn app.main:app --reload`
3. Ingest the PDF: `curl -X POST -F "file=@data/your.pdf" http://localhost:8000/ingest`
4. Ask a question: `curl -X POST -H "Content-Type: application/json" -d '{"question": "your question here"}' http://localhost:8000/query`

## Order of Implementation

The recommended order to write code:

1. **config.py** -- everything else depends on this
2. **ingestion.py** -- you can test this standalone with a PDF
3. **embeddings.py** -- you can test this with dummy text
4. **retrieval.py** -- you can test this with dummy vectors
5. **llm.py** -- you can test this with dummy chunks
6. **main.py** -- wire everything together last

Each module can be tested independently before integration. This is intentional.
