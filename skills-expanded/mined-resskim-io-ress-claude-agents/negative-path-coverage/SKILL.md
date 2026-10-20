---
name: negative-path-coverage
category: testing
description: Happy path bias로 인한 운영 사고 방지. 에러 경로/장애 시나리오/리소스 한계/타이밍 race를 명시적으로 테스트 케이스화하는 체크리스트. Wikipedia "Happy path" + Postman negative testing 기반.
---

# Negative Path Coverage (M4: Happy path bias)

Claude / 개발자 모두 가장 흔히 빠지는 함정: **정상 동작만 작성·테스트** 하고 에러 경로를 "나중에 추가"하기로 미룬다. 결과적으로 운영 중 처음 발생하는 에러 시나리오가 production 사고가 된다.

> Claude mental model 오류: "정상 흐름만 통과하면 PR 머지 OK" → 실제로 사고의 70%+ 가 unhappy path (timeout, partial failure, retry storm, resource limit) 에서 발생.

---

## Happy Path 와 Unhappy Path

- **Happy path** ([Wikipedia](https://en.wikipedia.org/wiki/Happy_path)): 모든 입력이 valid 하고 외부 의존이 정상인 default scenario.
- **Unhappy path**: invalid input / timeout / partial failure / resource exhaustion / 순서 위반 / 동시성 race.

Negative testing = unhappy path 를 의도적으로 trigger 해서 system 의 견고함을 검증.

---

## 4 카테고리 negative path

### 1. Input 경계 (validation)

| 함정 | 테스트 케이스 |
|---|---|
| empty string / null | `""`, `null`, `undefined` |
| 경계값 | 0, -1, MAX_INT, MIN_INT, 길이 0 / 1 / max+1 |
| 인코딩 | UTF-8 multi-byte, emoji, control chars, NULL byte (`\0`) |
| 형식 | malformed JSON, 부분 truncate, BOM 포함 |
| 의미적 invalid | future date when only past 허용, 음수 amount |

### 2. 외부 의존 실패 (resilience)

| 함정 | 테스트 케이스 | 도구 |
|---|---|---|
| Timeout | DB / API 가 30s 응답 안 함 | Toxiproxy, WireMock delay |
| Partial 성공 | DB write OK + Kafka publish 실패 | Testcontainers 일부 stop |
| 5xx storm | 외부 의존 100% 5xx | WireMock failure scenarios |
| Connection refused | 의존 서비스 down | docker stop |
| Slow read | 응답이 1KB/s 로 천천히 | tc qdisc netem |

### 3. 리소스 한계 (capacity)

| 함정 | 테스트 케이스 |
|---|---|
| DB connection pool 고갈 | 동시 요청 > pool size |
| Heap OOM | 큰 응답 / 누적 컬렉션 |
| File descriptor 고갈 | connection close 누락 |
| Disk full | log rotation 미설정 |
| K8s limits 초과 | CPU throttling / OOMKilled |

### 4. 동시성 / 순서 (timing)

| 함정 | 테스트 케이스 |
|---|---|
| Race condition | 같은 row 동시 update / `SELECT FOR UPDATE` 누락 |
| Idempotency | 같은 request 2번 → 결제 1회만 |
| Retry 중복 | 비멱등 POST + 5xx retry → 중복 결제 (Goti 실사례) |
| 순서 역전 | webhook 이 원본 event 보다 먼저 도착 |
| Stale read | replica lag 중 즉시 read |

---

## ❌ 안티패턴: "예외는 catch 만 하면 됨"

```java
// ❌ catch 하고 무시 → 에러 경로 검증 불가
try {
    paymentClient.charge(amount);
} catch (Exception e) {
    log.error("payment failed", e);   // 사용자에게 어떤 응답이?
    // 호출자는 success 로 인식? rollback?
}
```

```java
// ✅ 에러 분류 + 명시적 응답 + 테스트
try {
    return paymentClient.charge(amount);
} catch (TimeoutException e) {
    return PaymentResult.PENDING;     // 사용자에게 "처리 중" + 비동기 검증
} catch (InsufficientFundsException e) {
    return PaymentResult.FAILED;      // 즉시 fail
} catch (Exception e) {
    log.error("payment unknown", e);
    return PaymentResult.UNKNOWN;     // 운영 escalation
}
```

각 분기마다 **테스트 1건씩** 작성. WireMock / mock 으로 의도된 에러 trigger.

---

## ❌ Goti 실사례: 비멱등 POST + Istio 5xx retry → 중복 결제

```yaml
# Istio default VirtualService — 5xx 시 자동 retry 2회
retries:
  attempts: 3
  retryOn: 5xx,connect-failure
```

```java
// 결제 API — 비멱등 (Idempotency-Key 없음)
@PostMapping("/payments")
public PaymentResult charge(@RequestBody ChargeRequest req) {
    return paymentService.charge(req.userId, req.amount);
}
```

PG 가 transient 5xx 반환 → Istio retry → 중복 결제 발생.

수정:
- **Idempotency-Key 헤더** 의무화 + Redis 로 dedup
- **`retryOn` 에서 5xx 제거** (비멱등 endpoint) 또는 method=GET 만 retry

→ 이런 시나리오는 정상 테스트로 잡히지 않는다. negative path 테스트 의무화 필요.

---

## 작성 절차: "에러 경로 카탈로그" 의무화

1. 새 feature PR 작성 시 **에러 경로 카탈로그** 섹션 추가 (PR template 의무)
2. 위 4 카테고리에서 최소 **각 1건 이상** 시나리오 명시
3. 각 시나리오마다 **테스트 케이스 또는 의도적 미테스트 사유** 기록
4. 의도적 미테스트는 ADR 또는 risk register 로 escalate

PR template 예시:

```markdown
## Error Path Coverage

### Input validation
- [ ] empty input → `400 Bad Request`
- [ ] oversize input (1MB+) → `413 Payload Too Large`

### External dependency
- [ ] DB timeout → retry with backoff
- [ ] PG 5xx → `PaymentResult.UNKNOWN` + monitoring alert

### Resource limits
- [ ] connection pool 고갈 → `503 Service Unavailable`

### Timing / concurrency
- [ ] 동일 Idempotency-Key 2회 → 두 번째는 cached result 반환
```

---

## 자가 검증 체크리스트

신규 endpoint / 서비스 / job 추가 시:

- [ ] Input 4종 (empty / 경계 / 인코딩 / 형식) 테스트 케이스가 있는가?
- [ ] 외부 의존이 **timeout / 5xx / connection refused** 일 때 동작이 명시되었는가?
- [ ] 리소스 한계 (pool / heap / disk) 도달 시 graceful 한가? (cascade failure 없음)
- [ ] 비멱등 작업에 **Idempotency-Key** 가 강제되는가?
- [ ] Retry policy 가 **method/status code 별로 명시**되었는가? (5xx 일괄 retry 금지)
- [ ] Chaos test 가 분기 1회 실행되는가? (의존 down / network delay)
- [ ] PR template 에 **error path coverage** 섹션이 강제되는가?

---

## 외부 근거

- [Happy path — Wikipedia](https://en.wikipedia.org/wiki/Happy_path)
- [Negative testing for more resilient APIs — Postman blog](https://blog.postman.com/negative-testing-for-more-resilient-apis/)
- [Chaos Testing vs Chaos Engineering — BlazeMeter](https://www.blazemeter.com/blog/chaos-testing-vs-chaos-engineering)
- [Idempotency-Key HTTP Header — IETF draft](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)

---

## 연계 skill

- [`spring/bean-postprocessor-ordering.md`](../bean-postprocessor-ordering/SKILL.md) — M1 순서 race
- [`msa/consumer-driven-contracts.md`](../consumer-driven-contracts/SKILL.md) — M10 contract drift
- [`platform/resource-budget-calculator.md`](../resource-budget-calculator/SKILL.md) — M9 리소스 budget
