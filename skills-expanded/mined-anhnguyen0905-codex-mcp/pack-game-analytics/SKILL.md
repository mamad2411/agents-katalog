---
name: pack-game-analytics
description: Generic game analytics and in-app purchase measurement rules for reproducible, language-consistent deliverables.
---

# Game analytics pack (embed into Codex prompts)

Serves: game analytics — R2.2

## Standards block

```
Game analytics pack standards:
- Payer: user with ≥1 `af_purchase` in the window.
- Rates/Payer conversion: Payer conversion=payers/active users (window); ARPU=revenue/active users; ARPPU=revenue/payers; ARPDAU=revenue/DAU. Name numerator, denominator, window, and n.
- Checkout conversion: purchasers/users with `af_initiated_checkout` (same window, same user).
- Revenue: IAP=sum of deduped `af_purchase` revenue. Measured LTV=IAP+ad revenue only when `af_ad_revenue` exists; otherwise label provisional (IAP only).
- Tiers: state Minnow/Dolphin/Whale thresholds as quantile (e.g. P90/P99 of payer LTV) or absolute, and say whether LTV includes ads.
- Retention: return=≥1 session/app-open event (e.g. `af_app_opened` or session-start) on install calendar day+n; Dn=returning users/installs in eligible cohorts (install date ≤ window end−n); state the denominator.
- Events: `af_initiated_checkout`=potential buyer, not purchase; `af_purchase`=buyer. Dedupe by `af_order_id` before buyers or revenue. Funnel=initiated→purchased by same user within window. Failure shares divide by failed attempts.
- BigQuery: filter `_TABLE_SUFFIX` or partition date to the window; dry-run first; cap bytes billed read-only; never `SELECT *` on raw event tables.
- Small samples: report n with every rate; below a stated threshold (e.g. n<100 users or <30 events/cell), mark “insufficient sample” instead of ranking. A/B: state variant sizes, test, CI, and SRM check.
- Cohorts: never mix install-version and event-version cohorts; reconcile subtotals with totals.
- Vietnamese: on first use, write each English term as Vietnamese term (English term): người trả tiền (payer), nhóm người dùng (cohort), tỷ lệ giữ chân (retention), doanh thu (revenue). After that gloss the bare English term is fine; a bare use before it is a finding. Glosses in code, table header rows, comments, or URLs do not count; English (Vietnamese) is not a gloss.
```

## Core method

- Anchor every rate to its numerator, denominator, and window. Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Reconcile subtotals with the totals table before publishing. derived, unverified
- Keep install-version and event-version cohorts distinct. derived, unverified

## Failure modes

- Rates without denominators: reject the readout and add n. Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Duplicated orders: dedupe by af_order_id and reconcile sums. Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Immature Dn cohorts: exclude them and state eligibility. Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Unanchored prose numbers: attach a table, query, or invented example label. derived, unverified

## Reviewer checklist

- Confirm event, cohort, partition, and window definitions. derived, unverified
- Check every rate has n, every total reconciles, and small cells are marked. derived, unverified
- Confirm each English term in Vietnamese prose is glossed on first use, and A/B results include CI and SRM. Source: codex-flow run-language check (glossed terms pass).

## Provenance

- Payer: Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Rates/Payer conversion: Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Checkout conversion: derived, unverified.
- Revenue: Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Tiers: Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Retention: Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- Events: Source: local AppsFlyer game-economy analysis skill (metrics and QA reference).
- BigQuery: derived, unverified.
- Small samples: derived, unverified.
- Cohorts: derived, unverified.
- Vietnamese: Source: codex-flow run-language check (first-use gloss).
