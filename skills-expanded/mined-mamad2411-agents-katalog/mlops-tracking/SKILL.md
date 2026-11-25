---
name: mlops-tracking
category: platform
description: "MLflow 실험 추적 가이드 — MLflow 설치, 실험 추적, 모델 레지스트리, KServe 연동 Use when working with platform 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# MLflow 실험 추적 가이드

MLflow 설치, 실험 추적, 모델 레지스트리, KServe 연동

## MLflow

### 설치 및 설정

```bash
# 설치
pip install mlflow

# 서버 실행 (로컬)
mlflow server \
  --backend-store-uri postgresql://user:pass@localhost/mlflow \
  --default-artifact-root s3://mlflow-artifacts \
  --host 0.0.0.0 \
  --port 5000

# Kubernetes 배포
helm repo add community-charts https://community-charts.github.io/helm-charts
helm install mlflow community-charts/mlflow \
  --set backendStore.postgres.enabled=true \
  --set artifactRoot.s3.enabled=true \
  --set artifactRoot.s3.bucket=mlflow-artifacts
```

### 실험 추적

```python
import mlflow
from mlflow.tracking import MlflowClient

# 트래킹 서버 설정
mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("my-experiment")

# 실험 실행
with mlflow.start_run(run_name="training-run-1"):
    # 파라미터 로깅
    mlflow.log_params({
        "learning_rate": 0.01,
        "epochs": 100,
        "batch_size": 32
    })

    # 훈련 루프
    for epoch in range(100):
        loss = train_epoch()
        accuracy = evaluate()

        # 메트릭 로깅
        mlflow.log_metrics({
            "loss": loss,
            "accuracy": accuracy
        }, step=epoch)

    # 모델 로깅
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="my-classifier"
    )

    # 추가 아티팩트
    mlflow.log_artifact("confusion_matrix.png")
```

### 모델 레지스트리

```python
from mlflow import MlflowClient

client = MlflowClient()

# 모델 버전 등록
result = client.create_model_version(
    name="my-classifier",
    source="runs:/abc123/model",
    run_id="abc123"
)

# 스테이지 전환
client.transition_model_version_stage(
    name="my-classifier",
    version=1,
    stage="Staging"
)

# Production 배포
client.transition_model_version_stage(
    name="my-classifier",
    version=1,
    stage="Production"
)

# 모델 로드 (Production)
model = mlflow.pyfunc.load_model("models:/my-classifier/Production")
predictions = model.predict(data)
```

### MLflow + KServe 연동

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: mlflow-model
spec:
  predictor:
    model:
      modelFormat:
        name: mlflow
      storageUri: "s3://mlflow-artifacts/1/abc123/artifacts/model"
```

---

## 참조 스킬

- `/mlops` - MLOps 기본 (Kubeflow, KServe)
- `/llmops` - RAG 운영, 프롬프트 관리, LLM 평가 & 가드레일
- `/ml-serving` - ML 서빙 심화
