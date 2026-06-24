from __future__ import annotations

from pathlib import Path

from ml_platform.metrics import MetricsRegistry
from ml_platform.scoring import load_model, prediction_payload


MODEL_PATH = Path("models/sample_model.json")


def create_app(model_path: str | Path = MODEL_PATH):
    from fastapi import FastAPI, Response
    from pydantic import BaseModel, Field

    class PredictionRequest(BaseModel):
        rooms: float = Field(gt=0)
        sqft: float = Field(gt=0)

    app = FastAPI(title="ML Platform Model API", version="0.1.0")
    model = load_model(model_path)
    metrics = MetricsRegistry()

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "model": model.name, "version": model.version}

    @app.post("/predict")
    def predict(request: PredictionRequest):
        payload = prediction_payload(model, {"rooms": request.rooms, "sqft": request.sqft})
        metrics.observe(ok=True, warnings=len(payload["warnings"]))
        return payload

    @app.get("/metrics")
    def prometheus_metrics():
        return Response(metrics.prometheus_text(), media_type="text/plain; version=0.0.4")

    return app
