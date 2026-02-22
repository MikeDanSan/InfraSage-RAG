# Embeddings

## What Is an Embedding?

An embedding is a numerical representation of text as a vector (a list of numbers) in high-dimensional space. When you send a sentence to an embedding model, you get back something like a list of 1,536 floating-point numbers (for OpenAI's `text-embedding-3-small`).

The key insight: **texts with similar meaning end up close together in this vector space.** The sentence "How do I deploy to ECS?" and "What is the process for deploying containers on AWS?" would produce vectors that are numerically close to each other, even though they share almost no words.

## Why This Matters for RAG

In a RAG system, you need to find which chunks of your documents are relevant to a user's question. You can't do a keyword search because the user might phrase things differently than the document. Embeddings solve this by converting both the document chunks and the user's question into the same vector space, then finding which chunks are "nearest" to the question.

## How Embedding Models Work (High Level)

Embedding models are neural networks (usually transformers) that have been trained on massive amounts of text. During training, the model learns to place similar concepts near each other in vector space. You don't train this model yourself -- you call an API (like OpenAI's) that runs the model and returns the vector.

Think of it like a hash function, but instead of producing a unique fixed output, it produces a vector where **similar inputs produce similar outputs**.

## Dimensions

The "dimension" of an embedding is the length of the vector. Common dimensions:

| Model | Dimensions | Provider |
|-------|-----------|----------|
| text-embedding-3-small | 1,536 | OpenAI |
| text-embedding-3-large | 3,072 | OpenAI |
| text-embedding-ada-002 | 1,536 | OpenAI |

Higher dimensions can capture more nuance but cost more to store and search. For this project, 1,536 dimensions is the sweet spot.

**DevOps analogy**: Think of dimensions like fields in a log entry. More fields give you finer-grained querying, but they increase storage and index size. You pick the right granularity for your use case.

## Cosine Similarity

Once you have two vectors, you need a way to measure how "similar" they are. The standard approach is **cosine similarity**, which measures the angle between two vectors.

- **Cosine similarity = 1.0**: Vectors point in the same direction (identical meaning)
- **Cosine similarity = 0.0**: Vectors are perpendicular (unrelated)
- **Cosine similarity = -1.0**: Vectors point in opposite directions (opposite meaning, rare in practice)

The math: given vectors A and B, cosine similarity = (A dot B) / (|A| * |B|)

You don't need to implement this yourself -- FAISS handles it -- but understanding it helps you reason about retrieval quality.

## Cost Awareness

Embedding API calls are cheap but not free:

| Model | Price per 1M tokens |
|-------|---------------------|
| text-embedding-3-small | ~$0.02 |
| text-embedding-3-large | ~$0.13 |

A typical PDF page is roughly 500-800 tokens. So embedding a 100-page document costs a fraction of a cent. The real cost in RAG systems comes from the LLM completion call, not embeddings.

## What You'll Build

In `embeddings.py`, you will:

1. Take a list of text chunks (strings)
2. Call the OpenAI embedding API for each chunk (or in batches)
3. Get back a list of vectors (each a list of floats)
4. Return these vectors so they can be stored in FAISS

Key decisions you'll make:
- Which embedding model to use
- Whether to embed chunks one at a time or in batches (batching is better)
- How to handle API errors and retries

## Key Takeaways

- Embeddings convert text into numbers that capture meaning
- Similar text produces similar vectors
- Cosine similarity is the standard way to measure vector closeness
- Embedding is cheap; the expensive part is the LLM completion
- You call an API to get embeddings -- you don't train anything
