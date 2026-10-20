---
name: grill-while-coding
description: Pauses implementation to question the user about decisions that encode business rules or architecture — new features, conditionals/branches, classes, clauses, or similar structures. Use automatically during implementation whenever such a decision is about to be made, not just when explicitly invoked, so the user stays aware of and aligned with the code being written.
---

# Grill While Coding

## Quick start

Whenever you are about to implement something that encodes a business rule or an architectural decision — a new feature, an if/branch, a class, a clause, or any similar construct — pause before writing it and ask the user about it.

Ask one question at a time, state your recommended answer, and wait for confirmation before writing the code.

Example:

```
About to add a `maxRetries` cap on the payment webhook handler.
Recommend: 3 retries, exponential backoff, then dead-letter. Sound right, or different cap?
```

## Scope

Only surface decisions that actually carry business-rule or architectural weight. Skip purely mechanical or boilerplate code (formatting, obvious scaffolding, renames) — those don't need a check-in.

The goal is to keep the user oriented on the code and architecture as it's built, not to interview them about a plan before code exists (that's /grill-me's job).