---
name: golden-paths-infra
category: platform
description: "Golden Paths: Infrastructure & CI/CD — Infrastructure 템플릿, CI/CD 파이프라인, Observability 기본값 Use when working with platform 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Golden Paths: Infrastructure & CI/CD

Infrastructure 템플릿, CI/CD 파이프라인, Observability 기본값

## Quick Reference

```
Infrastructure 템플릿?
    │
    ├─ Database ─────────> Terraform RDS/CloudSQL 모듈
    ├─ Cache ────────────> ElastiCache/Redis 모듈
    └─ Queue ────────────> SQS/Kafka 설정

CI/CD 파이프라인?
    │
    ├─ Build ────────────> 빌드, 테스트
    ├─ Security ─────────> SAST, SCA, 이미지 스캔
    └─ Deploy ───────────> ArgoCD 트리거
```

---

## Infrastructure Templates

### Database Provisioning

```hcl
# terraform/modules/database/main.tf

variable "service_name" {
  description = "Service name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "tier" {
  description = "Service tier"
  type        = string
  default     = "tier-2"
}

variable "instance_class" {
  description = "Instance class based on tier"
  type        = map(string)
  default = {
    "tier-1" = "db.r6g.xlarge"
    "tier-2" = "db.r6g.large"
    "tier-3" = "db.t4g.medium"
  }
}

resource "aws_db_instance" "main" {
  identifier = "${var.service_name}-${var.environment}"

  engine         = "postgresql"
  engine_version = "15.4"
  instance_class = var.instance_class[var.tier]

  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_encrypted     = true

  multi_az               = var.environment == "prod"
  deletion_protection    = var.environment == "prod"
  skip_final_snapshot    = var.environment != "prod"

  performance_insights_enabled = true
  monitoring_interval          = 60

  tags = {
    Service     = var.service_name
    Environment = var.environment
    ManagedBy   = "terraform"
    GoldenPath  = "true"
  }
}
```

### Cache Provisioning

```hcl
# terraform/modules/cache/main.tf

resource "aws_elasticache_replication_group" "main" {
  replication_group_id = "${var.service_name}-${var.environment}"
  description          = "Redis cache for ${var.service_name}"

  engine               = "redis"
  engine_version       = "7.0"
  node_type            = var.environment == "prod" ? "cache.r6g.large" : "cache.t4g.medium"
  num_cache_clusters   = var.environment == "prod" ? 2 : 1

  automatic_failover_enabled = var.environment == "prod"
  multi_az_enabled          = var.environment == "prod"

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true

  tags = {
    Service     = var.service_name
    Environment = var.environment
    GoldenPath  = "true"
  }
}
```

### Queue Provisioning

```hcl
# terraform/modules/sqs/main.tf

resource "aws_sqs_queue" "main" {
  name = "${var.service_name}-${var.environment}"

  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 1209600  # 14 days
  receive_wait_time_seconds = 20       # Long polling

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 5
  })

  tags = {
    Service     = var.service_name
    Environment = var.environment
    GoldenPath  = "true"
  }
}

resource "aws_sqs_queue" "dlq" {
  name = "${var.service_name}-${var.environment}-dlq"

  message_retention_seconds = 1209600

  tags = {
    Service     = var.service_name
    Environment = var.environment
    Type        = "DLQ"
  }
}
```

---

## CI/CD Pipeline Templates

### GitHub Actions CI

```yaml
# .github/workflows/ci.yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: 'gradle'

      - name: Build
        run: ./gradlew build

      - name: Test
        run: ./gradlew test

      - name: Upload coverage
        uses: codecov/codecov-action@v4

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'

      - name: Run Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: p/ci

  docker:
    needs: [build, security]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
```

### Go CI Pipeline

```yaml
# .github/workflows/ci-go.yaml
name: Go CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
          cache: true

      - name: Build
        run: go build -v ./...

      - name: Test
        run: go test -v -race -coverprofile=coverage.out ./...

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.out

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'

      - name: golangci-lint
        uses: golangci/golangci-lint-action@v4
        with:
          version: latest
```

---

## Observability Defaults

### Grafana Dashboard Template

```json
{
  "title": "${service_name} Dashboard",
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "query": "label_values(namespace)"
      }
    ]
  },
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [{
        "expr": "sum(rate(http_server_requests_seconds_count{namespace=\"$namespace\"}[5m]))"
      }]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [{
        "expr": "sum(rate(http_server_requests_seconds_count{namespace=\"$namespace\",status=~\"5..\"}[5m])) / sum(rate(http_server_requests_seconds_count{namespace=\"$namespace\"}[5m]))"
      }]
    },
    {
      "title": "P99 Latency",
      "type": "timeseries",
      "targets": [{
        "expr": "histogram_quantile(0.99, sum(rate(http_server_requests_seconds_bucket{namespace=\"$namespace\"}[5m])) by (le))"
      }]
    }
  ]
}
```

### Prometheus Alerts

```yaml
# prometheus/alerts.yaml
groups:
  - name: ${service_name}-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_server_requests_seconds_count{namespace="${namespace}",status=~"5.."}[5m]))
          / sum(rate(http_server_requests_seconds_count{namespace="${namespace}"}[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
          service: ${service_name}
        annotations:
          summary: "High error rate for ${service_name}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, sum(rate(http_server_requests_seconds_bucket{namespace="${namespace}"}[5m])) by (le)) > 1
        for: 10m
        labels:
          severity: warning
          service: ${service_name}
```

### Helm Values Defaults

```yaml
# helm/values.yaml
replicaCount: 2

image:
  repository: ghcr.io/myorg/${service_name}
  pullPolicy: IfNotPresent
  tag: ""

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

podDisruptionBudget:
  enabled: true
  minAvailable: 1

serviceAccount:
  create: true
  annotations:
    eks.amazonaws.com/role-arn: ${iam_role_arn}

probes:
  liveness:
    httpGet:
      path: /health/live
      port: http
    initialDelaySeconds: 15
  readiness:
    httpGet:
      path: /health/ready
      port: http
    initialDelaySeconds: 5

metrics:
  enabled: true
  serviceMonitor:
    enabled: true
```

---

## 체크리스트

### Infrastructure
- [ ] Database 모듈 (RDS/CloudSQL)
- [ ] Cache 모듈 (ElastiCache/Redis)
- [ ] Queue 모듈 (SQS/Kafka)
- [ ] IAM 역할/정책

### CI/CD
- [ ] 빌드 파이프라인
- [ ] 테스트 자동화
- [ ] 보안 스캔 (SAST, SCA)
- [ ] 이미지 빌드/푸시
- [ ] ArgoCD 트리거

### Observability
- [ ] Grafana 대시보드 템플릿
- [ ] Prometheus 알림 규칙
- [ ] Helm values 기본값
- [ ] ServiceMonitor 설정

**관련 skill**: `/golden-paths` (원칙, 서비스 템플릿), `/gitops-argocd`, `/cicd-devsecops`

---

## Sources

- [What are Golden Paths](https://platformengineering.org/blog/what-are-golden-paths-a-guide-to-streamlining-developer-workflows)
- [Designing Golden Paths - Red Hat](https://www.redhat.com/en/blog/designing-golden-paths)
- [Golden Paths - Google Cloud](https://cloud.google.com/blog/products/application-development/golden-paths-for-engineering-execution-consistency)
- [AWS IDP Examples](https://docs.aws.amazon.com/prescriptive-guidance/latest/internal-developer-platform/examples.html)
