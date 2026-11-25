---
name: code-review-red-team
description: Use for code review, branch audit, security/reliability review, or adversarial review before delivery.
---

# Code Review And Red Team

Review code, not the coder. Findings lead.

## Review Order

1. Correctness and edge cases.
2. Domain model, states, transitions, invariants.
3. Security: auth, authorization, secrets, PII, injection, prompt injection, rate limits.
4. Reliability: retries, idempotency, transactions, timeouts, concurrency, caching.
5. Maintainability: names, boundaries, duplication, coupling.
6. Operability: logs, metrics, run IDs, replayability.
7. UX/accessibility.
8. Style only when it affects readability or tooling.

## Red-Team Pass

Try to break the favored conclusion:

- Malformed input.
- Empty/zero/one/boundary input.
- Permission mismatch.
- Stale cache.
- Retry after partial failure.
- Concurrent mutation.
- Mobile/responsive state for UI.
- Prompt injection or malicious retrieved text for AI systems.

## Finding Format

```md
### [Severity] Title
- Confidence:
- Evidence:
- Impact:
- Fix:
- Verification:
```

Verdict:

- `SHIP`: no confirmed P0/P1 and verification is adequate.
- `FIX-FIRST`: confirmed P0/P1 or missing high-risk verification.
- `BLOCKED`: required access, data, service, or approval is missing.

