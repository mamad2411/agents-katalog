---
name: spec-write-product
description: Write the PRODUCT.md phase of a gated spec-driven workflow for a significant user-facing feature or externally consumed surface. Use when the user asks for a product spec, desired behavior doc, PRD, behavior-first spec, or when a substantial or behaviorally ambiguous feature needs PRODUCT.md before TECH.md and implementation.
---

# spec-write-product

Write only the `PRODUCT.md` phase for a significant feature in the target product, app, service, API, CLI, library, or data model.

## Overview

The product spec should make the desired behavior unambiguous enough that an agent can implement it correctly and avoid regressions. Describe the feature purely from the user's perspective — what the user sees, does, and experiences, and the invariants that must hold for them. Do not include implementation details (internal types, state layout, module boundaries, data flow, algorithms).

"User" means whoever consumes the surface being designed:

- For UI / UX features: the human using the product or application.
- For a data model: the code that reads and writes that model.
- For an API, protocol, or library: the callers of that API — other services, client code, plugins, or agents.
- For a CLI tool or developer-facing surface: the developer invoking it.

The spec should describe behavior from that consumer's perspective: the shape of the surface, the operations they can perform, what they see back, invariants they can rely on, and edge cases they must handle — without prescribing how the surface is implemented underneath.

Implementation details, validation, and test planning live in a companion `TECH.md`, produced later by the `spec-write-tech` skill. Do not write or update `TECH.md` in the same phase as `PRODUCT.md`. After creating or materially changing `PRODUCT.md`, create or update sibling `GATES.json` with both statuses set to `pending`, then stop at the PRODUCT Review Gate and wait for the user to approve the product spec or explicitly ask to continue to the TECH phase.

Write specs to `specs-driven/<id>/PRODUCT.md`, where `<id>` is one of:

- a Linear ticket number (e.g. `specs-driven/APP-1234/PRODUCT.md`)
- a GitHub issue id, prefixed with `gh-` (e.g. `specs-driven/gh-4567/PRODUCT.md`)
- a GitLab issue id, prefixed with `gl-` (e.g. `specs-driven/gl-7890/PRODUCT.md`)
- a short kebab-case feature name (e.g. `specs-driven/vertical-tabs-hover-sidecar/PRODUCT.md`)

`specs-driven/` should contain only id-named directories as direct children — no engineer-named subdirectories.

The sibling gate state file is `specs-driven/<id>/GATES.json`. For new specs or materially changed product specs, it should contain:

```json
{
  "version": 1,
  "product": {
    "status": "pending"
  },
  "tech": {
    "status": "pending"
  }
}
```

Use only `pending` and `approved` statuses. Do not add hashes, revision ids, timestamps, approvers, or multiple artifact fields.

Ticket / issue references are optional. If the user has a Linear ticket, GitHub issue, or GitLab issue, use its id. If they don't, ask them for a feature name to use as the directory. Only create a new Linear ticket, GitHub issue, or GitLab issue when the user explicitly asks for one; in that case use the available Linear, GitHub, or GitLab tools respectively, and ask the user directly if team, labels, or repo are unclear.

## Before writing

Gather only the context you need: directory id (Linear ticket, GitHub issue, or feature name), feature summary, target users, key behaviors, edge cases, and any source material. Ask the user for missing product intent rather than guessing.

Classify unresolved questions before writing:

- **blocking**: the product behavior cannot be specified safely without an answer
- **non-blocking**: the spec can proceed with a recorded assumption and impact

Do not advance to TECH while blocking product questions remain.

### Figma mocks

If the feature has any UI or interaction design, ask the user whether a Figma mock exists before drafting the Behavior section, and include the link in the spec when one is provided. A mock is often the most reliable source of truth for visual states, spacing, and edge-case layouts — not asking can cause the Behavior section to guess at intent the designer already settled.

- If the user provides a link, include it under a short `## Figma` section (or inline near the top of Behavior) as `Figma: <link>`.
- If the user confirms no mock exists, note `Figma: none provided` so the absence is explicit rather than ambiguous.
- If the feature is purely backend (data model, API, CLI with no visual surface), skip the question and omit the section.

Do not silently drop design context; an explicit "none" is preferable to no mention at all on features where design would normally be expected.

## Structure

Required sections:

1. **Summary** — 1–3 sentences describing the feature and desired outcome.
2. **Behavior** — The meat of the spec. An exhaustive English description of how the feature works, written as stable numbered, testable invariants such as `B1`, `B2`, and `B3`. See "The Behavior section" below — this is where the spec earns its length, and everything else should stay thin to avoid duplicating it.

Optional sections — include only when they add signal beyond the core. Omit the heading entirely if empty; do not write "None" as a placeholder.

- **Problem** — Include only when the motivation isn't obvious from Summary.
- **Goals / Non-goals** — Include when scope is ambiguous or has been contested.
- **Figma** — Include with a link when one exists, or an explicit `Figma: none provided` note when design matters but no mock exists. Omit entirely for non-visual features. See "Figma mocks" above.
- **Diagram** — Include a Mermaid diagram only when it clarifies non-trivial product behavior, such as branching user journeys, role or permission interactions, object lifecycle states, complex state transitions, or cross-module product interactions. Omit diagrams for short linear flows or when the diagram would merely duplicate the numbered Behavior list.
- **Open questions** — Prefer inline `**Open question (blocking):** ...` or `**Open question (non-blocking):** ...` next to the relevant behavior. Include a dedicated section only if there are multiple unresolved questions worth collecting. Non-blocking questions must state the current assumption and impact.

Do not include Validation, Success criteria, or Testing sections. Validation and test planning live in the companion `TECH.md` (produced by `spec-write-tech`). Write Behavior as numbered invariants that are testable on their own — the tech spec can reference them directly.

## The Behavior section

Behavior is the spec. Everything else is framing.

The goal of Behavior is a complete English description of how the feature works, detailed enough that a tech spec can be written directly from it without the author having to guess or re-derive product intent. If a reader finishes Behavior with questions about what the feature does in some situation, the section is not done.

Describe, at minimum:

- Default behavior and the happy-path user flow.
- Every user-visible state and the transitions between them.
- All inputs the user can provide and how the feature responds.
- Empty states, error states, loading / pending states, and cancellation.
- Edge cases a reasonable implementer would not think to ask about — permission denied, offline, timeouts, races between state changes, multiple concurrent instances, stale or missing data, focus loss mid-interaction, interactions with adjacent features.
- Keyboard, accessibility, and focus expectations where relevant.
- Invariants that must hold at all times and behaviors that must not regress.

Length Behavior to match the feature. Trivial features may need a handful of invariants; complex features may need many, with sub-sections per flow or state. The rest of the spec should stay thin so Behavior can be as exhaustive as the feature requires without producing a bloated document overall. Err toward enumerating one more edge case rather than one fewer.

### Mermaid diagrams

Use Mermaid diagrams in `PRODUCT.md` sparingly. A diagram is appropriate when it makes complex user-visible behavior easier to review, such as a branched journey, lifecycle, permission path, state transition, or cross-module product interaction. Prefer the Mermaid type that matches the need: flowchart for branching flows, state diagram for lifecycles, and sequence diagram for user-visible cross-system interactions.

Do not include diagrams for simple linear behavior, narrow copy or UI tweaks, or flows that are clearer as numbered invariants. A diagram must complement the Behavior section, not replace it. Required behavior still belongs in stable numbered items, and every diagram should be supported by concise text that explains the important behavior or decision.

## Length heuristic

Behavior should be as long as the feature requires — do not truncate edge cases to hit a line target. The heuristic below applies to everything around Behavior (Summary, optional sections): keep that framing thin so the spec's total length reflects the feature's actual complexity, not structural overhead.

- Trivial fix or narrow UI tweak: no spec.
- Small feature (single module, few edge cases): framing plus Behavior typically ~30–60 lines total.
- Medium feature (cross-module, multiple states): typically ~80–150 lines total.
- Large or behaviorally rich feature: longer is fine, and most of the length should live in Behavior.

If you find yourself writing the same idea in Summary, Problem, Goals, and Behavior, collapse the framing — not the Behavior content.

## Writing guidance

- Prefer concrete, observable behavior over aspirational wording.
- Write Behavior as a list of invariants rather than prose when possible.
- Capture invariants that must not regress and edge cases that are easy to miss.
- Use Mermaid diagrams only when they clarify complex product behavior; avoid decorative, oversized, vague, or redundant diagrams.
- Avoid implementation details unless unavoidable for the UX.
- Each section should earn its place — if a section would repeat another or contain only boilerplate, omit it.

## Keep the spec current

Approved specs may ship in the same PR as the implementation. As implementation evolves, update `PRODUCT.md` in the same PR when user-facing behavior or UX details change. The checked-in spec should describe the feature that actually ships.

If `PRODUCT.md` changes after `TECH.md` exists, treat the current `TECH.md` as stale until it is updated from the latest reviewed product spec. Set both `product.status` and `tech.status` in `GATES.json` to `pending`.

## PRODUCT Review Gate

After writing or materially changing `PRODUCT.md`, stop before invoking `spec-write-tech`.

Gate handoff requirements:

- state whether blocking product questions remain
- if no blockers remain, ask the user to approve `PRODUCT.md` or explicitly request the TECH phase
- if blockers remain, show a concise list of all blocking product questions so the user can see the full gate scope
- even when the full blocker list is shown, ask the user to clarify only one blocking question at a time; prioritize the question that most directly unlocks the next `PRODUCT.md` revision
- ask only product-behavior blockers, not broad preference questions, implementation questions, or questions whose answer can be recorded as a non-blocking assumption
- for the active blocking question, provide suggested answer options only when they reduce user effort or clarify a real product tradeoff
- when suggested options are provided, offer one or two options; one option is acceptable when there is a clear recommended path and the user mainly needs to confirm or override it
- make suggested options concrete product choices, not technical implementation plans, and describe the user-visible behavior or workflow impact
- when there is a recommended option, mark it as recommended and give a short reason focused on product behavior, user effort, or workflow clarity
- summarize non-blocking questions as the assumptions and impact already recorded in `PRODUCT.md`

If the user answers a blocking question, update `PRODUCT.md` to reflect the decision, keep both statuses in `GATES.json` as `pending`, and return to the PRODUCT Review Gate. Continue this one-question-at-a-time loop until no blocking product questions remain. Selecting a suggested option answers only that blocking question; it does not approve the whole product spec unless the user also explicitly approves `PRODUCT.md` or asks to continue to TECH.

The gate passes only when:

- the user explicitly approves `PRODUCT.md`, or explicitly asks to continue to the TECH phase
- no blocking open questions remain
- non-blocking open questions have recorded assumptions and impact
- behavior is concrete enough that the TECH author does not need to guess product intent
- `product.status` is updated to `approved` in `GATES.json`

If the gate does not pass, revise `PRODUCT.md`, keep both statuses in `GATES.json` as `pending`, and remain in the product phase.

For large features, the implementer may optionally keep a `DECISIONS.md` file summarizing concrete decisions made during design and implementation. Offer it when it would help future agents; otherwise skip it.

## Related Skills

- `spec-implement`
- `spec-write-tech`
- `spec-driven-workflow`

## Example Behavior section

For a full sample Behavior section, read `references/behavior-example.md` when you need a concrete model for the expected shape.
