---
name: perf-budget
description: Set a perf budget — per critical user journey, single percentile + threshold, explicit budget components (network / compute / dependencies), tripwire alerts. Backend journeys; not web CWV or mobile.
---

# perf-budget

> A perf budget is a contract per critical user journey. One percentile, one threshold, components named. Without that, "make it fast" is the spec.

## When to use

- A new service or page is shipping and the team wants a target before code.
- An existing surface keeps regressing because the target was never written down.

## Inputs

- The critical user journey (CUJ) — one journey, not the whole service.
- The audience tier (high-end-desktop / median-mobile / low-end-mobile for frontend; in-datacenter / cross-region for backend).

## Procedure

1. **Pin the CUJ.** Example: "User opens /checkout and sees totals." Not "/checkout responds 200".
2. **Pick the percentile.** P95 or P99 — pick one. Avoid pyramid targets (P50 + P99 stacked).
3. **Pick the threshold.** Tied to user expectation, not "round number". For interactive: 200ms / 500ms / 1s are common thresholds. For batch: minutes.
4. **Decompose the budget** into components and pre-allocate ms per component:
   - Network / DNS / TCP / TLS.
   - CDN / origin.
   - Application compute (handler + middleware + serialization).
   - Database / cache / external API calls.
   - Render / hydration (frontend only).
   The sum should be ≤ threshold, with ≥ 20% headroom.
5. **Tripwire alerts**: an alert fires when the P-percentile crosses 80% of the threshold over a 10-minute window. Catches degradation before the budget is blown.
6. **Renegotiation rule**: budget can only be moved with an ADR. "We need more time for X" is not a budget change.

## Output

```text
Perf budget: /checkout sees totals (P99 latency)

CUJ: User loads /checkout after adding 1+ items.
Audience: median-mobile.
Percentile: P99.
Threshold: 1,000 ms.

Component allocations (sums to 800 ms; 200 ms headroom):
  Network (DNS+TCP+TLS):    150 ms
  CDN/origin fetch:         100 ms
  Handler + middleware:     150 ms
  Cart DB query:            120 ms
  Pricing service call:     180 ms
  Frontend render:          100 ms

Tripwire: P99 > 800 ms over a 10-min window → page sev3.
Renegotiation: requires ADR + sign-off from <role>.
```

## Quality bar

- One CUJ per budget.
- One percentile + one threshold.
- Components sum to ≤ threshold with 20% headroom named.
- Tripwire alert pre-fires at 80% of budget.
- Renegotiation gated through an ADR.

## Anti-patterns to avoid

- Pyramid targets (P50 + P99 + ...). Pick one.
- Budget without component breakdown. You can't tell what's eating it.
- Threshold at "round number". Match user expectation.
- Allowing budget changes by Slack ping. ADR-gate it.
