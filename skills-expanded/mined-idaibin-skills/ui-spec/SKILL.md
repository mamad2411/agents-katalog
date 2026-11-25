---
name: ui-spec
description: "Turn selected visual evidence into a UI Feature Spec or project-owned shared visual contract; not image generation or implementation."
---

# UI Specification

## Purpose

Produce an implementation-ready UI contract without replacing Product, shared design,
component/source, runtime-evidence, or delivery authority. This file is a routing map:
after selecting a branch, read only its referenced modules.

## Entry Gate

- Require either a source-grounded candidate brief or a selected/accepted visual
  source; otherwise stop as `evidence-incomplete`.
- Read effective repository guidance and current Worktree status before an authorized
  artifact write.
- Keep Product behavior, Feature UI Markdown, project-declared shared visual guidance,
  component/token source, runtime evidence, and Git delivery as separate authorities.

## Route Map

| Request state | Load | Result |
| --- | --- | --- |
| Applicability or source selection is unclear | [usage](references/usage.md) and [visual source](references/visual-source.md) | Resolve scope/source or stop |
| Direction is exploratory and unapproved | [candidate direction](references/candidate-visual-direction.md) | Ignored local candidate spec plus synchronized complete generation prompt; accepted shared authority unchanged; `Not Ready` |
| A page, flow, or accepted surface is selected | [workflow](references/workflow.md) and [documentation boundaries](references/documentation-boundaries.md) | Feature Spec and per-slice readiness |
| Check whether a supplied accepted UI contract needs a change | [contract evaluation](references/workflow.md#evaluation-and-handoff) and [evaluation rubric](references/evaluation-rubric.md) | Bounded contract delta or no-change result |
| Shared visual semantics are being adopted or changed | [profile gate](references/workflow.md#profile-gate) and [documentation boundaries](references/documentation-boundaries.md) | Bounded update to the project-declared shared authority |
| The project explicitly adopts Google DESIGN.md format or its additional completeness policy | [DESIGN.md contract](references/design-md-contract.md) | Applicable format/policy evidence for resolved `<design-root>/DESIGN.md` |
| Several independent surfaces are in scope | [multi-surface](references/multi-surface.md) | Shared index plus independently loadable slices/verdicts |
| An accepted surface requires a parameterized visual background | [visual asset contract](references/visual-asset-contract.md) | Source-bound recipe, readable area, fallback and target-surface acceptance |

## Invariants

- Candidate handoffs bind candidate spec/prompt revisions and hashes. Accepted-contract
  handoffs and evidence bind the accepted comparison-basis revision.
- Do not invent product behavior, exact values, assets, component ownership, rights,
  runtime facts, or shared semantics. Tag unknowns with the defined evidence level.
- Mark UI details absent from the accepted source as proposed, including added
  feedback placements or field-level errors; do not present them as accepted rules.
- For implementation handoff, an unresolved required component/owner mapping keeps
  that slice `Not Ready`. For each new page or visible UI slice, name the closest
  accepted page when one exists and actual public component/style owner in its existing
  contract or handoff; reuse them when they fit. If no accepted page exists or an owner
  does not fit, record that fact and reason without inventing a reference or blocking
  unrelated slices. "Existing owners unchanged" alone does not identify them.
- Do not duplicate shared tokens or component interfaces in a Feature Spec, introduce
  a parallel Registry/schema, or force Google `DESIGN.md` adoption because shared
  semantics change. Preserve the project's existing authority and approval requirements.
- A structured projection is conditional: use it only when a named owner, producer,
  non-LLM consumer, semantic version, executable validator, drift policy, and retirement rule
  already exist.
- Do not operate external AI, generate/edit images or SVG source, edit product source,
  operate browser/client state, or mutate Git. Route those actions to their owners.
- `Ready` covers only UI visual/interaction readiness. It is not Product approval,
  implementation, review, runtime, delivery, deployment, or production proof.

## Output Map

Return `ui.contract.specify@1.3.0` with lifecycle/profile, selected-source
identity/revision, selection/approval, rights/use/ignore boundaries, authority
disposition, slice IDs, applicable layout/state/interaction/accessibility and asset
contracts, delta/evidence references, comparison basis, per-slice readiness, and named
gaps. Candidate output additionally returns both ignored paths/hashes and handoff
status. Store task-local evidence under verified ignored `.codex/artifacts/`. Include
DESIGN/policy, viewport, SVG, or runtime-evidence fields only when the corresponding
module was activated.

## Reference Map

Load a module only when its condition applies:

| Condition | Module |
| --- | --- |
| Visual direction, theme, color, Preserve/Overhaul choice | [visual direction](references/visual-direction-and-anti-slop.md) |
| An accepted/candidate source names a scene archetype | [scene archetypes](references/scene-archetypes.md) |
| Layout ownership, inset, overlay, focus, hit order, or transition changes | [layout and interaction](references/frontend-layout-governance.md) |
| Repeated source measurements need normalization | [measurement normalization](references/measurement-normalization.md) |
| SVG/icon roles or fallback are part of acceptance | [SVG icon contract](references/svg-icon-system.md) |
| An accepted slice includes a parameterized gradient, texture or motion background | [visual asset contract](references/visual-asset-contract.md) |
| Current runtime is compared with a selected source | [visual evidence](references/frontend-visual-evidence.md) |
| Final readiness is being decided | [evaluation rubric](references/evaluation-rubric.md) |

Maintainers use [eval cases](references/eval-cases.md) for regression work; do not load
them during ordinary UI specification.
