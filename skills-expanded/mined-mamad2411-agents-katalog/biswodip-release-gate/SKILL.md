---
name: biswodip-release-gate
description: Build the evidence matrix, score the work out of 100 from evidence with mandatory caps, answer the absolute release blockers and write the final report with one honest release status. Use when asked whether something is production-ready, to score or grade a repository, to run a release gate, or to write a release or audit report.
license: Apache-2.0
metadata:
  author: Biswodip Goj
  version: 2.2.0
  homepage: https://github.com/Biswadipgoj
---
# Release gate — evidence matrix, score, one honest status

Phases 12–13. The score is a measurement, not a mood.

## 1. Evidence matrix

`reports/EVIDENCE-MATRIX-TEMPLATE.md`. Every requirement and every applicable gate:

```text
REQUIREMENT → IMPLEMENTATION (file:line) → TEST/PROCEDURE → RESULT → EVIDENCE → STATUS
```

`VERIFIED` requires all five: implementation location, procedure, actual result, date/commit, artifact. Anything else is `PARTIAL`, `UNVERIFIED`, `BLOCKED`, `OPEN` or `N/A` (with a reason). **Never convert `UNVERIFIED` to `VERIFIED` without new evidence.**

Pull the applicable gates from `references/02-master-shipping-gate.md` — 15 owner-mandated controls plus 2,200 gates across 120 domains. Grep the domain, do not read the file:

```bash
grep -n "^### " references/02-master-shipping-gate.md            # list the domains
grep -n -A11 "^### Webhooks" references/02-master-shipping-gate.md
```

## 2. Score

| Category | Weight |  | Category | Weight |
|---|---:|---|---|---:|
| Security | 25 | | Architecture / maintainability | 10 |
| Correctness / business integrity | 20 | | Performance | 5 |
| Reliability / failure handling | 15 | | Accessibility / responsive UX | 5 |
| Test / evidence quality | 15 | | Design / interaction | 5 |

Score each 0–10 from evidence, weight, sum. **A category with no evidence scores 0**, not "probably fine".

**Caps that override the number:** unresolved Critical → 49 · unresolved High in an exposed path → 69 · authorization bypass → 49 · exposed production secret → 49 (until rotated and contained) · unsafe financial state transition → 49 · fabricated or missing critical evidence → 59. All of these are blocked.

Bands: 90–100 gate may pass with no blocker and all mandatory evidence · 80–89 strong, gates still required · 70–79 substantial work remains · 0–69 blocked.

## 3. Absolute blockers — answer each yes/no from evidence

critical vulnerability · exposed production secret · browser-accessible privileged credential · broken authorization · unauthenticated privileged endpoint · cross-user or cross-tenant access · client-authoritative security or financial decision · unsafe financial state transition · known data-loss condition · unrecoverable migration risk · authentication bypass · unbounded resource exhaustion on a reachable endpoint · intentionally disabled control · security regression without compensating control · production debug functionality · unverified critical requirement · fabricated test evidence.

A high-risk finding that stays open needs documented acceptance by the authorized owner, with an expiry.

## 4. Final sequence

1. Build from a clean checkout. 2. Run unit, integration and security tests. 3. Scan dependencies and the built bundle for secrets. 4. Re-run the authorized adversarial tests on the candidate. 5. Validate migrations, rollback and a **tested** restore. 6. Validate observability and audit trails. 7. Review every unresolved finding. 8. Record evidence. Only then deploy.

## 5. Report

`reports/RELEASE-REPORT-TEMPLATE.md`. Include failures — a report that hides them is worthless. Run the prose through `no-ai-slop`: lead with the decision, keep detail concrete, no puffery.

**Status — exactly one:** `RELEASE READY` · `RELEASE READY WITH DOCUMENTED ACCEPTED RISKS` · `NOT RELEASE READY` · `BLOCKED — INSUFFICIENT EVIDENCE`.

Never: "looks good", "seems secure", "probably production ready", "should be fine", "everything is perfect".

## Exit gate

- [ ] Matrix complete, no blank statuses.
- [ ] Score computed from the matrix with caps applied.
- [ ] Every blocker answered from evidence.
- [ ] Evidence locations listed so someone else can re-check them.
- [ ] One status word, and it is honest.

Procedures: `lifecycle/12-score.md`, `lifecycle/13-release.md`. Detail: `references/05-release-gate-baseline-templates.md`.
