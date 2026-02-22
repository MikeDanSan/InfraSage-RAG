# Vector Search and FAISS

## The Problem

You have thousands of embedding vectors (one per document chunk). A user asks a question, and you embed that question into a vector too. Now you need to find which of your stored vectors are most similar to the question vector.

This is a **nearest neighbor search** problem. For small datasets (under 100k vectors), you can do an exact brute-force comparison. For larger datasets, you need approximate methods. FAISS handles both.

## What Is FAISS?

FAISS (Facebook AI Similarity Search) is a library built by Meta for efficient similarity search over dense vectors. It's written in C++ with Python bindings, so it's fast.

Key characteristics:
- **Runs locally** -- no server, no network calls, just a library
- **In-memory** -- the index lives in RAM (can be saved to/loaded from disk)
- **Supports multiple index types** -- from exact search to approximate
- **Battle-tested** -- used in production at Meta scale

**DevOps analogy**: Think of FAISS like SQLite for vectors. It's an embedded engine, not a client-server database. You import it, create an index, and query it in-process. No ports, no connections, no cluster management.

## Index Types

FAISS offers many index types. The ones that matter for this project:

### IndexFlatL2 (what you'll use)
- Exact brute-force search using L2 (Euclidean) distance
- Compares the query vector against every stored vector
- 100% accurate, no approximation
- Fine for datasets under ~100k vectors
- **This is your starting point**

### IndexFlatIP
- Same as above but uses Inner Product (related to cosine similarity)
- If you normalize your vectors first, inner product equals cosine similarity
- Useful when you specifically want cosine similarity ranking

### IndexIVFFlat
- Approximate search using inverted file index
- Clusters vectors, then only searches nearby clusters
- Faster for large datasets, slightly less accurate
- **Not needed for Phase 1**

For your project with a few PDFs, `IndexFlatL2` or `IndexFlatIP` is the right choice. You'd only switch to approximate indexes if you had millions of vectors.

## How Search Works (Step by Step)

1. You have an index containing N vectors, each of dimension D (e.g., 1536)
2. User asks a question
3. You embed the question into a vector of the same dimension D
4. You call `index.search(query_vector, k)` where k is how many results you want
5. FAISS returns two arrays:
   - **distances**: how far each result is from the query (lower = more similar for L2)
   - **indices**: the position (index) of each result in the original dataset

The indices let you map back to the original text chunks. You store your chunks in a list, and the FAISS index position corresponds to the list position.

## Top-k Retrieval

"Top-k" means you retrieve the k most similar chunks. Common values:

| k | Use Case |
|---|----------|
| 3 | Conservative, less noise, may miss relevant context |
| 5 | Good default for most RAG systems |
| 10 | More context, but may include less relevant chunks |

**Start with k=5.** The tradeoff: higher k gives the LLM more context but also more noise and higher token usage (cost).

## Persistence

FAISS indexes can be saved to disk and loaded back:

```
faiss.write_index(index, "path/to/index.faiss")
index = faiss.read_index("path/to/index.faiss")
```

This means you don't re-embed your documents every time you restart. Embed once, save the index, load it on startup.

You'll also need to persist the mapping from index positions to text chunks (FAISS only stores vectors, not the original text). A simple approach: save the chunk list as a JSON file alongside the FAISS index.

## Distance vs. Similarity

A common source of confusion:

- **L2 distance**: lower = more similar (0 means identical)
- **Cosine similarity**: higher = more similar (1.0 means identical)
- **Inner product**: higher = more similar (when vectors are normalized)

FAISS returns distances. If you want to show similarity scores to users, you may need to convert. For L2, a simple inversion or normalization works. For inner product on normalized vectors, the returned value already acts like cosine similarity.

## What You'll Build

In `retrieval.py`, you will:

1. Create a FAISS index of the appropriate type
2. Add embedding vectors to the index
3. Implement a search function that takes a query vector and returns top-k results
4. Map FAISS result indices back to the original text chunks
5. Save and load the index from disk
6. Save and load the chunk mapping alongside the index

Key decisions you'll make:
- Which index type (start with IndexFlatL2 or IndexFlatIP)
- How to store the chunk-to-index mapping
- What metadata to return with search results (distances, chunk text, chunk positions)

## Scaling Considerations (for your AWS background)

At small scale (this project), FAISS on a single machine is fine. At production scale:

- **Managed vector databases** (Pinecone, Weaviate, AWS OpenSearch with vector support) replace FAISS
- They handle sharding, replication, and concurrent access
- AWS OpenSearch Serverless now supports vector search natively
- pgvector (PostgreSQL extension) is another option if you already run RDS

You'd swap FAISS for a managed service the same way you'd swap SQLite for RDS -- same concept, different operational model.

## Key Takeaways

- FAISS is an embedded vector search library, not a server
- IndexFlatL2 gives exact search and is perfect for small datasets
- Top-k retrieval returns the k most similar chunks to a query
- You must persist both the FAISS index and the text-to-index mapping
- At scale, you'd replace FAISS with a managed vector database
