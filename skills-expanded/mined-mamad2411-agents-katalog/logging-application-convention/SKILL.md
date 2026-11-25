---
name: logging-application-convention
category: observability
description: "Application Logging Convention — 애플리케이션 코드에서 로그를 작성할 때 따라야 할 양식과 패턴. Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Application Logging Convention

애플리케이션 코드에서 로그를 작성할 때 따라야 할 양식과 패턴.
멀티 언어(Java, Go, Python) 백엔드 서비스 공통 로깅 컨벤션.

## Quick Reference

```
로그 메시지 양식 결정
    ├─ 비즈니스 이벤트 ──> logfmt: action={ACTION} key={value} ...
    ├─ 에러/예외 ────────> logfmt + 예외 객체 마지막 인자
    ├─ 배치/요약 ────────> logfmt + count={N} duration_ms={N}
    └─ 디버깅 ──────────> logfmt (DEBUG 레벨, 프로덕션 OFF)

Loki 파싱
    ├─ 필드 추출 ────────> | logfmt
    ├─ action 필터 ─────> | action="PAYMENT_CREATE"
    └─ ID 추적 ─────────> | orderId="uuid"
```

---

## 핵심 규칙

### 1. logfmt 양식 필수

모든 비즈니스 로그 메시지는 `key=value` (logfmt) 형식으로 작성한다.

```java
// ✅ logfmt
log.info("action=PAYMENT_CREATE orderId={} memberId={} amount={}", orderId, memberId, amount);

// ❌ 자유형식 한국어
log.info("결제가 완료되었습니다. 주문번호: {}", orderId);

// ❌ action 없음
log.info("orderId={} amount={}", orderId, amount);
```

### 2. action 필드 필수

| 형식 | 설명 |
|------|------|
| `{DOMAIN}_{VERB}` | 정상 이벤트 |
| `{DOMAIN}_{VERB}_FAILED` | 실패 |
| `{DOMAIN}_{VERB}_SKIP` | 건너뜀 |
| `{DOMAIN}_{VERB}_RETRY` | 재시도 |

**Domain prefix**: `PAYMENT_`, `ORDER_`, `QUEUE_`, `SEAT_`, `RESALE_`, `USER_`, `GUARDRAIL_`, `METRIC_`

**동사**: `CREATE`, `CONFIRM`, `CANCEL`, `REFUND`, `ENTER`, `EXIT`, `EXPIRE`, `HOLD`, `RELEASE`, `VALIDATE`, `POLL`, `SYNC`, `LOGIN`, `CHECK`

### 3. 필수 필드

| 필드 | 규칙 |
|------|------|
| `action` | 모든 비즈니스 로그에 필수 |
| 도메인 ID | 1개 이상 (orderId, memberId, gameId 등) |
| `reason` | FAILED/SKIP 시 필수 |
| `error` | ERROR 레벨 시 예외 메시지 |

### 4. 로그 레벨

| 레벨 | 사용 시점 | 프로덕션 |
|------|----------|---------|
| ERROR | 복구 불가, 즉각 대응 | 100% 수집 |
| WARN | 비정상이지만 복구 가능 | 100% 수집 |
| INFO | 주요 비즈니스 이벤트 | 100% (샘플링 가능) |
| DEBUG | 디버깅 상세 | 비활성화 |

---

## 언어별 패턴

### Java (SLF4J)

```java
// 정상 이벤트
log.info("action=PAYMENT_CREATE orderId={} memberId={} amount={} method={}",
         orderId, memberId, amount, paymentMethod);

// 실패 — 예외는 마지막 인자 (stacktrace 자동 포함)
log.error("action=PAYMENT_FAILED orderId={} reason={} error={}",
          orderId, reason, e.getMessage(), e);

// 소요 시간 측정
long start = System.currentTimeMillis();
// ... 처리 ...
log.info("action=PAYMENT_CONFIRM orderId={} paymentId={} duration_ms={}",
         orderId, paymentId, System.currentTimeMillis() - start);

// 배치 요약 (반복문 내부 로그 금지)
log.info("action=SEAT_BATCH_EXPIRE gameId={} count={} duration_ms={}",
         gameId, expiredCount, elapsed);
```

### Go (slog)

```go
slog.Info("action=METRIC_POLL",
    "source", "redis",
    "duration_ms", elapsed.Milliseconds(),
    "count", len(results))

slog.Error("action=METRIC_POLL_FAILED",
    "source", "database",
    "error", err.Error())
```

### Python (structlog / logging)

```python
logger.info("action=GUARDRAIL_CHECK",
            user_id=user_id,
            risk_score=score,
            decision=decision)

logger.warning("action=GUARDRAIL_BLOCK",
               user_id=user_id,
               risk_score=score,
               reason="bot_detected")
```

---

## 금지 패턴

| 금지 | 이유 | 대안 |
|------|------|------|
| 자유형식 한국어 메시지 | Loki 자동 파싱 불가 | logfmt 양식 사용 |
| action 없는 로그 | 대시보드 필터/집계 불가 | `action=` 필수 포함 |
| PII (이메일, 전화, 카드) | 개인정보보호법 위반 | ID만 사용 |
| 문자열 연결 (`"a=" + val`) | 성능 낭비 (로그 비활성화 시에도 연결) | SLF4J placeholder `{}` |
| 반복문 내부 로그 | 로그 폭발 | 건수 요약 로그 |
| 예외 삼키기 (`catch {}`) | 디버깅 불가 | 로깅 후 rethrow 또는 처리 |
| `e.printStackTrace()` | stdout 직접 출력, 구조화 안 됨 | `log.error("...", e)` |

---

## OTel 연동

### 자동 포함 필드 (개발자 작성 불필요)

OTel Java Agent + Spring Boot logging pattern이 자동 주입:

- `trace_id` / `span_id` — 분산 추적 상관관계
- `service.name` — 서비스 식별
- `timestamp`, `level`, `thread`, `logger`

### Loki 쿼리 패턴

```logql
# action 필터
{service_name=~"my-app-.+"} | logfmt | action="PAYMENT_CREATE"

# 특정 주문 추적 (서비스 무관)
{service_name=~"my-app-.+"} | logfmt | orderId="target-uuid"

# action별 에러 집계 (대시보드용)
sum by (action) (
  count_over_time({service_name=~"$svc"} | logfmt | level="ERROR" [5m])
)

# 처리 시간 p95
{service_name=~"$svc"} | logfmt | action="PAYMENT_CONFIRM"
  | unwrap duration_ms | quantile_over_time(0.95, [5m])
```

### Grafana 대시보드 변수 매핑

```
$service_name = job label → PromQL용
$svc          = service.name → Loki/Tempo용

LogQL:   {service_name=~"$svc"} | logfmt | action="$action"
TraceQL: {resource.service.name="$svc"}
```

---

## 모듈별 필수 로그 포인트

각 모듈에서 반드시 로그를 남겨야 하는 비즈니스 이벤트:

### Payment (금융 거래 — 전 포인트 필수)

- `PAYMENT_CREATE` — 결제 생성 시작
- `PAYMENT_CONFIRM` — PG 확인 요청
- `PAYMENT_CONFIRM_COMPLETE` — 결제 확정 완료
- `PAYMENT_FAILED` (ERROR) — 결제 실패
- `PAYMENT_CANCEL` — 결제 취소
- `PAYMENT_REFUND` — 환불 처리

### Queue (대기열)

- `QUEUE_ENTER` — 진입
- `SEAT_ENTER` — 좌석 선택 진입
- `QUEUE_EXIT` — 퇴출/만료

### Seat/Ticketing (좌석)

- `SEAT_HOLD` — 점유
- `SEAT_RELEASE` — 해제
- `SEAT_HOLD_EXPIRE` (WARN) — 만료

### Order (주문)

- `ORDER_CREATE` — 생성
- `ORDER_CONFIRM` — 확정
- `ORDER_CANCEL` — 취소

---

## 참고

- ADR: `docs/adr/0006-logging-convention.md`
- 컨벤션 가이드: `docs/conventions/logging-standard.md`
- Loki 쿼리 가이드: [`/logging-loki`](../logging-loki/SKILL.md)
- OTel 설정: [`/observability-otel`](../observability-otel/SKILL.md)
