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

---

## 005 — Page-Aware Fixed-Size Chunking

### Problem
The source PDFs contain different document structures, and PDF text
extraction can flatten paragraph boundaries. A chunking strategy was
needed that preserved page-level source metadata while providing
consistent chunk sizes.

### Options Considered
1. Fixed-size chunking across extracted text
2. Paragraph-based chunking
3. Page-aware fixed-size chunking

### Experiment
Using 2,000-character chunks with 200-character overlap:

- EU AI Act:
  - Fixed-size: 331 chunks
  - Paragraph-based: 144 chunks
- NIST AI RMF:
  - Fixed-size: 59 chunks
  - Paragraph-based: 46 chunks
- NIST AI RMF Playbook:
  - Fixed-size: 186 chunks
  - Paragraph-based: 147 chunks
- NIST Generative AI Profile:
  - Fixed-size: 88 chunks
  - Paragraph-based: 63 chunks

Paragraph boundaries were unreliable because PDF extraction flattened
some document structure.

### Selected Approach
Page-aware fixed-size chunking with:
- Chunk size: 2,000 characters
- Overlap: 200 characters

### Why
- Preserves document and page metadata
- Provides consistent chunk sizes
- Avoids depending on unreliable paragraph boundaries
- Supports source-level citations

### Trade-offs
Advantages:
- Simple and predictable
- Preserves page references
- Easy to reproduce

Limitations:
- Chunks can split semantic sections
- Some pages contain short metadata or navigation chunks

### Current Status
872 chunks generated and indexed.

---

## 006 — Short-Chunk Filtering

### Problem
Some extracted PDF pages produced extremely short chunks containing
titles, URLs, or section headings rather than substantive policy text.

### Experiment
The baseline contained 872 chunks.

Filtering chunks shorter than 200 characters removed 7 chunks,
reducing the collection from 872 to 865 chunks.

Retrieval evaluation showed:
- Baseline Recall@1: 85.71%
- After filtering: 71.43%
- Recall@5 remained 100%

### Decision
Reject blanket short-chunk filtering.

### Why
Although the removed chunks were mostly metadata or navigation
artifacts, removing them reduced Recall@1 on the evaluation set.

### Current Status
The full 872-chunk collection is retained.

---

## 007 — Cross-Encoder Reranking

### Problem
Embedding similarity can retrieve semantically related but less
specific chunks above more directly relevant evidence.

### Experiment
A cross-encoder reranker was tested on the top 10 vector-search
candidates using:

`cross-encoder/ms-marco-MiniLM-L-6-v2`

Results:
- Baseline Recall@1: 85.71%
- Reranked Recall@1: 85.71%
- Baseline Recall@5: 100%
- Reranked Recall@5: 100%

The reranker improved the ranking of a specific EU AI Act risk
management query, but did not improve aggregate retrieval metrics.

### Decision
Do not add cross-encoder reranking to the production pipeline yet.

### Why
The additional model introduces:
- Extra inference latency
- Additional complexity
- Another model dependency

There was no measurable aggregate retrieval improvement to justify
those costs at this stage.

### Current Status
Evaluated and rejected for the current baseline.

---

## 008 — Metadata-Aware Reranking

### Problem
Some source pages contain title, URL, cover, or navigation chunks
that can rank highly because of semantic similarity even though they
provide little substantive evidence.

### Experiment
A targeted metadata penalty was applied to the top 10 retrieved
candidates. Obvious metadata/navigation chunks received a small
distance penalty while remaining in the knowledge base.

The experiment successfully moved obvious metadata chunks lower in
some rankings. For example, the NIST Playbook cover moved below
substantive content.

However, the aggregate retrieval results remained:

- In-scope document hit rate: 100%
- Recall@1: 85.71%
- Recall@5: 100%

For the NIST AI RMF purpose query, the metadata penalty removed the
title-only chunk from the top position, but a less directly relevant
chunk still ranked above the more useful evidence.

### Decision
Reject metadata-aware reranking for the current production pipeline.

### Why
It changed rankings but did not improve the key retrieval metric.
Adding another heuristic would increase retrieval complexity without
demonstrated aggregate improvement.

### Current Status
Evaluated and rejected for the current baseline.

---

## 009 — Retrieval Baseline

### Current Evaluation
The current retrieval baseline uses:
- Page-aware fixed-size chunks
- 2,000-character chunk size
- 200-character overlap
- `sentence-transformers/all-MiniLM-L6-v2`
- ChromaDB
- Top-k semantic retrieval

Evaluation results:
- In-scope document hit rate: 7/7 (100%)
- Recall@1: 6/7 (85.71%)
- Recall@5: 7/7 (100%)

Out-of-scope questions produced higher nearest-neighbor distances
than the in-scope questions in the current evaluation set.

### Interpretation
The baseline reliably retrieves the correct source document within
the top 5 results, but top-1 ranking still has room for improvement.

### Current Status
Accepted as the retrieval baseline for the next stage of development.