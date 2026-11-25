---
name: observability-otel-collector-helm
category: observability
description: "OTel Collector Helm Chart 패턴 — Kubernetes 환경별 OTel Collector 배포, ArgoCD 통합, TLS/인증 설정 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# OTel Collector Helm Chart 패턴

Kubernetes 환경별 OTel Collector 배포, ArgoCD 통합, TLS/인증 설정

## Quick Reference

```
OTel Collector Helm chart (v0.147.1, 2026-03)
    │
    ├─ mode: deployment ──> Gateway (OTLP 수신 → 백엔드 전송)
    │   - HPA 가능, replicas 설정
    │   - Cluster-level 수집 (clusterMetrics, kubernetesEvents)
    │
    ├─ mode: daemonset ───> Agent (노드별 수집)
    │   - 노드당 1 Pod
    │   - Host/kubelet 메트릭, 컨테이너 로그
    │
    └─ mode: statefulset ─> Stateful (persistent queue 등)
```

---

## Helm Chart 기본 정보

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm install otel-collector open-telemetry/opentelemetry-collector \
  --set image.repository="otel/opentelemetry-collector-k8s" \
  --set mode=deployment
```

| 항목 | 값 |
|------|-----|
| Chart | `opentelemetry-collector` |
| 최신 버전 | 0.147.1 (2026-03-18) |
| appVersion | 0.147.0 |
| 이미지 | `otel/opentelemetry-collector-k8s` (contrib 포함) |
| `mode` | **필수** — `deployment`, `daemonset`, `statefulset` |

---

## 환경별 Values 패턴

### 디렉토리 구조

```
Goti-k8s/
  values-stacks/
    dev/
      otel-collector-front-values.yaml   # Front Collector (app → Kafka)
      otel-collector-back-values.yaml    # Back Collector (Kafka → backends)
    prod/
      otel-collector-front-values.yaml
      otel-collector-back-values.yaml
```

### Front Collector — dev (App → Kafka + Mimir)

```yaml
# otel-collector-front-values.yaml (dev)
image:
  repository: otel/opentelemetry-collector-k8s
mode: deployment
replicaCount: 1

presets:
  kubernetesAttributes:
    enabled: true

config:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318

  processors:
    memory_limiter:
      check_interval: 1s
      limit_mib: 400
      spike_limit_mib: 100

    attributes/env:
      actions:
        - key: deployment.environment
          value: dev
          action: upsert
        - key: service.namespace
          value: goti
          action: upsert

    batch:
      timeout: 5s
      send_batch_size: 1024

  exporters:
    # Metrics → Mimir 직접 (Kafka 불필요)
    otlphttp/mimir:
      endpoint: http://mimir-nginx.monitoring.svc:80/otlp

    # Traces → Kafka 버퍼
    kafka/traces:
      brokers:
        - goti-kafka-bootstrap.kafka.svc:9092
      topic: observability.traces.v1
      encoding: otlp_proto
      protocol_version: "3.6.0"
      required_acks: 1
      compression: zstd
      producer:
        max_message_bytes: 2000000
      sending_queue:
        enabled: true
        queue_size: 5000
      retry_on_failure:
        enabled: true
        initial_interval: 5s
        max_interval: 30s

    # Logs → Kafka 버퍼
    kafka/logs:
      brokers:
        - goti-kafka-bootstrap.kafka.svc:9092
      topic: observability.logs.v1
      encoding: otlp_proto
      protocol_version: "3.6.0"
      required_acks: 1
      compression: lz4
      producer:
        max_message_bytes: 2000000
      sending_queue:
        enabled: true
        queue_size: 10000

  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, attributes/env, batch]
        exporters: [kafka/traces]
      metrics:
        receivers: [otlp]
        processors: [memory_limiter, attributes/env, batch]
        exporters: [otlphttp/mimir]
      logs:
        receivers: [otlp]
        processors: [memory_limiter, attributes/env, batch]
        exporters: [kafka/logs]

resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

ports:
  metrics:
    enabled: true
    containerPort: 8888
    servicePort: 8888

serviceMonitor:
  enabled: true
  extraLabels:
    release: kube-prometheus-stack
```

### Back Collector — dev (Kafka → Tempo + Loki)

```yaml
# otel-collector-back-values.yaml (dev)
image:
  repository: otel/opentelemetry-collector-k8s
mode: deployment
replicaCount: 1

config:
  receivers:
    kafka/traces:
      brokers:
        - goti-kafka-bootstrap.kafka.svc:9092
      topic: observability.traces.v1
      encoding: otlp_proto
      protocol_version: "3.6.0"
      group_id: otel-backend-traces
      initial_offset: latest
      session_timeout: 30s
      heartbeat_interval: 10s

    kafka/logs:
      brokers:
        - goti-kafka-bootstrap.kafka.svc:9092
      topic: observability.logs.v1
      encoding: otlp_proto
      protocol_version: "3.6.0"
      group_id: otel-backend-logs
      initial_offset: latest
      session_timeout: 30s
      heartbeat_interval: 10s

  processors:
    memory_limiter:
      check_interval: 1s
      limit_mib: 800
      spike_limit_mib: 200

    # Tail Sampling (traces)
    tail_sampling:
      decision_wait: 5s
      num_traces: 50000
      policies:
        - name: errors
          type: status_code
          status_code:
            status_codes: [ERROR]
        - name: slow-requests
          type: latency
          latency:
            threshold_ms: 500
        - name: probabilistic
          type: probabilistic
          probabilistic:
            sampling_percentage: 100   # dev: 100%

    # PII 마스킹 (logs)
    transform/pii:
      log_statements:
        - context: log
          statements:
            - replace_pattern(body, "01[016789][- ]?\\d{3,4}[- ]?(\\d{4})", "010-****-$$1")

    batch/traces:
      timeout: 5s
      send_batch_size: 2048

    batch/logs:
      timeout: 5s
      send_batch_size: 1024

  exporters:
    otlp/tempo:
      endpoint: tempo.monitoring.svc:4317
      tls:
        insecure: true

    otlphttp/loki:
      endpoint: http://loki.monitoring.svc:3100/otlp

  service:
    pipelines:
      traces:
        receivers: [kafka/traces]
        processors: [memory_limiter, tail_sampling, batch/traces]
        exporters: [otlp/tempo]
      logs:
        receivers: [kafka/logs]
        processors: [memory_limiter, transform/pii, batch/logs]
        exporters: [otlphttp/loki]

resources:
  requests:
    cpu: 200m
    memory: 512Mi
  limits:
    cpu: 1
    memory: 1Gi

ports:
  metrics:
    enabled: true
    containerPort: 8888

serviceMonitor:
  enabled: true
  extraLabels:
    release: kube-prometheus-stack
```

### Prod 오버레이 차이점

```yaml
# otel-collector-front-values.yaml (prod) — dev 대비 변경점만
replicaCount: 2

config:
  processors:
    attributes/env:
      actions:
        - key: deployment.environment
          value: prod           # ← dev → prod
          action: upsert

  exporters:
    kafka/traces:
      brokers:
        - goti-kafka-bootstrap.kafka.svc:9093   # TLS 포트
      auth:
        sasl:
          mechanism: SCRAM-SHA-512
          username: otel-collector
          password: ${env:KAFKA_PASSWORD}
        tls:
          insecure: false

    kafka/logs:
      brokers:
        - goti-kafka-bootstrap.kafka.svc:9093
      auth:
        sasl:
          mechanism: SCRAM-SHA-512
          username: otel-collector
          password: ${env:KAFKA_PASSWORD}
        tls:
          insecure: false

resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 1000m
    memory: 2Gi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

# Back Collector prod 차이점
# tail_sampling: sampling_percentage: 10  (100% → 10%)
```

---

## ArgoCD Application 통합

### Multi-Source Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: otel-collector-front-dev
  namespace: argocd
spec:
  project: monitoring
  sources:
    - repoURL: https://open-telemetry.github.io/opentelemetry-helm-charts
      chart: opentelemetry-collector
      targetRevision: "0.147.1"
      helm:
        valueFiles:
          - $values/values-stacks/dev/otel-collector-front-values.yaml
    - repoURL: git@github.com:Team-Ikujo/Goti-k8s.git
      targetRevision: main
      ref: values
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## Presets

| Preset | 모드 | 설명 |
|--------|------|------|
| `kubernetesAttributes` | any | K8s 메타데이터 (pod, namespace, node) 자동 주입 |
| `logsCollection` | daemonset | 컨테이너 stdout/stderr 수집 (filelog receiver) |
| `hostMetrics` | daemonset | 노드 CPU/메모리/디스크/네트워크 |
| `kubeletMetrics` | daemonset | kubelet API에서 pod/container 메트릭 |
| `clusterMetrics` | deployment | kube-state-metrics 유사 클러스터 메트릭 |
| `kubernetesEvents` | deployment | K8s 이벤트 수집 |

Goti 구성: Front Collector는 `kubernetesAttributes`만 사용 (앱 텔레메트리 중심).

---

## ServiceMonitor 설정 (CRITICAL)

```yaml
serviceMonitor:
  enabled: true
  extraLabels:
    release: kube-prometheus-stack   # Prometheus Operator selector 매칭 필수
```

`extraLabels`에 `release: kube-prometheus-stack` 없으면 메트릭 수집 안 됨.
Alloy `prometheus.operator.servicemonitors` 대신 Prometheus/Mimir가 직접 scrape.

---

## TLS + SASL 인증 (Kafka prod)

```yaml
# Kafka exporter에 SCRAM-SHA-512 설정
exporters:
  kafka/traces:
    brokers:
      - goti-kafka-bootstrap.kafka.svc:9093
    auth:
      sasl:
        mechanism: SCRAM-SHA-512
        username: otel-collector
        password: ${env:KAFKA_PASSWORD}   # K8s Secret에서 환경변수 주입
      tls:
        insecure: false
        # Strimzi 자동 생성 CA 사용 시
        ca_file: /etc/kafka-certs/ca.crt
```

```yaml
# Helm values — 환경변수 및 볼륨 마운트
extraEnvs:
  - name: KAFKA_PASSWORD
    valueFrom:
      secretKeyRef:
        name: otel-collector   # Strimzi KafkaUser가 생성한 Secret
        key: password

extraVolumes:
  - name: kafka-certs
    secret:
      secretName: goti-kafka-cluster-ca-cert

extraVolumeMounts:
  - name: kafka-certs
    mountPath: /etc/kafka-certs
    readOnly: true
```

---

## Anti-Patterns

| 안티패턴 | 결과 | 올바른 접근 |
|---------|------|-----------|
| `mode` 미지정 | 배포 실패 | 반드시 deployment/daemonset 중 선택 |
| Front/Back을 하나의 Collector에 합치기 | Kafka 소비자가 OTLP 수신과 리소스 경합 | 별도 Helm release로 분리 |
| `extraLabels` 미설정 | ServiceMonitor 매칭 불가, self-monitoring 안 됨 | `release: kube-prometheus-stack` |
| prod에서 `tls.insecure: true` | 평문 통신 | TLS + SASL 필수 |
| Back Collector replicas > Kafka partitions | 일부 pod idle (파티션 할당 불가) | replicas ≤ partitions |
| `image.repository` 미지정 | 기본 core collector (contrib 없음) | `otel/opentelemetry-collector-k8s` |
| Helm array override 시 부분 지정 | 배열 전체 교체됨 (merge 아님) | 전체 배열 명시 |

---

## 체크리스트

### 설치
- [ ] Helm repo 추가 (`open-telemetry`)
- [ ] `image.repository: otel/opentelemetry-collector-k8s` 설정 (contrib)
- [ ] `mode` 설정 (front: deployment, back: deployment)
- [ ] ServiceMonitor `extraLabels` 설정

### 환경별
- [ ] dev values 작성 (plaintext Kafka, filesystem)
- [ ] prod values 작성 (TLS+SASL Kafka, S3)
- [ ] 환경별 `deployment.environment` attribute 설정

### ArgoCD
- [ ] Application multi-source 설정
- [ ] targetRevision 고정 (chart version)
- [ ] syncPolicy 설정 (automated + prune + selfHeal)

---

## 참조 스킬

- `/observability-alloy-to-otel` — Alloy → OTel 마이그레이션
- `/observability-otel-optimization` — Kafka 버퍼, Strimzi 토픽 설정
- `/observability-mimir-monolithic` — Mimir 싱글바이너리
- `/observability-otel-scale` — 대규모 트래픽 스케일링
