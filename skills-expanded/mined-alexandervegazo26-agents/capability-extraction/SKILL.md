---
name: capability-extraction
version: 1.0.0
description: Harvesting technique for reverse-engineering an existing application's actual capabilities, business rules, data model, and integration surface from code and safe observed execution. Used by product-archaeologist. Do NOT use for deriving who uses the system — that is `persona-discovery`'s harvest; this is what the system actually does. Do NOT use for writing new requirements for a system that doesn't exist yet — that is `requirements-craft`.
---

# Capability Extraction

## Principle
Every capability, business rule, and data-model claim needs a citation — a `path:line` reference, a schema/migration reference, or a specific observed-execution note (what was run, in what environment, what was seen). A claim with no citation is a guess wearing a finding's clothes, and it doesn't go in the output.

## Static evidence sources
- **Capability inventory** — routes/endpoints, screens/pages, CLI commands, scheduled/batch jobs, admin or back-office functions, webhooks and exports, feature-flagged functionality (including flags that suggest a feature was partially built and never finished).
- **Business rules** — validation logic, calculations (pricing, discounts, eligibility), workflow and state-machine transitions, permission and gating checks, default values that encode an assumption. These are usually the *only* place undocumented business logic lives — the code is the spec whether anyone wrote it down or not.
- **Data model** — entities, relationships, cardinality, and constraints from schema, migrations, and ORM/model definitions. This is evidence for the domain model the system actually operates on, which may differ from any documented one.
- **Integration surface** — external services called, webhooks received, data imported/exported, third-party auth providers, anything the system depends on or is depended on by.
- **Non-functional baseline** — what the code and config actually reveal about current scale handling, auth mechanism, deployment shape — described as what *is*, not evaluated as good or bad.
- **Gap and pain-point evidence** — dead code paths, abandoned feature flags, TODO/FIXME/HACK comments, unusually defensive error handling clustered around one area (a strong signal that area has caused real pain before), and — where accessible — commit history showing repeated fixes to the same spot.

## Dynamic evidence — safe observed execution
Where a non-production environment is available, running the application and observing actual behavior is often faster and more reliable than tracing code by hand for confirming what a business rule actually produces (an error message, a calculated value, a state transition). Treat an observation as evidence with the same citation discipline as a code reference — what was run, in what environment, what was seen — and corroborate against the code where feasible rather than treating the observation alone as sufficient.

**Never confuse "this is what happens" with "this is what was intended."** Current behavior may itself be a bug that's been live long enough to look like a deliberate rule — if a discovered rule looks suspicious (an off-by-one, an inconsistency with a similar rule elsewhere in the system), flag it as *possibly a defect, not confirmed intended behavior* rather than asserting it as a deliberate capability. This is the same distinction `qa-engineer` draws between Verified behavior and a bug wearing a spec's clothing, and the same reason its Oracle Hierarchy ranks historical implementation behavior *below* a written specification rather than treating it as authoritative.

Where a specific hazard domain is in play, the skill that owns it lists what actually goes wrong there: `datetime-correctness` for a date rule that looks off by a day, `caching-and-invalidation` for a "rule" that's really a staleness artifact, `concurrency-and-thread-safety` for behavior that only reproduces under load. A rule extracted from observed behavior in one of those areas deserves extra scrutiny before it's written down as intended design.

## Triangulation and classification
Use the same three-way status as `persona-discovery`:
- **Confirmed** — ≥2 independent evidence sources agree (e.g., a validation rule in code and a matching error string in the UI, or a schema constraint and an observed rejection).
- **Candidate** — one source only.
- **Rejected** — contradicted by other evidence; keep with the contradiction cited rather than discarding it silently.

Never promote a candidate to confirmed on inference alone — list candidates for the user's decision, the same discipline `persona-discovery` applies to its own roster.

## Cross-checking against other evidence sources
Where `persona-discovery` has already run, map each capability to the persona(s) that can reach it. A capability with no persona able to reach it (orphaned, admin-only, or dead) and a persona with jobs-to-be-done that have no corresponding capability are both genuine findings — surface them, don't silently reconcile.

Where `product-analyst` has existing requirements for this system, cross-check implemented capabilities against them the same way — an implemented capability with no requirement, or a requirement with no implementation trace, is a finding for the PRD's gap section.
