---
name: agent-tool-result-caching
description: "Cache expensive tool results within a run and across runs with TTL, invalidation, and privacy boundaries."
category: agents
tags: ["caching","tools","cost","agents"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Skills Library
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Agent Tool Result Caching

> **RU:** Кэш результатов tools агента - Кэш дорогих tool results внутри run и между run: TTL, инвалидация и границы приватности.

## 1. Skill Meta
**Name:** Agent Tool Result Caching
**Description:** Cache expensive tool results within a run and across runs with TTL, invalidation, and privacy boundaries.
**When to load:** Use when agent runs repeat expensive tools and need cache discipline.
**Outcomes:** Production-usable cache design with TTL, keys, and privacy rules.

## 2. Core Directive
Prefer precise cache keys and explicit invalidation. Never cache secrets or cross-tenant data.

## 3. Operating Protocol
1. Define cache key from tool+args+tenant.
2. Set TTL by freshness needs.
3. Redact before persistence.
4. Measure hit rate and cost saved.
5. Provide bypass for forced refresh.

## 4. Required Deliverables
1. Cache architecture for the user's stack.
2. Keying + TTL policy.
3. Anti-patterns.
4. Validation checklist.
5. Sample config.

## 5. Execution Sequence
1. Inventory expensive tools.
2. Design keys/TTL.
3. Implement store.
4. Instrument hits/misses.
5. Document residual risks.

## 6. Domain Depth
In-run memoization vs cross-run store; privacy; stampede control; invalidation on skill/version change.

## 7. Anti-Patterns (Hard Failures)
- Caching authenticated personalized results under a global key.
- Infinite TTL on volatile market or security data.
- Shipping placeholders as finished work.

## 8. Validation Checklist
- [ ] Assumptions stated
- [ ] Metrics defined
- [ ] Rollback considered
- [ ] No banned anti-patterns
- [ ] Output complete

## 9. Integration with Syntedge Orchestrator
Declare cache backend; persist metrics; emit Run Card.

## 10. Reference Vocabulary
- `caching`
- `tools`
- `cost`
- `agents`

---
*Syntedge Research Skills Library - agents / agent-tool-result-caching*
