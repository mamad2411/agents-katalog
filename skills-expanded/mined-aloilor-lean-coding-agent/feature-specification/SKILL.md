---
name: feature-specification
description: "Write a client-reviewable FEAT-NNN Feature Specification for one software feature: user stories, scope, functional requirements, business rules, edge cases, Given/When/Then acceptance criteria, and open questions."
disable-model-invocation: true
---

# Feature Specification

Produce one Feature Specification per feature: a document a client can review, developers can build against, and QA can test against. It defines *what the feature must do*, not how to implement it.

## Concepts To Keep Distinct

- A **PRD** explains why a product exists and covers many features. A **Feature Specification** covers exactly one feature and defines its behavior precisely. If the user hands you a PRD, split it and spec one feature at a time.
- **User Story** — the need, from the user's perspective. Context for non-technical readers; too vague to build against alone.
- **Functional Requirement** — exactly what the system must do.
- **Acceptance Criterion** — how to prove the behavior works.

The chain *User Stories → Functional Requirements → Acceptance Criteria* is the spine of the document. Preserve it rigorously: the client understands the stories, developers build the requirements, QA verifies the criteria.

Do not force every requirement into "As a [user], I want…". Permissions, validation, audit logging, idempotency, concurrency, integrations, performance, and security read badly as stories; write them directly as FRs, business rules, or NFRs.

## References

- Read [references/template.md](references/template.md) before writing. It is the fixed template: section names, order, ID prefixes, and formatting are not negotiable.
- Read at least one example in [references/examples/](references/examples/) that matches the variant you are writing:
  - [feat-004-export-invoice-pdf.md](references/examples/feat-004-export-invoice-pdf.md) — full variant, UI feature with permissions and file output.
  - [feat-001-user-registration.md](references/examples/feat-001-user-registration.md) — full variant, security-sensitive feature with requirements that are not user stories.
  - [feat-012-order-shipped-push-notification.md](references/examples/feat-012-order-shipped-push-notification.md) — lean variant, small feature.

## Process

### 1. Gather what exists

Collect the feature request, any PRD, ticket, mockup, or prior spec the user provides. When working inside a repository, also:

- Look for existing `FEAT-NNN` IDs in the repository so the next ID is unique.
- Read `docs/conventions/GLOSSARY.md` or an equivalent glossary when present, and use the project's own names for roles, entities, and screens.
- Inspect relevant code only to ground terminology, existing permissions, and current behavior. Do not let implementation details leak into the spec.

### 2. Pick the variant

The **lean** variant keeps only Feature, Objective, User Stories, Scope, Out of Scope, Functional Requirements, Acceptance Criteria, and Open Questions. The **full** variant keeps every section.

Decide in this order:

1. **The user said.** A request for a short, quick, lightweight, or one-page spec, or calling the feature small, means lean. A request for a detailed or complete spec means full. The user's word wins over your own assessment.
2. **Otherwise, assess the feature.** Write the full variant if any of these is true, because each one creates rules, permissions, or failure modes that the omitted sections exist to capture:
   - different roles get different abilities, or the feature changes who can do what;
   - money is involved: payments, billing, pricing, refunds, seats;
   - authentication, account security, or an action that cannot be undone (deletion, cancellation, sending to a third party);
   - personal, health, or financial data is collected, exposed, or moved somewhere new, or a legal or compliance obligation applies;
   - an external system or another team's service must be integrated;
   - there is a lifecycle with states, scheduling or availability, or two people can act on the same thing at once;
   - you expect more than about 8 functional requirements.

   Otherwise write the lean variant: a single self-contained behavior on an existing screen or flow, reusing existing permissions and data.
3. **Still unsure?** Write the full variant; empty-feeling sections are a signal that something has not been thought through.

Lean applies to the content as well as the section list: merge closely related requirements, cover each distinct behavior with one acceptance criterion rather than one per requirement, and aim for a spec that fits on one or two pages. When the user asked for lean but the feature trips one of the full-variant triggers, keep it lean anyway and raise the risk as an open question.

State the variant and the one-line reason in your report so the user can override it.

### 3. Resolve blocking unknowns

A specification is only valuable if it removes ambiguity, so do not invent business decisions and present them as agreed. For each unknown:

- If the codebase or provided material answers it, use that answer.
- If it blocks writing a coherent spec (who the actors are, what the core behavior is, what is in scope), ask the user. Batch these into one short message with your recommended answer for each.
- Otherwise, make a reasonable choice and record it under **Dependencies and Assumptions** (in the lean variant, which lacks that section, list it in your report), or raise it under **Open Questions** when the client must decide.

Every open question carries a recommended answer, the reason for it, and the IDs it affects. Write the rest of the spec as if the recommendation is accepted, so the document is complete and buildable: the client either confirms the recommendation or picks something else, and only the listed IDs change. A bare question forces the client to design the answer themselves and leaves holes in the requirements.

### 4. Write the spec

Follow the template exactly. Writing rules:

- **One behavior per requirement.** Split compound FRs so each can be accepted or rejected on its own.
- **Use normative language consistently.** `shall` for mandatory behavior; `should` only for targets that may be missed without failing acceptance (typically NFRs); `may` for permitted but optional behavior.
- **Be concrete and measurable.** Replace "fast", "user-friendly", "secure", "large" with numbers, formats, limits, and examples (e.g. `invoice-{invoiceNumber}.pdf`, "up to 1,000 line items", "within 3 seconds").
- **Name things the way users see them.** Use exact action labels, screen names, and role names.
- **Make Out of Scope explicit.** List what a reasonable reader might assume is included but is not. This is what prevents scope disputes later.
- **Write acceptance criteria in Given / When / Then.** Cover the main success path, every permission boundary, each business-relevant edge case, and failure behavior. Reference FRs by ID when a criterion verifies a list or rule defined there.
- **Keep user stories to 1–5**, near the top, for the people who matter most.
- **Stay implementation-agnostic.** No database tables, class names, or libraries unless the client explicitly requires a technology; those belong in a technical plan.
- **Number IDs sequentially within each prefix** (`US-1`, `FR-1`, `BR-1`, `EC-1`, `AC-1`, `NFR-1`, `OQ-1`) and never reuse or renumber IDs in a later version; mark removed items as `(Removed in vX.Y)` so version history stays traceable.

### 5. Self-check before delivering

- Every user story is realized by at least one FR.
- Every FR is verified by at least one AC, or is explicitly covered by an NFR with a measurable target.
- Every permission boundary and failure mode in the FRs, BRs, and ECs has a matching AC.
- No vague adjectives remain without a measurable definition.
- Nothing in Scope contradicts Out of Scope.
- Every open question has a recommendation, a reason, and the affected IDs, and those IDs are written to match the recommendation.
- Status is `Draft` when Open Questions remain; `Proposed` only when the spec is ready for client review with no open questions.

### 6. Save and report

In a repository, save the specification at `docs/specs/FEAT-NNN-<kebab-case-name>/FEAT-NNN-<kebab-case-name>.md`, creating the feature directory as needed. Choose the next free `FEAT-NNN` unless the user supplies an ID. If you are not working in a repository, return the spec in the response.

Report the file path, the variant used and why, the assumptions you made, and any open questions the client should resolve, with your recommendation for each.

## Updating An Existing Spec

Bump the version (`1.0` → `1.1` for clarifications, `2.0` for scope changes), keep existing IDs stable, and reset Status to `Draft` or `Proposed` to reflect the current state of the updated specification.
