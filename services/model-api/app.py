from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from ml_platform.metrics import MetricsRegistry
from ml_platform.scoring import load_model, prediction_payload


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    rooms: float = Field(gt=0)
    sqft: float = Field(gt=0)


def create_app(model_path: str | Path | None = None) -> FastAPI:
    # Resolve at startup, not import time, so every worker verifies its artifact.
    model_path = model_path or os.environ.get("MODEL_PATH", "models/sample_model.json")
    model = load_model(model_path)
    for variable, actual in (
        ("MODEL_NAME", model.name),
        ("MODEL_VERSION", model.version),
    ):
        expected = os.environ.get(variable)
        if expected and expected != actual:
            raise ValueError(
                f"{variable}={expected!r} does not match artifact {actual!r}"
            )

    app = FastAPI(title="ML Platform Model API", version="0.2.0")
    metrics = MetricsRegistry()

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        if request.url.path == "/predict":
            metrics.observe(ok=False)
        return JSONResponse(
            status_code=422,
            content={"detail": "Expected only positive, finite rooms and sqft values"},
        )

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "model": model.name, "version": model.version}

    @app.post("/predict")
    def predict(request: PredictionRequest):
        try:
            payload = prediction_payload(
                model, {"rooms": request.rooms, "sqft": request.sqft}
            )
        except ValueError as exc:
            metrics.observe(ok=False)
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        metrics.observe(ok=True, warnings=len(payload["warnings"]))
        return payload

    @app.get("/metrics")
    def prometheus_metrics():
        return Response(
            metrics.prometheus_text(), media_type="text/plain; version=0.0.4"
        )

    return app
