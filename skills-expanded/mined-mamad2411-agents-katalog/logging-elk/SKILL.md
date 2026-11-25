---
name: logging-elk
category: observability
description: "ELK Stack Log Analysis Guide — Elasticsearch + Kibana를 활용한 로그 검색/분석 가이드 (보안팀/개발팀용) Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# ELK Stack Log Analysis Guide

Elasticsearch + Kibana를 활용한 로그 검색/분석 가이드 (보안팀/개발팀용)

## Quick Reference (선택 기준)
```
ELK vs Loki 선택
    ├─ ELK ─────────> 전체 텍스트 검색, 복잡한 집계
    │                 장기 보관, 컴플라이언스 감사
    │
    └─ Loki ────────> 비용 효율, 간단한 검색
                      Prometheus/Grafana 연계
```

### ELK 장점/제한
| 장점 | 제한 |
|------|------|
| 전체 텍스트 인덱싱 | 높은 리소스 사용 |
| 강력한 집계/분석 | 관리 복잡성 |
| Kibana SIEM 내장 | 비용 (라이선스) |
| 장기 보관 최적화 | 스케일 시 복잡성 |

---

## 역할별 Elasticsearch 쿼리

### 개발팀용 쿼리

**에러 검색**
```json
// 특정 서비스 에러 로그
GET /logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "service": "order-service" } },
        { "match": { "level": "error" } }
      ],
      "filter": [
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ]
    }
  },
  "sort": [{ "@timestamp": "desc" }],
  "size": 100
}
```

**trace_id로 전체 흐름 추적**
```json
GET /logs-*/_search
{
  "query": {
    "term": { "trace_id.keyword": "abc123def456" }
  },
  "sort": [{ "@timestamp": "asc" }]
}
```

**느린 요청 분석**
```json
GET /logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "range": { "duration_ms": { "gte": 1000 } } }
      ],
      "filter": [
        { "term": { "service.keyword": "api-gateway" } }
      ]
    }
  },
  "aggs": {
    "by_endpoint": {
      "terms": { "field": "endpoint.keyword", "size": 10 },
      "aggs": {
        "avg_duration": { "avg": { "field": "duration_ms" } },
        "p95_duration": { "percentiles": { "field": "duration_ms", "percents": [95] } }
      }
    }
  }
}
```

### 보안팀용 쿼리

| 쿼리 유형 | 인덱스 | 핵심 조건 |
|----------|--------|----------|
| 로그인 실패 분석 | security-logs-* | `event: login_failed` + IP별 집계 |
| Brute Force 탐지 | security-logs-* | 5분 내 5회 이상 실패 |
| 봇/매크로 탐지 | bot-detection-* | `is_bot: true` + confidence >= 0.9 |
| 개인정보 접근 | pii-access-* | accessor별 접근 횟수/고유 대상 수 |

**예시: Brute Force 탐지**
```json
GET /security-logs-*/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "term": { "event.keyword": "login_failed" } },
        { "range": { "@timestamp": { "gte": "now-5m" } } }
      ]
    }
  },
  "aggs": {
    "by_ip": {
      "terms": { "field": "client_ip.keyword", "min_doc_count": 5 }
    }
  }
}
```

자세한 보안 로그 분석은 `/logging-security` 참조.

---

## Query DSL 심화

### Bool Query (복합 조건)
```json
{
  "query": {
    "bool": {
      "must": [],      // AND 조건
      "should": [],    // OR 조건
      "must_not": [],  // NOT 조건
      "filter": []     // 스코어 영향 없는 필터
    }
  }
}
```

### 전체 텍스트 검색
```json
// match: 분석기 적용 (토큰화)
{ "match": { "message": "connection error" } }

// match_phrase: 순서 유지
{ "match_phrase": { "message": "connection refused" } }

// wildcard: 와일드카드
{ "wildcard": { "message.keyword": "*Exception*" } }

// regexp: 정규식
{ "regexp": { "message.keyword": ".*timeout.*" } }
```

### 집계 (Aggregations)
```json
{
  "aggs": {
    // 버킷 집계
    "by_service": {
      "terms": { "field": "service.keyword", "size": 10 }
    },
    // 메트릭 집계
    "stats": {
      "stats": { "field": "duration_ms" }
    },
    // 날짜 히스토그램
    "over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "1h"
      }
    }
  }
}
```

---

## Kibana 대시보드

### 개발팀 대시보드 구성
```
┌──────────────┬──────────────┬──────────────┐
│ Total Errors │ Error Rate   │ Avg Duration │
│   (카운트)   │   (게이지)   │   (메트릭)   │
├──────────────┴──────────────┴──────────────┤
│           에러 타임라인 (막대 차트)          │
├──────────────────────────────────────────────┤
│           서비스별 에러 분포 (파이 차트)      │
├──────────────────────────────────────────────┤
│           로그 테이블 (Discover 임베드)       │
└──────────────────────────────────────────────┘
```

### 보안팀 SIEM 대시보드
```
┌──────────────┬──────────────┬──────────────┐
│ Login Failed │ Bot Detected │ PII Access   │
│   (1시간)    │   (1시간)    │   (1시간)    │
├──────────────┴──────────────┴──────────────┤
│        지리적 분포 (Maps 시각화)             │
├────────────────────┬─────────────────────────┤
│  공격 시도 타임라인│  Top 10 의심 IP         │
├────────────────────┴─────────────────────────┤
│           Security Events 테이블             │
└──────────────────────────────────────────────┘
```

---

## Kibana 알림 설정

### Detection Rule 생성
```json
// Kibana > Security > Rules > Create new rule
{
  "name": "Brute Force Detection",
  "description": "5분 내 동일 IP에서 5회 이상 로그인 실패",
  "type": "threshold",
  "query": "event.keyword: login_failed",
  "threshold": 5,
  "threshold_field": "client_ip.keyword",
  "time_window": "5m",
  "severity": "high",
  "actions": [
    {
      "action_type": "slack",
      "params": {
        "message": "Brute force detected from {{context.threshold_field}}"
      }
    }
  ]
}
```

### Watcher Alert (X-Pack)
```json
PUT _watcher/watch/high_error_rate
{
  "trigger": {
    "schedule": { "interval": "1m" }
  },
  "input": {
    "search": {
      "request": {
        "indices": ["logs-*"],
        "body": {
          "query": {
            "bool": {
              "must": [
                { "term": { "level.keyword": "error" } },
                { "range": { "@timestamp": { "gte": "now-5m" } } }
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": { "ctx.payload.hits.total.value": { "gt": 100 } }
  },
  "actions": {
    "slack_notification": {
      "webhook": {
        "url": "${SLACK_WEBHOOK}",
        "body": "{{ctx.payload.hits.total.value}} errors in last 5 minutes"
      }
    }
  }
}
```

---

## 인덱스 관리

### ILM (Index Lifecycle Management)
```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "1d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### 인덱스 템플릿
```json
PUT _index_template/logs-template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy"
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "level": { "type": "keyword" },
        "service": { "type": "keyword" },
        "trace_id": { "type": "keyword" },
        "message": { "type": "text" },
        "duration_ms": { "type": "long" }
      }
    }
  }
}
```

---

## 보안 설정

### RBAC (역할 기반 접근 제어)
```json
// 개발팀 역할
PUT _security/role/developer
{
  "indices": [
    {
      "names": ["logs-*"],
      "privileges": ["read"],
      "query": { "term": { "env.keyword": "development" } }
    }
  ]
}

// 보안팀 역할
PUT _security/role/security_analyst
{
  "indices": [
    {
      "names": ["security-logs-*", "bot-detection-*", "pii-access-*"],
      "privileges": ["read"]
    }
  ],
  "applications": [
    {
      "application": "kibana-.kibana",
      "privileges": ["feature_siem.all", "feature_discover.read"]
    }
  ]
}
```

---

## 성능 최적화

### 쿼리 최적화
```
✅ 좋은 쿼리
───────────
- filter context 사용 (캐싱)
- keyword 필드로 정확 매칭
- 시간 범위 필터 우선

❌ 나쁜 쿼리
───────────
- wildcard 선두에 * 사용
- script 쿼리 과다 사용
- 모든 필드 text 타입
```

### 인덱싱 전략
```
로그 타입별 인덱스 분리
─────────────────────
logs-app-{date}        → 애플리케이션 로그
logs-security-{date}   → 보안 이벤트
logs-payment-{date}    → 결제 로그 (5년 보관)
logs-pii-{date}        → 개인정보 접근 (1년+)
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 단일 인덱스 | 검색 느림 | 날짜/타입별 분리 |
| 모든 필드 text | 저장 낭비 | keyword/text 구분 |
| ILM 미설정 | 디스크 폭발 | 생명주기 정책 |
| RBAC 미설정 | 데이터 노출 | 역할별 권한 |

---

## 체크리스트

### 개발팀
- [ ] 에러/성능 쿼리 숙지
- [ ] Discover 사용법
- [ ] trace_id 검색

### 보안팀
- [ ] Security 대시보드 구성
- [ ] Detection Rule 설정
- [ ] 감사 로그 쿼리
- [ ] 알림 규칙 설정

### 운영
- [ ] ILM 정책 설정
- [ ] 인덱스 템플릿
- [ ] RBAC 구성
- [ ] 백업 정책

**관련 skill**: `/monitoring-logs`, `/logging-security`, `/logging-loki`

---

## 참고 자료
- [Elasticsearch Query DSL](https://logz.io/blog/elasticsearch-queries/)
- [Kibana Alerting](https://www.elastic.co/kibana/alerting)
- [Elastic SIEM 구현](https://medium.com/@thecloudarchitect/the-complete-elastic-siem-implementation-manual-3815100f872c)
