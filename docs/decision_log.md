# Engineering Decision Log

## 001 — Local LLM for Generation

### Problem
The project requires an LLM generation layer, but no paid API
credits are available.

### Options Considered
1. OpenAI API
2. Anthropic API
3. Local open-weight LLM

### Selected Approach
Use Qwen2.5-1.5B-Instruct locally through Hugging Face Transformers.

### Why
- No API cost
- Keeps policy documents local
- Works on the development machine
- Easy to integrate with the existing Python pipeline

### Trade-offs
Advantages:
- No API dependency
- No per-request API cost
- Better data locality

Limitations:
- Lower generation quality than many larger hosted models
- CPU inference is slower
- Limited model capacity

### Current Status
Working successfully with the RAG pipeline.

---

## 002 — Embedding Model

### Problem
The RAG system needs semantic embeddings for policy retrieval.

### Selected Approach
`sentence-transformers/all-MiniLM-L6-v2`

### Why
- Lightweight
- Runs locally
- 384-dimensional embeddings
- Easy integration with Sentence Transformers
- Suitable as an initial retrieval baseline

### Trade-offs
Advantages:
- Fast local inference
- No API cost
- Simple implementation

Limitations:
- Not assumed to be optimal for policy/legal retrieval
- Retrieval quality must be evaluated

### Current Status
872 policy chunks successfully embedded and indexed in ChromaDB.

---

## 003 — Vector Database

### Problem
The system needs persistent semantic search over policy chunks.

### Selected Approach
ChromaDB

### Why
- Simple local persistent vector store
- Easy Python integration
- Suitable for the project prototype
- Supports metadata alongside documents

### Current Status
872 chunks successfully indexed.

---

## 004 — Abstention Behavior

### Problem
A compliance assistant should not answer questions when the
knowledge base does not provide sufficient evidence.

### Initial Approach
Instruct the LLM to abstain when retrieved context does not
contain enough information.

### Experiment
Question:
"What is the current price of Bitcoin?"

Result:
The model correctly responded that the provided sources did
not contain enough information.

### Remaining Improvement
The retriever still returns nearest-neighbor chunks for the
out-of-scope question. A retrieval-confidence threshold will
be evaluated so that low-confidence questions can be rejected
before generation and citations can be omitted.

### Status
Initial abstention behavior works; confidence-based abstention
is still to be implemented.