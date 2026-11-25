---
name: adr
description: Write, review, and apply architecture decision records (ADRs). Use when explicitly asked to record a consequential architecture decision, review an ADR, or reason about work governed by existing decisions.
---

# ADR

An architecture decision record captures one consequential decision and why it made sense at the time. It gives future contributors the context to respect a decision or deliberately revisit it. An accepted ADR states the intended architecture; it does not prove that the implementation already conforms.

Read applicable accepted ADRs before changing architecture. Write a new ADR only when the user asks for one. Writing a record does not authorize implementing its decision.

These conventions draw on Umbod's ADR practice: lead with the decision, make trade-offs explicit, preserve decision history, and keep records discoverable from the project's agent instructions. Follow the target repository's location, metadata, and lifecycle conventions.

## Table of contents

| Concept | Read when |
|---|---|
| [Decisions and rationale](references/decisions-and-rationale.md) | Deciding what deserves a record, drafting the reasoning, or reviewing an ADR. |
| [Applying and revisiting decisions](references/lifecycle.md) | Working under an existing ADR, resolving a conflict, or replacing a decision. |
| [ADR record](record/structure.md) | Creating or updating a durable record and its index. |
