---
name: monitoring-logs
category: observability
description: "Log Monitoring Patterns — Fluent Bit, Loki, 로그 파이프라인 설정 가이드 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Log Monitoring Patterns

Fluent Bit, Loki, 로그 파이프라인 설정 가이드

## Quick Reference (결정 트리)
```
로그 파이프라인
    ├─ Edge 수집 ───> Fluent Bit (경량, DaemonSet)
    ├─ 중앙 처리 ───> OTel Collector (변환, 라우팅)
    └─ 저장소 ─────> Loki (비용 효율, Grafana 통합)

비용 최적화 (샘플링)
    ├─ ERROR ───> 100% 수집
    ├─ WARN ────> 50%
    ├─ INFO ────> 10%
    └─ DEBUG ───> 0% (프로덕션 비활성화)
```

---

## CRITICAL: 로그 비용 최적화

### 레벨별 샘플링 효과
```
최적화 전: 6,500,000 로그/일 → $9,750/월
최적화 후:   500,000 로그/일 →   $750/월
절감: 92.3%
```

---

## Fluent Bit 설정

### DaemonSet 기본 설정
```yaml
# fluent-bit.conf
[SERVICE]
    Flush 5
    Parsers_File parsers.conf

[INPUT]
    Name tail
    Path /var/log/containers/*.log
    Parser docker
    Tag kube.*
    Mem_Buf_Limit 5MB

[FILTER]
    Name kubernetes
    Match kube.*
    Merge_Log On
    K8S-Logging.Parser On
```

### 레벨별 샘플링 필터
```yaml
# ERROR: 100% 수집
[FILTER]
    Name rewrite_tag
    Match kube.*
    Rule $level ^(error|ERROR)$ error.$TAG true

# WARN: 50% 샘플링
[FILTER]
    Name throttle
    Match warn.*
    Rate 500
    Window 5

# INFO: 10% 샘플링
[FILTER]
    Name throttle
    Match info.*
    Rate 100
    Window 5

# DEBUG: 프로덕션 제외
[FILTER]
    Name grep
    Match kube.*
    Exclude level ^(debug|DEBUG)$
```

### 민감정보 마스킹
```lua
-- mask.lua
function mask_sensitive(tag, timestamp, record)
    if record["message"] then
        -- 이메일
        record["message"] = string.gsub(record["message"], "[%w._]+@[%w._]+%.[%w]+", "[EMAIL]")
        -- 카드번호
        record["message"] = string.gsub(record["message"], "%d%d%d%d[- ]?%d%d%d%d[- ]?%d%d%d%d[- ]?%d%d%d%d", "[CARD]")
        -- 전화번호
        record["message"] = string.gsub(record["message"], "01[0-9][-]?%d%d%d%d[-]?%d%d%d%d", "[PHONE]")
    end
    return 1, timestamp, record
end
```

---

## Loki 설정

### Storage 티어링
```yaml
storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    shared_store: s3
  aws:
    s3: s3://ap-northeast-2/loki-logs
    region: ap-northeast-2

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: s3
      schema: v12

limits_config:
  retention_period: 30d
```

### 레벨별 Retention 정책
```yaml
limits_config:
  retention_stream:
    - selector: '{level="error"}'
      period: 90d    # ERROR: 90일
    - selector: '{level="warn"}'
      period: 30d    # WARN: 30일
    - selector: '{level="info"}'
      period: 7d     # INFO: 7일
```

---

## LogQL 쿼리 패턴

### 기본 쿼리
```logql
# 서비스별 에러
{namespace="production", app="order-service"} |= "error"

# JSON 파싱 후 필터
{app="api-gateway"} | json | level="error" | status_code >= 500
```

### 집계 쿼리
```logql
# 분당 에러 수
sum(count_over_time({namespace="production"} |= "error" [1m])) by (app)

# 에러율
sum(rate({app="order-service"} |= "error" [5m])) / sum(rate({app="order-service"} [5m])) * 100
```

### Pattern 매칭
```logql
# IP 추출
{app="nginx"} | pattern `<ip> - - [<_>] "<method> <path> <_>" <status>` | status >= 500

# 응답시간 추출
{app="api-gateway"} | json | unwrap duration_ms | duration_ms > 1000
```

---

## OTel Collector 로그 처리

```yaml
receivers:
  filelog:
    include: [/var/log/containers/*.log]
    operators:
      - type: json_parser

processors:
  batch:
    timeout: 5s
  transform:
    log_statements:
      - context: log
        statements:
          - replace_pattern(body, "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b", "[EMAIL]")
  probabilistic_sampler:
    sampling_percentage: 10

exporters:
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
    labels:
      attributes:
        level: ""
        service.name: ""

service:
  pipelines:
    logs:
      receivers: [filelog]
      processors: [batch, transform, probabilistic_sampler]
      exporters: [loki]
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| DEBUG 전체 수집 | 비용 폭발 | 프로덕션 비활성화 |
| 민감정보 로깅 | 규정 위반 | 마스킹 필터 |
| 구조화 없는 로그 | 쿼리 어려움 | JSON 구조화 |
| 무제한 보존 | 스토리지 비용 | 레벨별 retention |
| 단일 인덱스 | 쿼리 느림 | 레이블 기반 분리 |

---

## 체크리스트

### 수집
- [ ] Fluent Bit DaemonSet 배포
- [ ] 레벨별 샘플링 설정
- [ ] 민감정보 마스킹 확인

### 저장
- [ ] Loki 배포 및 S3 연동
- [ ] Retention 정책 설정

### 쿼리
- [ ] Grafana Explore 연동
- [ ] 주요 LogQL 쿼리 저장

**관련 skill**: `/observability`, `/observability-otel`, `/monitoring-grafana`
