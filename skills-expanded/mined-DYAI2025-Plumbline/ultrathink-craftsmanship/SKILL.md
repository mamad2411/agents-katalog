---
name: ultrathink-craftsmanship
description: Use for expensive, one-pass reasoning gates that stress-test a specification, plan, or near-final implementation for bias, hidden coupling, weak evidence, and craftsmanship risks.
---

# Ultrathink Craftsmanship

A deep reasoning gate, not a correctness proof. Run once per configured gate unless the workflow explicitly allows another iteration.

## Modes
- `full`: specification sanity and architecture risk review.
- `kurz` / `kurz+`: compact iteration judgment near release.

## Checklist
- What claim is least evidenced?
- What hidden assumption would invalidate the plan?
- What edge case crosses module, data, security, or UX boundaries?
- Where could tests pass while production wiring is absent?
- What should be removed, simplified, or deferred?

Pair with `konfabulations-audit` for external claims.

