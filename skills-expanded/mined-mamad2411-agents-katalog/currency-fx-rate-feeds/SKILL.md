---
name: currency-fx-rate-feeds
description: >
  Design and operate FX rate feeds for owned fintech/commerce systems: source
  selection, staleness SLAs, mid vs bid/ask, base currency normalization,
  failover, and auditability of conversion. Use when pricing, payouts, or
  reporting depend on external FX APIs or ECB/central-bank files — not market
  abuse or unauthorized data scraping.
---

# Currency FX Rate Feeds

## Scope And Authorization

- **In scope:** Rate ingestion, storage, and conversion services for products you operate under licensed/authorized business use of data providers.
- **Out of scope:** Scraping bank sites against ToS; trading/manipulation schemes; using feeds for unlicensed financial advice products without compliance review.
- Prefer paper trading / sandbox keys for provider integration tests.
- Redact API keys; treat rate history as business-sensitive.
- Pair with `code-quality-standards`, retry/backoff, and secrets hygiene.

## When To Use

- Multi-currency checkout, wallet balances, or settlement.
- Choosing providers (commercial FX API, central bank XML/CSV, broker).
- Defining “rate as of” timestamps and cutover rules.
- Handling missing pairs, peg breaks, and flash anomalies.
- Auditing which rate was used for a historical transaction.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Payment card processing | payments skills |
| General retry/backoff | `retry-backoff-patterns` |
| Secrets for API keys | `secrets-management-hygiene` |
| Observability | `observability-metrics-tracing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain model

| Concept | Notes |
| --- | --- |
| Base / quote | `EURUSD` = USD per 1 EUR (confirm provider convention!) |
| Mid / bid / ask | Pricing policy must pick one; spreads matter for payouts |
| As-of time | UTC timestamp of observation vs effective business date |
| Staleness SLA | Max age before fail/fallback |
| Cross rates | Via USD or EUR when direct pair missing |
| Inverse | `1/rate` with precision rules |

## Workflow

### 1. Confirm scope and success criteria

1. Currencies supported; regulatory constraints; provider contracts.
2. Success: conversions reproducible from stored snapshots; SLA alerts; failover tested; no silent stale rates on money movement.

### 2. Select sources

| Source type | Good for | Watch |
| --- | --- | --- |
| Licensed commercial API | Low latency, many pairs | Cost, ToS, accuracy SLA |
| Central bank daily | Accounting reference | Not real-time; limited pairs |
| Broker/LP | Trading desks | Connectivity, licensing |
| Manual ops override | Incidents | Strict audit + dual control |

Prefer **two independent sources** for critical paths when budget allows.

### 3. Ingest pipeline

```text
fetch → validate schema → anomaly checks → persist snapshot → publish current → metrics
```

```python
# Pseudo validation
def validate_tick(pair: str, rate: Decimal, ts: datetime, now: datetime) -> None:
    if rate <= 0:
        raise ValueError("non-positive rate")
    if now - ts > STALE_AFTER:
        raise ValueError("stale")
    if pair in last and abs(rate - last[pair]) / last[pair] > SPIKE_PCT:
        flag_anomaly(pair, rate)  # may quarantine
```

### 4. Storage for audit

```sql
-- Example
create table fx_rate_snapshot (
  id bigserial primary key,
  pair text not null,
  rate numeric(24,12) not null,
  source text not null,
  observed_at timestamptz not null,
  ingested_at timestamptz not null default now(),
  unique (source, pair, observed_at)
);
```

Money movement rows should store: `pair`, `rate`, `source`, `observed_at`, `conversion_id`.

### 5. Conversion API

```text
POST /v1/convert { "amount": "100.00", "from": "USD", "to": "EUR", "as_of": "..." }
→ { "amount": "91.23", "rate": "...", "source": "...", "observed_at": "..." }
```

Rules:

1. Use fixed decimal arithmetic (`Decimal`), not binary float.
2. Rounding mode documented (half-even vs half-up) per product/legal.
3. Reject if rate older than SLA unless `allow_stale` + elevated role.
4. Cross via configured pivot with precision policy.

### 6. Failover and incidents

| Failure | Response |
| --- | --- |
| Provider 5xx/timeout | Retry with jitter; secondary source |
| Anomaly spike | Freeze pair; alert; last good within SLA or halt conversions |
| Partial pair set | Degrade only affected currencies |
| Total outage | Queue non-critical; block settlement if policy requires live rates |

### 7. Verify

```bash
# Health
curl -sS https://fx.example.local/v1/rates/EURUSD | jq .
# Staleness metric alert test
# Replay: given snapshot id, conversion matches historical payment
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Precision | Decimal + policy | IEEE float money |
| Audit | Store rate used on txn | Recompute years later from “latest” |
| Stale | Fail closed on payouts | Silent 3-day-old rates |
| Anomaly | Quarantine + human | Blind accept 100x spike |
| Convention | Document pair notation | Mix inverted pairs |

## Output Checklist

- [ ] Provider licenses and pairs documented
- [ ] Mid/bid/ask policy chosen
- [ ] Ingest validation + anomaly rules
- [ ] Snapshot storage with as-of
- [ ] Conversion uses Decimal + rounding policy
- [ ] Txns persist rate metadata
- [ ] Staleness SLA + alerts
- [ ] Failover path tested
- [ ] Secrets for API keys secured
- [ ] Residual risk (weekend gaps, pegs) noted

## Rules

- Money paths fail closed on missing/stale/anomalous rates unless product explicitly allows.
- Honor data provider ToS and licensing.
- Focus on **FX rate feed design and operations**.
