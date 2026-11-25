---
name: subscription-billing-metrics
category: business
description: "Subscription Billing — Metrics & Dashboards — 구독 비즈니스 메트릭 — MRR/ARR/Churn/Cohort SQL + Grafana 대시보드 + 외부 도구. `subscription-billing.md`(메인 hub)의 회고/운영 분석 단계 분리. Use when working with business 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Subscription Billing — Metrics & Dashboards

구독 비즈니스 메트릭 — MRR/ARR/Churn/Cohort SQL + Grafana 대시보드 + 외부 도구. `subscription-billing.md`(메인 hub)의 회고/운영 분석 단계 분리.

**회고 약점은 메트릭으로 채운다** — 데이터 없이는 "왜 churn이 늘었는가" 답할 수 없음. 이 문서는 SQL/대시보드 패널/도구 선택 가이드를 제공한다.

## When to Use

- 구독 비즈니스 분기 회고, 월간 MRR 리포팅
- Churn 원인 분석 (Voluntary vs Involuntary 분기)
- Cohort retention 추적, LTV 계산
- Grafana / Metabase / ChartMogul 대시보드 구축
- Dunning 단계별 효과 측정

**관련 skill**:
- `business/subscription-billing.md` — 메인 hub, 도메인 모델 (invoices/subscriptions 테이블)
- `business/subscription-billing-flows.md` — Dunning/Plan Change 흐름 (메트릭 발생 지점)
- `observability/observability-cost.md` — cardinality 주의 (high-cardinality 라벨 회피)
- `sre/sli-slo.md` — billing SLO 정의 (webhook 처리 지연, reconciliation 정합)

---

## 1. 핵심 지표 (Tier 1)

| 지표 | 정의 | 측정 주기 |
|---|---|---|
| **MRR / ARR** | 활성 구독의 월/연 환산 매출 | 일간 |
| **MRR Movement** | New + Expansion + Reactivation − Contraction − Churn | 월간 |
| **Gross / Net Churn Rate** | (Churned MRR) / (Start MRR), Expansion 차감 후 = Net | 월간 |
| **Voluntary vs Involuntary Churn** | 사용자 해지 vs 결제 실패 미회수 | 월간 |
| **Recovery Rate** | dunning으로 회수된 invoice / past_due 발생 invoice | 주간 |
| **LTV / CAC Ratio** | Lifetime Value / Customer Acquisition Cost | 분기 |
| **Trial → Paid Conversion** | trial 시작 → 결제 전환율 | 주간 |
| **Cohort Retention Curve** | 가입월 코호트별 N개월 후 잔존율 | 월간 |

**원칙**:
- Voluntary vs Involuntary 분기는 필수. 둘은 다른 문제(UX vs 결제 인프라)이고 다른 액션을 부른다.
- LTV는 cohort 기반 계산이 정확. 평균 churn rate 기반은 새 cohort에 부적합.
- Net MRR Movement < 0이면 "성장 정체" 첫 신호.

---

## 2. MRR Movement SQL (월간 분해)

```sql
-- PostgreSQL, subscriptions/invoices 도메인 테이블 가정
WITH monthly_state AS (
  SELECT
    date_trunc('month', period_start) AS month,
    customer_id,
    SUM(amount_paid) / 100.0 AS mrr  -- cents → 단위 통화
  FROM invoices
  WHERE status = 'paid'
  GROUP BY 1, 2
)
SELECT
  curr.month,
  SUM(CASE WHEN prev.mrr IS NULL THEN curr.mrr END) AS new_mrr,
  SUM(CASE WHEN curr.mrr > prev.mrr THEN curr.mrr - prev.mrr END) AS expansion_mrr,
  SUM(CASE WHEN curr.mrr < prev.mrr THEN prev.mrr - curr.mrr END) AS contraction_mrr,
  SUM(CASE WHEN curr.mrr IS NULL THEN -prev.mrr END) AS churned_mrr,
  SUM(curr.mrr) - SUM(COALESCE(prev.mrr, 0)) AS net_mrr_change
FROM monthly_state curr
LEFT JOIN monthly_state prev
  ON prev.customer_id = curr.customer_id
  AND prev.month = curr.month - INTERVAL '1 month'
GROUP BY curr.month
ORDER BY curr.month DESC;
```

**해석**:
- `new_mrr`: 이번 달 처음 결제한 신규 고객
- `expansion_mrr`: 기존 고객의 plan upgrade / seat 추가
- `contraction_mrr`: downgrade / seat 감소
- `churned_mrr`: 이번 달 결제 없는 이전 고객
- `net_mrr_change`: 이번 달 순증감

**주의**: prorated charge는 한 invoice에 합산되어 amount_paid에 영향. 정확한 MRR은 `subscription_items.unit_amount * quantity`로 산출 가능 (Stripe data sync 필요).

---

## 3. Cohort Retention SQL

```sql
-- 가입월 코호트별 N개월 후 잔존
WITH cohorts AS (
  SELECT customer_id, date_trunc('month', created_at) AS cohort_month
  FROM subscriptions WHERE status != 'canceled' OR canceled_at > created_at
)
SELECT
  c.cohort_month,
  EXTRACT(month FROM age(date_trunc('month', i.period_start), c.cohort_month)) AS month_offset,
  COUNT(DISTINCT c.customer_id) AS retained
FROM cohorts c
JOIN invoices i ON i.customer_id = c.customer_id AND i.status = 'paid'
GROUP BY 1, 2
ORDER BY 1, 2;
```

**시각화**: month_offset을 가로축, cohort_month를 세로축으로 한 retention 히트맵. 월별 코호트 비교로 retention 트렌드 파악.

---

## 4. Voluntary vs Involuntary Churn 분기 SQL

```sql
-- 해지 사유별 분류 (cancellation_reason은 cancel API에서 받거나 자체 라벨링)
SELECT
  date_trunc('month', canceled_at) AS month,
  CASE
    WHEN cancellation_reason IN ('payment_failed', 'card_expired') THEN 'involuntary'
    WHEN cancellation_reason IN ('user_canceled', 'too_expensive', 'unused') THEN 'voluntary'
    ELSE 'unknown'
  END AS churn_type,
  COUNT(*) AS count,
  SUM(mrr_at_cancel) / 100.0 AS lost_mrr
FROM subscriptions
WHERE canceled_at IS NOT NULL
GROUP BY 1, 2
ORDER BY 1 DESC, 2;
```

→ Involuntary 비율이 높으면 dunning/Card Updater 강화 (`subscription-billing-flows.md` §2 Dunning).
→ Voluntary 비율이 높으면 UX/가격/기능 문제 (cancellation_reason 추가 분석).

---

## 5. Grafana 대시보드 패널 (권장 구성)

| 패널 | 데이터 소스 | 쿼리 |
|---|---|---|
| MRR 추이 (12개월) | PostgreSQL | §2 MRR Movement |
| Net MRR Movement (월별 stacked bar) | PostgreSQL | §2의 new/expansion/contraction/churned |
| Churn rate (Voluntary vs Involuntary) | PostgreSQL | §4 |
| Dunning funnel | PostgreSQL/Prom | 1차/2차/3차 단계별 회수율 |
| Trial 전환율 | PostgreSQL | trial_end 시점 active 비율 |
| Cohort Retention 히트맵 | PostgreSQL | §3 |
| Past_due 잔액 alert | Prometheus | `sum(past_due_mrr) > threshold` |
| Webhook 처리 지연 | Prometheus histogram | p99 (`payment-integration` §4 기준) |
| Reconciliation drift | Prometheus | `pg_subs_count - stripe_subs_count != 0` |

**알림 규칙 예시**:
- Net MRR < 0 (월말 마감): Slack #revenue
- Recovery rate < 60% (주간): #billing-ops
- Webhook 처리 지연 p99 > 5s: PagerDuty (incident)
- Reconciliation drift > 10건: #billing-ops (즉시)

→ cardinality 주의: tenant_id, customer_id를 라벨로 직접 넣지 말 것 (`observability/observability-cost.md`).

---

## 6. 외부 도구 (Build vs Buy)

| 도구 | 적합 | 가격 |
|---|---|---|
| **ProfitWell** (Paddle 인수) | 기본 MRR/Churn 분석 | 무료 |
| **ChartMogul** | 엔터프라이즈 구독 분석, NRR/GRR/LTV 자동 | 유료 (월 $129~) |
| **Stripe Sigma** | Stripe 데이터 SQL 직접 쿼리, 자체 SQL 작성 | Stripe 거래액 0.02% |
| **Metabase / Cube.dev** | 자체 BI 구축 (PG 쿼리 기반) | 오픈소스 / 자체 호스팅 |
| **Looker / Mode / Hex** | 데이터팀 있을 때 | 유료 |

### 결정 기준

| 상황 | 추천 |
|---|---|
| MVP, 데이터팀 없음 | ProfitWell (무료) |
| Stripe 단독, 자체 SQL 필요 | Stripe Sigma |
| 다중 PG, 자체 도메인 모델 | Metabase + 자체 SQL (위 §2~4 재사용) |
| 엔터프라이즈, NRR/cohort 자동화 | ChartMogul |

→ ADR 결정. **PII/매출 데이터 외부 전송 정책 필수** — 컴플라이언스(SOC2/GDPR/PCI) 검토.

---

## 7. 안티패턴

| 안티패턴 | 왜 위험 |
|---|---|
| MRR을 `amount_paid` 단순 합으로 계산 | prorated charge로 변동성 큼. `unit_amount * quantity` 권장 |
| Voluntary/Involuntary 분기 안 함 | UX 문제와 인프라 문제 섞여 액션 불가 |
| Churn rate 계산을 customer 단위 | MRR 가중치 무시 — 큰 고객 1명 이탈 = 작은 고객 100명 이탈로 동치 처리됨 |
| Cohort를 user_count로만 측정 | revenue cohort가 더 의미 있음 |
| Trial 전환율을 일간 변동으로 의사결정 | 통계적 유의미성 부족, 주/월 단위 권장 |
| 외부 도구에 PII 전송 (이름/이메일) | GDPR/PCI 위반. 익명 ID로 매핑 |

---

## 다음 단계

- 도메인 모델 (invoices/subscriptions 스키마) → `subscription-billing.md` §2
- 운영 흐름 (Dunning/Plan Change 발생 지점) → `subscription-billing-flows.md`
- SLO 정의 (webhook 지연, reconciliation 정합) → `sre/sli-slo.md`
- 비용 (대시보드 자체 비용) → `observability/observability-cost.md`
