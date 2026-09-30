@"
# AI Compliance & Policy Assistant

A RAG-based Generative AI application for retrieving and answering questions about AI governance, compliance, and responsible AI using authoritative policy and regulatory documents.

The system combines semantic retrieval, local LLM generation, source citations, retrieval-based abstention, and prompt-injection guardrails.

## Project Status

Working local prototype.

## Problem Statement

AI governance and compliance documents are often long, technical, and difficult to search manually.

This project explores how a Retrieval-Augmented Generation (RAG) system can help users ask natural-language questions and receive answers grounded in a controlled collection of authoritative AI governance and regulatory documents.

The system is designed to:

- Retrieve relevant policy evidence
- Generate answers using retrieved evidence
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

Official source links are documented in [Sources.md](Sources.md).

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

The approach preserves document and page metadata while avoiding dependence on unreliable paragraph boundaries in extracted PDFs.

The final knowledge base contains:

872 chunks

4. Embeddings

The project uses:

sentence-transformers/all-MiniLM-L6-v2

The model produces 384-dimensional embeddings.

The embedding model was selected as a lightweight local baseline with no external API cost.

5. Vector Storage

ChromaDB is used as the local persistent vector store.

Each indexed chunk contains:

Text
Document metadata
Page metadata
Chunk identifier
Vector embedding

The current collection contains 872 chunks.

6. Retrieval

When a user asks a question:

The question is converted into an embedding.
ChromaDB performs semantic similarity search.
The top-k relevant chunks are returned.
The best retrieval distance is checked against the abstention threshold.
7. Abstention

The system uses:

ABSTENTION_THRESHOLD = 1.0

If the best retrieved distance is greater than the threshold, the system returns:

The provided sources do not contain enough information to answer this question.

This prevents clearly out-of-scope questions from being passed to the generation model.

The threshold was selected using the current evaluation set and is documented as a prototype limitation because the evaluation set is small.

8. Generation

The current local generation model is:

Qwen/Qwen2.5-0.5B-Instruct

Qwen2.5-1.5B-Instruct was initially tested but could not be loaded reliably in the development environment because of a Windows paging-file limitation.

The smaller 0.5B model was selected because it successfully runs in the available development environment.

For production, the model could be replaced with a larger or managed model-serving solution depending on cost, latency, security, compute, and data-governance requirements.

9. Citations

Retrieved chunks are presented to the generation model as numbered sources.

The application extracts source numbers from the model response and maps them back to retrieved document metadata.

The API can return:

Document name
Page number
Chunk ID
Source number

A fallback citation is used when the model does not return source numbers. In that case, the highest-ranked retrieved source is cited.

This provides source traceability, but a returned citation does not by itself guarantee that every generated statement is fully supported by that source.

10. Prompt-Injection Protection

A lightweight rule-based detector checks user queries for common prompt-injection patterns.

Examples include attempts to:

Ignore previous instructions
Disregard previous instructions
Override instructions
Reveal the system prompt
Follow new instructions
Act without restrictions

Detected attempts are rejected before retrieval and generation.

This is a prototype guardrail rather than a complete prompt-injection defense.

API

The application uses FastAPI.

Health Check
GET /health

Example response:

{
  "status": "healthy",
  "service": "AI Compliance Assistant"
}
Ask a Question
POST /ask

Request:

{
  "question": "What are the four core functions of the NIST AI Risk Management Framework?",
  "top_k": 5
}

The response includes:

Question
Answer
Citations
Grounded status
Abstention status
Best retrieval distance
Prompt-injection detection status
Setup
1. Clone the repository
git clone https://github.com/swetha-rajan18/AI-Compliance-Assistant.git
cd AI-Compliance-Assistant
2. Create a virtual environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Add source documents

Place the four source PDFs in:

data/raw/

The expected documents are:

nist_ai_rmf_1.0.pdf
nist_ai_rmf_playbook.pdf
nist_generative_ai_profile.pdf
eu_ai_act.pdf

The PDFs are intentionally excluded from GitHub. See Sources.md for the official sources.

5. Prepare the knowledge base

Run the project's ingestion and chunking scripts to generate the processed documents and chunks, then build the local ChromaDB vector store.

Generated data is intentionally excluded from GitHub through .gitignore.

Running the API

Start the FastAPI application:

uvicorn src.api:app --reload

The API will be available locally at:

http://127.0.0.1:8000

Interactive API documentation is available through FastAPI's generated documentation interface.

Test the health endpoint

In another terminal:

Invoke-RestMethod http://127.0.0.1:8000/health
Test the question endpoint
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/ask `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"question":"What are the four core functions of the NIST AI Risk Management Framework?","top_k":5}'
Evaluation

The project includes a small retrieval evaluation dataset in:

evaluation/questions.json

The current evaluation contains:

7 in-scope questions
3 out-of-scope questions

The in-scope questions cover:

NIST AI RMF
NIST Generative AI Profile
NIST AI RMF Playbook
EU AI Act

The out-of-scope questions include:

Bitcoin price
Bangalore weather
Most recent IPL winner
Current Retrieval Results

On the current evaluation set:

Document hits: 7/7
Document hit rate: 100%
Recall@1: 7/7 = 100%
Recall@5: 7/7 = 100%

The evaluation set was corrected during development to make one EU AI Act question specific to post-market monitoring. The resulting Recall@1 change should therefore not be interpreted as a retriever improvement; the evaluation question itself changed.

Because the evaluation set is small, these results should not be generalized to broader real-world retrieval performance.

Retrieval Experiments

Several retrieval strategies were evaluated rather than selecting a configuration without testing.

Chunking

Compared:

Fixed-size chunking
Paragraph-based chunking
Page-aware fixed-size chunking

The selected approach was page-aware fixed-size chunking with 2,000-character chunks and 200-character overlap.

Short-Chunk Filtering

Filtering chunks shorter than 200 characters was tested.

Results:

Baseline Recall@1: 85.71%
After filtering: 71.43%
Recall@5 remained 100%

The filtering approach was rejected because it reduced Recall@1 on the evaluation set.

Cross-Encoder Reranking

A cross-encoder reranker using:

cross-encoder/ms-marco-MiniLM-L-6-v2

was evaluated on the top 10 retrieved candidates.

Results:

Baseline Recall@1: 85.71%
Reranked Recall@1: 85.71%
Baseline Recall@5: 100%
Reranked Recall@5: 100%

The reranker was rejected because it did not improve aggregate retrieval metrics while adding model dependency, latency, and complexity.

Metadata-Aware Reranking

A lightweight metadata penalty was tested to move title, URL, and navigation chunks lower in the ranking.

The experiment changed some rankings but did not produce a measurable aggregate improvement.

It was therefore rejected for the current pipeline.

Responsible AI and Guardrails

The project includes several controls intended to reduce unsupported behavior:

Retrieval-Based Abstention

Questions with insufficient retrieval evidence are rejected before generation.

Prompt-Injection Detection

Basic attempts to override system behavior are detected and rejected before retrieval and generation.

Source Citations

The API exposes source metadata associated with retrieved evidence.

Grounding Evaluation

A lexical evidence-overlap evaluation was implemented to compare generated answers with cited evidence.

A final automated grounding score was not claimed for the current Qwen2.5-0.5B configuration because the earlier evaluation environment could not reliably load the Qwen2.5-1.5B model.

Manual API validation was used instead to verify:

In-scope answer generation
Source citation generation
Out-of-scope abstention
Prompt-injection rejection
Testing

The automated test suite covers the core ingestion, chunking, text-cleaning, and guardrail components.

Run:

pytest tests

Current result:

18 passed
Project Structure
AI-Compliance-Assistant/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── chunks/
│
├── src/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── inspect_loader.py
│   │   ├── ingest_documents.py
│   │   └── text_cleaner.py
│   │
│   ├── retrieval/
│   │   ├── chunker.py
│   │   ├── paragraph_chunker.py
│   │   ├── page_chunker.py
│   │   ├── build_chunks.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   └── rag_pipeline.py
│   │
│   └── api.py
│
├── evaluation/
│   ├── questions.json
│   ├── evaluate_retrieval.py
│   └── evaluate_grounding.py
│
├── experiments/
│   ├── analyze_chunk_lengths.py
│   ├── compare_pdf_extractors.py
│   ├── compare_chunking.py
│   ├── test_chunking.py
│   ├── test_page_chunking.py
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   ├── test_rag.py
│   ├── test_llm.py
│   ├── test_reranking.py
│   └── test_metadata_reranking.py
│
├── tests/
│   ├── test_pdf_loader.py
│   ├── test_text_cleaner.py
│   ├── test_chunker.py
│   └── test_rag_guardrails.py
│
├── docs/
│   └── decision_log.md
│
├── Sources.md
├── README.md
├── requirements.txt
├── pytest.ini
└── .gitignore
Engineering Decisions

Major implementation decisions and experiment results are documented in:

docs/decision_log.md

The decision log covers:

Local LLM selection
Embedding model selection
Vector database selection
Chunking strategy
Short-chunk filtering
Cross-encoder reranking
Metadata-aware reranking
Retrieval evaluation
Abstention threshold
Prompt-injection guardrail
Citation handling
Grounding evaluation
FastAPI
Dockerization decision
Docker

Dockerization was investigated but deferred for the current portfolio milestone.

A Docker build was attempted and reached dependency installation, but the large machine-learning dependency stack caused environment/build issues.

The current project therefore runs locally rather than as a Docker container.

Containerization remains a potential production deployment step with a CPU-optimized dependency strategy or separate model-serving architecture.

Security and Data Considerations

The source PDFs are kept locally and are not committed to the repository.

The repository's .gitignore excludes:

Raw PDFs
Processed data
Generated chunks
Vector databases
Environment files
Python caches
Build artifacts

The current prototype does not implement production authentication, rate limiting, access control, or full observability.

Limitations

The current prototype has several limitations:

Small retrieval evaluation dataset
Local CPU-oriented LLM generation
Smaller 0.5B generation model
Lightweight prompt-injection detection
Automated final grounding score not completed for the final model configuration
Citation validation is not fully automated
Retrieval-distance threshold is based on a small evaluation set
No production authentication
No production rate limiting
No production observability
Dockerization deferred
Future Improvements

Potential future improvements include:

Larger and more diverse evaluation datasets
More robust grounding and citation evaluation
Stronger prompt-injection defenses
Improved retrieval models
Hybrid lexical + semantic retrieval
Reranking if supported by future evaluation results
Larger or managed LLM deployment
Automated monitoring and observability
Authentication and rate limiting
Containerized deployment
Cloud deployment
Human-review workflows for higher-risk compliance questions
Key Technologies
Python
PyMuPDF
Sentence Transformers
ChromaDB
Hugging Face Transformers
Qwen2.5-0.5B-Instruct
FastAPI
Pytest
Git / GitHub
Source Documents

The project uses publicly available AI governance and regulatory documents from NIST and the European Union.

See Sources.md for the official source links.

License

This repository contains the project's source code and documentation.

The original policy and regulatory PDFs are not redistributed in this repository. Users should obtain source documents directly from their respective official publishers.
