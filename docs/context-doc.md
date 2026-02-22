# Project: InfraSage-RAG

## Purpose

I am a DevOps Engineer with 5+ years of software engineering experience (AWS background). I am transitioning into supporting AI systems and LLM-powered products from an infrastructure and DevOps perspective.

This project is NOT a toy chatbot.

It is a deliberate learning project to deeply understand:

- Embeddings
- Vector databases
- Retrieval-Augmented Generation (RAG)
- Token usage
- LLM API interaction
- AI system architecture
- Observability considerations
- Cost awareness

The goal is to build a minimal but production-minded RAG system from scratch without hiding complexity behind heavy frameworks like LangChain (at least initially).

---

# High-Level Architecture

User → FastAPI Backend → 
    ├── PDF Parser
    ├── Chunking Logic
    ├── Embedding Model API
    ├── FAISS Vector Index
    └── LLM Completion API

---

# Technical Requirements

Language: Python 3.11+

Frameworks/Libraries:
- FastAPI
- FAISS (local vector DB)
- OpenAI or compatible LLM API
- PyPDF or pdfplumber for PDF parsing
- tiktoken (for token counting)
- Pydantic

No LangChain for initial version.
No LlamaIndex.
Build core logic manually.

---

# Functional Requirements

## 1. Document Ingestion

- Accept a PDF file
- Extract text
- Clean text
- Chunk text (configurable chunk size and overlap)
- Generate embeddings per chunk
- Store embeddings in FAISS
- Persist index locally

## 2. Query Endpoint

- Accept user question
- Embed the question
- Perform similarity search (top-k)
- Retrieve relevant chunks
- Construct prompt manually
- Send to LLM API
- Return structured response

## 3. Observability

- Log:
  - Token usage
  - Retrieval scores
  - Latency per stage
- Print cost estimation per request

## 4. Configuration

- .env for API keys
- Configurable:
  - Chunk size
  - Overlap
  - Top-k retrieval
  - Model name

---

# Non-Functional Requirements

- Clean folder structure
- Clear separation of concerns
- Typed functions
- Reproducible local setup
- Requirements.txt or pyproject.toml
- Dockerfile for containerization

---

# Folder Structure (Target)

infra-sage-rag/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── ingestion.py
│   ├── embeddings.py
│   ├── retrieval.py
│   ├── llm.py
│   └── utils.py
│
├── data/
├── index/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md

---

# Learning Objectives

While building, I want to understand deeply:

1. What exactly an embedding vector represents
2. Why chunk size affects retrieval accuracy
3. How cosine similarity works in practice
4. How token limits impact prompt design
5. Latency breakdown of AI systems
6. Where production risks would occur
7. How this would scale in AWS

The AI pair programming assistant should:
- Explain tradeoffs
- Not abstract away core logic
- Encourage understanding before optimization
- Suggest improvements after MVP is complete

---

# Phase Plan

## Phase 1 – Core RAG (MVP)
- PDF → chunks → embeddings → FAISS
- Query → retrieve → prompt → LLM response

## Phase 2 – Observability & Cost Awareness
- Token tracking
- Latency timing
- Cost estimation

## Phase 3 – Production Readiness
- Dockerize
- Add logging strategy
- Add structured config
- Discuss AWS deployment design

---

# Success Criteria

- I can explain RAG architecture without notes
- I understand embedding flow
- I can diagram the system from memory
- I can explain scaling considerations in AWS
- I can describe cost drivers

---

# Important Constraint

This project is about learning AI system internals from a DevOps perspective.

Do not over-engineer.
Do not hide logic behind frameworks.
Prioritize clarity over abstraction.

---

# Future Extensions (Not Now)

- Replace FAISS with managed vector DB
- Add evaluation metrics
- Add caching layer
- Add streaming responses
- Add auth layer

---

# Assistant Role

You are acting as a senior AI engineer guiding a DevOps engineer into AI systems.

Teach. Don't just generate code.
Explain decisions.
Encourage best practices.

