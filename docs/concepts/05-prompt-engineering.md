# Prompt Engineering for RAG

## Why This Matters

The prompt is the interface between your retrieval system and the LLM. A good retrieval pipeline that feeds into a poorly constructed prompt will still produce bad answers. Prompt engineering is not about tricks -- it's about clearly communicating what you want the model to do.

## Anatomy of a RAG Prompt

A RAG prompt has four parts:

### 1. System Instruction
Tells the LLM how to behave. For RAG, the critical instruction is: **only answer from the provided context.**

```
You are a helpful assistant that answers questions based on the provided context.
If the context does not contain enough information to answer, say "I don't have enough information to answer that."
Do not make up information.
```

Without this instruction, the LLM will happily fill in gaps with its training data, which may be outdated or wrong for your use case.

### 2. Retrieved Context
The chunks your retrieval system found. How you format these matters:

- Separate chunks clearly (with dividers or labels)
- Optionally include metadata like source page number
- Order by relevance (most relevant first) -- LLMs pay more attention to the beginning

### 3. User Question
The original question, placed after the context so the model reads the context first.

### 4. Output Instruction (optional)
Guidance on response format: "Answer in 2-3 sentences", "Respond in bullet points", "Include the source page number."

## Token Budget Management

Every token costs money and counts against the context window. You need to manage the budget:

```
context_window = model_max_tokens  (e.g., 128,000 for gpt-4o)
reserved_for_completion = 500-1000 tokens
reserved_for_system_prompt = ~150 tokens
reserved_for_question = ~50-100 tokens
available_for_chunks = context_window - reserved_for_completion - system - question
```

In practice, you rarely hit the window limit with gpt-4o (128k tokens). But you still care about token count because **you pay per token**.

### Cost Per Request (approximate)

| Model | Input Cost (per 1M tokens) | Output Cost (per 1M tokens) |
|-------|---------------------------|----------------------------|
| gpt-4o-mini | ~$0.15 | ~$0.60 |
| gpt-4o | ~$2.50 | ~$10.00 |

A typical RAG query with 5 chunks (~1,250 tokens) plus system prompt (~150 tokens) plus question (~50 tokens) = ~1,450 input tokens. With a ~300 token response:

- gpt-4o-mini: ~$0.0004 per request
- gpt-4o: ~$0.0066 per request

At 1,000 requests/day, that's $0.40/day with gpt-4o-mini or $6.60/day with gpt-4o. This matters at scale.

## Using tiktoken

tiktoken is OpenAI's tokenizer library. It lets you count tokens locally without an API call:

```python
import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")
token_count = len(encoding.encode("your text here"))
```

Use this to:
- Count tokens before sending the API request (pre-validate)
- Estimate cost before incurring it
- Log token usage for observability
- Truncate context if it would exceed the budget

## Common Prompt Mistakes in RAG

| Mistake | Consequence | Fix |
|---------|------------|-----|
| No "only use context" instruction | LLM hallucinates from training data | Add explicit grounding instruction |
| Dumping all chunks as one blob | LLM can't distinguish between chunks | Separate chunks with clear dividers |
| Too many chunks | Exceeds token limit or dilutes relevance | Reduce top-k or truncate |
| Question before context | Model may start answering before reading context | Place context first, question after |
| No "I don't know" instruction | LLM guesses when context is insufficient | Explicitly instruct to say "I don't know" |

## What You'll Implement

In `llm.py`, the prompt construction function will:

1. Accept a question string and a list of context chunks
2. Count tokens for each component using tiktoken
3. Assemble the prompt within budget
4. Return the formatted prompt (or send it to the API directly)

The key learning here: you're building the prompt manually, not relying on a framework. This forces you to understand exactly what the LLM sees.

## Key Takeaways

- The prompt has four parts: system instruction, context, question, output format
- "Only answer from the provided context" is the most important instruction in RAG
- Token counting with tiktoken enables cost estimation and budget management
- Place context before the question in the prompt
- You pay per token, so prompt size directly affects cost
