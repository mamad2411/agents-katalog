---
name: seldon-core
description: Seldon Core v2 patterns for Kubernetes-native ML model serving — SeldonDeployment CRD, canary rollouts, REST/gRPC, Istio integration, autoscaling, and custom Python servers.
origin: custom
---

# Seldon Core Patterns

Production ML model serving on Kubernetes using Seldon Core v2.

## When to Activate

- Deploying ML models to Kubernetes
- Setting up canary or shadow deployments for models
- Integrating model serving with Istio service mesh
- Configuring autoscaling for inference workloads
- Building multi-step inference pipelines (pre/post-processing + model)

## SeldonDeployment CRD — sklearn Server

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: iris-classifier
  namespace: ml-serving          # ✅ dedicated namespace
  labels:
    app: iris-classifier
    team: ml
    env: prod
spec:
  name: iris
  predictors:
    - name: default
      replicas: 2
      graph:
        name: classifier
        implementation: SKLEARN_SERVER
        modelUri: s3://my-bucket/models/iris/v1/
        envSecretRefName: seldon-s3-secret   # ✅ secrets via K8s Secret
      componentSpecs:
        - spec:
            containers:
              - name: classifier
                resources:
                  requests:
                    memory: "512Mi"
                    cpu: "500m"
                  limits:
                    memory: "1Gi"
                    cpu: "1"
                readinessProbe:
                  httpGet:
                    path: /health/status
                    port: 9000
                  initialDelaySeconds: 10
                  periodSeconds: 5
                livenessProbe:
                  httpGet:
                    path: /health/ping
                    port: 9000
                  initialDelaySeconds: 30
                  periodSeconds: 10
      traffic: 90               # ✅ 90% stable

    - name: canary
      replicas: 1
      graph:
        name: classifier-v2
        implementation: SKLEARN_SERVER
        modelUri: s3://my-bucket/models/iris/v2/
        envSecretRefName: seldon-s3-secret
      componentSpecs:
        - spec:
            containers:
              - name: classifier-v2
                resources:
                  requests:
                    memory: "512Mi"
                    cpu: "500m"
                  limits:
                    memory: "1Gi"
                    cpu: "1"
      traffic: 10               # ✅ 10% canary
```

## Custom Python Model Server

```python
# src/MyModel.py — Seldon microservice interface
import joblib
import numpy as np
from typing import List, Dict, Any


class MyModel:
    """Custom Seldon Core Python model server."""

    def __init__(self) -> None:
        self.model = joblib.load("/mnt/models/model.pkl")
        self.ready = True

    def predict(
        self,
        X: np.ndarray,
        features_names: List[str] | None = None,
        meta: Dict[str, Any] | None = None,
    ) -> np.ndarray:
        return self.model.predict_proba(X)

    def health_status(self) -> Dict[str, str]:
        return {"status": "ok", "model_loaded": str(self.ready)}

    def metadata(self) -> Dict[str, Any]:
        return {
            "name": "fraud-detector",
            "versions": ["v2"],
            "platform": "seldon",
            "inputs": [{"name": "input", "datatype": "FP32", "shape": [-1, 30]}],
            "outputs": [{"name": "output", "datatype": "FP32", "shape": [-1, 2]}],
        }
```

```yaml
# SeldonDeployment with custom Python server
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: fraud-detector
  namespace: ml-serving
spec:
  predictors:
    - name: default
      replicas: 2
      graph:
        name: fraud-model
        implementation: SKLEARN_SERVER
        modelUri: s3://my-bucket/models/fraud/v2/
      componentSpecs:
        - spec:
            containers:
              - name: fraud-model
                image: my-registry/fraud-detector:v2.1.0   # pinned — never :latest
                env:
                  - name: PREDICTIVE_UNIT_SERVICE_PORT
                    value: "9000"
                  - name: MODEL_VERSION
                    value: "v2"
                volumeMounts:
                  - name: model-store
                    mountPath: /mnt/models
            volumes:
              - name: model-store
                emptyDir: {}
      traffic: 100
```

## Multi-Step Inference Pipeline

```yaml
# Preprocessing → Model → Postprocessing
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: fraud-pipeline
  namespace: ml-serving
spec:
  predictors:
    - name: default
      graph:
        name: preprocessor
        implementation: CUSTOM_SERVER
        modelUri: s3://my-bucket/models/preprocessor/
        children:
          - name: fraud-model
            implementation: SKLEARN_SERVER
            modelUri: s3://my-bucket/models/fraud/v2/
            children:
              - name: postprocessor
                implementation: CUSTOM_SERVER
                modelUri: s3://my-bucket/models/postprocessor/
```

## REST & gRPC Endpoints

```bash
# REST prediction
curl -X POST \
  http://<ingress-ip>/seldon/ml-serving/iris-classifier/api/v1.0/predictions \
  -H "Content-Type: application/json" \
  -d '{"data": {"ndarray": [[5.1, 3.5, 1.4, 0.2]]}}'

# V2 inference protocol (REST)
curl -X POST \
  http://<ingress-ip>/v2/models/iris-classifier/infer \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [{
      "name": "input",
      "shape": [1, 4],
      "datatype": "FP32",
      "data": [[5.1, 3.5, 1.4, 0.2]]
    }]
  }'

# gRPC prediction
grpcurl \
  -d '{"data": {"ndarray": [[5.1, 3.5, 1.4, 0.2]]}}' \
  -plaintext <ingress-ip>:80 \
  seldon.protos.Seldon/Predict
```

## Istio Integration (Helm values)

```yaml
# values-seldon.yaml
istio:
  enabled: true
  gateway: istio-system/seldon-gateway

executor:
  requestLogger:
    enabled: true
    defaultEndpoint: "http://broker-ingress.knative-eventing.svc.cluster.local/default/seldon"

ambassador:
  enabled: false

certManager:
  enabled: true
```

```bash
# Install Seldon Core with Istio
helm repo add seldonio https://storage.googleapis.com/seldon-charts
helm upgrade --install seldon-core seldonio/seldon-core-operator \
  --namespace seldon-system \
  --create-namespace \
  -f values-seldon.yaml \
  --version 1.17.1
```

## HPA Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: iris-classifier-hpa
  namespace: ml-serving
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: iris-classifier-default-0-classifier
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

## Kubernetes Secret for S3

```bash
kubectl create secret generic seldon-s3-secret \
  --from-literal=AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) \
  --from-literal=AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key) \
  --from-literal=AWS_DEFAULT_REGION=us-east-1 \
  -n ml-serving
```

## Monitoring — Prometheus Annotations

```yaml
# Add to SeldonDeployment componentSpec pod template
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/path: "/prometheus"
  prometheus.io/port: "6000"
```

## Best Practices

| Practice | Detail |
|----------|--------|
| ✅ Separate namespace | Isolate `ml-serving` from application workloads |
| ✅ Canary rollout | Always split traffic 90/10 before full promotion |
| ✅ Istio integration | mTLS, distributed tracing, traffic management |
| ✅ Autoscaling | HPA on CPU/memory; KEDA for queue-based scaling |
| ✅ Resource limits | Always set `requests` and `limits` on every container |
| ✅ Health checks | `readinessProbe` + `livenessProbe` on every predictor |
| ✅ Pinned image tags | Never `:latest` — use `v2.1.0` |
| ✅ Secrets via K8s Secret | Use `envSecretRefName`, never plain env vars |

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| ❌ Direct 100% deploy to prod | Use `traffic` split (canary) always |
| ❌ Shared namespace with apps | Dedicated `ml-serving` namespace |
| ❌ No resource limits | OOMKilled in prod; always set limits |
| ❌ Secrets in env vars in YAML | Use `envSecretRefName` pointing to K8s Secret |
| ❌ `:latest` image tag | Pin to exact version e.g. `v2.1.0` |
| ❌ No health checks | Add `readinessProbe` and `livenessProbe` |

