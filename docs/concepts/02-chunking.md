# Chunking

## Why Chunk at All?

LLMs have a limited context window (the maximum number of tokens they can process at once). You can't feed an entire 200-page PDF into a prompt. Instead, you split the document into smaller pieces (chunks), embed each one, and at query time only retrieve the most relevant chunks to include in the prompt.

Chunking is the step between "I have raw text from a PDF" and "I have pieces ready to embed."

## What Makes a Good Chunk?

A good chunk is:

- **Self-contained enough** to be useful on its own (a reader could understand it without the surrounding text)
- **Small enough** to fit several chunks into a prompt alongside the user's question
- **Large enough** to contain meaningful information (not just a sentence fragment)

This is a tradeoff. There is no universally correct chunk size.

## Chunk Size

Chunk size is measured in characters or tokens. Common ranges:

| Chunk Size (chars) | Rough Token Count | Tradeoff |
|--------------------|-------------------|----------|
| 200-500 | ~50-125 tokens | Very granular, good precision, may lose context |
| 500-1000 | ~125-250 tokens | Balanced, most common starting point |
| 1000-2000 | ~250-500 tokens | More context per chunk, may dilute relevance |

**Start with 1,000 characters.** You can tune this later once you see how retrieval performs.

**DevOps analogy**: This is like choosing log aggregation window sizes. Too small and you get noise. Too large and you lose the ability to pinpoint issues. You tune based on what queries you're running.

## Overlap

Overlap means that consecutive chunks share some text at their boundaries. If your chunk size is 1,000 characters with 200 characters of overlap, then:

- Chunk 1: characters 0-999
- Chunk 2: characters 800-1799
- Chunk 3: characters 1600-2599

Why overlap? Without it, important information that spans a chunk boundary gets split across two chunks, and neither chunk alone contains the full context. Overlap reduces this problem.

**Typical overlap**: 10-20% of chunk size. For a 1,000-character chunk, use 100-200 characters of overlap.

**Tradeoff**: More overlap means more chunks, which means more embeddings to compute and store. But it improves retrieval quality at boundaries.

## Chunking Strategies

### 1. Fixed-size chunking (what you'll build first)
Split text into chunks of N characters with M characters of overlap. Simple, predictable, works well as a starting point.

### 2. Sentence-based chunking
Split on sentence boundaries so chunks don't break mid-sentence. Better quality but requires sentence detection.

### 3. Paragraph/section-based chunking
Split on paragraph breaks or headers. Preserves document structure but produces variable-size chunks.

### 4. Recursive chunking
Try to split on paragraphs first, then sentences, then characters -- progressively smaller separators. This is what LangChain uses internally. You can build a simple version of this yourself.

**For Phase 1, use fixed-size chunking.** It's the simplest to implement and understand. You can revisit smarter strategies later.

## How Chunk Size Affects Retrieval

This is one of the most important things to internalize:

- **Too small**: Chunks lack context. The retriever finds a relevant fragment but the LLM can't construct a good answer from it.
- **Too large**: Chunks contain too much irrelevant text mixed with relevant text. The embedding becomes a blurry average of many topics, reducing retrieval precision.
- **No overlap**: Information at chunk boundaries is effectively lost.

When your RAG system gives bad answers, chunk size is one of the first things to investigate.

## What You'll Build

In `ingestion.py`, you will:

1. Accept a PDF file path
2. Extract raw text from the PDF (using pdfplumber or PyPDF)
3. Clean the text (remove excessive whitespace, fix encoding issues)
4. Split the text into chunks using configurable chunk_size and chunk_overlap
5. Return a list of text chunks ready for embedding

Key decisions you'll make:
- Which PDF library to use (pdfplumber is generally more reliable for layout)
- How to handle page boundaries (should a chunk span pages?)
- What "cleaning" means for your documents
- Initial chunk_size and overlap values

## Key Takeaways

- Chunking bridges raw document text and the embedding step
- Chunk size is a tradeoff between precision and context
- Overlap prevents information loss at boundaries
- Start simple (fixed-size), tune later
- Bad chunking is a common root cause of bad RAG answers
