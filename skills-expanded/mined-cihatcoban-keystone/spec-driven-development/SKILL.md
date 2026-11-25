---
name: spec-driven-development
description: Writes a specification with measurable acceptance criteria before code exists. Triggers - write a spec for this feature, we need a PRD before we start, what exactly are we building, define the scope, requirements doc.
---

# Spec-Driven Development

A spec is the shared, checkable statement of what will exist. Without one,
"done" is decided after the fact by whoever is most tired. With one, the
argument happens while it is still cheap — on paper.

A spec is not a design document. It says *what* and *how we will know*; design
decisions belong in `architecture-decisions`, sequencing in
`planning-and-task-breakdown`.

## When to use

- New feature, new subsystem, new integration
- Any change to observable behavior of something people depend on
- Experiments too — a spike gets a five-line spec with a deadline and a
  question it must answer

**When not to use:** typo fixes, dependency bumps, refactors that preserve
behavior exactly (those need tests, not a spec).

## Shape

Store as `docs/specs/NNN-short-name.md`.

```markdown
# <Title>
Status: draft | approved | implemented | superseded by NNN
Owner: · Date: · Related: ADR-NNN, spec-NNN

## 1. Problem
Who cannot do what today, and the cost of that.

## 2. Outcome
The capability that exists afterwards, in one sentence.

## 3. Users and scenarios
For each actor, the concrete walkthrough. Include the unhappy paths.

## 4. Acceptance criteria
Numbered, independently verifiable, each one testable as written.

## 5. Out of scope
Deliberate exclusions, so scope creep has to argue with a document.

## 6. Interface impact
Public API, schema, events, config, CLI — what changes for callers, and whether
the change is backward compatible.

## 7. Data impact
New/changed data, migration need, retention, personal data, reversibility.

## 8. Quality impact
Which CONSTRAINTS.md dimensions this touches; new budgets it must meet.

## 9. Failure and degradation
What happens when a dependency is down, slow, or returns garbage.
What the user sees. What we log.

## 10. Risks and unknowns
Risk → mitigation. Unknown → how we will resolve it (spike, sample, prototype).

## 11. Alternatives considered
Options rejected and why. Absence of this section means the first idea won.
```

## Writing acceptance criteria

The single highest-leverage part. A criterion is well-formed when a test can
be written from it without asking a question.

| Weak | Strong |
|---|---|
| "Search should be fast" | "p95 search response ≤ 300 ms at 50 concurrent users with 1M rows" |
| "Handles errors gracefully" | "On upstream 5xx, returns 503 with retry-after, logs one warning with correlation id, no partial write persists" |
| "Users can export data" | "Export produces a CSV with columns A–F; rows match the filtered view exactly; 100k rows complete within 60 s; interrupted export leaves no file" |
| "Should be secure" | "Only users with role X can call it; rejects requests without a valid token with 401; never logs the token" |

Rules: one behavior per criterion; include the boundary ("at 1M rows", "when
the token is expired"); name the observable result, not the implementation.

## Discipline

1. **Section 5 is mandatory.** An empty out-of-scope list means the boundary
   hasn't been thought about.
2. **Sections 7 and 9 cannot be skipped.** "No data impact" and "no degraded
   mode needed" are valid answers; blank is not.
3. **Two pages is the ceiling.** Longer means the work should be decomposed
   into several specs with their own criteria.
4. **Unresolved question → explicit assumption.** Write "Assumption:" with the
   consequence if wrong, and proceed. Never leave a blank to be filled by
   whoever implements it.
5. **Approval before code.** The spec is the thing being approved, not the
   implementation that follows.
6. **Superseding, not editing.** A shipped spec is a historical record. Changes
   after implementation go in a new spec that supersedes it.

## Exit checklist

- [ ] Every acceptance criterion could be turned into a test as written
- [ ] Out-of-scope list is non-empty
- [ ] Interface and data impact stated, including "none" where true
- [ ] Failure behavior described for each external dependency
- [ ] At least one rejected alternative recorded with a reason
- [ ] Assumptions listed with consequences
- [ ] Reviewed and marked approved before implementation starts
