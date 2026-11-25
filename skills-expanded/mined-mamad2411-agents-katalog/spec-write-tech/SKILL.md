---
name: spec-write-tech
description: Write the TECH.md phase of a gated spec-driven workflow after PRODUCT.md has been reviewed. Use when the user asks for a technical spec, implementation plan, architecture doc, or validation plan derived from an approved product spec or behavior-first specification.
---

# spec-write-tech

Write the `TECH.md` phase for a significant feature in the target product, app, service, API, CLI, library, or data model.

## Overview

The tech spec should translate reviewed product intent into an implementation plan that fits the existing codebase, documents architectural choices, and makes the work easier for agents to execute and reviewers to evaluate.

Write specs to `specs-driven/<id>/TECH.md`, where `<id>` is one of:

- a Linear ticket number (e.g. `specs-driven/APP-1234/TECH.md`)
- a GitHub issue id, prefixed with `gh-` (e.g. `specs-driven/gh-4567/TECH.md`)
- a GitLab issue id, prefixed with `gl-` (e.g. `specs-driven/gl-7890/TECH.md`)
- a short kebab-case feature name (e.g. `specs-driven/vertical-tabs-hover-sidecar/TECH.md`)

Match the id used by the sibling `PRODUCT.md` when one exists. `specs-driven/` should contain only id-named directories as direct children.

The sibling gate state file is `specs-driven/<id>/GATES.json`. It stores only `version`, `product.status`, and `tech.status`; statuses may only be `pending` or `approved`.

Ticket / issue references are optional. If the user has a Linear ticket, GitHub issue, or GitLab issue, use its id. If they don't, ask them for a feature name to use as the directory. Only create a new Linear ticket, GitHub issue, or GitLab issue when the user explicitly asks for one; in that case use the available Linear, GitHub, or GitLab tools respectively, and ask the user directly if team, labels, or repo are unclear.

## Prerequisites

Before writing `TECH.md`, confirm:

- sibling `PRODUCT.md` exists
- sibling `GATES.json` exists
- `product.status` is `approved` in `GATES.json`, which is the persisted record that PRODUCT Review Gate passed because the user explicitly approved `PRODUCT.md` or explicitly asked to continue to TECH
- no blocking product open questions remain
- non-blocking product open questions have recorded assumptions and impact

If any prerequisite is missing, do not write `TECH.md`. Return to `spec-write-product` or ask for the missing review signal.

## Research before writing

Before drafting, read the latest reviewed `PRODUCT.md`, inspect the relevant code, and identify the main files, types, data flow, and ownership boundaries. Do not guess about current architecture when the code can be inspected directly.

## Structure

Required sections:

1. **Context** — What's being built, how the current system works in the area being changed, and the most relevant files with line references. Combine the "problem," "current state," and "relevant code" into one grounded section. Example references:
   - `app/src/workspace/mod.rs:42` — entry point for the user flow
   - `app/src/workspace/workspace.rs (120-220)` — state and event handling that will likely change
   Reference `PRODUCT.md` for user-visible behavior rather than restating it.
2. **Proposed changes** — The implementation plan: which modules change, new types/APIs/state being introduced, data flow, ownership boundaries, and how the design follows existing patterns. Call out tradeoffs when there is more than one reasonable path.
3. **Product behavior mapping** — Map important numbered Behavior invariants from `PRODUCT.md` to the implementation areas and validation approach. Do not redefine product behavior.
4. **Testing and validation** — How the implementation will be verified against the product behavior. Owns everything about proving the feature works: unit tests, integration tests, manual steps, screenshots, videos, and any other verification. Reference the numbered Behavior invariants from `PRODUCT.md` directly rather than restating them; each important invariant should map to a concrete test or verification step. This section is where validation lives — `PRODUCT.md` intentionally does not have a Validation section.

Optional sections — include only when they add signal. Omit the heading entirely if empty; do not write "None" as a placeholder.

- **End-to-end flow** — Include only when tracing the path through the system tells you something the Proposed changes list doesn't.
- **Diagram** — Include a Mermaid diagram when it clarifies non-trivial architecture, data movement, request flow, state transitions, async work, migration sequencing, or integrations faster than prose alone. Prefer one or two focused diagrams over broad or decorative ones, and omit diagrams when the plan is small or clearer as prose and bullets.
- **Risks and mitigations** — Include when there are real failure modes, regressions, migration concerns, or rollout hazards worth calling out.
- **Parallelization** — Include when work can cleanly split across multiple agents and that split is non-obvious.
- **Follow-ups** — Include when there is deferred cleanup or future work worth naming.

### Mermaid diagrams

Use Mermaid diagrams more actively in `TECH.md` than in `PRODUCT.md`, but keep them conditional. Add a diagram when it answers a concrete implementation question: how components interact, how data moves, how a request proceeds through layers, how an async job changes state, how a migration is sequenced, or how external integrations connect.

Choose a Mermaid type that matches the technical need: flowchart for architecture or branching implementation flow, sequence diagram for cross-system calls, state diagram for lifecycles or background jobs, and focused architecture-style flowcharts for system boundaries. Do not add decorative diagrams, oversized diagrams, vague node labels, or diagrams that simply restate a short checklist.

Every diagram must be accompanied by concise prose explaining the design decision, behavior, or data flow that matters. Diagrams complement the technical plan; they do not replace Proposed changes, Product behavior mapping, or Testing and validation.

## Length heuristic

Right-size the spec to the feature:

- Single-file change with clear approach: skip spec-driven workflow entirely, or keep `TECH.md` under ~40 lines if the workflow was already chosen.
- Multi-module change with some ambiguity: target ~80–150 lines.
- Large cross-cutting or architecturally novel change: longer is fine when every section earns its place.

If Context and Proposed changes end up describing the same files and state from different angles, collapse them.

## Writing guidance

- Ground the plan in actual codebase structure and patterns.
- Prefer concrete implementation guidance over generic architecture language.
- Explain why the proposed design fits this repo.
- Reference `PRODUCT.md` for behavior instead of restating it.
- Use Mermaid diagrams when they materially clarify technical flow or structure, and omit them when prose is clearer.
- If technical research shows product behavior is infeasible or should change, return to `PRODUCT.md`; do not silently redefine behavior in `TECH.md`.
- Each section should earn its place — if a section would repeat another or contain only boilerplate, omit it.

## Keep the spec current

Approved specs may ship in the same PR as the implementation. Update `TECH.md` in the same PR when module boundaries, implementation sequencing, risks, validation strategy, or rollout assumptions change, and set `tech.status` in `GATES.json` to `pending`. The checked-in spec should describe the implementation that actually ships.

If `PRODUCT.md` changes after `TECH.md` is written, treat the current `TECH.md` as stale until it is updated from the latest reviewed `PRODUCT.md`. Set both statuses in `GATES.json` to `pending`.

## TECH Review Gate

After writing or materially changing `TECH.md`, set `tech.status` in `GATES.json` to `pending` and stop before implementation.

Gate handoff requirements:

- state whether blocking technical questions remain
- if no blockers remain, ask the user to approve `TECH.md` or explicitly request implementation
- if blockers remain, show a concise list of all blocking technical questions so the user can see the full gate scope
- even when the full blocker list is shown, ask the user to clarify only one blocking technical question at a time; prioritize the question that most directly unlocks the next `TECH.md` revision
- treat a blocking technical question as a decision required before safe implementation, such as unclear module ownership, an architecture choice, migration or rollout risk, validation strategy, dependency choice, or another unresolved implementation prerequisite
- keep active blockers technical; if an answer changes product behavior, user-visible acceptance expectations, or externally observable semantics, update `PRODUCT.md`, set both statuses in `GATES.json` to `pending`, and return to PRODUCT Review Gate before revising TECH again
- for the active blocking question, provide suggested answer options only when they reduce user effort or clarify a real implementation tradeoff
- when suggested options are provided, offer one or two options; one option is acceptable when there is a clear recommended path and the user mainly needs to confirm or override it
- make suggested options concrete technical plan choices, not product behavior changes, and describe the implementation impact, risk, validation impact, or workflow impact
- when there is a recommended option, mark it as recommended and give a short reason focused on codebase fit, risk reduction, implementation clarity, or validation confidence
- summarize non-blocking technical questions as the assumptions and impact already recorded in `TECH.md`

If the user answers a blocking technical question, update `TECH.md` to reflect the decision, keep `tech.status` in `GATES.json` as `pending`, and return to the TECH Review Gate. Continue this one-question-at-a-time loop until no blocking technical questions remain. Implementation cannot begin while any blocking technical question remains. Selecting a suggested option answers only that blocking technical question; it does not approve the whole technical spec unless the user also explicitly approves `TECH.md` or asks to continue to implementation.

The gate passes only when:

- the user explicitly approves `TECH.md`, or explicitly asks to continue to implementation
- no blocking technical questions remain
- non-blocking technical questions have recorded assumptions and impact
- the technical plan is consistent with `PRODUCT.md`
- risks, module boundaries, and validation steps are clear enough for implementation
- the implementer can start without redesigning the main approach
- `tech.status` is updated to `approved` in `GATES.json`

If the gate does not pass, revise `TECH.md` and keep `tech.status` as `pending`. If the revision changes product behavior, update `PRODUCT.md`, set both statuses in `GATES.json` to `pending`, and pass PRODUCT Review Gate again before updating `TECH.md`.

For large features, the implementer may optionally keep a `DECISIONS.md` file summarizing concrete decisions. Offer it when it would help future agents; otherwise skip it.

## Related Skills

- `spec-implement`
- `spec-write-product`
- `spec-driven-workflow`
