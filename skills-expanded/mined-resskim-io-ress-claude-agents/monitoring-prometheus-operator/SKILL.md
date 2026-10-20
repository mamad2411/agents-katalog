---
name: monitoring-prometheus-operator
category: observability
description: "Prometheus Operator CRD 패턴 가이드 — ServiceMonitor, PodMonitor, PrometheusRule CRD 패턴 및 앱 Helm chart 통합 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Prometheus Operator CRD 패턴 가이드

ServiceMonitor, PodMonitor, PrometheusRule CRD 패턴 및 앱 Helm chart 통합

## Quick Reference (결정 트리)

```
앱 메트릭 수집 방법?
    │
    ├─ Service가 있는 앱 ──> ServiceMonitor
    │
    ├─ Service 없는 앱 ───> PodMonitor (직접 Pod 타겟팅)
    │     (CronJob, DaemonSet 등)
    │
    ├─ 알림 룰 정의 ──────> PrometheusRule
    │
    └─ scrape config 직접? ─> 비권장 (CRD 사용 권장)
```

---

## ServiceMonitor

K8s Service의 엔드포인트를 Prometheus 스크래핑 대상으로 등록하는 CRD.

### 기본 패턴

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
  namespace: myapp
  labels:
    monitoring: "true"               # Prometheus selector와 매칭
spec:
  selector:
    matchLabels:
      app: myapp                     # 대상 Service의 label
  namespaceSelector:
    matchNames:
      - myapp
  endpoints:
    - port: metrics                  # Service의 port name
      interval: 30s
      path: /metrics                 # 메트릭 엔드포인트
      scrapeTimeout: 10s
```

### 멀티 포트 서비스

```yaml
spec:
  endpoints:
    - port: http-metrics             # 앱 메트릭 (8080)
      interval: 30s
      path: /metrics
    - port: grpc-metrics             # gRPC 메트릭 (9090)
      interval: 60s
      path: /metrics
```

### Bearer Token 인증이 필요한 경우

```yaml
spec:
  endpoints:
    - port: metrics
      bearerTokenSecret:
        name: monitoring-token
        key: token
      tlsConfig:
        insecureSkipVerify: true
```

---

## PodMonitor

Service가 없는 워크로드(CronJob, DaemonSet, sidecar)를 직접 스크래핑.

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: batch-jobs
  labels:
    monitoring: "true"
spec:
  selector:
    matchLabels:
      app: batch-processor
  podMetricsEndpoints:
    - port: metrics
      interval: 60s
      path: /metrics
  namespaceSelector:
    matchNames:
      - batch
```

### ServiceMonitor vs PodMonitor 선택 기준

| 기준 | ServiceMonitor | PodMonitor |
|------|---------------|------------|
| Service 있음 | O (권장) | 가능하지만 불필요 |
| Service 없음 | 불가 | O (유일한 옵션) |
| Headless Service | 가능 | 가능 |
| CronJob/Job | 불가 | O |
| DaemonSet (sidecar) | 가능 | O (더 직관적) |
| IP 변경에 안전 | O (Service 경유) | Pod 재생성 시 자동 반영 |

---

## PrometheusRule

Prometheus 알림 룰을 K8s 리소스로 선언적 관리.

### 앱별 알림 룰

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
  namespace: myapp
  labels:
    monitoring: "true"
spec:
  groups:
    - name: myapp.rules
      rules:
        # 에러율 알림
        - alert: HighErrorRate
          expr: |
            sum(rate(http_requests_total{job="myapp",code=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{job="myapp"}[5m]))
            > 0.05
          for: 5m
          labels:
            severity: critical
            team: backend
          annotations:
            summary: "{{ $labels.job }} 에러율 {{ $value | humanizePercentage }}"
            runbook_url: "https://wiki.example.com/runbook/high-error-rate"

        # 지연 시간 알림
        - alert: HighLatencyP99
          expr: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket{job="myapp"}[5m])) by (le)
            ) > 0.5
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "{{ $labels.job }} P99 지연 {{ $value }}s"

        # Pod restart 알림
        - alert: PodRestarting
          expr: |
            increase(kube_pod_container_status_restarts_total{namespace="myapp"}[1h]) > 3
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "{{ $labels.pod }} 1시간 내 {{ $value }}회 재시작"
```

---

## 앱 Helm Chart 통합

### Helm Chart에 ServiceMonitor/PrometheusRule 포함

```
charts/myapp/
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── servicemonitor.yaml          # 조건부 생성
│   └── prometheusrule.yaml          # 조건부 생성
└── values.yaml
```

### values.yaml

```yaml
# 모니터링 설정
monitoring:
  serviceMonitor:
    enabled: true                    # Phase 0에서는 false
    interval: 30s
    path: /metrics
    port: http
    labels: {}                       # 추가 labels

  prometheusRule:
    enabled: true                    # Phase 0에서는 false
    rules:
      errorRate:
        enabled: true
        threshold: 0.05              # 환경별 override 가능
        severity: critical
      latencyP99:
        enabled: true
        threshold: 0.5               # 환경별 override
        severity: warning

# 메트릭 포트
metricsPort: 8080
```

### templates/servicemonitor.yaml

```yaml
{{- if .Values.monitoring.serviceMonitor.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
    monitoring: "true"
    {{- with .Values.monitoring.serviceMonitor.labels }}
    {{- toYaml . | nindent 4 }}
    {{- end }}
spec:
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  endpoints:
    - port: {{ .Values.monitoring.serviceMonitor.port | default "http" }}
      interval: {{ .Values.monitoring.serviceMonitor.interval | default "30s" }}
      path: {{ .Values.monitoring.serviceMonitor.path | default "/metrics" }}
      scrapeTimeout: 10s
{{- end }}
```

### templates/prometheusrule.yaml

```yaml
{{- if .Values.monitoring.prometheusRule.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
    monitoring: "true"
spec:
  groups:
    - name: {{ include "myapp.fullname" . }}.rules
      rules:
        {{- if .Values.monitoring.prometheusRule.rules.errorRate.enabled }}
        - alert: {{ include "myapp.fullname" . }}-HighErrorRate
          expr: |
            sum(rate(http_requests_total{job="{{ include "myapp.fullname" . }}",code=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{job="{{ include "myapp.fullname" . }}"}[5m]))
            > {{ .Values.monitoring.prometheusRule.rules.errorRate.threshold }}
          for: 5m
          labels:
            severity: {{ .Values.monitoring.prometheusRule.rules.errorRate.severity }}
          annotations:
            summary: "High error rate on {{ include "myapp.fullname" . }}"
        {{- end }}
        {{- if .Values.monitoring.prometheusRule.rules.latencyP99.enabled }}
        - alert: {{ include "myapp.fullname" . }}-HighLatency
          expr: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket{job="{{ include "myapp.fullname" . }}"}[5m])) by (le)
            ) > {{ .Values.monitoring.prometheusRule.rules.latencyP99.threshold }}
          for: 10m
          labels:
            severity: {{ .Values.monitoring.prometheusRule.rules.latencyP99.severity }}
          annotations:
            summary: "High P99 latency on {{ include "myapp.fullname" . }}"
        {{- end }}
{{- end }}
```

### 환경별 Override

```yaml
# values-dev.yaml — kind에서는 비활성화 가능
monitoring:
  serviceMonitor:
    enabled: true
    interval: 60s                    # dev는 느리게

  prometheusRule:
    enabled: false                   # dev에서는 알림 불필요

# values-prod.yaml — 엄격한 설정
monitoring:
  serviceMonitor:
    enabled: true
    interval: 15s                    # prod는 자주

  prometheusRule:
    enabled: true
    rules:
      errorRate:
        threshold: 0.01              # prod는 더 엄격 (1%)
        severity: critical
      latencyP99:
        threshold: 0.3               # prod는 300ms
        severity: warning
```

---

## 메트릭 노출 패턴 (앱 코드)

### Go (prometheus/client_golang)

```go
import "github.com/prometheus/client_golang/prometheus/promhttp"

// /metrics 엔드포인트 등록
mux.Handle("/metrics", promhttp.Handler())
```

### Java (Spring Boot Actuator)

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,prometheus
  metrics:
    tags:
      application: ${spring.application.name}
```

### Python (prometheus_client)

```python
from prometheus_client import start_http_server, Counter

REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'path', 'code'])

start_http_server(8080)  # /metrics 자동 노출
```

---

## Prometheus가 ServiceMonitor를 못 찾을 때 체크리스트

```
1. [ ] Prometheus의 serviceMonitorSelector가 올바른가?
       → serviceMonitorSelectorNilUsesHelmValues: false (모두 탐색)
       → 또는 matchLabels가 ServiceMonitor의 labels와 매칭

2. [ ] ServiceMonitor의 namespace가 Prometheus가 탐색하는 범위에 있는가?
       → serviceMonitorNamespaceSelector가 설정되어 있으면 확인

3. [ ] ServiceMonitor의 selector가 실제 Service의 labels와 매칭되는가?
       → kubectl get svc -l app=myapp으로 확인

4. [ ] Service의 port name이 ServiceMonitor의 endpoints[].port와 일치하는가?
       → port 이름이 아닌 번호를 쓰면 안 됨

5. [ ] 앱이 /metrics 엔드포인트를 실제로 노출하는가?
       → kubectl port-forward pod/myapp 8080 && curl localhost:8080/metrics

6. [ ] RBAC: Prometheus ServiceAccount가 해당 namespace에 접근 가능한가?
```
