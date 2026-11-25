---
name: monitoring-grafana
category: observability
description: "Grafana Monitoring Patterns — Grafana 대시보드, 알림, RBAC 설정 가이드 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Grafana Monitoring Patterns

Grafana 대시보드, 알림, RBAC 설정 가이드

## Quick Reference (결정 트리)
```
역할별 대시보드
    ├─ 개발자 ────> RED Dashboard (에러율, 응답시간)
    ├─ DevOps ────> Infrastructure Dashboard (리소스, 용량)
    ├─ SRE ───────> SLO Dashboard (가용성, 에러 버짓)
    └─ PM ────────> Summary Dashboard (비즈니스 메트릭)
```

---

## CRITICAL: 역할별 RBAC 설정

### Organization Roles
| Role | 권한 | 대상 |
|------|------|------|
| Admin | 전체 관리 | SRE, Platform Team |
| Editor | 대시보드/알림 편집 | DevOps |
| Viewer | 읽기 전용 | 개발자, PM |

### 팀 기반 접근 제어
```yaml
# grafana.ini
[users]
auto_assign_org = true
auto_assign_org_role = Viewer
```

### 폴더별 권한
```
/Dashboards
    ├─ /Infrastructure (DevOps: Editor, 개발자: None)
    ├─ /Application (개발자: Viewer, DevOps: Editor)
    ├─ /SLO (SRE: Admin, PM: Viewer)
    └─ /Summary (모두: Viewer)
```

### API로 팀 권한 설정
```bash
# 팀 생성
curl -X POST -d '{"name":"developers"}' \
  http://admin:admin@localhost:3000/api/teams
# 폴더 권한 설정
curl -X POST -d '{"items":[{"teamId":1,"permission":1}]}' \
  http://admin:admin@localhost:3000/api/folders/app/permissions
```

---

## 데이터소스 설정

### Prometheus
```yaml
# provisioning/datasources/prometheus.yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    isDefault: true
    jsonData:
      timeInterval: "15s"
```

### Loki (Trace 연동)
```yaml
- name: Loki
  type: loki
  url: http://loki:3100
  jsonData:
    derivedFields:
      - name: TraceID
        matcherRegex: '"trace_id":"([^"]+)"'
        url: '$${__value.raw}'
        datasourceUid: tempo
```

### Tempo
```yaml
- name: Tempo
  type: tempo
  url: http://tempo:3200
  jsonData:
    tracesToLogs:
      datasourceUid: loki
      filterByTraceID: true
```

### Tempo datasource tags — scoped tag 필수
`tracesToLogsV2`, `tracesToMetrics`, `tracesToProfiles`의 `tags[].key`는 Tempo v2 API 호출에 사용되므로 **scoped tag**이어야 한다.

```
tracesToLogsV2/Metrics/Profiles tags[].key:
- ❌ "service.name" (Tempo v2 API 400 에러)
- ✅ "resource.service.name" (scoped tag 필수)
- tracesToLogsV2.query 내 ${__span.tags["service.name"]}는 그대로 유지 (API 호출 아님)
```

---

## 대시보드 템플릿

### RED Dashboard (개발자용)
```
┌─────────────┬─────────────┬─────────────┐
│ Request Rate│ Error Rate  │ Duration    │
├─────────────┴─────────────┴─────────────┤
│         Error Rate by Endpoint          │
├─────────────────────────────────────────┤
│         Latency Distribution            │
└─────────────────────────────────────────┘
```

**주요 쿼리:**
```promql
# Request Rate
rate(http_requests_total{service="$service"}[5m])
# Error Rate
sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m])) * 100
# P95 Duration
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### Infrastructure Dashboard (DevOps용)
```promql
# CPU Usage
sum(rate(container_cpu_usage_seconds_total{namespace="$ns"}[5m])) by (pod) * 100
# Memory Usage
container_memory_usage_bytes / container_spec_memory_limit_bytes * 100
```

### SLO Dashboard (SRE용)
```promql
# Availability (99.9% 목표)
sum(rate(http_requests_total{status!~"5.."}[30d])) / sum(rate(http_requests_total[30d])) * 100
# Error Budget Remaining
(1 - (sum(rate(http_requests_total{status=~"5.."}[30d])) / sum(rate(http_requests_total[30d])))) / 0.001 * 100
```

---

## 알림 설정

### 채널 구성
```yaml
# provisioning/alerting/contacts.yaml
apiVersion: 1
contactPoints:
  - name: slack-critical
    receivers:
      - uid: slack-p1
        type: slack
        settings:
          url: ${SLACK_WEBHOOK_URL}
          channel: "#alerts-critical"
  - name: pagerduty-oncall
    receivers:
      - uid: pd-p1
        type: pagerduty
        settings:
          integrationKey: ${PAGERDUTY_KEY}
```

### 알림 계층 (P1/P2/P3)
| 우선순위 | 조건 | 채널 | 응답 |
|----------|------|------|------|
| P1 Critical | 에러율 > 5% | PagerDuty + Slack | 5분 |
| P2 Warning | 에러율 > 1% | Slack | 4시간 |
| P3 Info | 디스크 > 70% | Slack | 24시간 |

### 알림 규칙
```yaml
groups:
  - name: app-alerts
    interval: 1m
    rules:
      - name: High Error Rate
        condition: B
        data:
          - refId: A
            model:
              expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100 > 5
        for: 5m
        labels:
          severity: critical
```

---

## Cross-Datasource 변수 전략

### 문제
Prometheus에서 `job="{namespace}/{service-name}"` (namespace/name 형식)이지만, Loki/Tempo에서는 `resource.service.name="{service-name}"` (name만).
동일 변수로 모든 datasource를 쿼리하면 매핑 불일치가 발생한다.

### 해결: 기본 변수 + 숨겨진 파생 변수

```json
// 대시보드 변수 설정 (JSON)
{
  "templating": {
    "list": [
      {
        "name": "service_name",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(up, job)",
        "label": "Service"
      },
      {
        "name": "svc",
        "type": "custom",
        "query": "",
        "hide": 2,
        "regex": ".*/(.*)",
        "allValue": "",
        "includeAll": false
      }
    ]
  }
}
```

| Datasource | 변수 | 쿼리 예시 | 주의사항 |
|-----------|------|----------|----------|
| Prometheus | `$service_name` | `job="$service_name"` | {namespace}/{service-name} 형식 |
| Loki | `$svc` | `{service_name=~"$svc"}` | namespace 제거, detected_level 사용 |
| Tempo (TraceQL) | `$svc` | `resource.service.name="$svc"` | `=~` regex 사용 금지 |

### TraceQL 변수 제약 (CRITICAL)
- TraceQL `=~` regex에 Grafana multi-value 변수 사용 금지 → 400 에러
- PromQL의 `=~`는 pipe-separated 변환 지원하지만 TraceQL은 미지원
- 대안: `select()`로 결과 컬럼에 표시, 테이블 내 사용자 필터링

```
# ❌ TraceQL에서 regex 변수 사용 → 400 에러
{resource.service.name="$svc" && span.http.route=~"$http_route"}

# ✅ select()로 결과에 표시만
{resource.service.name="$svc"} | select(span.http.route, duration)
```

### Anti-pattern
```
# ❌ 모든 datasource에 동일 변수 사용
Prometheus: job="$service_name"    → OK ({namespace}/{service-name})
Loki: service_name="$service_name" → FAIL ({namespace}/{service-name} ≠ {service-name})
```

---

## Reverse Proxy 뒤 보안 설정

ALB/nginx(HTTPS) → Grafana(HTTP) 구성 시 CSRF Origin 불일치 발생.

### 필수 설정
```ini
# grafana.ini 또는 환경변수
[security]
csrf_trusted_origins = https://your-domain.com

# 환경변수
GF_SECURITY_CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

### Anti-pattern
```
❌ Reverse proxy(HTTPS) 뒤 Grafana 운영 시 CSRF 설정 누락
→ POST 요청(대시보드 저장, 설정 변경) 시 "Origin not allowed" 에러
```

---

## Provisioning (IaC)

### File Provisioning

```yaml
apiVersion: 1
providers:
  - name: default
    folder: ''
    type: file
    options:
      path: /var/lib/grafana/dashboards
    updateIntervalSeconds: 30  # 대시보드 JSON 변경 시 30초 내 자동 reload
```

**핵심**: `updateIntervalSeconds: 30` → 컨테이너 재시작 없이 대시보드 JSON 파일 변경 자동 반영

### 대시보드 Provider
```yaml
apiVersion: 1
providers:
  - name: default
    folder: ''
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

### Helm 배포
```yaml
grafana:
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: default
          folder: ''
          type: file
          options:
            path: /var/lib/grafana/dashboards
  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          url: http://prometheus-server
          isDefault: true
```

---

## Tempo Internal Link 패턴

Trace ID를 클릭하면 Tempo에서 해당 트레이스를 직접 여는 internal link 설정.

```json
// "url": "" 필수 (비워야 internal link 동작)
{
  "title": "트레이스 상세 보기",
  "url": "",
  "internal": {
    "datasourceUid": "tempo",
    "datasourceName": "Tempo",
    "query": { "queryType": "traceql", "query": "${__value.raw}" }
  }
}
```

- `"url": ""`은 반드시 빈 문자열이어야 한다. 값이 있으면 external link로 동작.
- `${__value.raw}`는 셀의 raw 값 (trace ID)을 전달.

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 모든 사용자 Admin | 설정 변경 사고 | RBAC 역할 분리 |
| 알림 과다 | Alert Fatigue | 우선순위별 채널 분리 |
| 수동 대시보드 | 복구 불가 | Provisioning IaC |
| 단일 대시보드 | 정보 과부하 | 역할별 분리 |
| 민감한 임계값 | 잦은 오탐 | 5분 이상 지속 조건 |
| Cross-datasource 동일 변수 | Loki/Tempo 쿼리 실패 | 기본 + 숨겨진 파생 변수 |
| Reverse proxy 뒤 CSRF 미설정 | POST 요청 차단 | `csrf_trusted_origins` 설정 |

---

## 체크리스트

### RBAC
- [ ] 역할별 Organization Role 할당
- [ ] 팀 생성 및 사용자 배정
- [ ] 폴더별 권한 설정

### 데이터소스
- [ ] Prometheus/Loki/Tempo 연결
- [ ] Trace-Log 연동 설정

### 대시보드 & 알림
- [ ] 역할별 대시보드 생성
- [ ] 우선순위별 알림 규칙 설정
- [ ] Provisioning IaC 구성

**관련 skill**: `/observability`, `/observability-otel`, `/monitoring-troubleshoot`
