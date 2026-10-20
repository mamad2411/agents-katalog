---
name: subscription-billing-flows
category: business
description: "Subscription Billing Flows (운영 흐름) — Proration, Dunning, Plan Change, Invoice + Multi-currency, Metered, Trial 어뷰즈, Multi-tenancy seat. subscription-billing.md (메인 hub) 의 운영 분기. Use when 구독 운영 흐름 / proration / dunning 구현이 필요할 때."
effort: xhigh
deprecated: false
---

# Subscription Billing — Flows (운영 흐름)

구독 운영 흐름 전용 — Proration, Dunning, Plan Change(+미리보기 의사코드), Invoice + Multi-currency, Metered, Trial 어뷰즈, Multi-tenancy seat. `subscription-billing.md`(메인 hub)의 운영 단계 깊이 분리.

신규 부트스트랩이 아닌 **이미 결제 흐름이 도는 SaaS에서 변경/실패/사용량/seat 시나리오에 막혔을 때** 보는 가이드. 도메인 모델/상태 머신/Provider 선택/Webhook 기본은 메인 hub 참조.

## When to Use

- Plan 변경 / 환불 / proration UX 설계 시
- Dunning 회수율 개선, 카드 갱신 처리, Smart Retries 도입 검토
- Multi-currency / 한국 세금계산서 시스템 통합
- Metered billing(API 콜 / 토큰 / GB) 도입
- Trial 어뷰즈 발견 후 대응
- B2B Seat 모델 설계 (active 정의, 추가/회수 정책)

**관련 skill (cross-link)**:
- `business/subscription-billing.md` — 메인 hub (도메인/상태/Webhook/보안/ADR/Quick Start)
- `business/subscription-billing-metrics.md` — Dunning 결과 메트릭, Cohort 분석
- `business/payment-integration.md` — 일회성 결제 부모, webhook idempotency 원칙
- `business/notification-multichannel.md` — Dunning 3-stage 이메일/SMS
- `business/audit-log.md` — plan change, refund 추적
- `business/feature-flags.md` — plan-based gating, kill-switch
- `business/rate-limiting.md` — trial 어뷰즈, usage cap

---

## 1. Proration (가장 흔한 버그 발생 지점)

플랜 변경/취소가 주기 중간에 일어나면 차액을 계산해 다음 invoice에 반영.

### 시나리오 매트릭스

| 시나리오 | 처리 | UX 신호 |
|---|---|---|
| **Upgrade (mid-cycle)** | 즉시 차액 청구 또는 다음 invoice에 prorated charge | "지금 차액만 결제됩니다" |
| **Downgrade (mid-cycle)** | 다음 주기부터 적용 (잔여 기간 환불 X) 또는 credit balance 적립 | "다음 결제일부터 적용됩니다" |
| **Cancel mid-cycle** | 보통 주기 끝에 종료 (refund X). B2C는 즉시+환불 옵션 | "MM-DD까지 이용 가능" |
| **Quantity change (seat)** | mid-cycle 즉시 prorated. 추가 시 charge, 감소 시 credit | "5 → 7 seat 추가 차액" |
| **Trial → Paid 도중 변경** | trial 종료 시 새 plan으로 전환 | UI에 명시 |

### Stripe proration_behavior 옵션

| 값 | 동작 | 적합 |
|---|---|---|
| `create_prorations` (default) | 차액을 invoice item으로 추가, 다음 invoice에 합산 | B2B SaaS 표준 |
| `always_invoice` | 즉시 invoice 발행 + 결제 시도 | 즉시 차액 받고 싶을 때 |
| `none` | proration 없음, 다음 주기부터만 적용 | 단순 모델, downgrade 표준 |

### 주의

- **연간 → 월간 downgrade**: 잔여 기간 처리 ADR 필수. credit balance / 환불 / 만료까지 유지 — 비즈니스 정책 사항.
- **세금/할인 함께 proration**: Stripe Tax는 자동 계산하지만 자체 구현 시 매우 까다롭다. **Tax SaaS (Stripe Tax / Avalara) 위임 권장**.
- **시간대**: subscription의 `current_period_end`는 UTC. 사용자 표시는 tenant timezone 변환.

---

## 2. Dunning (결제 실패 → 회수)

결제 실패 시 자동 재시도 + 사용자 통지 + 점진적 강제. **dunning 설계가 LTV의 핵심 변수.**

### Smart Retry 흐름 (Stripe 표준)

```
payment_failed
  └─ Smart Retry 1회차 (1~3일)
       └─ 실패 → 이메일 1차 (soft reminder)
            └─ Retry 2회차 (3~5일)
                 └─ 실패 → 이메일 2차 (urgency)
                      └─ Retry 3회차 (7일)
                           └─ 실패 → 이메일 3차 (final notice)
                                └─ 4회차 (10~14일)
                                     └─ 실패 → unpaid → 기능 차단
```

**Stripe Smart Retries**: ML로 카드사별 성공 확률 높은 시점에 재시도. 자체 cron보다 +20~40% 회수율.

### 카드 라이프사이클 대응

| 실패 원인 | Stripe 자동 처리 | 자체 구현 시 |
|---|---|---|
| 만료 카드 | **Card Account Updater** (Visa/MC/Amex) — 자동 갱신 | 사용자에게 카드 재등록 요청 |
| 카드 분실/재발급 | Network Tokens로 새 PAN 자동 매핑 | 유저 액션 필요 |
| 한도 초과/잔액 부족 | Smart Retry 시점 분산 | 직접 cron + 백오프 |
| 사기 의심/승인 거절 | Stripe Radar | 별도 사기 탐지 |
| 카드 정지 | 사용자 통지 | 사용자 통지 |

→ **결론**: 가능하면 Stripe/PG 내장 dunning 사용. 자체 구현 시 retry 일정 + 카드 사이클 모두 처리.

### Dunning 이메일 템플릿 (3-stage)

| 단계 | 시점 | 톤 | 액션 버튼 |
|---|---|---|---|
| Soft (1차) | 실패 직후 | 친절, "일시적일 수 있어요" | "결제 정보 확인" |
| Urgent (2차) | 3~5일 후 | 명확, "기능 제한이 임박" | "지금 카드 업데이트" |
| Final (3차, 7일+) | 차단 직전 | 최종, "MM-DD에 차단 예정" | "결제 / 해지" 동시 노출 |

→ 다채널 통지: 이메일 + 인앱 + 옵션 SMS. `business/notification-multichannel.md` 결합.

### 운영 메트릭 (요약)

- Involuntary churn rate, Recovery rate, Smart Retry 단계별 성공률, MRR loss from past_due
- 상세 SQL/대시보드: `subscription-billing-metrics.md`

---

## 3. Plan Change (Upgrade / Downgrade / Quantity)

### 결정 매트릭스

| 변경 유형 | 기본 정책 | 예외 |
|---|---|---|
| Upgrade (가격↑) | **즉시 적용** + prorated charge | 명시적 "다음 주기부터" 옵션 |
| Downgrade (가격↓) | **다음 주기부터 적용** | B2C는 즉시 옵션 (UX) |
| Seat 추가 | 즉시 + prorated charge | (없음) |
| Seat 감소 | 다음 주기부터 / credit balance | 즉시 환불은 비추 |
| Annual ↔ Monthly | ADR 필수 (할인율/잔여) | — |
| Add-on 추가/제거 | upgrade와 동일 | — |
| Trial 도중 변경 | trial 유지, 종료 시 새 plan | — |

### 구현 흐름

```
PUT /subscriptions/{id}
  body: { items: [{ price: "price_pro_monthly", quantity: 1 }] }

서버:
  1. 권한 검증 (tenant admin만)
  2. 변경 가능 상태 확인 (active / trialing만)
  3. PG API: subscription.update + proration_behavior 명시
  4. 응답에서 upcoming_invoice 미리보기 → 사용자 확인 (선택)
  5. audit-log: plan_changed 이벤트
  6. feature-flags 평가 즉시 갱신 (캐시 무효화)
```

**미리보기 필수**: `POST /invoices/upcoming` (Stripe)으로 변경 후 청구액 미리보기 → 사용자 동의 후 실제 변경. "예상치 못한 청구" 컴플레인 최대 차단.

```python
# Plan change with preview — 사용자 동의 후 적용
def change_plan(subscription_id: str, new_price_id: str, actor: User):
    sub = stripe.Subscription.retrieve(subscription_id)
    require_admin(actor, sub.tenant_id)            # RBAC 검증
    require_status_in(sub, ["active", "trialing"]) # 변경 가능 상태

    # 1단계: 미리보기만 (실제 변경 X)
    preview = stripe.Invoice.upcoming(
        customer=sub.customer,
        subscription=sub.id,
        subscription_items=[{"id": sub["items"].data[0].id, "price": new_price_id}],
        subscription_proration_behavior="create_prorations",
    )
    if not user_confirms(preview.amount_due, preview.lines):
        return                                     # 사용자 거부

    # 2단계: 실제 변경 (idempotency_key로 중복 차단)
    updated = stripe.Subscription.modify(
        subscription_id,
        items=[{"id": sub["items"].data[0].id, "price": new_price_id}],
        proration_behavior="create_prorations",
        idempotency_key=f"plan_change:{subscription_id}:{new_price_id}:{int(time.time())}",
    )
    audit_log.write("plan_changed", actor=actor.id, before=sub, after=updated)
    feature_flags.invalidate(sub.tenant_id)        # 즉시 반영
```

**원칙**: preview → 동의 → 실제 변경 → audit-log → feature-flag 캐시 무효화. preview 단계에서 거부 시 부작용 0.

---

## 4. Invoice 처리 + Multi-currency

### 라이프사이클

```
draft → finalize → open → (paid | uncollectible | void)
```

| 상태 | 의미 | 가능 액션 |
|---|---|---|
| `draft` | 생성 중, 변경 가능 | line item 추가/삭제, 발행 |
| `open` | 발행됨, 미결제 | 결제 시도, void, 부분 결제 |
| `paid` | 전액 결제 완료 | 환불(credit note) |
| `uncollectible` | 회수 포기 (write-off) | (terminal) |
| `void` | 무효 처리 | (terminal) |

### 핵심 원칙

- **Invoice는 immutable**: 발행 후 line item 수정 금지. 오류 시 credit note 발행.
- **PDF/legal text는 PG에 위임**: 자체 PDF 생성은 폰트/세금 표기/회계 기준 등 함정 多.
- **세금 자동화**: Stripe Tax / Avalara / TaxJar. 자체 구현은 EU/US sales tax/한국 부가세 모두 비추.
- **이메일 첨부 vs 링크**: 링크 + 영구 보관 URL 권장. 첨부는 큰 PDF + spam 위험.
- **회계 시스템 연동**: invoice ID = 회계 시스템 invoice number 매핑.

### 한국 특수성

- **세금계산서**: 부가세 별도 발행 (Bill36524 / 더존 / 자체 ERP 연동)
- **현금영수증**: B2C 의무 발행 (PG가 처리하기도 함)
- **카드 영수증 vs 세금계산서**: 동일 거래에 둘 다 발행 금지 (이중 처리)

### Multi-currency / FX (글로벌 SaaS 핵심 함정)

| 패턴 | 권장 | 이유 |
|---|---|---|
| **통화별 PlanVersion 분리** | ✅ 권장 | USD/KRW/EUR 별 Price 객체. 환율 계산 회피, 지역별 가격 정책 |
| **단일 base currency + FX 변환** | ⚠️ 비추 | 환율 변동으로 매월 청구액 달라짐, 회계 헬 |
| **Customer currency lock** | ✅ 필수 | 첫 결제 시 통화 고정. 변경 시 새 customer 또는 명시적 승인 |
| **Stripe Multi-currency Prices** | ✅ 추천 | 단일 Price ID에 통화별 amount 매핑, 자동 라우팅 |
| **반올림 정책 ADR** | ✅ 필수 | KRW=정수, USD/EUR=2 decimal, JPY=정수. proration 시 0.5원 단위 처리 |

**핵심 결정**:
- **Pricing**: 환율 자동 변환 vs 지역별 수동 (예: $10 ≠ ₩13,000 PPP 조정). 보통 **수동 + 분기 재검토**.
- **Refund 시 통화**: 결제 통화로 환불. cross-currency 환불 금지 (FX 손실 분쟁).
- **Display vs charge**: UI는 사용자 locale, 결제는 customer locked currency. 불일치 시 명시.
- **세금**: 통화별 세율 다름 (KR VAT 10%, JP CT 10%, EU VAT 17~27%). Stripe Tax / Avalara 위임 권장.
- **한국 단일 통화 SaaS**: Multi-currency 무시 가능. 글로벌 진출 시 새 customer + 새 subscription으로 마이그레이션 (in-place 변환은 회계 거부).

---

## 5. Usage-based Billing (Metered)

`credit-system.md`(P2-A 후속)와 깊이 연결. 구독 컨텍스트의 핵심.

### 패턴

```
사용 발생 (API call / token / GB)
  ▼
UsageRecord 생성 (idempotency_key 필수)
  ▼
배치 또는 실시간으로 PG에 report
  ▼
주기 종료 시 invoice에 합산
```

### Stripe Meters (2025+)

기존 `usage_records` API → **Meters + Events** 모델로 전환. 1초당 1k+ 이벤트 처리, 집계 함수 (sum/count/last/max).

### 주의

- **Idempotency**: 같은 사용 이벤트 재시도 시 1번만 카운트. `idempotency_key` 필수.
- **Late events**: 주기 종료 후 도착 이벤트는 **다음 주기로** 또는 `void` (정책 결정 필요).
- **Cap/Threshold**: 사용량 폭증 방지. Threshold 도달 시 알림 + 자동 차단 옵션 (`business/rate-limiting.md` 결합).
- **Free tier (예: 월 1만 콜 무료)**: usage_record는 다 기록, invoice 계산 시 차감.

---

## 6. Trial 관리 + 어뷰즈 방지

| 패턴 | 적합 | 어뷰즈 위험 |
|---|---|---|
| Free trial (카드 등록 안 받음) | 전환율↑, B2C | 멀티계정 어뷰즈 高 |
| Free trial (카드 등록 받음) | B2B SaaS 표준 | 어뷰즈 低, 전환율 다소↓ |
| Reverse trial (Pro로 시작 → 만료 후 Free) | "기능 맛보기" UX | 어뷰즈 中 |
| Pay-and-trial (소액 결제 후 시작) | 어뷰즈 최소화 | 전환율↓ |

### 어뷰즈 방지

- **Email/도메인 제한**: 같은 회사 도메인은 1 trial. (`business/multi-tenancy.md` tenant 결합)
- **Device fingerprint / IP 제한**: [`anti-bot`](../anti-bot/SKILL.md) 활용
- **Card fingerprint**: Stripe `card.fingerprint`로 동일 카드 탐지 (PCI 안전)
- **Rate limiting**: trial 시작 endpoint에 IP/계정 단위 limit (`business/rate-limiting.md`)

---

## 7. Multi-tenancy 결합 (B2B SaaS Seat 모델)

| 모델 | 구독 위치 | 적합 |
|---|---|---|
| **Tenant 단위 구독** | Subscription.tenant_id | B2B SaaS 표준. 회사가 결제. |
| **사용자 단위 구독** | Subscription.user_id | B2C, individual 라이센스 |
| **Seat 모델** | Subscription.quantity = 사용자 수 | B2B 팀 라이센스 |
| **Hybrid** | base seat + usage | 2026 트렌드 (AI 제품) |

### Seat 관리

```
Tenant: 5 seat 구입
  ├─ 사용자 4명 active → 1 seat 여유
  ├─ 6번째 invite 시도 → "seat 부족, 추가하시겠습니까?"
  └─ admin이 추가 → quantity=6, prorated charge
```

- **Active seat 정의**: 30일 내 로그인 / 마지막 로그인 / 명시적 active 토글 — ADR 필수
- **Seat 회수**: 사용자 deactivate → 즉시 seat 반환 vs 주기 끝에 반환
- **Owner/Admin**: 결제 권한은 admin only. `business/auth-oauth-social.md` + RBAC.

→ 상세: `business/multi-tenancy.md`

---

## 다음 단계

- 메트릭/대시보드 구축 → `subscription-billing-metrics.md`
- 도메인 모델/상태 머신/Webhook 기본/ADR 템플릿 → `subscription-billing.md` (메인 hub)
- AI 사용량 모네타이징 → `business/credit-system.md` (P2-A 후속 예정)
