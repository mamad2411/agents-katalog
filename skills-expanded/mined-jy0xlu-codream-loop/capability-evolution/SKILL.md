---
name: capability-evolution
description: Use when a task needs controlled capability discovery and adoption across official plugins, local skills, and trusted GitHub projects.
---

# Capability Evolution

Use this skill during active work when the task may need a better capability than the ones already in hand.

It discovers, validates, and adopts capabilities. It does not promote memory by itself.

## Use This Skill When

- a task needs tool or workflow choice before execution
- official plugins, local skills, or external projects may improve the route
- the user questions whether capability search really happened

## Intent Classification

Classify before discovery:

- `repair`: broken workflow, failed integration, or missing capability
- `optimize`: better speed, quality, confidence, or repeatability
- `innovate`: new capability or workflow
- `explore`: external search after official and local choices are insufficient

`explore` is only for cases where official and local options fail.

## Discovery Order

Check in order and stop at the first sufficient fit:

1. enabled official plugins
2. installable official plugins
3. local built-in skills
4. trusted GitHub skills or projects

Do not jump straight to GitHub search if a good official or local option already exists.

## Observable Discovery

Capability discovery must leave evidence, not just a conclusion. For non-trivial decisions, show searched layers, skipped or blocked layers, selected and rejected candidates, and whether GitHub or external search was reached. See `references/discovery-evidence.md` for the full checklist.

## Validation And Reporting

Before adoption, check relevance, maintenance recency, source trust, and integration cost versus expected benefit. Report before or while adopting third-party GitHub capabilities or making material global setup changes.

## Working Loop

1. recall the smallest relevant memory slice
2. classify the task intent
3. discover capabilities in the fixed order and keep observable evidence
4. escalate to GitHub or external project search only when official and local options are insufficient
5. validate the best candidate
6. adopt or invoke the capability only if the validation clears
7. finish the task work
8. if the new capability produced a high-signal result, hand off the event to `capture-memory`

## Hard Constraints

- do not push weak, inferred, or still-competing signal into `ACTIVE.md` or `LEARNINGS.md` during active work
- explicit strong signal with a clear destination may be handed off to `capture-memory` for direct landing under the current `AGENTS.md` rules
- do not treat GitHub search as a default step
- do not claim capability discovery worked unless the searched layers and candidate decisions are visible
- do not silently import third-party capabilities
- do not confuse one-off experimentation with stable policy
- keep capability evolution separate from memory promotion

## Output Expectations

When this skill influences a decision, show: intent, discovery path, searched/skipped/blocked layers, selected/rejected candidates, whether GitHub or third-party search was reached, and whether the result should be captured into Dream Loop memory.
