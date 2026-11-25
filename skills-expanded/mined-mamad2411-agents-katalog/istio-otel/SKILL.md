---
name: istio-otel
category: service-mesh
description: "Istio + OpenTelemetry 통합 가이드 — Telemetry API v1, ExtensionProviders, W3C Trace Context, OTel Collector 연동 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio + OpenTelemetry 통합 가이드

Telemetry API v1, ExtensionProviders, W3C Trace Context, OTel Collector 연동

## Quick Reference (결정 트리)

```
Istio 텔레메트리 설정?
    │
    ├─ 트레이싱 ───────> Telemetry API + OTel Collector
    │       │
    │       ├─ Sidecar → 자동 Span 생성 (Envoy)
    │       └─ Ambient → ztunnel(L4만) / waypoint(L7 Span)
    │                    앱 레벨 OTel SDK 계측 필요
    │
    ├─ 메트릭 ─────────> Telemetry API + Prometheus
    │       └─ 커스텀 레이블 추가/제거 (카디널리티 제어)
    │
    └─ Access Logging ─> Telemetry API + Envoy/OTel ALS
            └─ OTel Collector로 로그 전송 가능
```

---

## CRITICAL: Telemetry API v1

### 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│  Istio Telemetry API (telemetry.istio.io/v1)                │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────────┐            │
│  │ Tracing  │   │ Metrics  │   │ AccessLogging │            │
│  │          │   │          │   │               │            │
│  │ providers│   │ providers│   │  providers    │            │
│  └────┬─────┘   └────┬─────┘   └──────┬───────┘            │
│       │              │                 │                     │
│       v              v                 v                     │
│  ┌─────────┐   ┌──────────┐   ┌──────────────┐            │
│  │  OTel   │   │Prometheus│   │ Envoy/OTel   │            │
│  │Collector│   │          │   │    ALS       │            │
│  └─────────┘   └──────────┘   └──────────────┘            │
│                                                              │
│  적용 범위:                                                   │
│  - istio-system: 메시 전체 기본값                             │
│  - namespace: 네임스페이스 오버라이드                          │
│  - workload: 워크로드 선택적 적용                             │
└─────────────────────────────────────────────────────────────┘
```

### 핵심 원칙

```
1. 계층적 오버라이드: istio-system(기본) < namespace < workload
2. 여러 provider 동시 사용 가능 (tracing → OTel, metrics → Prometheus)
3. Istio 1.22+에서 Telemetry API v1 Stable
4. MeshConfig의 extensionProviders에서 백엔드 정의
```

---

## ExtensionProviders 설정

### MeshConfig (IstioOperator)

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    enableTracing: true
    defaultConfig:
      tracing:
        sampling: 1.0             # 기본 샘플링 (Telemetry API로 오버라이드 가능)

    extensionProviders:
    # OTel Collector (gRPC - OTLP)
    - name: otel-tracing
      opentelemetry:
        service: otel-collector.observability.svc.cluster.local
        port: 4317
        resource_detectors:
          environment: {}

    # OTel Collector (HTTP - OTLP)
    - name: otel-tracing-http
      opentelemetry:
        service: otel-collector.observability.svc.cluster.local
        port: 4318
        http:
          path: "/v1/traces"
          timeout: 5s

    # Jaeger (Zipkin 프로토콜)
    - name: jaeger
      zipkin:
        service: jaeger-collector.tracing.svc.cluster.local
        port: 9411

    # Access Log → OTel Collector (ALS)
    - name: otel-access-log
      envoyOtelAls:
        service: otel-collector.observability.svc.cluster.local
        port: 4317

    # Envoy 기본 Access Log
    - name: envoy-access-log
      envoyFileAccessLog:
        path: /dev/stdout
```

---

## 트레이싱 설정

### 메시 전체 기본값

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: mesh-default
  namespace: istio-system
spec:
  tracing:
  - providers:
    - name: otel-tracing
    randomSamplingPercentage: 1.0   # 프로덕션: 1%
    customTags:
      cluster_id:
        environment:
          name: ISTIO_META_CLUSTER_ID
          defaultValue: "unknown"
      mesh_id:
        literal:
          value: "production-mesh"
      node_id:
        environment:
          name: POD_NAME
```

### 네임스페이스별 오버라이드

```yaml
# staging: 100% 샘플링
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: debug-tracing
  namespace: staging
spec:
  tracing:
  - providers:
    - name: otel-tracing
    randomSamplingPercentage: 100.0
---
# 고트래픽 서비스: 0.1% 샘플링
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: low-sampling
  namespace: high-traffic
spec:
  tracing:
  - providers:
    - name: otel-tracing
    randomSamplingPercentage: 0.1
```

### 워크로드별 설정

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: payment-tracing
  namespace: production
spec:
  selector:
    matchLabels:
      app: payment-service
  tracing:
  - providers:
    - name: otel-tracing
    randomSamplingPercentage: 10.0   # 결제는 높은 샘플링
    customTags:
      payment_version:
        environment:
          name: APP_VERSION
```

---

## CRITICAL: W3C Trace Context 전파

### 애플리케이션 책임

```
Istio(Envoy)는 inbound 요청에서 Span을 생성하지만,
outbound 요청에 trace 헤더를 자동 전파하지 않음.

애플리케이션이 수신 헤더를 하위 요청에 복사해야 함!

전파해야 할 헤더:
┌──────────────────────────────────────────────┐
│  W3C Trace Context (권장)                      │
│  - traceparent                                │
│  - tracestate                                 │
│                                               │
│  B3 (Zipkin 호환)                              │
│  - x-b3-traceid                               │
│  - x-b3-spanid                                │
│  - x-b3-parentspanid                          │
│  - x-b3-sampled                               │
│  - x-b3-flags                                 │
│                                               │
│  Envoy                                        │
│  - x-request-id                               │
│                                               │
│  Istio                                        │
│  - x-envoy-attempt-count                      │
└──────────────────────────────────────────────┘
```

### 언어별 전파 예시

```yaml
# Spring Boot (자동 - spring-cloud-sleuth/micrometer-tracing)
# application.yml
management:
  tracing:
    propagation:
      type: W3C    # W3C + B3 모두 지원
    sampling:
      probability: 1.0

# Go (수동)
# import "go.opentelemetry.io/otel/propagation"
# propagator := propagation.NewCompositeTextMapPropagator(
#     propagation.TraceContext{},
#     propagation.Baggage{},
# )
# otel.SetTextMapPropagator(propagator)

# Node.js (자동 - @opentelemetry/auto-instrumentations-node)
# const { NodeSDK } = require('@opentelemetry/sdk-node');
# const sdk = new NodeSDK({
#   traceExporter: new OTLPTraceExporter(),
# });
```

---

## 메트릭 커스터마이징

### 레이블 제거 (카디널리티 감소)

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: reduce-cardinality
  namespace: istio-system
spec:
  metrics:
  - providers:
    - name: prometheus
    overrides:
    # 불필요한 레이블 제거
    - match:
        metric: REQUEST_COUNT
        mode: CLIENT_AND_SERVER
      tagOverrides:
        request_protocol:
          operation: REMOVE
        grpc_response_status:
          operation: REMOVE
    # 커스텀 레이블 추가
    - match:
        metric: REQUEST_COUNT
        mode: SERVER
      tagOverrides:
        api_version:
          operation: UPSERT
          value: "request.headers['x-api-version'] | 'unknown'"
```

### Ambient Mode 메트릭

```yaml
# Ambient에서 reporter 라벨 구분
#   reporter="source"   → Sidecar 모드
#   reporter="ztunnel"  → Ambient L4
#   reporter="waypoint" → Ambient L7

# Prometheus 쿼리 예시
# L4 메트릭 (ztunnel)
sum(rate(istio_tcp_sent_bytes_total{reporter="ztunnel"}[5m])) by (destination_workload)

# L7 메트릭 (waypoint 필요)
sum(rate(istio_requests_total{reporter="waypoint"}[5m])) by (response_code)
```

---

## Access Logging → OTel

### OTel Collector로 Access Log 전송

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: otel-access-logging
  namespace: istio-system
spec:
  accessLogging:
  - providers:
    - name: otel-access-log        # envoyOtelAls provider
    filter:
      expression: "response.code >= 400 || connection.mtls == false"
```

### Envoy Access Log + 필터링

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: filtered-access-log
  namespace: production
spec:
  accessLogging:
  - providers:
    - name: envoy-access-log
    filter:
      expression: "response.code >= 400"  # 에러만
---
# 특정 서비스: 전체 로그 (디버깅)
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: debug-access-log
  namespace: production
spec:
  selector:
    matchLabels:
      app: payment-service
  accessLogging:
  - providers:
    - name: envoy-access-log
    # filter 없음 → 전체 로그
```

---

## OTel Collector 구성

### Istio 전용 Pipeline

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
  namespace: observability
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

    processors:
      batch:
        timeout: 10s
        send_batch_size: 1024
      # Istio 메타데이터 보강
      k8sattributes:
        extract:
          metadata:
          - k8s.namespace.name
          - k8s.deployment.name
          - k8s.pod.name
      # 샘플링 (tail-based)
      tail_sampling:
        policies:
        - name: error-policy
          type: status_code
          status_code:
            status_codes: [ERROR]
        - name: slow-policy
          type: latency
          latency:
            threshold_ms: 1000
        - name: default
          type: probabilistic
          probabilistic:
            sampling_percentage: 1

    exporters:
      otlp/tempo:
        endpoint: tempo.observability:4317
        tls:
          insecure: true
      otlp/jaeger:
        endpoint: jaeger-collector.tracing:4317
        tls:
          insecure: true

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch, k8sattributes, tail_sampling]
          exporters: [otlp/tempo]
        logs:
          receivers: [otlp]
          processors: [batch, k8sattributes]
          exporters: [otlp/tempo]
```

---

## Sidecar vs Ambient 텔레메트리 비교

| 기능 | Sidecar | Ambient (ztunnel) | Ambient (waypoint) |
|------|---------|--------------------|--------------------|
| L7 메트릭 | 자동 | X (L4만) | 자동 |
| 트레이싱 Span | 자동 | X | 자동 |
| Access Log | 자동 | L4 로그 | L7 로그 |
| 앱 계측 필요 | 헤더 전파만 | OTel SDK 권장 | 헤더 전파만 |
| reporter 라벨 | source/destination | ztunnel | waypoint |

### Ambient 권장 전략

```
1. ztunnel만 사용 (L4 only):
   → 앱에서 OTel SDK로 직접 계측
   → 앱이 trace 생성 + 헤더 전파 모두 담당

2. waypoint 추가 (L7):
   → Envoy가 L7 Span 자동 생성
   → 앱은 헤더 전파만 담당 (Sidecar와 동일)

권장: 중요 서비스에 waypoint 배포 + 앱 OTel SDK 병행
```

---

## 디버깅

```bash
# Telemetry 리소스 확인
kubectl get telemetry -A

# 적용된 트레이싱 설정 확인
istioctl proxy-config bootstrap <pod> -n <ns> -o json | \
  jq '.bootstrap.tracing'

# OTel Collector 연결 확인
istioctl proxy-config cluster <pod> -n <ns> | grep otel

# 샘플링 비율 확인
istioctl proxy-config bootstrap <pod> -n <ns> -o json | \
  jq '.bootstrap.tracing.clientSampling'

# trace 헤더 전파 확인 (curl 테스트)
kubectl exec <pod> -- curl -v -H "traceparent: 00-..." http://target-service/api
```

---

## 체크리스트

### 트레이싱
- [ ] ExtensionProvider 등록 (OTel Collector)
- [ ] Telemetry 리소스 생성 (istio-system)
- [ ] 프로덕션 샘플링 비율 설정 (1~5%)
- [ ] 앱에서 trace 헤더 전파 확인
- [ ] customTags 설정 (cluster, environment)

### 메트릭
- [ ] 불필요한 레이블 제거 (카디널리티)
- [ ] Ambient reporter 라벨 대시보드 반영
- [ ] 커스텀 메트릭 레이블 추가 검토

### Access Logging
- [ ] 프로덕션: 에러만 필터링
- [ ] OTel ALS 연동 여부 결정
- [ ] 로그 포맷 커스터마이징

### OTel Collector
- [ ] tail_sampling 정책 설정
- [ ] k8sattributes processor 활성화
- [ ] 백엔드 연결 확인 (Tempo/Jaeger)

**관련 skill**: `/istio-tracing`, `/istio-metrics`, `/istio-observability`, `/observability-otel`, `/observability-otel-scale`
