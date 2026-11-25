---
name: observability-incident-playbook
category: observability
description: "Observability Incident Playbook — Alert 수신 -> 진단 -> RCA -> 복구 -> 포스트모템까지 E2E 인시던트 대응 워크플로우 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Observability Incident Playbook

Alert 수신 -> 진단 -> RCA -> 복구 -> 포스트모템까지 E2E 인시던트 대응 워크플로우

## Quick Reference (증상 -> 시작 도구 결정 트리)

```
증상별 시작점?
    │
    ├─ 높은 에러율 (5xx 급증) ────> Metrics 먼저 (PromQL)
    │   └─ rate() 확인 → 원인 trace 드릴다운
    │
    ├─ 느린 응답 (Latency 증가) ──> Traces 먼저 (TraceQL)
    │   └─ span waterfall → 병목 구간 식별
    │
    ├─ 앱 크래시 (OOM, Panic) ───> Logs 먼저 (LogQL)
    │   └─ 에러 로그 → exit code → 리소스 확인
    │
    ├─ CPU 스파이크 ──────────────> Profiles 먼저 (FlameQL)
    │   └─ flame graph → 핫 함수 식별
    │
    └─ 복합 증상 ────────────────> Metrics → Trace → Log → Profile 순차 피벗
```

관련 스킬: `/monitoring-troubleshoot`, `/alerting-discord`, `/observability-otel`, `/observability-pyroscope`, `/monitoring-self-monitoring`

---

## CRITICAL: 5-Stage Incident Response Flow

모든 인시던트는 아래 5단계를 순차적으로 따른다. 단계를 건너뛰지 않는다.

### Stage 1: Detect (감지) — 0~2분

- 알림 수신 확인 (Discord/PagerDuty/Grafana Alert)
- 영향받는 서비스와 범위 1차 파악
- 인시던트 채널 생성 및 담당자 호출

### Stage 2: Triage (분류) — 2~5분

- SEV 레벨 결정 (SEV1~SEV4, 아래 분류표 참조)
- 영향받는 사용자 수/비율 추정
- 커뮤니케이션 시작 (상태 페이지 업데이트)
- 최근 배포/변경 사항 확인: `kubectl rollout history`, ArgoCD sync history

### Stage 3: Investigate (조사) — 5~30분

- Signal-Based Investigation 수행 (아래 상세 절차)
- 가설 수립 → 데이터 검증 → 기각/수용 반복
- 관련 팀에 에스컬레이션 (필요 시)
- 타임라인 기록 시작

### Stage 4: Mitigate (완화) — 즉시

- 근본 원인 수정 또는 임시 완화 조치 적용
- 롤백, 스케일 아웃, 트래픽 차단 등 선택
- 완화 후 메트릭 정상화 확인 (최소 10분 관찰)
- 상태 페이지 업데이트: "Identified → Monitoring"

### Stage 5: Review (검토) — 인시던트 종료 후 48시간 이내

- 포스트모템 문서 작성 (아래 템플릿)
- 타임라인 재구성
- Action Items 도출 및 담당자/기한 배정
- 팀 회고 미팅 진행

---

## Signal-Based Investigation

### Metric -> Trace -> Log -> Profile 피벗 경로

4개 신호를 순차적으로 연결하여 근본 원인을 좁혀간다. 각 단계에서 다음 신호로 피벗할 지점을 찾는다.

### Step 1: Metrics (PromQL) — 전체 상황 파악

에러율, 지연시간, 처리량을 확인하여 문제 범위를 좁힌다.

```promql
# 5xx 에러율 확인
sum(rate(http_server_request_duration_seconds_count{http_response_status_code=~"5.."}[5m]))
  by (http_route, service_name)

# P99 지연시간 확인
histogram_quantile(0.99,
  sum(rate(http_server_request_duration_seconds_bucket[5m])) by (le, http_route)
)

# 에러 버짓 소진율 (SLO 기반)
1 - (
  sum(rate(http_server_request_duration_seconds_count{http_response_status_code!~"5.."}[1h]))
  / (sum(rate(http_server_request_duration_seconds_count[1h])) > 0)
)

# Pod 리소스 사용량
container_memory_working_set_bytes{container!=""} / container_spec_memory_limit_bytes
```

피벗 포인트: 에러가 많은 `http_route` + `service_name` 조합을 식별 -> TraceQL로 이동

### Step 2: Traces (TraceQL) — 개별 요청 추적

문제가 있는 경로의 개별 trace를 조사하여 병목 span을 찾는다.

```
# 에러 trace 검색
{resource.service.name="order-service" && status=error}

# 특정 엔드포인트의 느린 요청
{resource.service.name="order-service" && span.http.route="/api/orders" && duration>1s}

# 특정 상태 코드 필터링
{resource.service.name="order-service" && span.http.response.status_code>=500}

# 다운스트림 서비스 영향 확인
{resource.service.name="payment-service" && status=error} | select(span.http.route, status)
```

피벗 포인트: trace_id를 복사 -> LogQL에서 해당 trace의 상세 로그 확인

### Step 3: Logs (LogQL) — 상세 컨텍스트 확인

trace에서 찾은 에러의 상세 로그와 스택트레이스를 확인한다.

```logql
# 특정 trace의 로그 조회
{service_name=~"order-service"} |= "trace_id" |= "<trace_id_value>"

# 에러 로그 필터링 (Loki Native OTLP)
{service_name=~"order-service"} | detected_level="ERROR" | json | line_format "{{.message}}"

# 예외 스택트레이스 검색
{service_name=~"order-service"} |= "Exception" | json | line_format "{{.body}}"

# 시간대별 에러 빈도
sum by (detected_level) (count_over_time(
  {service_name=~"order-service"} | detected_level="ERROR" [5m]
))
```

주의: Loki Native OTLP 환경에서는 `detected_level="ERROR"` (대문자) 사용. `level="error"` 금지.

피벗 포인트: CPU/메모리 이상이 의심되면 -> Pyroscope 프로파일 확인

### Step 4: Profiles (FlameQL) — 성능 병목 정밀 분석

CPU 스파이크, 메모리 누수 등 리소스 수준 문제를 프로파일로 분석한다.

```
# CPU 프로파일 조회
{service_name="order-service", profile_type="cpu"}

# 메모리 할당 프로파일
{service_name="order-service", profile_type="inuse_space"}

# 특정 시간대 비교 (diff view)
# Grafana Pyroscope UI에서 시간 범위 선택 후 Diff 모드 활성화

# Goroutine 프로파일 (Go 서비스)
{service_name="order-service", profile_type="goroutine"}
```

주의: Pyroscope tag에 점(`.`) 사용 불가 -> `service_name` (O), `service.name` (X)

---

## Runbook Templates

### Runbook 1: High Error Rate (5xx 에러율 SLO 초과)

**Step 1 — 범위 확인**: 어떤 서비스/엔드포인트인가

```promql
topk(5, sum by (service_name, http_route) (
  rate(http_server_request_duration_seconds_count{http_response_status_code=~"5.."}[5m])
))
```

**Step 2 — 최근 변경 확인**

```bash
argocd app history <app-name> --output json | jq '.[0:3]'
kubectl rollout history deployment/<service-name> -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | grep -i "configmap\|secret"
```

**Step 3 — 의존성 확인**

```promql
# 다운스트림 에러율
sum by (service_name) (rate(http_client_request_duration_seconds_count{http_response_status_code=~"5.."}[5m]))
# DB 커넥션 풀
hikaricp_connections_active / hikaricp_connections_max
```

**Step 4 — 완화**: 롤백(`kubectl rollout undo`), 스케일 아웃(`kubectl scale --replicas=N`), 또는 Istio rate limit 적용

### Runbook 2: High Latency (P99 SLO 초과)

**Step 1 — 계층별 지연 식별**

```promql
# 서비스별 P99
histogram_quantile(0.99, sum by (le, service_name) (rate(http_server_request_duration_seconds_bucket[5m])))
# 다운스트림 호출 지연
histogram_quantile(0.99, sum by (le, http_route) (rate(http_client_request_duration_seconds_bucket{service_name="order-service"}[5m])))
```

**Step 2 — Span Waterfall**: `{resource.service.name="order-service" && duration>2s}` -> Tempo UI에서 가장 긴 span = 병목

**Step 3 — Flame Graph**: Pyroscope Diff 모드로 정상 시간대와 비교

**Step 4 — 리소스**: CPU throttling(`rate(container_cpu_cfs_throttled_seconds_total[5m])`), GC pause(`rate(jvm_gc_pause_seconds_sum[5m])`)

### Runbook 3: Pod CrashLoopBackOff

**Step 1 — Exit Code 분석**

```bash
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Last State"
# Exit 137=OOMKilled | Exit 1=앱 에러 | Exit 143=SIGTERM(graceful shutdown 실패)
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

**Step 2 — OOM vs 앱 에러 분기**

```bash
kubectl top pod <pod-name> -n <namespace>              # OOM: 메모리 확인
kubectl logs <pod-name> -n <namespace> --previous --tail=100  # 앱 에러: 로그 확인
```

```logql
{service_name=~"order-service"} | detected_level=~"ERROR|FATAL" | json
```

**Step 3 — 완화**: OOM이면 `kubectl set resources --limits=memory=1Gi`, 앱 에러면 로그 기반 디버깅

### Runbook 4: Disk Full (사용률 90% 초과)

**Step 1 — 디스크 사용 주체 식별**

```bash
kubectl exec -it <pod-name> -n <namespace> -- df -h
kubectl exec -it <pod-name> -n <namespace> -- du -sh /data/* | sort -rh | head -10
```

**Step 2 — 긴급 정리**: TSDB WAL(`curl -X POST http://prometheus:9090/-/compact`), Loki retention 조정, 앱 로그 logrotate

**Step 3 — 재발 방지**: PV autoResize 설정, retention 정책 검토, `--storage.tsdb.retention.time/size` 설정

---

## Post-Incident Review Template

인시던트 종료 후 48시간 이내에 아래 구조로 포스트모템을 작성한다.

### RCA 문서 구조

```markdown
# [인시던트 제목] 포스트모템

발생일: YYYY-MM-DD HH:MM ~ HH:MM (KST)
심각도: SEV1 / SEV2 / SEV3 / SEV4
작성자:
상태: Draft | Reviewed | Action Items Complete

## 1. 요약 (1-2문장)
## 2. 영향 범위 (사용자 수, 실패 요청, 에러율 피크)
## 3. 타임라인 (분 단위 기록)
## 4. 근본 원인 (Root Cause)
## 5. 대응 과정 (무엇이 효과적이었고 무엇이 아니었는가)
## 6. Action Items (담당/기한/우선순위)
## 7. 교훈 (Keep / Problem / Try)
```

### 타임라인 재구성 방법

```
1. Grafana Explore에서 인시던트 시간대 선택
2. 알림 발생 시점 → 최초 대응 → 원인 파악 → 완화 적용 → 정상화 순서로 기록
3. 각 시점의 메트릭 스크린샷 첨부 (Grafana 패널 Share → Snapshot)
4. Tempo trace link 포함 (원인 trace를 영구 보존)
```

### Action Items 형식

| # | 조치 | 유형 | 우선순위 | 담당 | 기한 | 상태 |
|---|------|------|---------|------|------|------|
| 1 | 알림 임계값 조정 | 감지 개선 | P1 | - | - | TODO |
| 2 | 회로 차단기 추가 | 복원력 | P1 | - | - | TODO |
| 3 | 런북 업데이트 | 문서화 | P2 | - | - | TODO |

유형 분류: 감지 개선 / 복원력 / 프로세스 / 문서화 / 모니터링

---

## Grafana Explore Workflows

### Metric -> Trace 피벗 (Exemplars)

Prometheus 메트릭에서 직접 관련 trace로 이동하는 경로.

```yaml
# Prometheus exemplar 설정 (Spring Boot)
management:
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true
```

- Grafana Panel Edit -> Query -> Options -> Exemplars: ON
- 메트릭 그래프 위의 점(dot) 클릭 -> Tempo trace 뷰로 자동 이동
- `histogram_quantile(0.99, sum by (le) (rate(..._bucket[5m])))` 쿼리에서 exemplar 확인

### Trace -> Log 피벗 (trace_id 상관)

Trace에서 해당 요청의 상세 로그로 이동하는 경로.

```yaml
# Tempo → Loki 연결 (Grafana datasource provisioning)
datasources:
  - name: Tempo
    type: tempo
    uid: tempo
    jsonData:
      tracesToLogsV2:
        datasourceUid: loki
        filterByTraceID: true
        tags: [{key: "service.name", value: "service_name"}]

# Loki → Tempo 연결 (derived fields)
  - name: Loki
    type: loki
    uid: loki
    jsonData:
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "trace_id=(\\w+)"
          name: TraceID
          url: "$${__value.raw}"
```

Tempo UI에서 trace 선택 -> "Logs for this span" 클릭 -> Loki 로그 자동 필터링

### Trace -> Profile 피벗 (Span Profiles)

느린 span에서 해당 시점의 CPU/메모리 프로파일로 드릴다운.

```yaml
# Tempo datasource에 Pyroscope 연결
datasources:
  - name: Tempo
    type: tempo
    uid: tempo
    jsonData:
      tracesToProfilesV2:
        datasourceUid: pyroscope
        tags:
          - key: service.name
            value: service_name
        profileTypeId: "process_cpu:cpu:nanoseconds:cpu:nanoseconds"
```

Tempo span 상세 뷰 -> "Profiles" 탭 -> 해당 span 실행 시점의 flame graph 확인.
정상 시간대와 비교하려면 Pyroscope Diff 뷰 활용.

---

## Communication & Escalation

### Severity 분류

| 등급 | 기준 | 예시 | 대응 시간 |
|------|------|------|----------|
| SEV1 | 전체 서비스 중단, 데이터 유실 위험 | 전체 API 다운, DB 장애 | 즉시 (5분 이내) |
| SEV2 | 주요 기능 장애, 다수 사용자 영향 | 결제 실패, 에러율 > 5% | 15분 이내 |
| SEV3 | 부분 기능 저하, 일부 사용자 영향 | 특정 API 느림, 에러율 > 1% | 1시간 이내 |
| SEV4 | 경미한 문제, 사용자 영향 거의 없음 | 내부 도구 오류, 로그 경고 | 업무 시간 내 |

### Severity별 커뮤니케이션 템플릿

**SEV1/SEV2 초기 알림** (감지 후 5분 이내):
```
[SEV{N}] {서비스명} 장애 발생
- 시작 시각: HH:MM KST | 증상: {1줄 요약}
- 영향: {사용자/기능 영향 범위} | 담당: @{담당자} | 상태: 조사 중
```

**SEV1/SEV2 중간 업데이트** (30분마다):
```
[SEV{N}] {서비스명} 장애 업데이트
- 경과: {N}분 | 상태: {조사 중 / 원인 파악 / 완화 적용 중}
- 발견 사항: {현재까지 파악된 내용}
- 다음 조치: {계획} | ETA: {예상 복구 시간 또는 "파악 중"}
```

**SEV1/SEV2 해결 알림**:
```
[SEV{N}] {서비스명} 장애 해결
- 지속 시간: HH:MM ~ HH:MM KST ({N}분)
- 근본 원인: {1줄 요약} | 조치: {완화/수정 내용} | 포스트모템: {예정일}
```

**SEV3/SEV4 알림**:
```
[SEV{N}] {서비스명} 이슈 감지 - 증상: {요약} | 영향: {제한적} | 조치: {예정}
```

### 에스컬레이션 매트릭스

```
SEV1:
  0~5분   → On-call 엔지니어 호출
  5~15분  → 팀 리드 + 관련 서비스 담당자 호출
  15~30분 → 엔지니어링 매니저 보고
  30분+   → CTO/VP 보고 (비즈니스 영향 시)

SEV2:
  0~15분  → On-call 엔지니어 + 팀 리드
  15~60분 → 관련 팀 담당자
  60분+   → 엔지니어링 매니저

SEV3:
  업무 시간 내 담당 팀에서 처리
  4시간 이상 미해결 시 팀 리드 보고

SEV4:
  담당자가 백로그에 등록 후 일정에 맞춰 처리
```

### 상태 페이지 업데이트 가이드라인

| 단계 | 상태 | 업데이트 시점 |
|------|------|-------------|
| 감지 | Investigating | 장애 감지 즉시 |
| 원인 파악 | Identified | 근본 원인 또는 유력 가설 확인 시 |
| 완화 적용 | Monitoring | 완화 조치 적용 후 모니터링 시작 시 |
| 해결 | Resolved | 메트릭 정상화 확인 후 (최소 10분 관찰) |
| 포스트모템 | Postmortem | 포스트모템 문서 완료 시 (링크 첨부) |

규칙:
- SEV1/SEV2는 상태 페이지 업데이트 필수
- 업데이트 간격: SEV1은 15분, SEV2는 30분
- 기술 용어 최소화, 사용자 관점에서 영향과 예상 복구 시간 중심으로 작성
- "조사 중입니다"만 반복하지 않고 진행 상황을 구체적으로 기술
