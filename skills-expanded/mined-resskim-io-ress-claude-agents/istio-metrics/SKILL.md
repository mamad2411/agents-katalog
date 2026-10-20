---
name: istio-metrics
category: service-mesh
description: "Istio Metrics & Prometheus Integration — Istio Prometheus 연동, ServiceMonitor 설정, RED 메트릭 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Metrics & Prometheus Integration

Istio Prometheus 연동, ServiceMonitor 설정, RED 메트릭

## Quick Reference

```
메트릭 수집
    │
    ├─ Sidecar Mode ─────> Pod별 상세 메트릭
    │   └─ istio_requests_total (pod 레이블)
    │
    └─ Ambient Mode ─────> Node/Waypoint 레벨
        ├─ ztunnel: L4 메트릭만
        └─ waypoint: L7 메트릭 (배포 시)
```

---

## ServiceMonitor 설정

### Sidecar Mode

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istio-sidecar-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      security.istio.io/tlsMode: istio
  namespaceSelector:
    any: true
  endpoints:
  - port: http-envoy-prom
    path: /stats/prometheus
    interval: 15s
---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: envoy-stats
  namespace: monitoring
spec:
  selector:
    matchExpressions:
    - key: security.istio.io/tlsMode
      operator: Exists
  namespaceSelector:
    any: true
  podMetricsEndpoints:
  - port: "15020"
    path: /stats/prometheus
    interval: 15s
```

### Ambient Mode

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ztunnel-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: ztunnel
  namespaceSelector:
    matchNames:
    - istio-system
  endpoints:
  - port: http-monitoring
    path: /stats/prometheus
    interval: 15s
---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: waypoint-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      gateway.istio.io/managed: istio.io-mesh-controller
  namespaceSelector:
    any: true
  podMetricsEndpoints:
  - port: "15020"
    path: /stats/prometheus
    interval: 15s
```

---

## RED 메트릭 쿼리

```yaml
# 1. Request Rate
sum(rate(istio_requests_total{reporter="destination"}[5m])) by (destination_service_name)

# 2. Error Rate
sum(rate(istio_requests_total{reporter="destination", response_code=~"5.*"}[5m]))
  /
sum(rate(istio_requests_total{reporter="destination"}[5m])) by (destination_service_name)

# 3. Latency (P99)
histogram_quantile(0.99,
  sum(rate(istio_request_duration_milliseconds_bucket{reporter="destination"}[5m]))
  by (destination_service_name, le)
)

# 4. TCP 연결 (Ambient ztunnel)
sum(rate(istio_tcp_connections_opened_total[5m])) by (reporter)
sum(rate(istio_tcp_sent_bytes_total[5m])) by (reporter)
```

---

## 메트릭 커스터마이징 (Telemetry API)

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-metrics
  namespace: istio-system
spec:
  metrics:
  - providers:
    - name: prometheus
    overrides:
    # 불필요한 레이블 제거 (카디널리티 감소)
    - match:
        metric: REQUEST_COUNT
      tagOverrides:
        request_protocol:
          operation: REMOVE
        destination_principal:
          operation: REMOVE
```

---

## Grafana 대시보드

### 권장 대시보드 ID

| ID | 용도 |
|----|------|
| 7645 | Control Plane (istiod 상태) |
| 7639 | Mesh Dashboard (전체 트래픽) |
| 7636 | Service Dashboard (서비스별) |
| 7630 | Workload Dashboard (Pod별) |
| 11829 | Performance (Envoy 리소스) |

### Ambient Mode 패널 추가

```yaml
panels:
- title: "ztunnel TCP Connections"
  targets:
  - expr: "sum(rate(istio_tcp_connections_opened_total{app=\"ztunnel\"}[5m])) by (node)"

- title: "Waypoint Request Rate"
  targets:
  - expr: "sum(rate(istio_requests_total{app=\"waypoint\"}[5m])) by (destination_service_name)"
```

---

## 체크리스트

- [ ] ServiceMonitor/PodMonitor 설정
- [ ] 스크래핑 간격 조정 (15-30s)
- [ ] 레이블 카디널리티 관리
- [ ] Ambient용 대시보드 조정
- [ ] 알림 규칙 설정

**관련 skill**: `/istio-observability`, `/istio-core`, `/monitoring-grafana`
