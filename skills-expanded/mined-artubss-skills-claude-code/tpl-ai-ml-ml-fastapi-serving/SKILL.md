---
name: tpl-ai-ml-ml-fastapi-serving
description: Template do pack (ai-ml/05-ml-fastapi-serving.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/05-ml-fastapi-serving.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: ML Model Serving with FastAPI + Pydantic v2 + Prometheus

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/05-ml-fastapi-serving.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Language:** Python 3.12
- **API:** FastAPI + Pydantic v2 + uvicorn
- **Model:** scikit-learn (joblib) / PyTorch (TorchScript)
- **Containerization:** Docker (multi-stage)
- **Metrics:** prometheus-client (custom metrics)
- **Validation:** Pydantic v2 strict mode
- **Monitoring:** Feature drift detection (Evidently AI)

---

## PROJECT STRUCTURE
```
ml-api/
├── app/
│   ├── main.py              # FastAPI app factory
│   ├── models/
│   │   ├── loader.py        # Singleton model loader
│   │   └── registry.py      # Model version registry
│   ├── routes/
│   │   ├── predict_v1.py    # /v1/predict
│   │   └── health.py        # /healthz
│   ├── schemas/
│   │   ├── request.py       # PredictRequest (Pydantic v2)
│   │   └── response.py      # PredictResponse
│   ├── middleware/
│   │   ├── metrics.py       # Prometheus instrumentation
│   │   └── logging.py       # Prediction logging
│   └── drift/
│       └── detector.py       # Feature drift detection
├── artifacts/
│   ├── model_v1.pkl          # Serialized model
│   └── feature_config.json   # Feature names + expected ranges
├── tests/
│   └── test_predict.py
├── Dockerfile
└── requirements.txt
```

---

## ARCHITECTURE RULES
1. **Model loads at startup, not per request** — load into a singleton; requests share the instance.
2. **Versioned endpoints** — `/v1/predict`, `/v2/predict`; never deprecate without a migration path.
3. **Input validation is strict** — reject requests with wrong types or out-of-range values before inference.
4. **Prediction logging is mandatory** — every prediction logged with features + output (for monitoring and retraining).
5. **Drift detection is async** — check drift in background; never block the prediction path.
6. **A/B testing via weighted routing** — `/predict` routes to model A or B; log which model served each request.
7. **Never pickle arbitrary objects** — use `joblib` for sklearn; TorchScript or ONNX for PyTorch.
8. **Metrics export on `/metrics`** — Prometheus scrape endpoint always available.

---

## MODEL LOADER (SINGLETON)

```python
# app/models/loader.py
import joblib
import torch
from pathlib import Path
from functools import lru_cache
import logging
import json

logger = logging.getLogger(__name__)

class ModelLoader:
    _sklearn_model = None
    _feature_config: dict | None = None

    @classmethod
    def load(cls, model_path: str = "artifacts/model_v1.pkl",
             config_path: str = "artifacts/feature_config.json") -> None:
        if cls._sklearn_model is not None:
            return   # Already loaded

        logger.info(f"Loading model from {model_path}")
        cls._sklearn_model = joblib.load(model_path)

        with open(config_path) as f:
            cls._feature_config = json.load(f)

        logger.info("Model loaded successfully")

    @classmethod
    def get_model(cls):
        if cls._sklearn_model is None:
            raise RuntimeError("Model not loaded. Call ModelLoader.load() at startup.")
        return cls._sklearn_model

    @classmethod
    def get_feature_config(cls) -> dict:
        return cls._feature_config or {}


# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.loader import ModelLoader

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model before accepting traffic
    ModelLoader.load()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(lifespan=lifespan, title="ML Prediction API", version="1.0.0")
```

---

## PYDANTIC V2 SCHEMAS

```python
# app/schemas/request.py
from pydantic import BaseModel, Field, model_validator
from typing import Annotated
import numpy as np

class PredictRequest(BaseModel):
    model_config = {"strict": True}   # Pydantic v2 strict mode

    # Example: house price prediction features
    bedrooms:    Annotated[int,   Field(ge=1, le=20, description="Number of bedrooms")]
    bathrooms:   Annotated[float, Field(ge=0.5, le=15, description="Number of bathrooms")]
    sqft:        Annotated[int,   Field(ge=100, le=20000, description="Square footage")]
    year_built:  Annotated[int,   Field(ge=1800, le=2024, description="Year built")]
    zip_code:    Annotated[str,   Field(pattern=r"^\d{5}$", description="5-digit ZIP")]

    @model_validator(mode="after")
    def validate_bathroom_bedroom_ratio(self) -> "PredictRequest":
        if self.bathrooms > self.bedrooms * 2:
            raise ValueError(
                f"Bathrooms ({self.bathrooms}) > 2x bedrooms ({self.bedrooms}) is unrealistic"
            )
        return self

    def to_feature_array(self) -> list[float]:
        return [
            float(self.bedrooms),
            float(self.bathrooms),
            float(self.sqft),
            float(2024 - self.year_built),   # Age instead of year
        ]

# app/schemas/response.py
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class PredictResponse(BaseModel):
    prediction_id: UUID = Field(default_factory=uuid4)
    predicted_price: float
    confidence_interval: tuple[float, float]
    model_version: str
    features_used: list[str]
```

---

## PREDICT ENDPOINT

```python
# app/routes/predict_v1.py
from fastapi import APIRouter, HTTPException, Request
from app.schemas.request import PredictRequest
from app.schemas.response import PredictResponse
from app.models.loader import ModelLoader
from app.middleware.metrics import (
    prediction_counter, prediction_latency, prediction_errors
)
from app.middleware.logging import log_prediction
import time, logging, numpy as np

router = APIRouter(prefix="/v1")
logger = logging.getLogger(__name__)

MODEL_VERSION = "1.0.0"
FEATURE_NAMES = ["bedrooms", "bathrooms", "sqft", "age"]

@router.post("/predict", response_model=PredictResponse)
async def predict(body: PredictRequest, request: Request):
    start = time.monotonic()

    try:
        model = ModelLoader.get_model()
        features = np.array([body.to_feature_array()])

        # Inference
        prediction = model.predict(features)[0]

        # Confidence interval (if model supports it, e.g., GradientBoosting)
        # Fallback: ±10% for demonstration
        ci_low  = prediction * 0.90
        ci_high = prediction * 1.10

        response = PredictResponse(
            predicted_price=round(float(prediction), 2),
            confidence_interval=(round(ci_low, 2), round(ci_high, 2)),
            model_version=MODEL_VERSION,
            features_used=FEATURE_NAMES,
        )

        # Log for monitoring + retraining pipeline
        await log_prediction(
            prediction_id=str(response.prediction_id),
            features=body.model_dump(),
            prediction=float(prediction),
            model_version=MODEL_VERSION,
        )

        prediction_counter.labels(model_version=MODEL_VERSION, status="success").inc()
        return response

    except Exception as e:
        prediction_errors.labels(error_type=type(e).__name__).inc()
        logger.error({"event": "prediction_error", "error": str(e)})
        raise HTTPException(status_code=500, detail="Prediction failed")

    finally:
        latency = time.monotonic() - start
        prediction_latency.labels(model_version=MODEL_VERSION).observe(latency)
```

---

## PROMETHEUS METRICS

```python
# app/middleware/metrics.py
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app
from starlette.routing import Mount

prediction_counter = Counter(
    "ml_predictions_total",
    "Total predictions",
    ["model_version", "status"],
)

prediction_latency = Histogram(
    "ml_prediction_duration_seconds",
    "Prediction latency",
    ["model_version"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)

prediction_errors = Counter(
    "ml_prediction_errors_total",
    "Prediction errors by type",
    ["error_type"],
)

model_loaded = Gauge(
    "ml_model_loaded",
    "Whether model is loaded (1=yes)",
    ["model_version"],
)

# Mount /metrics endpoint
metrics_app = make_asgi_app()

def add_metrics_route(app):
    app.mount("/metrics", metrics_app)
```

---

## FEATURE DRIFT DETECTION

```python
# app/drift/detector.py — run in background, don't block predictions
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd
import asyncio
import logging

logger = logging.getLogger(__name__)

DRIFT_CHECK_INTERVAL = 3600    # Check every hour
DRIFT_THRESHOLD      = 0.3     # Alert if drift score > 0.3

class DriftDetector:
    def __init__(self, reference_data: pd.DataFrame):
        self.reference = reference_data
        self.predictions_buffer: list[dict] = []

    def add_prediction(self, features: dict):
        self.predictions_buffer.append(features)

    async def check_drift_loop(self):
        while True:
            await asyncio.sleep(DRIFT_CHECK_INTERVAL)
            if len(self.predictions_buffer) >= 100:
                self._run_drift_check()

    def _run_drift_check(self):
        current = pd.DataFrame(self.predictions_buffer[-1000:])
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=self.reference, current_data=current)
        results = report.as_dict()

        drift_share = results["metrics"][0]["result"]["share_of_drifted_columns"]
        logger.info({"event": "drift_check", "drift_share": drift_share})

        if drift_share > DRIFT_THRESHOLD:
            logger.warning({
                "event": "feature_drift_detected",
                "drift_share": drift_share,
                "action": "Consider retraining model",
            })
        self.predictions_buffer.clear()
```

---

## A/B TESTING ENDPOINT

```python
# app/routes/ab_test.py
import random
from fastapi import APIRouter
from app.models.loader import ModelLoader
from app.schemas.request import PredictRequest

router = APIRouter()

# 80% model A, 20% model B
AB_CONFIG = {"model_v1": 0.8, "model_v2": 0.2}

@router.post("/predict")
async def predict_ab(body: PredictRequest):
    variant = random.choices(
        list(AB_CONFIG.keys()),
        weights=list(AB_CONFIG.values()),
    )[0]

    model = ModelLoader.get_model(variant)
    features = [body.to_feature_array()]
    prediction = model.predict(features)[0]

    return {
        "prediction": float(prediction),
        "model_variant": variant,   # Log this; analyze per-variant metrics
    }
```

---

## DOCKERFILE

```dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

FROM base AS builder
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM base AS production
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PORT=8000
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH

HEALTHCHECK --interval=30s --timeout=5s CMD wget -qO- http://localhost:8000/healthz || exit 1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "2", "--log-config", "log_config.json"]
```
