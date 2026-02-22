"""
Vector storage and similarity search.

Responsibilities:
- Create and manage a FAISS index
- Add embedding vectors to the index
- Search the index for top-k similar vectors given a query vector
- Map FAISS result indices back to original text chunks
- Save and load the index and chunk mapping to/from disk
"""
