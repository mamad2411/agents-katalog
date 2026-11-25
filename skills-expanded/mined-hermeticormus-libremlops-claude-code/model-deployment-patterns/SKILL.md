---
name: "model-deployment-patterns"
description: "Model serving patterns with code: production FastAPI serving, the Triton model repository layout, ONNX export with validation, canary deployment on Kubernetes, and load testing with Locust. Use when serving a model in production."
---

# Model Deployment Patterns

Expert patterns for model serving, ONNX export, Triton configuration, and traffic splitting.

## Pattern 1: FastAPI Production Serving

Production-ready FastAPI service with model loaded at startup, health checks, and Prometheus metrics.

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import time
import logging
from prometheus_fastapi_instrumentator import Instrumentator

logger = logging.getLogger(__name__)

class PredictRequest(BaseModel):
    features: list[float]
    user_id: str

class PredictResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str
    latency_ms: float

# Global model state
model_state = {"model": None, "version": None, "ready": False}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model at startup, release at shutdown."""
    logger.info("Loading model...")
    model_state["model"] = joblib.load("models/model.pkl")
    model_state["version"] = open("models/version.txt").read().strip()
    model_state["ready"] = True
    logger.info(f"Model v{model_state['version']} loaded")
    yield
    logger.info("Shutting down")

app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)  # /metrics endpoint for Prometheus

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/ready")
def ready():
    if not model_state["ready"]:
        raise HTTPException(status_code=503, detail="Model not ready")
    return {"status": "ready", "model_version": model_state["version"]}

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    if not model_state["ready"]:
        raise HTTPException(status_code=503, detail="Service not ready")

    t0 = time.perf_counter()
    X = np.array(request.features).reshape(1, -1)

    try:
        proba = model_state["model"].predict_proba(X)[0, 1]
        prediction = int(proba >= 0.5)
    except Exception as e:
        logger.error(f"Prediction failed for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    latency_ms = (time.perf_counter() - t0) * 1000

    return PredictResponse(
        prediction=prediction,
        probability=round(float(proba), 6),
        model_version=model_state["version"],
        latency_ms=round(latency_ms, 2)
    )
```

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY models/ models/
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

## Pattern 2: Triton Model Repository Layout

Config and directory structure for Triton multi-model serving.

```
model_repository/
├── sentiment_onnx/
│   ├── config.pbtxt
│   └── 1/
│       └── model.onnx
└── fraud_tensorrt/
    ├── config.pbtxt
    └── 1/
        └── model.plan
```

```protobuf
# model_repository/sentiment_onnx/config.pbtxt
name: "sentiment_onnx"
backend: "onnxruntime"
max_batch_size: 64

input [
  {
    name: "input_ids"
    data_type: TYPE_INT64
    dims: [ 512 ]
  },
  {
    name: "attention_mask"
    data_type: TYPE_INT64
    dims: [ 512 ]
  }
]

output [
  {
    name: "logits"
    data_type: TYPE_FP32
    dims: [ 2 ]
  }
]

dynamic_batching {
  preferred_batch_size: [ 16, 32, 64 ]
  max_queue_delay_microseconds: 5000
}

instance_group [
  {
    kind: KIND_GPU
    count: 2
    gpus: [ 0 ]
  }
]
```

```bash
# Start Triton server
docker run --gpus all \
  -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v /path/to/model_repository:/models \
  nvcr.io/nvidia/tritonserver:23.10-py3 \
  tritonserver --model-repository=/models

# Check model status
curl http://localhost:8000/v2/models/sentiment_onnx/ready

# Python client
import tritonclient.http as httpclient
import numpy as np

client = httpclient.InferenceServerClient(url="localhost:8000")
inputs = [
    httpclient.InferInput("input_ids", [1, 512], "INT64"),
    httpclient.InferInput("attention_mask", [1, 512], "INT64"),
]
inputs[0].set_data_from_numpy(input_ids_np)
inputs[1].set_data_from_numpy(attention_mask_np)
outputs = [httpclient.InferRequestedOutput("logits")]
response = client.infer("sentiment_onnx", inputs, outputs=outputs)
logits = response.as_numpy("logits")
```

## Pattern 3: ONNX Export and Validation

Export PyTorch model to ONNX and validate numerical equivalence.

```python
import torch
import onnxruntime as ort
import numpy as np

def export_to_onnx(
    model: torch.nn.Module,
    dummy_input: torch.Tensor,
    output_path: str = "model.onnx",
    opset_version: int = 17
) -> None:
    model.eval()
    with torch.no_grad():
        torch.onnx.export(
            model,
            dummy_input,
            output_path,
            export_params=True,
            opset_version=opset_version,
            do_constant_folding=True,
            input_names=["input"],
            output_names=["output"],
            dynamic_axes={
                "input": {0: "batch_size"},
                "output": {0: "batch_size"},
            },
        )
    print(f"Exported to {output_path}")

def validate_onnx(
    torch_model: torch.nn.Module,
    onnx_path: str,
    test_input: torch.Tensor,
    atol: float = 1e-4
) -> bool:
    """Verify ONNX outputs match PyTorch outputs within tolerance."""
    torch_model.eval()
    with torch.no_grad():
        torch_output = torch_model(test_input).numpy()

    ort_session = ort.InferenceSession(
        onnx_path,
        providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
    )
    ort_inputs = {ort_session.get_inputs()[0].name: test_input.numpy()}
    ort_output = ort_session.run(None, ort_inputs)[0]

    max_diff = np.abs(torch_output - ort_output).max()
    passed = max_diff <= atol
    print(f"Max output diff: {max_diff:.2e} ({'PASS' if passed else 'FAIL'})")
    return passed

# Benchmark throughput comparison
import time

def benchmark_throughput(model_fn, inputs, n_iters=1000) -> float:
    """Returns samples per second."""
    for _ in range(50):  # warmup
        model_fn(inputs)
    t0 = time.perf_counter()
    for _ in range(n_iters):
        model_fn(inputs)
    elapsed = time.perf_counter() - t0
    return n_iters * inputs.shape[0] / elapsed
```

## Pattern 4: Canary Deployment via Kubernetes

Traffic splitting between model versions using Kubernetes and Istio.

```yaml
# istio-virtual-service.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: sentiment-model-vs
spec:
  hosts:
    - sentiment-model
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: sentiment-model
            subset: v2
    - route:
        # 90% stable / 10% canary
        - destination:
            host: sentiment-model
            subset: v1
          weight: 90
        - destination:
            host: sentiment-model
            subset: v2
          weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: sentiment-model-dr
spec:
  host: sentiment-model
  subsets:
    - name: v1
      labels:
        version: "1.2.3"
    - name: v2
      labels:
        version: "1.3.0"
```

## Pattern 5: Load Testing with Locust

Validate serving latency and throughput before production traffic.

```python
# locustfile.py
from locust import HttpUser, task, between
import json
import random

class MLModelUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        # Verify health
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Health check failed")

    @task(10)
    def predict_single(self):
        features = [random.random() for _ in range(50)]
        with self.client.post(
            "/predict",
            json={"features": features, "user_id": "load_test_user"},
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Predict failed: {response.status_code}")
                return
            data = response.json()
            if data.get("latency_ms", 0) > 100:
                response.failure(f"Latency {data['latency_ms']:.0f}ms exceeds 100ms SLA")

    @task(1)
    def health_check(self):
        self.client.get("/health")
```

```bash
# Run load test: 100 concurrent users, ramp for 60s
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users=100 \
  --spawn-rate=10 \
  --run-time=2m \
  --headless \
  --csv=load_test_results

# Key metrics: p50 < 20ms, p99 < 100ms, failure rate < 0.1%
```

## Anti-Patterns

### Anti-Pattern 1: Loading Model Per Request
Loading `joblib.load("model.pkl")` inside the `/predict` handler means every request pays the model loading cost (100ms–1s). Always load at application startup using lifespan context or `@app.on_event("startup")`.

### Anti-Pattern 2: No Health/Readiness Distinction
`/health` (liveness): is the process alive? `GET /health` should return 200 immediately.
`/ready` (readiness): is the model loaded and ready to serve? Returns 503 during startup. Kubernetes uses both. Merging them means Kubernetes kills pods still loading their model.

### Anti-Pattern 3: Dynamic Batching Without Latency Cap
Dynamic batching without `max_queue_delay_microseconds` lets requests queue indefinitely during low traffic. A batch of 1 is better than waiting 5 seconds for a full batch. Always set a max wait time.

### Anti-Pattern 4: Deploying Without Load Testing
A model that handles 10 requests/sec in development may fail at 1000 req/s in production. Always load test with locust/k6 against realistic concurrency before production traffic. Measure p99, not just mean latency.
