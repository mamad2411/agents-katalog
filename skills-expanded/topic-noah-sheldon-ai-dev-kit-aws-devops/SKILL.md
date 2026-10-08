---
name: aws-devops
description: AWS DevOps — ECS, Lambda, Docker, Kubernetes, ArgoCD, GitHub Actions, Jenkins, Ansible, CI/CD pipelines, IaC, monitoring, cost optimization, and security.
origin: AI Dev Kit
---

# AWS DevOps

Production-grade AWS and DevOps practices: container orchestration with ECS and Kubernetes, serverless with Lambda, container security, CI/CD pipelines with GitHub Actions and Jenkins, infrastructure-as-code, monitoring, cost optimization, and security hardening.

## When to Use

- Deploying containerized applications on AWS with ECS or EKS
- Building serverless functions with Lambda and optimizing for cold starts
- Designing CI/CD pipelines with automated testing, scanning, and deployment gates
- Managing infrastructure with Terraform, CloudFormation, or AWS CDK
- Implementing GitOps with ArgoCD for Kubernetes deployments
- Configuring Ansible for idempotent server provisioning
- Monitoring applications with CloudWatch, X-Ray, and alerting
- Optimizing AWS costs and enforcing security best practices

## Core Concepts

### 1. ECS: Fargate vs EC2

**Fargate Task Definition** (serverless containers):

```json
{
  "family": "rag-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::123456789:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789:role/ragApiTaskRole",
  "containerDefinitions": [
    {
      "name": "rag-api",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/rag-api:v2.3.0",
      "portMappings": [{ "containerPort": 8000, "protocol": "tcp" }],
      "environment": [
        { "name": "LOG_LEVEL", "value": "info" },
        { "name": "VECTOR_DB_URL", "value": "https://pinecone-endpoint" }
      ],
      "secrets": [
        { "name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:rag-api-keys:OPENAI_API_KEY::" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/rag-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

**Autoscaling with Target Tracking**:

```python
# Using boto3 to configure autoscaling
import boto3

appautoscaling = boto3.client("application-autoscaling")

# Register scalable target
appautoscaling.register_scalable_target(
    ServiceNamespace="ecs",
    ResourceId="service/rag-cluster/rag-api",
    ScalableDimension="ecs:service:DesiredCount",
    MinCapacity=2,
    MaxCapacity=20,
)

# Target tracking policy on CPU
appautoscaling.put_scaling_policy(
    ServiceNamespace="ecs",
    ResourceId="service/rag-cluster/rag-api",
    ScalableDimension="ecs:service:DesiredCount",
    PolicyName="rag-api-cpu-tracking",
    PolicyType="TargetTrackingScaling",
    TargetTrackingScalingPolicyConfiguration={
        "TargetValue": 60.0,  # Target 60% CPU utilization
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
        },
        "ScaleInCooldown": 300,
        "ScaleOutCooldown": 60,
    },
)
```

**Fargate vs EC2 Decision Matrix**:

| Criteria | Fargate | EC2 |
|----------|---------|-----|
| **Management** | Serverless, no EC2 provisioning | Self-managed instances |
| **Cost** | Pay per vCPU/memory-hour | Pay per instance (cheaper at scale) |
| **Startup** | ~2-3s cold start | Instant (warm pool) |
| **Custom kernels** | No | Yes (GPU, custom networking) |
| **Best for** | Microservices, variable workloads | High-throughput, GPU, steady-state |

### 2. Lambda: Serverless Functions

**Function Design with Layers**:

```python
# lambda_function.py
import json
import os
import logging
from openai import OpenAI
from embedding_layer import get_embedding  # from Lambda Layer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connection pooling — reuse client across invocations
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def handler(event, context):
    """Lambda handler for RAG query endpoint."""
    logger.info(f"Received event: {json.dumps(event, indent=2)}")

    try:
        body = json.loads(event["body"])
        query = body["query"]
        top_k = body.get("top_k", 5)

        # Retrieve and respond
        response = process_rag_query(query, top_k)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response),
        }
    except Exception as e:
        logger.exception("Error processing RAG query")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
        }

def process_rag_query(query: str, top_k: int) -> dict:
    """Process a RAG query with embedding retrieval and LLM generation."""
    embedding = get_embedding(query)
    # ... retrieval and generation logic
    return {"answer": "...", "sources": [...]}
```

**Cold Start Optimization**:

```python
# Global scope initialization (runs once per container, not per invocation)
import boto3
import httpx

# Reuse connections across invocations
http_client = httpx.Client()
s3_client = boto3.client("s3")

# Preload model/cache during init
embedding_cache = {}
MODEL = None

def warm_cache():
    """Called during cold start to preload resources."""
    global MODEL
    MODEL = load_embedding_model()  # Runs only on cold start

warm_cache()  # Executed once when container starts
```

**Event Source Mapping** (SQS trigger):

```yaml
# serverless.yml
functions:
  processEmbeddings:
    handler: src/embeddings.handler
    timeout: 300
    memorySize: 1024
    layers:
      - arn:aws:lambda:us-east-1:123456789:layer:embedding-runtime:3
    events:
      - sqs:
          arn: arn:aws:sqs:us-east-1:123456789:embedding-queue
          batchSize: 10
          maximumBatchingWindow: 5
    reservedConcurrency: 50  # Limit concurrent executions
```

**Provisioned Concurrency** for latency-sensitive functions:

```hcl
resource "aws_lambda_provisioned_concurrency_config" "rag_api" {
  function_name                     = aws_lambda_function.rag_api.function_name
  provisioned_concurrent_executions = 10
  qualifier                         = aws_lambda_alias.rag_api_live.name
}
```

### 3. Docker: Production Container Builds

**Multi-Stage Build with Distroless Image**:

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY src/ ./src/
RUN python -m compileall src/

# Stage 2: Production (distroless for minimal attack surface)
FROM gcr.io/distroless/python3-debian12

WORKDIR /app
COPY --from=builder /install /usr/local
COPY --from=builder /build/src ./src

USER nonroot:nonroot
EXPOSE 8000

ENTRYPOINT ["python3", "-m", "src.main"]
```

**Layer Caching Optimization**:

```dockerfile
# Layer ordering matters — put least-changing layers first
FROM python:3.12-slim

# 1. System deps (rarely change)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

# 2. Python dependencies (change with requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Application code (changes frequently)
COPY src/ ./src/
```

**Trivy Security Scanning**:

```bash
# Scan image for vulnerabilities
trivy image 123456789.dkr.ecr.us-east-1.amazonaws.com/rag-api:v2.3.0

# CI integration — fail on CRITICAL or HIGH
trivy image --exit-code 1 --severity CRITICAL,HIGH \
  123456789.dkr.ecr.us-east-1.amazonaws.com/rag-api:v2.3.0

# Scan filesystem for misconfigurations
trivy config Dockerfile docker-compose.yml
```

### 4. Kubernetes: Production Deployments

```yaml
# Deployment with HPA
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime deployment
  template:
    metadata:
      labels:
        app: rag-api
    spec:
      containers:
        - name: rag-api
          image: 123456789.dkr.ecr.us-east-1.amazonaws.com/rag-api:v2.3.0
          ports:
            - containerPort: 8000
          resources:
            requests:
              cpu: 250m
              memory: 512Mi
            limits:
              cpu: "1"
              memory: 1Gi
          envFrom:
            - configMapRef:
                name: rag-api-config
          env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: rag-api-secrets
                  key: OPENAI_API_KEY
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: rag-api
spec:
  type: ClusterIP
  selector:
    app: rag-api
  ports:
    - port: 80
      targetPort: 8000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: rag-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: rag-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### 5. ArgoCD: GitOps Deployments

```yaml
# Application definition
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: rag-api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/rag-infra.git
    targetRevision: main
    path: k8s/production/rag-api
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
  revisionHistoryLimit: 10
```

**Sync Waves** for ordered deployment:

```yaml
# ConfigMap first (wave -1)
apiVersion: v1
kind: ConfigMap
metadata:
  name: rag-api-config
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
# Deployment (wave 0 — default)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-api
---
# Service and Ingress (wave 1 — after deployment healthy)
apiVersion: v1
kind: Service
metadata:
  name: rag-api
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

**App-of-Apps Pattern**:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: rag-platform
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/rag-infra.git
    targetRevision: main
    path: apps/rag-platform
    directory:
      recurse: true
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 6. GitHub Actions: CI/CD Pipelines

```yaml
# .github/workflows/deploy.yml
name: Build, Test, Scan, Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: 123456789.dkr.ecr.us-east-1.amazonaws.com
  IMAGE_NAME: rag-api

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - run: pip install -r requirements.txt
      - run: ruff check src/ tests/
      - run: black --check src/
      - run: mypy src/
      - run: pytest tests/ --cov=src/ --cov-report=xml --cov-fail-under=80

      - uses: actions/upload-artifact@v4
        if: matrix.python-version == '3.12'
        with:
          name: coverage-report
          path: coverage.xml

  security-scan:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          severity: CRITICAL,HIGH
          exit-code: 1
      - run: trivy fs --severity CRITICAL,HIGH --exit-code 1 .

  deploy:
    needs: [build-and-test, security-scan]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-deploy
          aws-region: us-east-1

      - name: Update ECS Task Definition
        run: |
          aws ecs update-service \
            --cluster rag-cluster \
            --service rag-api \
            --force-new-deployment

      - name: Wait for Deployment
        run: |
          aws ecs wait services-stable \
            --cluster rag-cluster \
            --services rag-api
```

### 7. Terraform: Infrastructure as Code

```hcl
# ECS cluster and service
resource "aws_ecs_cluster" "rag" {
  name = "rag-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_service" "rag_api" {
  name            = "rag-api"
  cluster         = aws_ecs_cluster.rag.id
  task_definition = aws_ecs_task_definition.rag_api.arn
  desired_count   = 3
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [aws_security_group.rag_api.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.rag_api.arn
    container_name   = "rag-api"
    container_port   = 8000
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
}

# ALB with health checks
resource "aws_lb_target_group" "rag_api" {
  name        = "rag-api-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 2
    matcher             = "200"
  }
}
```

## Anti-Patterns

- **Fat Lambda packages** — bundling all dependencies in the deployment package instead of using layers
- **No circuit breaker** — ECS deployments without `deployment_circuit_breaker` causing prolonged bad deploys
- **Hard-coded credentials** — secrets in environment variables instead of AWS Secrets Manager or Parameter Store
- **Unbounded Lambda concurrency** — no `reservedConcurrency` leading to downstream service overload
- **Single-AZ deployments** — ECS tasks or pods in one availability zone with no fault tolerance
- **No resource limits** — containers without CPU/memory requests and limits causing noisy-neighbor issues
- **Skipping image scans** — deploying containers without Trivy or ECR scan for vulnerabilities
- **Manual k8s manifests** — `kubectl apply` from developer machines instead of ArgoCD GitOps
- **No deployment health checks** — missing liveness/readiness probes causing traffic to unhealthy pods
- **Ignoring cost signals** — not using Cost Explorer, Compute Optimizer, or right-sizing recommendations

## Best Practices

1. **Use Fargate for microservices** — unless you need GPU, custom kernels, or have steady high utilization
2. **Store secrets in Secrets Manager** — reference via ARN in task definitions, never hard-code
3. **Multi-stage Docker builds** — separate build and runtime to minimize image size and attack surface
4. **Enable ECS Circuit Breaker** — automatic rollback when deployments fail health checks
5. **Set resource requests and limits** — prevent resource contention and enable accurate HPA scaling
6. **Use ArgoCD for GitOps** — declarative, auditable deployments with automatic sync and self-heal
7. **Scan images in CI** — Trivy scan on every build, block merges on CRITICAL/HIGH findings
8. **Lambda: reuse connections** — initialize HTTP clients and SDK clients outside the handler
9. **Provisioned concurrency for latency-sensitive Lambdas** — eliminate cold starts for SLA-bound functions
10. **Infrastructure as Code** — all AWS resources defined in Terraform/CDK, no console-only changes
11. **Blue-green or canary for production** — use CodeDeploy or Argo Rollouts for zero-downtime releases
12. **Tag all resources** — enforce tagging for cost allocation, ownership, and lifecycle management

## Related Skills

- **data-pipelines-ai** — deploying Airflow/Prefect and Kafka pipelines on AWS
- **observability-telemetry** — CloudWatch, X-Ray, Grafana monitoring for AWS services
- **openai-api** — production LLM API integration with proper connection pooling and error handling
- **mlops-rag** — deploying RAG systems on ECS/EKS with model versioning and A/B testing
