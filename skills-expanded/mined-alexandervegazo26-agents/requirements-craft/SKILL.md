---
name: requirements-craft
version: 1.0.0
description: Elicitation and specification technique for turning a vague ask into testable requirements — user story structure, acceptance criteria patterns, and ambiguity detection. Load when writing or reviewing requirements, before design or implementation starts.
---

# Requirements Craft

## Elicitation

- Ask "what problem does this solve, for whom" before "what should it do" — a requirement without a stated user/problem is a guess wearing a spec's clothing.
- Distinguish a stated requirement from an inferred one. If it's inferred, say so and get it confirmed rather than silently treating it as given.
- Look for the requirement behind the requirement: a requested feature is often a proxy for an underlying need that a simpler solution could satisfy.

## Solution-in-disguise detection

When the ask already names a specific technical solution ("add a column for X," "build a dashboard that shows Y") rather than a problem, don't accept the solution as the requirement itself. Extract the underlying need first — what outcome is this solution actually meant to serve? State that need explicitly as the requirement, and flag the requested solution as one candidate implementation, not the definition of done, if it isn't obviously the only reasonable way to meet the need. Whose job it is to pick among alternatives is a design decision, not a requirements one — flag it for that owner rather than resolving it here.

## User story structure

`As a <role>, I want <capability>, so that <outcome>.` The "so that" clause is not decoration — if you can't state it, the story likely isn't ready. One clear outcome per story; a story with "and" in the capability clause is probably two stories.

## Acceptance criteria

Write as Given/When/Then or an equivalent falsifiable form. Every criterion must be answerable with a fact, not an opinion — "the page loads faster" is not a criterion; "p95 response time under 300ms for the search endpoint" is.

Cover: the happy path, at least one negative/error path, and any explicitly stated non-functional constraint (performance, accessibility, security) relevant to this story.

**Number every criterion with a stable ID** once published (e.g. `AC-1`, `AC-2`). Downstream agents — `qa-engineer`'s Oracle Hierarchy, `code-reviewer`'s requirement tracing, `database-engineer`'s requirement tracing — cite these IDs directly; an unnumbered criterion is invisible to the traceability process it exists to anchor. If a published criterion must change after work has started against it, note the change explicitly rather than editing it silently in place — anything already traced against the old version needs to know it went stale.

## Ambiguity detection

Common ambiguity smells to catch before handoff: vague quantifiers ("fast," "several," "most users"), undefined actors ("the system decides" — decides how?), missing error/edge-case behavior, and conflicting criteria between two stories touching the same feature. Flag each explicitly rather than silently resolving it with a guess — see the assumption-register pattern in the owning agent's spec.

## Work breakdown

Split by independently deliverable/testable slices, not by technical layer (don't split "build the API" and "build the UI" into separate stories if neither is independently valuable — slice vertically by user-visible behavior where possible).
