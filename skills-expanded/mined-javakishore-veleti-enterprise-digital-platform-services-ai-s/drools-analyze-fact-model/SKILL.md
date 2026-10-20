---
name: drools-analyze-fact-model
description: Analyze Drools fact object models, relationships, property access, mutability, equality, derived facts, and working-memory behavior. Use when rule correctness or performance depends on how application objects are represented and updated as facts.
---

# Analyze Fact Model

1. Inspect Java/domain objects used as facts and the rules that consume them.
2. Identify relevant properties, relationships, collections, and derived values.
3. Check insert, update, modify, delete, and logical insertion behavior.
4. Verify mutations are communicated to working memory correctly.
5. Identify broad or unstable fact structures that increase rule coupling or evaluation cost.
6. Preserve domain semantics when recommending changes.

## Output
- Fact Model
- Working-Memory Lifecycle
- Rule Dependencies
- Correctness/Performance Risks
- Recommended Changes
