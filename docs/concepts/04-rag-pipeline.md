# The RAG Pipeline

## What Is RAG?

Retrieval-Augmented Generation (RAG) is a pattern that makes LLMs answer questions using your own documents instead of relying solely on their training data. The idea is simple:

1. **Retrieve** relevant context from your documents
2. **Augment** the LLM's prompt with that context
3. **Generate** an answer grounded in the retrieved information

Without RAG, an LLM can only answer from what it learned during training (which has a knowledge cutoff and doesn't know about your private docs). With RAG, you feed it the relevant parts of your documents at query time.

**DevOps analogy**: Think of RAG like a runbook-assisted incident response. Instead of relying solely on an engineer's memory (the LLM's training), you pull up the relevant runbook pages (retrieval) and hand them to the engineer alongside the alert details (the prompt). The engineer uses both to respond.

## The Two Phases

### Phase A: Ingestion (offline, happens once per document)

```
PDF --> Extract Text --> Clean --> Chunk --> Embed Each Chunk --> Store in FAISS
```

This runs when you upload a new document. The output is a FAISS index and a chunk mapping file saved to disk. Once ingested, the document doesn't need to be processed again.

### Phase B: Query (online, happens per user question)

```
User Question --> Embed Question --> Search FAISS (top-k) --> Get Relevant Chunks
    --> Build Prompt (question + chunks) --> Send to LLM --> Return Answer
```

This runs every time a user asks a question. The critical path here determines your response latency.

## The Prompt Construction Step

This is the part most tutorials gloss over, but it's where you have the most control over answer quality. You are manually constructing the text that the LLM sees.

A typical RAG prompt looks like:

```
You are a helpful assistant. Answer the question based only on the provided context.
If the context doesn't contain enough information, say so.

Context:
---
{chunk_1_text}
---
{chunk_2_text}
---
{chunk_3_text}

Question: {user_question}

Answer:
```

Key decisions in prompt construction:

- **System instruction**: Tell the LLM to only use the provided context (reduces hallucination)
- **Context formatting**: How you separate and present the chunks
- **Chunk ordering**: Most relevant first? Or some other order?
- **Token budget**: You need to fit the system prompt + all chunks + the question + room for the answer within the model's context window

## Token Limits and Budget

Every LLM has a maximum context window:

| Model | Context Window |
|-------|---------------|
| gpt-4o-mini | 128k tokens |
| gpt-4o | 128k tokens |
| gpt-3.5-turbo | 16k tokens |

Your prompt must fit within this window. The budget looks like:

```
Total tokens available = context window
Used by: system prompt (~100-200 tokens)
       + retrieved chunks (varies, this is the bulk)
       + user question (~20-100 tokens)
       + completion/answer (~200-500 tokens)
```

If your 5 retrieved chunks are each 250 tokens, that's 1,250 tokens for context. Add system prompt and question overhead, and you're well within budget for any modern model.

**Use tiktoken** to count tokens before sending the request. This lets you:
- Warn if the prompt would exceed the limit
- Estimate cost before the API call
- Log actual usage for observability

## The LLM Completion Call

After constructing the prompt, you send it to the LLM API and get back a response. This is the most expensive and slowest step in the pipeline.

What the API returns:
- The generated answer text
- Token usage (prompt tokens + completion tokens)
- Model metadata

What you'll track:
- Prompt token count
- Completion token count
- Latency of the API call
- Estimated cost

## Where Things Go Wrong

Understanding failure modes is critical for production systems:

| Problem | Root Cause | What to Investigate |
|---------|-----------|-------------------|
| Irrelevant answers | Bad retrieval | Chunk size, embedding quality, top-k too low |
| Hallucinated facts | LLM ignoring context | Prompt instruction not strong enough |
| Partial answers | Missing context | Chunks don't cover the topic, overlap too low |
| Slow responses | LLM latency | Model choice, prompt length, streaming |
| Expensive | Token waste | Too many chunks retrieved, large model for simple questions |

## Latency Breakdown

A typical RAG request looks like:

| Step | Typical Latency |
|------|----------------|
| Embed the question | 100-300ms |
| FAISS search | <10ms (local, small index) |
| Prompt construction | <1ms |
| LLM completion | 1-5 seconds (depends on model and output length) |

The LLM call dominates latency. Everything else is fast. This is important for knowing where to optimize.

## What You'll Build

In `llm.py`, you will:

1. Construct a prompt from the user's question and retrieved chunks
2. Call the OpenAI chat completion API
3. Return the answer along with token usage metadata

In `main.py` (FastAPI), you will:

1. Create an ingestion endpoint (POST /ingest) that accepts a PDF and runs the ingestion pipeline
2. Create a query endpoint (POST /query) that accepts a question and runs the query pipeline
3. Wire together all the modules: ingestion.py -> embeddings.py -> retrieval.py -> llm.py

## The Full Data Flow

Putting it all together:

**Ingestion**:
1. User uploads PDF to POST /ingest
2. `ingestion.py` extracts and chunks the text
3. `embeddings.py` generates vectors for each chunk
4. `retrieval.py` stores vectors in FAISS and saves to disk
5. Return success with metadata (chunk count, etc.)

**Query**:
1. User sends question to POST /query
2. `embeddings.py` embeds the question
3. `retrieval.py` searches FAISS for top-k similar chunks
4. `llm.py` constructs prompt and calls LLM
5. Return answer with metadata (token usage, latency, cost estimate)

## Key Takeaways

- RAG has two phases: offline ingestion and online query
- Prompt construction is where you control answer quality
- Token counting is essential for cost and limit management
- The LLM call is the bottleneck in latency and cost
- Bad answers are usually a retrieval problem, not an LLM problem
- Understanding the full pipeline end-to-end is exactly what this project teaches you
