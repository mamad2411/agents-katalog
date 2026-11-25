---
name: capture-intake-and-gaps
description: Use when a product request must be separated from repository evidence and checked for prior decisions and behavioural gaps.
---

# Capture evidence and product gaps

## Inputs
Stable request identity; supplied feature, design, and supporting sources; repository access; known Product and Engineering owners.

## Procedure
1. Preserve the supplied request and linked material separately from repository evidence; record locator, revision, access, and `current|stale|missing|conflicting` state for each.
2. Search narrowly for prior PRDs, decisions, behavioural tests, and code that establish current behaviour or a direct dependency. Distinguish confirmed conflict from possible impact; never silently supersede a prior decision.
3. Capture only current-system constraints needed to state behaviour truthfully. Keep possible implementations and broad architecture with Planner.
4. Classify each claim as requested, observed, decided, conflicting, proposed, or unknown.
5. Check actors, permissions, lifecycle, validation, loading/empty states, failure, recovery, retry, repeated action, concurrency, idempotency, side effects, and measurable outcomes.
6. Check applicable security, privacy, accessibility, reliability, operability, auditability, compliance, and regional concerns; give a rationale for material non-applicability.
7. Classify design as aligned, incomplete, mismatched, absent, or not required. For every gap, name the decision, evidence, owner, and blocking effect.

## Output
Separate source registers, a prior-decision impact table, current-behaviour constraints, and a prioritised owned gap register.

## Stop condition
Stop when request identity is missing, a controlling source cannot be inspected, or conflicting evidence prevents an honest draft. Continue with explicit limits only when the missing evidence is non-blocking.
