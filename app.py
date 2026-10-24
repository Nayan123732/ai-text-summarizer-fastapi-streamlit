import sys
import threading
from contextlib import asynccontextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from text_summarizer.logging import logger
from text_summarizer.pipeline.prediction import PredictionPipeline

MAX_CHARS = 20000

state = {}
predict_lock = threading.Lock()  # one summary at a time keeps memory use low

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up: loading the model (this can take a minute)")
    state["pipeline"] = PredictionPipeline()
    logger.info("Ready for requests")
    yield
    state.clear()


app = FastAPI(title="Text Summarizer API", lifespan=lifespan)


class SummarizeRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": "pipeline" in state}


@app.post("/predict")
def predict(request: SummarizeRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is empty.")
    if len(text) > MAX_CHARS:
        raise HTTPException(
            status_code=413,
            detail=f"Text is too long ({len(text)} characters). The limit is {MAX_CHARS}.",
        )

    pipeline = state.get("pipeline")
    if pipeline is None:
        raise HTTPException(status_code=503, detail="The model is still loading. Try again shortly.")

    try:
        with predict_lock:
            summary = pipeline.predict(text)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Summarization failed. Check logs/running_logs.log.")

    original_words = len(text.split())
    summary_words = len(summary.split())
    compression = round(max(0.0, (1 - summary_words / original_words) * 100), 1) if original_words else 0.0

    return {
        "summary": summary,
        "original_words": original_words,
        "summary_words": summary_words,
        "compression_percent": compression,
    }
