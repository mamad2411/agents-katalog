---
name: business-logic-security
description: Find and fix business logic vulnerabilities. Use when reviewing
  flows that abuse business rules.
metadata:
  tags: business, logic, security
---

# Business Logic Security

## Use this skill when
- Reviewing pricing, coupons, quotas, and limit logic
- Finding logic flaws: race conditions, decimal abuse, negative quantities
- Reviewing workflows that can be replayed or abused

## Do not use this skill when
- Standard OWASP injection/XSS checks (use full-stack-security-engineer)
- Only cherry-picking an isolated code review

## Instructions
1. Understand the business rules before reviewing (prices, limits, entitlements).
2. Walk every state transition and ask what an attacker could skew.
3. Check numeric handling: decimals, rounding, negative values, integer overflow.
4. Check limits: quotas, free tiers, trial enforcement, rate tricks.
5. Check multi-step workflows for order swaps, skip, replay, and race.
6. Check for divergence between displayed vs enforced values.
7. Verify idempotency and the one-action-per-object rules.
8. Provide a proof-of-concept and a server-side fix per finding.

## Checklist
- Prices/limits enforced server-side
- No trusting client-supplied amounts
- Concurrency-safe entitlement checks

## Output Format
- Finding | abuse scenario | business impact | proof-of-concept | fix

## Common Mistakes
- Ignoring concurrency on counters
- Rounding errors that leak money
- Trusting client-computed totals
