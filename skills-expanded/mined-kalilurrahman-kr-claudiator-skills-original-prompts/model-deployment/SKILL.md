---
name: model-deployment
description: Deploy ML models to production with FastAPI, TorchServe, or SageMaker. Outputs serving infrastructure, scaling, monitoring, and A/B testing.
argument-hint: [model type, throughput requirements, latency SLA]
allowed-tools: Read, Write, Bash
---

# ML Model Deployment

Deploy ML models to production with proper serving infrastructure, versioning, monitoring, and rollback capabilities. Not just "pickle and Flask" — production-grade APIs, autoscaling, canary releases, and drift detection.

## Process

1. **Choose serving framework.** FastAPI (custom), TorchServe (PyTorch), TF Serving (TensorFlow), SageMaker (AWS).
2. **Package model.** Serialization format, dependencies, preprocessing code.
3. **Design API.** REST endpoints, request/response schemas, batching.
4. **Add validation.** Input schema validation, output sanity checks.
5. **Implement caching.** Feature store, prediction cache for duplicate requests.
6. **Set up monitoring.** Latency, throughput, error rate, data drift.
7. **Plan scaling.** Horizontal (more instances), vertical (bigger GPU), autoscaling.
8. **Add A/B testing.** Shadow mode, canary deployment, traffic splitting.

## Output Format

### Model Deployment: [Model Name]

**Framework:** FastAPI + Docker  
**Model:** XGBoost 1.7  
**Throughput:** 1000 req/s  
**Latency:** p95 < 50ms  
**Scaling:** HPA 2-10 pods @ 70% CPU  
**Monitoring:** Prometheus + Grafana

---

## FastAPI Serving (Lightweight)

### Model Packaging
```python
# model.py
import joblib
import numpy as np
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    user_id: str
    features: dict

class PredictionResponse(BaseModel):
    user_id: str
    prediction: float
    probability: float
    model_version: str

class Model:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)
        self.version = "1.2.0"
    
    def preprocess(self, features: dict) -> np.ndarray:
        """Convert features dict to model input"""
        feature_vector = np.array([
            features['age'],
            features['income'],
            features['tenure_months']
        ]).reshape(1, -1)
        return feature_vector
    
    def predict(self, features: dict) -> dict:
        X = self.preprocess(features)
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0][1]
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'model_version': self.version
        }

# Load model at startup
model = Model('models/churn_model.pkl')
```

### FastAPI Application
```python
# app.py
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI(title="ML Model API", version="1.0")

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health_check():
    """K8s health check"""
    return {"status": "healthy", "model_version": model.version}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Make prediction"""
    start = time.time()
    
    try:
        result = model.predict(request.features)
        latency = (time.time() - start) * 1000
        
        return PredictionResponse(
            user_id=request.user_id,
            prediction=result['prediction'],
            probability=result['probability'],
            model_version=result['model_version']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch")
def predict_batch(requests: list[PredictionRequest]):
    """Batch predictions"""
    results = []
    for req in requests:
        result = model.predict(req.features)
        results.append(PredictionResponse(
            user_id=req.user_id,
            **result
        ))
    return results
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
scikit-learn==1.3.2
joblib==1.3.2
prometheus-fastapi-instrumentator==6.1.0
```

---

## TorchServe (PyTorch Models)

### Model Handler
```python
# handler.py
import torch
from ts.torch_handler.base_handler import BaseHandler

class ChurnHandler(BaseHandler):
    def initialize(self, context):
        """Load model"""
        self.manifest = context.manifest
        properties = context.system_properties
        model_dir = properties.get("model_dir")
        
        # Load PyTorch model
        self.model = torch.jit.load(f"{model_dir}/model.pt")
        self.model.eval()
        
        self.initialized = True
    
    def preprocess(self, data):
        """Convert input to tensor"""
        # data is list of requests
        features = []
        for row in data:
            body = row.get("body") or row.get("data")
            features.append([
                body['age'],
                body['income'],
                body['tenure_months']
            ])
        
        return torch.tensor(features, dtype=torch.float32)
    
    def inference(self, data):
        """Run model"""
        with torch.no_grad():
            output = self.model(data)
        return output
    
    def postprocess(self, data):
        """Format output"""
        probabilities = torch.softmax(data, dim=1)
        predictions = probabilities.argmax(dim=1)
        
        return [
            {
                'prediction': int(pred),
                'probability': float(prob[1])
            }
            for pred, prob in zip(predictions, probabilities)
        ]
```

### Package Model
```bash
# Create MAR (Model Archive)
torch-model-archiver \
  --model-name churn_model \
  --version 1.0 \
  --serialized-file model.pt \
  --handler handler.py \
  --export-path model-store/

# Start TorchServe
torchserve \
  --start \
  --model-store model-store \
  --models churn=churn_model.mar \
  --ncs
```

### Predict
```bash
curl -X POST http://localhost:8080/predictions/churn \
  -H "Content-Type: application/json" \
  -d '{"age": 35, "income": 75000, "tenure_months": 24}'
```

---

## Model Versioning

### MLflow Model Registry
```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_uri = "runs:/abc123/model"
mlflow.register_model(model_uri, "churn_model")

# Promote to production
client.transition_model_version_stage(
    name="churn_model",
    version=3,
    stage="Production"
)

# Load production model
model = mlflow.pyfunc.load_model("models:/churn_model/Production")
```

### API Versioning
```python
from fastapi import FastAPI

app = FastAPI()

# v1 endpoint (old model)
@app.post("/v1/predict")
def predict_v1(request: PredictionRequest):
    model_v1 = load_model("v1")
    return model_v1.predict(request)

# v2 endpoint (new model)
@app.post("/v2/predict")
def predict_v2(request: PredictionRequest):
    model_v2 = load_model("v2")
    return model_v2.predict(request)
```

---

## Input Validation

```python
from pydantic import BaseModel, Field, validator

class ChurnFeatures(BaseModel):
    age: int = Field(..., ge=18, le=100, description="User age")
    income: float = Field(..., gt=0, description="Annual income")
    tenure_months: int = Field(..., ge=0, description="Months as customer")
    
    @validator('income')
    def validate_income(cls, v):
        if v > 1_000_000:
            raise ValueError('Income suspiciously high')
        return v
    
    @validator('tenure_months')
    def validate_tenure(cls, v):
        if v > 600:  # 50 years
            raise ValueError('Tenure suspiciously long')
        return v

class PredictionRequest(BaseModel):
    user_id: str
    features: ChurnFeatures

# FastAPI automatically validates
@app.post("/predict")
def predict(request: PredictionRequest):
    # request.features is guaranteed valid
    ...
```

---

## Caching

### Feature Store Integration
```python
import redis

cache = redis.Redis(host='redis', port=6379)

@app.post("/predict")
def predict(request: PredictionRequest):
    # Check cache
    cache_key = f"features:{request.user_id}"
    cached = cache.get(cache_key)
    
    if cached:
        features = json.loads(cached)
    else:
        # Fetch from feature store
        features = fetch_features(request.user_id)
        cache.setex(cache_key, 300, json.dumps(features))
    
    return model.predict(features)
```

### Prediction Cache
```python
@app.post("/predict")
def predict(request: PredictionRequest):
    # Cache predictions for duplicate requests
    cache_key = f"pred:{hash(json.dumps(request.features))}"
    cached = cache.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    prediction = model.predict(request.features)
    cache.setex(cache_key, 60, json.dumps(prediction))
    
    return prediction
```

---

## Batch Prediction

```python
@app.post("/predict/batch")
async def predict_batch(requests: list[PredictionRequest]):
    """Vectorized prediction for efficiency"""
    
    # Convert to numpy array (batch processing)
    features_matrix = np.array([
        [r.features.age, r.features.income, r.features.tenure_months]
        for r in requests
    ])
    
    # Single model call for all predictions
    predictions = model.predict_proba(features_matrix)
    
    return [
        PredictionResponse(
            user_id=req.user_id,
            prediction=int(pred > 0.5),
            probability=float(pred[1])
        )
        for req, pred in zip(requests, predictions)
    ]
```

---

## Monitoring

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram, Gauge

prediction_counter = Counter(
    'predictions_total',
    'Total predictions made',
    ['model_version', 'outcome']
)

prediction_latency = Histogram(
    'prediction_latency_seconds',
    'Prediction latency',
    ['model_version']
)

model_score_distribution = Histogram(
    'prediction_score',
    'Distribution of prediction scores',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

@app.post("/predict")
def predict(request: PredictionRequest):
    start = time.time()
    
    result = model.predict(request.features)
    
    # Track metrics
    prediction_counter.labels(
        model_version=model.version,
        outcome='churn' if result['prediction'] == 1 else 'no_churn'
    ).inc()
    
    prediction_latency.labels(model_version=model.version).observe(
        time.time() - start
    )
    
    model_score_distribution.observe(result['probability'])
    
    return result
```

### Grafana Dashboard Queries
```promql
# Predictions per second
rate(predictions_total[5m])

# P95 latency
histogram_quantile(0.95, rate(prediction_latency_seconds_bucket[5m]))

# Error rate
rate(predictions_total{outcome="error"}[5m]) / rate(predictions_total[5m])

# Score distribution shift (drift detection)
histogram_quantile(0.5, rate(prediction_score_bucket[1h]))
```

---

## A/B Testing

### Traffic Splitting
```python
import random

@app.post("/predict")
def predict(request: PredictionRequest):
    # 90% traffic to v1, 10% to v2
    if random.random() < 0.9:
        model = model_v1
        version = "v1"
    else:
        model = model_v2
        version = "v2"
    
    result = model.predict(request.features)
    result['model_version'] = version
    
    # Log for analysis
    log_prediction(request, result, version)
    
    return result
```

### Shadow Mode
```python
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Serve v1 (production)
    result_v1 = model_v1.predict(request.features)
    
    # Shadow call to v2 (log only, don't serve)
    async def shadow_predict():
        result_v2 = model_v2.predict(request.features)
        log_shadow_prediction(request, result_v2, "v2")
    
    asyncio.create_task(shadow_predict())
    
    return result_v1
```

---

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: model
        image: ml-model:1.2.0
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Rules

- Model must be versioned — track which model version served each prediction for debugging.
- Input validation is mandatory — prevent invalid inputs from causing errors or bad predictions.
- Health check endpoint required — K8s needs /health for liveness/readiness probes.
- Latency p95 < 100ms for online serving — users won't wait longer.
- Batch predictions for throughput > 100 req/s — vectorization is 10-100x faster than loops.
- Cache features when possible — avoid repeated database queries for same user.
- Monitor prediction distribution — sudden shifts indicate data drift.
- Shadow mode before full deployment — validate new model without affecting users.
- Rollback plan required — be able to revert to previous model version in < 5 minutes.
- Never load model on every request — load once at startup, cache in memory.
