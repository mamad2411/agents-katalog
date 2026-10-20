---
name: generic-spec-authoring
description: Apply when authoring or editing docs/requirements/*.md, docs/bdd/*.feature, or docs/design/*.md. Defines ID conventions, TBC handling, Gherkin discipline, and the requirement-mirrored design-doc format.
metadata:
  stack: [generic]
  requires: [generic-docs-standards]
---

# Spec authoring

Three artefact types — requirements, BDD scenarios, design docs — three sets of rules. Always tag every BDD scenario and every design section to a requirement ID.

## Requirements (`docs/requirements/*.md`)

### ID format

- Functional requirements: `[FR-<AREA>-<NNN>]` (e.g. `[FR-IDV-013]`, `[FR-CARD-027]`).
- Non-functional requirements: `[NFR-<AREA>-<NNN>]`.
- `<AREA>` is a short uppercase token tied to the feature area (`IDV`, `CARD`, `SCA`, `ONB` for onboarding, `BFF`, etc.). Add new areas sparingly.
- `<NNN>` is a zero-padded integer, monotonically increasing within `<AREA>`. **Never reuse an ID** even if the requirement is deleted — leave a tombstone with `Status: Withdrawn`.

### Status

Use one of: `Done`, `In Progress`, `TBD`, `Pending`, `Blocked`, `Withdrawn`. No emoji.

### `TBC` handling

Sections under a `## TBC` header (or `### TBC <topic>`) are **not authoritative**:

- The gate-pipeline skill will not enforce them.
- Code generation should not assume them.
- They exist to capture open questions to resolve later.

When a `TBC` resolves, move the content out from under the `TBC` header into a normal section with a real ID.

### Writing style

Plain-language rule list. One requirement per bullet, ID at the start.

> `[FR-CARD-027]` The system MUST allow a customer admin to set a daily spending limit per card, in the card's currency.

Avoid prose narratives. If you need narrative to explain *why*, that goes in the matching design doc.

## BDD scenarios (`docs/bdd/*.feature`)

### Gherkin discipline

- Standard `Feature: / Scenario: / Given / When / Then / And` structure.
- One feature file per requirement area (often per top-level FR-AREA).
- Tag every scenario with the requirement ID it satisfies: `@FR-CARD-027`.
- Scenarios must map to **testable** behaviour — observable user-facing state changes. Not implementation-level.
- Prefer **representative scenarios** over exhaustive ones. Edge cases go in design docs, not BDD.
- **Value-agnostic phrasing.** When the specific value is *incidental* to the behaviour, phrase it generically and let it round-trip — e.g. "When the user creates a tournament **with a specific type**" / "Then the tournament is created **with the selected type**", not "with type Private … created with type Private". Hard-coding a value implies the behaviour is value-specific when it isn't, and invites a scenario per value.
  - **Exception — outcome-driving values stay concrete.** When *different* values produce *different* outcomes, enumerate them in a `Scenario Outline` + `Examples` table (that is exactly what outlines are for). The visibility matrix (Public listed to all, Private/Template only to owner) is value-driven → keep the values. A create→edit round-trip is value-agnostic → keep it generic.
  - Heuristic: if you could swap the literal for any other valid value and the `Then` would read the same, make it generic.

```gherkin
@FR-CARD-027
Scenario: Admin sets a daily spending limit
  Given a customer admin is viewing an issued card
  When the admin sets the daily spending limit to 5000 DKK
  Then the limit appears on the card detail view
  And the mobile app shows the new limit on the cardholder's card screen
```

### What does NOT belong in BDD

- Edge cases of the form "what happens if the user clicks twice / on slow networks / etc." — those are design concerns.
- Validation rules. Those live in the requirement and the FluentValidation code.
- Implementation details. "When the user clicks save and the BFF receives a POST" — the user doesn't experience HTTP verbs.

## Design docs (`docs/design/*.md`)

### Structure

Brief intro then a section per governing requirement, mirroring the requirement's ID:

```markdown
# Card spending limits — design

This document covers the design for [FR-CARD-027..030].

## [FR-CARD-027] Daily spending limit per card

How the system is shaped to satisfy this requirement…
```

The full project-specific section layout (Context → Architecture → State machine → Sequence diagrams → Response per requirement → Open questions → References) lives in [`docs/design/_index.md`](../../../docs/design/_index.md). The four rules below govern *what to write in each section*, regardless of layout.

### Rule 1 — Current state only

Design docs describe how the system is shaped **now**. They are not ADRs. No dated change blocks, no `v2 changes:` headers, no revision history, no strikethrough `~~RESOLVED 2026-05-13~~` entries. The git log and PR descriptions are the audit trail; the doc is the snapshot.

When an open question is answered:

- If the resolution changes the architecture → edit the affected `§Response per requirement` entry directly and remove the question.
- If the resolution is "code/tests already cover it" → just remove the question. Don't leave a tombstone.

A trade-off that was rejected can still appear inline with the requirement that would have answered it, expressed in present tense as a deviation rationale (e.g. *"A separate limit aggregate was considered and rejected because…"*). Never as a dated changelog entry.

### Rule 2 — High-level only

A design response is **2–5 lines** per requirement. If you reach ten lines, implementation detail is leaking in. Keep code samples out; if pseudocode is essential to communicate a decision, make it short and free of language-specific syntax.

### Rule 3 — Do not mirror the code

Self-documenting code stays in code. The following do **not** belong in a design doc:

- Exact class, port, adapter, method, or service names (`IDataProtectionProvider`, `CryptographicOperations.ZeroMemory`, `VerificationStateSigner`, `RunCompareStep`).
- Method signatures, type declarations, nullability annotations.
- Configuration keys, environment-variable names, NuGet package names, framework registration calls.
- Regex patterns, exact hashing/algorithm parameters beyond *what kind* of primitive (saying *"HMAC-SHA256"* is fine; naming the helper class that wraps it is not).
- Column-mapping tables (provider field → DB column → DTO property). Mappings live in adapter tests.
- File paths into `api/`, `spa/`, `mobile-app/`. The doc says *what* the design is, not *which file* implements it.

Heuristic: if you rename a class or swap a library version, the design doc should not need to change.

### Rule 4 — Traceability is file-level and §Response-level, not universal

Requirements are business-driven; design is tech-driven. The two don't map one-to-one.

- The **design file** maps to its requirements file (or, for cross-cutting docs like `api-layering-and-ports.md`, to a stated scope across multiple areas).
- Entries under **§Response per requirement** are headed by the FR/NFR IDs they realise — that's the mechanical traceability layer.
- Other sections (Context, Architecture, State machines, Sequence diagrams, deep-dive subsections on tech-shaped concerns) are tech-driven and need not carry an FR/NFR ID. They exist because the architecture needs them, not because business asked for them.

If a tech section feels unmoored from anything — neither requirements nor a real architectural concern — that's the signal to question whether it belongs at all, *not* to invent an FR for it.

## Anti-patterns

- A BDD scenario with no requirement tag — orphan; either the requirement is missing or the scenario shouldn't exist.
- A `§Response per requirement` entry without an FR/NFR ID — same problem, opposite direction. (Other design sections do not need IDs; see Rule 4.)
- A design section that explains *how* a routine is written (encryption, parsing, comparison) rather than *what the system decides to do* about it. The how is in code.
- A "Resolved" entry kept under `§Open questions` with a date stamp instead of being folded into the affected design section (or dropped if code/tests are sufficient).
- A provider/vendor field-mapping table in the design doc.
- Editing a requirement without a corresponding update to the design or BDD when behaviour changes. The writing order (requirements → BDD → design) means downstream files always lag the requirement update; close the loop in the same change set.
- Resurrecting a withdrawn requirement ID for a new requirement. Always pick a fresh number.
