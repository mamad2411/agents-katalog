---
name: security-qa-scenarios
description: "Design security QA for changed permissions, tenant boundaries, inputs, state, or abuse paths."
---

# Security QA Scenarios

Generate concrete negative and abuse-case tests from actors, objects, trust boundaries, state, inputs, time, and limits.

## Trigger boundary

Use this skill when a feature or incident needs security QA for abuse cases, negative paths, permissions, tenant isolation, malformed inputs, state transitions, rate limits, or evidence.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no security-relevant behavior, trust-boundary, permission, input, state, or limit impact; follow the repository's established convention directly.

## Evidence

Prefer code, tests, logs, config, API contracts, and data examples over assumptions.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Security definition of done; Testy bezpieczeństwa w development
- [02-jak-wymyslac-scenariusze-testowe.md](./references/02-jak-wymyslac-scenariusze-testowe.md) - Jak wymyślać scenariusze testowe
- [03-katalog-scenariuszy-qa.md](./references/03-katalog-scenariuszy-qa.md) - Katalog scenariuszy QA; Checklist QA
