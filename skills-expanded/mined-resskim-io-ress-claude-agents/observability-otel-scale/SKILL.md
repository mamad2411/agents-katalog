---
name: observability-otel-scale
category: observability
description: "OpenTelemetry 대규모 트래픽 설정 가이드 — 초당 수만~수십만 요청 환경을 위한 OTel Collector 스케일링, 샘플링 전략, 비용 최적화 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# OpenTelemetry 대규모 트래픽 설정 가이드

초당 수만~수십만 요청 환경을 위한 OTel Collector 스케일링, 샘플링 전략, 비용 최적화

## Quick Reference (결정 트리)

```
대규모 트래픽 OTel 아키텍처?
    |
    +-- 초당 1만 요청 미만 ----------> 단일 Collector + Head Sampling
    |
    +-- 초당 1만~10만 요청 ----------> Agent + Gateway 패턴
    |       |
    |       +-- 샘플링 ---------------> Tail-based (중요 트레이스 보존)
    |       +-- 버퍼링 ---------------> Kafka/Redis 큐
    |
    +-- 초당 10만+ 요청 -------------> 분산 Collector + Load Balancing
            |
            +-- Multi-tier ------------> Agent → Gateway → Backend
            +-- Sharding --------------> Trace ID 기반 샤딩

샘플링 전략?
    |
    +-- 비용 최적화 우선 ------------> Head Sampling (10-20%)
    +-- 에러/지연 분석 우선 ---------> Tail-based Sampling
    +-- 하이브리드 -----------------> Probabilistic + Error-based
```

---

## CRITICAL: 트래픽 규모별 아키텍처

### 소규모 (< 10K RPS)

```
App Pods ──────> OTel Collector ──────> Backend (Tempo/Jaeger)
                 (Deployment)
```

### 중규모 (10K - 100K RPS)

```
┌─────────────────────────────────────────────────────────────────┐
│  Node 1                    Node 2                    Node N     │
│  ┌─────────┐              ┌─────────┐              ┌─────────┐ │
│  │ App Pod │              │ App Pod │              │ App Pod │ │
│  └────┬────┘              └────┬────┘              └────┬────┘ │
│       │                        │                        │      │
│       ▼                        ▼                        ▼      │
│  ┌─────────┐              ┌─────────┐              ┌─────────┐ │
│  │ Agent   │              │ Agent   │              │ Agent   │ │
│  │(DaemonSet)             │(DaemonSet)             │(DaemonSet) │
│  └────┬────┘              └────┬────┘              └────┬────┘ │
└───────┼────────────────────────┼────────────────────────┼──────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │   Gateway Collector     │
                    │   (Deployment, HPA)     │
                    │   - Tail Sampling       │
                    │   - Aggregation         │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
         ┌─────────┐       ┌─────────┐       ┌─────────┐
         │  Tempo  │       │  Loki   │       │Prometheus│
         │(Traces) │       │ (Logs)  │       │(Metrics) │
         └─────────┘       └─────────┘       └─────────┘
```

### 대규모 (100K+ RPS)

```
                            ┌──────────────────┐
                            │  Load Balancer   │
                            │(Trace ID Hashing)│
                            └────────┬─────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│ Gateway Pool 1│          │ Gateway Pool 2│          │ Gateway Pool N│
│ (Shard A-F)   │          │ (Shard G-M)   │          │ (Shard N-Z)   │
└───────┬───────┘          └───────┬───────┘          └───────┬───────┘
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   ▼
                          ┌─────────────────┐
                          │      Kafka      │
                          │  (Buffer/Queue) │
                          └────────┬────────┘
                                   │
                                   ▼
                    ┌─────────────────────────┐
                    │   Backend Collector     │
                    │   - Final Processing    │
                    │   - Export to Storage   │
                    └─────────────────────────┘
```

---

## Agent Collector (DaemonSet)

### Helm 설치

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts

helm install otel-agent open-telemetry/opentelemetry-collector \
  --namespace observability \
  --create-namespace \
  -f otel-agent-values.yaml
```

### Agent 설정

```yaml
# otel-agent-values.yaml
mode: daemonset

presets:
  kubernetesAttributes:
    enabled: true
  kubeletMetrics:
    enabled: true

config:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
          max_recv_msg_size_mib: 16  # 대용량 배치 처리
        http:
          endpoint: 0.0.0.0:4318

    # Host 메트릭 수집
    hostmetrics:
      collection_interval: 30s
      scrapers:
        cpu:
        memory:
        disk:
        network:

  processors:
    # 메모리 보호
    memory_limiter:
      check_interval: 1s
      limit_mib: 400
      spike_limit_mib: 100

    # 배치 처리
    batch:
      timeout: 1s
      send_batch_size: 1024
      send_batch_max_size: 2048

    # K8s 메타데이터 추가
    k8sattributes:
      extract:
        metadata:
          - k8s.namespace.name
          - k8s.deployment.name
          - k8s.pod.name
          - k8s.node.name
      pod_association:
        - sources:
            - from: resource_attribute
              name: k8s.pod.ip

    # 리소스 속성 정리
    resource:
      attributes:
        - key: host.name
          from_attribute: k8s.node.name
          action: upsert

  exporters:
    otlp:
      endpoint: otel-gateway.observability:4317
      tls:
        insecure: true
      sending_queue:
        enabled: true
        num_consumers: 10
        queue_size: 10000
      retry_on_failure:
        enabled: true
        initial_interval: 5s
        max_interval: 30s
        max_elapsed_time: 300s

  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, k8sattributes, resource, batch]
        exporters: [otlp]
      metrics:
        receivers: [otlp, hostmetrics]
        processors: [memory_limiter, k8sattributes, resource, batch]
        exporters: [otlp]
      logs:
        receivers: [otlp]
        processors: [memory_limiter, k8sattributes, resource, batch]
        exporters: [otlp]

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 256Mi

# 각 노드에 배포
tolerations:
  - operator: Exists
```

---

## Gateway Collector (Deployment + HPA)

### Gateway 설정

```yaml
# otel-gateway-values.yaml
mode: deployment
replicaCount: 3

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

config:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
          max_recv_msg_size_mib: 32

  processors:
    memory_limiter:
      check_interval: 1s
      limit_mib: 1500
      spike_limit_mib: 400

    batch:
      timeout: 2s
      send_batch_size: 2048
      send_batch_max_size: 4096

    # CRITICAL: Tail-based Sampling
    tail_sampling:
      decision_wait: 10s
      num_traces: 100000
      expected_new_traces_per_sec: 10000
      policies:
        # 1. 에러는 100% 수집
        - name: error-policy
          type: status_code
          status_code:
            status_codes: [ERROR]

        # 2. 느린 요청은 100% 수집
        - name: latency-policy
          type: latency
          latency:
            threshold_ms: 1000

        # 3. 특정 서비스는 높은 비율
        - name: critical-service
          type: string_attribute
          string_attribute:
            key: service.name
            values: [payment-service, order-service]
            enabled_regex_matching: false
          sample_rate: 50  # 50%

        # 4. 나머지는 낮은 비율
        - name: probabilistic-policy
          type: probabilistic
          probabilistic:
            sampling_percentage: 5

    # 속성 필터링 (비용 절감)
    attributes:
      actions:
        # 불필요한 속성 제거
        - key: http.request.header.cookie
          action: delete
        - key: http.request.header.authorization
          action: delete
        - key: db.statement
          action: hash  # 민감 데이터 해싱

    # 스팬 필터링
    filter:
      error_mode: ignore
      traces:
        span:
          # health check 제외
          - 'attributes["http.route"] == "/health"'
          - 'attributes["http.route"] == "/ready"'
          - 'attributes["http.route"] == "/metrics"'

  exporters:
    otlp/tempo:
      endpoint: tempo-distributor.observability:4317
      tls:
        insecure: true
      sending_queue:
        enabled: true
        num_consumers: 20
        queue_size: 50000

    prometheusremotewrite:
      endpoint: http://prometheus.observability:9090/api/v1/write
      resource_to_telemetry_conversion:
        enabled: true

    loki:
      endpoint: http://loki-gateway.observability:3100/loki/api/v1/push

  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, filter, tail_sampling, attributes, batch]
        exporters: [otlp/tempo]
      metrics:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [prometheusremotewrite]
      logs:
        receivers: [otlp]
        processors: [memory_limiter, attributes, batch]
        exporters: [loki]

resources:
  limits:
    cpu: 2
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi

# Pod Anti-Affinity (분산 배치)
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: otel-gateway
          topologyKey: kubernetes.io/hostname
```

---

## CRITICAL: Tail-based Sampling 설정

### 샘플링 정책 우선순위

```yaml
# 정책 평가 순서 (첫 매치 적용)
tail_sampling:
  policies:
    # 1순위: 에러 트레이스 (100%)
    - name: errors
      type: status_code
      status_code:
        status_codes: [ERROR]

    # 2순위: 느린 요청 (100%)
    - name: slow-requests
      type: latency
      latency:
        threshold_ms: 500

    # 3순위: 특정 작업 (100%)
    - name: important-operations
      type: string_attribute
      string_attribute:
        key: operation.name
        values:
          - checkout
          - payment
          - refund

    # 4순위: 복합 조건
    - name: composite-policy
      type: composite
      composite:
        max_total_spans_per_second: 1000
        policy_order: [errors, slow-requests, probabilistic]
        rate_allocation:
          - policy: errors
            percent: 50
          - policy: slow-requests
            percent: 30
          - policy: probabilistic
            percent: 20

    # 최종: 확률적 샘플링
    - name: probabilistic
      type: probabilistic
      probabilistic:
        sampling_percentage: 5
```

### Trace ID 기반 Load Balancing

```yaml
# Gateway 앞에 Load Balancer 설정 (Trace ID 해싱)
apiVersion: v1
kind: Service
metadata:
  name: otel-gateway-lb
  namespace: observability
  annotations:
    # AWS NLB
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 600  # Tail sampling decision_wait보다 길게
  ports:
    - port: 4317
      targetPort: 4317
      protocol: TCP
      name: otlp-grpc
  selector:
    app.kubernetes.io/name: otel-gateway
---
# 또는 Envoy로 Trace ID 기반 라우팅
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: otel-gateway
  namespace: observability
spec:
  host: otel-gateway
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpHeaderName: "traceparent"  # W3C Trace Context
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Gateway 단일 인스턴스 | SPOF + 병목 | HPA + Anti-affinity |
| Tail sampling 미사용 | 중요 트레이스 유실 | 에러/지연 100% 수집 |
| 무제한 queue_size | OOM | 적절한 제한 + 알림 |
| 모든 속성 전송 | 비용 폭증 | 속성 필터링 |

---

## 체크리스트

### 아키텍처
- [ ] 트래픽 규모 파악
- [ ] Agent/Gateway 분리 (10K+ RPS)
- [ ] HPA 설정
- [ ] Pod Anti-affinity

### 샘플링
- [ ] Tail-based sampling 설정
- [ ] 에러/지연 트레이스 100%
- [ ] 확률적 샘플링 비율 결정

## 참조 스킬

- `/observability-otel-optimization` - Kafka 버퍼, 비용 최적화, 모니터링 알림
- `/observability-otel` - OTel 기본 설정
- `/monitoring-grafana` - Grafana 모니터링
