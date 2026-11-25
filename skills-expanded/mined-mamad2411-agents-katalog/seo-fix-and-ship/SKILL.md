---
name: seo-fix-and-ship
description: Runs pre-publish SEO checks and post-launch monitoring. Use before releasing template/URL changes or after deploying SEO fixes.
---

# SEO Fix and Ship

## Overview

Ship only when verification evidence is captured; monitor afterward.

## When to Use

- Pre-publish gates; launching SEO fixes

**Not for:** Open-ended strategy workshops (use interview/audit).

## Official sources

- https://developers.google.com/search/docs/fundamentals/get-started
- https://developers.google.com/search/docs/monitor-debug/search-console-start

## Process

1. Run Definition of Done + relevant domain skill verifications.
2. Confirm staging/production parity for canonical host.
3. Deploy; spot-check live headers/HTML.
4. Use GSC URL Inspection on key URLs; monitor coverage/performance for regressions.
5. Keep a rollback note for redirects/canonical mistakes.
6. Schedule a follow-up check (e.g. 3–14 days) via `search-console-ops`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Ship and watch rankings tomorrow." | Monitor GSC over days/weeks; schedule a follow-up. |
| "Staging canonicals can point at prod forever." | Confirm host parity before launch to avoid wrong consolidation. |
| "No rollback plan for redirects." | Bad redirects/canonicals need a documented undo path. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] Pre-publish checklist done with evidence
- [ ] Live spot-check recorded
- [ ] Monitoring follow-up scheduled
