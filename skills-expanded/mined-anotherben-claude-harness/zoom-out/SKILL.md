---
name: zoom-out
description: Step back from a confusing code area and map the surrounding modules, callers, ownership, runtime flow, state/status lifecycle, and edge cases. Use when the user says "zoom out", "give me the bigger picture", "how does this fit together", or when debugging, planning, refactor review, or local code details risk obscuring the system shape.
---

# Zoom Out

Use this when the immediate file or function is too narrow to explain the real system behavior.
Deep Think should use this as a subroutine for debugging, planning, refactor review, and
any proposed fix that may only cover the first visible symptom.

## Workflow

1. Identify the current focus: file, symbol, route, worker, UI flow, bug, or decision.
2. Read the nearest source of truth for that focus, then map the first ring outward:
   - direct callers and consumers
   - upstream entry points
   - downstream services, jobs, queries, or UI surfaces
   - sibling modules and sibling business states that may share the same rule
   - tests and verification points
   - relevant docs, ADRs, glossary terms, or vault notes
3. Expand to one more ring only if the first ring does not explain root cause, ownership, lifecycle/status cohort, blast radius, or proof path. Stop expanding when the next move is clear and falsifiable.
4. If the behavior depends on status, state, lifecycle phase, queue state, approval stage, or visibility filters, enumerate the full cohort before recommending a change:
   - included active or pre-submit states
   - excluded terminal states
   - display names versus database/API literals
   - transitions that can race, retry, or leave stale rows behind
5. Explain the system in plain language before diving back into details.
6. Name the ownership boundary: which module owns the behavior, which modules merely consume it, and where changes should land.
7. End with the next concrete move: where to inspect, what to test, or what decision is now clearer.

## Output Shape

- **What this area does:** one short paragraph.
- **How it is reached:** entry points and callers.
- **What it depends on:** services, data, integrations, or config.
- **What depends on it:** consumers and user-facing surfaces.
- **Lifecycle/status sweep:** included, excluded, and ambiguous states or phases.
- **Risky edges:** places likely to break if changed.
- **Next move:** one recommended action.

Keep it source-grounded. If you did not read the relevant source, say that the map is provisional.
