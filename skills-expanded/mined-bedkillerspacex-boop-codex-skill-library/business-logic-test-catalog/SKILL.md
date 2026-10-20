---
name: business-logic-test-catalog
description: >
  Catalog of business-logic test cases for owned apps: workflow skips, price/quantity
  manipulation, race conditions, coupon abuse, privilege steps, limit bypass, and
  multi-step state machines. Use when building QA/security test matrices for logic
  flaws, or systemizing tests beyond injection — pair with `business-logic-vuln` for
  exploitation narrative and fixes.
---

# Business Logic Test Catalog

## Scope And Authorization

- **In scope:** Applications you own or are authorized to test; use test tenants and payment sandboxes.
- **Out of scope:** Fraud against production payment rails; harming real customers; out-of-policy bounty techniques.
- Prefer non-prod for destructive races; production only with explicit RoE and micro-PoC.
- Redact personal and payment data from catalogs and evidence.
- Pair findings analysis with `business-logic-vuln`; authz with IDOR skills.

## When To Use

- Building a reusable regression pack for logic abuse cases.
- Expanding coverage beyond OWASP injection lists into **stateful** abuse.
- Onboarding testers with app-specific workflows (checkout, claims, trading).
- Mapping controls: rate limits, idempotency, server-side price trust.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Deep narrative of a logic flaw class | `business-logic-vuln` |
| Classic injection (SQLi/XSS) | injection skills |
| Pure IDOR object access | `idor-broken-object-authorization` |
| Load/perf only | perf skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Category | Abuse theme |
| --- | --- |
| Workflow | Skip steps, replay old steps, reorder |
| Economic | Negative qty, price override, FX rounding |
| Limits | Cap bypass, quota reset tricks |
| Identity | Horizontal/vertical privilege in flows |
| Time | Expiry ignore, timezone, schedule races |
| Promo | Stacking coupons, self-referral |
| Concurrency | Double-spend, double-claim races |
| Files/jobs | Reprocess final states |

## Workflow

### 1. Confirm scope and success criteria

1. List critical business processes and money/trust boundaries.
2. Success: catalog linked to automated or manual cases; each case has expected reject; owners for gaps.
3. Identify test payment methods and feature flags.

### 2. Map state machines

```text
Example checkout:
Cart → Quote → PaymentAuth → Capture → Fulfill → Complete
Illegal: Complete without PaymentAuth; Capture twice; edit price after Quote lock
```

1. For each state, list allowed transitions and actors.
2. Note client-visible fields vs server-authoritative fields.
3. Record idempotency keys and lock points.

### 3. Use the catalog (customize per app)

**A. Workflow integrity**

| ID | Case | Probe | Expected |
| --- | --- | --- | --- |
| W1 | Skip step | Jump to final API without prior | 4xx |
| W2 | Replay completed | Re-POST complete | No double side effect |
| W3 | Old version | Submit stale quote id after price change | Reject or reprice |
| W4 | Out-of-order | Fulfill before pay | Reject |
| W5 | Parallel branches | Two tabs different steps | Consistent final state |

**B. Economic / value**

| ID | Case | Probe | Expected |
| --- | --- | --- | --- |
| E1 | Client price | Lower `unit_price` in body | Server price used |
| E2 | Negative quantity | `qty=-1` | Reject |
| E3 | Overflow qty | Huge qty | Reject / cap |
| E4 | Currency mismatch | Pay currency ≠ quote | Reject |
| E5 | Rounding | Split payments / tax edges | Accounting invariants hold |

**C. Promotions / referrals**

| ID | Case | Probe | Expected |
| --- | --- | --- | --- |
| P1 | Stack forbidden coupons | Apply two exclusives | One only |
| P2 | Expired coupon | Backdated clock not trusted | Reject |
| P3 | Self-referral | Same payment instrument / device policy | Block per policy |
| P4 | Reuse one-time code | Second redemption | Reject |

**D. Limits and quotas**

| ID | Case | Probe | Expected |
| --- | --- | --- | --- |
| L1 | Daily cap | Exceed via many small | Cap enforced server-side |
| L2 | Race to cap | Parallel requests | No over-grant |
| L3 | Other tenant quota | Swap tenant id | 403 |

**E. Authz in workflows**

| ID | Case | Probe | Expected |
| --- | --- | --- | --- |
| A1 | Horizontal | User B order id in user A flow | 403/404 |
| A2 | Vertical | User hits admin approve | 403 |
| A3 | Step-up skip | Skip MFA challenge token | Reject |

**F. Concurrency**

| ID | Case | Probe | Expected |
| --- | --- | --- | --- |
| C1 | Double submit | Parallel pay confirm | One capture |
| C2 | Double redeem | Parallel coupon | One success |
| C3 | Inventory | Oversell race | No negative stock |

**G. Miscellaneous**

| ID | Case | Probe | Expected |
| --- | --- | --- | --- |
| M1 | Feature flag | Disabled flow API still open | 404/403 |
| M2 | Webhook replay | Old signed webhook | Reject/idempotent |
| M3 | Export re-run | Reprocess job | Idempotent |

### 4. Instrument tests

```bash
# Example: race harness against staging only
# seq + xargs or k6 scenario for C1/C2
k6 run races/double_capture.js
pytest -q tests/logic/ --env=staging
```

1. Tag tests `@logic @money @race`.
2. Prefer API-level tests; add UI for true multi-tab cases.
3. Assert **business invariants** (balance, stock, single capture) not only HTTP 200.

### 5. Track controls

| Control | Maps to cases |
| --- | --- |
| Server-side pricing | E* |
| Idempotency keys | W2, C1, M2 |
| DB constraints / locks | C*, L2 |
| Authz middleware | A* |
| Feature flags | M1 |
| Rate limits | L* support |

### 6. Report gaps

1. Missing case → ticket with invariant statement.
2. Flaky race → fix app locks, not “sleep in test” only.
3. Feed new product features back into catalog in same PR as feature.

### 7. Hand off

1. Store catalog in repo (`docs/logic-test-catalog.md`) with owners.
2. CI: run non-destructive subset each PR; races nightly on staging.
3. Link serious flaws to `business-logic-vuln` write-ups.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Authority | Server prices | Trust client `total` |
| Races | Invariant asserts | Single-thread tests only |
| Data | Sandbox pays | Real card charges for tests |
| Catalog | Living with features | One-off pentest PDF only |
| Authz | Cross-user cases | Happy-path QA only |
| Status | Expect explicit reject | “200 with wrong state” accepted |

## Output Checklist

- [ ] Critical processes and state machines mapped
- [ ] Catalog customized with app-specific IDs
- [ ] Expected rejects documented
- [ ] Automated subset + race jobs defined
- [ ] Invariant assertions (money/stock) present
- [ ] Controls matrix linked
- [ ] Gaps ticketed
- [ ] Non-prod evidence retained (redacted)
- [ ] Feature process updates catalog
- [ ] Cross-link `business-logic-vuln` for confirmed issues

## Rules

- Test only authorized environments; protect real user funds and data.
- Assert business invariants, not just status codes.
- Keep the catalog living alongside product changes.
- Race tests can be destructive — isolate data.
- This skill is the **case library**; root-cause/fix patterns are in `business-logic-vuln`.
