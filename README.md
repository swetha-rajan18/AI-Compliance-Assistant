# AI Compliance & Policy Assistant

A RAG-based Generative AI application for retrieving and answering
questions about AI governance, compliance, and responsible AI using
authoritative policy and regulatory documents.

The system combines semantic retrieval, local LLM generation,
source citations, retrieval-based abstention, and prompt-injection
guardrails.

## Project Status

Working local prototype.

## Problem Statement

AI governance and compliance documents are often long, technical,
and difficult to search manually.

This project explores how a Retrieval-Augmented Generation (RAG)
system can help users ask natural-language questions and receive
answers grounded in a controlled collection of authoritative
AI governance and regulatory documents.

The system is designed to:

- Retrieve relevant policy evidence
- Generate concise answers using retrieved evidence
- Provide source and page references
- Abstain when the knowledge base does not provide sufficient evidence
- Reject basic prompt-injection attempts
- Expose the RAG pipeline through a FastAPI API

## Knowledge Base

The initial knowledge base contains:

- NIST AI Risk Management Framework (AI RMF)
- NIST AI RMF Playbook
- NIST Generative AI Profile
- EU AI Act

The original source PDFs are not included in this repository.

Official source links are documented separately in
`Sources.md`.

## System Architecture

```mermaid
flowchart TD
    A[Policy & Regulatory PDFs] --> B[PDF Ingestion]
    B --> C[Text Cleaning]
    C --> D[Page-Aware Chunking]
    D --> E[Sentence Transformer Embeddings]
    E --> F[ChromaDB]

    U[User Question] --> G[Prompt Injection Check]
    G --> H[Semantic Retrieval]
    H --> I{Retrieval Distance}
    I -->|Insufficient Evidence| J[Abstain]
    I -->|Sufficient Evidence| K[Build RAG Prompt]
    K --> L[Qwen2.5-0.5B-Instruct]
    L --> M[Answer + Source References]

    F --> H
    M --> N[FastAPI Response]
    J --> N

RAG Data Flow
1. Document Ingestion

PDF documents are processed using PyMuPDF.

Each page is stored with metadata including:

Document ID
Document name
Page number
Extracted text
2. Text Cleaning

Extracted PDF text is normalized by:

Removing unnecessary line breaks
Rejoining hyphenated words
Normalizing whitespace
3. Chunking

The selected strategy is page-aware fixed-size chunking.

Configuration:

Chunk size: 2,000 characters
Overlap: 200 characters

The approach preserves document and page metadata while avoiding
dependence on unreliable paragraph boundaries in extracted PDFs.

The final knowledge base contains:

872 chunks

4. Embeddings

The project uses:

sentence-transformers/all-MiniLM-L6-v2

The model produces 384-dimensional embeddings.

5. Vector Storage

ChromaDB is used as the local persistent vector store.

Each chunk contains:

Text
Document metadata
Page metadata
Chunk identifier
Vector embedding
6. Retrieval

When a user asks a question:

The question is converted into an embedding.
ChromaDB performs semantic similarity search.
The top-k relevant chunks are returned.
The best retrieval distance is checked against the abstention threshold.
7. Abstention

The system uses:

ABSTENTION_THRESHOLD = 1.0

If the best retrieved distance is greater than the threshold, the
system returns:

The provided sources do not contain enough information to answer
this question.

This prevents clearly out-of-scope questions from being passed to
the generation model.

8. Generation

The current local generation model is:

Qwen/Qwen2.5-0.5B-Instruct

Qwen2.5-1.5B-Instruct was initially tested but could not be loaded
reliably in the development environment because of Windows virtual
memory limitations.

The smaller 0.5B model was selected for the local prototype because
it successfully runs in the available environment.

For production, the model could be replaced with a larger or managed
model-serving solution depending on cost, latency, security, and
data-governance requirements.

9. Citations

Retrieved chunks are presented to the generation model as numbered
sources.

The API returns citation metadata including:

Document
Page
Chunk ID
Source number
10. Prompt-Injection Protection

A lightweight rule-based detector checks user queries for common
prompt-injection patterns.

Examples include attempts to:

Ignore previous instructions
Override instructions
Reveal the system prompt
Follow new instructions
Remove restrictions

Detected attempts are rejected before retrieval and generation.

API

The application uses FastAPI.