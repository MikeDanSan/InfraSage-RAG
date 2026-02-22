"""
Embedding generation.

Responsibilities:
- Accept a list of text chunks (or a single query string)
- Call the OpenAI embedding API
- Return a list of embedding vectors (list of list of floats)
- Handle batching for efficiency
- Handle API errors gracefully
"""
