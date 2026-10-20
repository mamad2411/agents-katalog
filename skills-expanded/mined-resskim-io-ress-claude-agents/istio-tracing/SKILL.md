---
name: istio-tracing
category: service-mesh
description: "Istio Distributed Tracing — Jaeger/Tempo 연동, Span 생성, Access Logging Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Distributed Tracing

Jaeger/Tempo 연동, Span 생성, Access Logging

## Quick Reference

```
트레이싱 설정
    │
    ├─ Sidecar Mode ─────> 자동 Span 생성
    │   └─ Envoy에서 요청/응답 헤더 자동 전파
    │
    └─ Ambient Mode ─────> 제한적
        ├─ ztunnel: L4만 (Span 없음)
        ├─ waypoint: L7 Span 생성
        └─ 권장: 앱에서 직접 Span 생성
```

---

## Jaeger 연동

### Telemetry 설정

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-tracing
  namespace: istio-system
spec:
  tracing:
  - providers:
    - name: jaeger
    randomSamplingPercentage: 1.0  # 1% 샘플링
    customTags:
      environment:
        literal:
          value: production
```

### IstioOperator 설정

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    defaultConfig:
      tracing:
        sampling: 1.0  # 1%
        zipkin:
          address: jaeger-collector.tracing:9411
    extensionProviders:
    - name: jaeger
      zipkin:
        service: jaeger-collector.tracing.svc.cluster.local
        port: 9411
```

---

## Tempo 연동 (Grafana Stack)

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: otel-tracing
  namespace: istio-system
spec:
  tracing:
  - providers:
    - name: otel
    randomSamplingPercentage: 1.0
---
# IstioOperator extensionProvider
spec:
  meshConfig:
    extensionProviders:
    - name: otel
      opentelemetry:
        service: otel-collector.monitoring.svc.cluster.local
        port: 4317
```

---

## Ambient Mode 트레이싱

```yaml
# 앱 레벨 계측 권장 (Ambient)
# OpenTelemetry SDK 직접 사용

# Java (Spring Boot)
dependencies:
  - io.opentelemetry:opentelemetry-api
  - io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter

# Go
import "go.opentelemetry.io/otel"

# waypoint 배포 시 L7 Span 추가됨
```

---

## Access Logging

### Sidecar Mode

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: access-logging
  namespace: istio-system
spec:
  accessLogging:
  - providers:
    - name: envoy
    filter:
      expression: "response.code >= 400"  # 에러만
---
# 전체 로그 (개발용)
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: full-access-log
  namespace: development
spec:
  accessLogging:
  - providers:
    - name: envoy
```

### Ambient Mode

```bash
# ztunnel 로그 확인
kubectl logs -n istio-system -l app=ztunnel -f

# waypoint 로그 확인
kubectl logs -n production -l gateway.istio.io/managed -f
```

### 커스텀 로그 포맷

```yaml
meshConfig:
  accessLogFile: /dev/stdout
  accessLogFormat: |
    [%START_TIME%] "%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%"
    %RESPONSE_CODE% %RESPONSE_FLAGS% %BYTES_RECEIVED% %BYTES_SENT%
    %DURATION% "%REQ(X-FORWARDED-FOR)%" "%REQ(USER-AGENT)%"
```

---

## OTel Collector 연동

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
  namespace: monitoring
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317

    processors:
      batch:
        timeout: 10s

    exporters:
      otlp/tempo:
        endpoint: tempo.monitoring:4317
        tls:
          insecure: true

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch]
          exporters: [otlp/tempo]
```

---

## 체크리스트

- [ ] 샘플링 비율 설정 (프로덕션: 1-5%)
- [ ] Ambient 시 앱 계측 추가
- [ ] 헤더 전파 확인 (x-request-id, x-b3-*)
- [ ] Access Log 필터링 적용

**관련 skill**: `/istio-observability`, `/observability-otel`, `/monitoring-logs`
