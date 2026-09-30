from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag.rag_pipeline import RAGPipeline


app = FastAPI(
    title="AI Compliance Assistant",
    description="RAG-based AI governance and compliance research assistant.",
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


class AskResponse(BaseModel):
    question: str
    answer: str
    citations: list[dict]
    grounded: bool
    abstained: bool
    best_distance: float | None
    prompt_injection_detected: bool


rag_pipeline = RAGPipeline()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Compliance Assistant",
    }


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    if request.top_k < 1 or request.top_k > 10:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 10.",
        )

    try:
        result = rag_pipeline.answer(
            question=request.question,
            top_k=request.top_k,
        )
        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {exc}",
        )