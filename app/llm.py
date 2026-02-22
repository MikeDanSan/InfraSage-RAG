"""
LLM interaction and prompt construction.

Responsibilities:
- Construct a RAG prompt from user question + retrieved chunks
- Count tokens using tiktoken for budget management
- Call the OpenAI chat completion API
- Return the answer text along with token usage metadata
- Estimate cost based on token usage and model pricing
"""
