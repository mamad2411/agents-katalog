---
name: python-blueprint-authoring
description: Author a review-ready greenfield `blueprint.md` contract for a new or baseline-only Python repository, reusing the locked blueprint v1 schema already consumed by `python-project-init-greenfield`.
complexity: high
risk_profile:
  - ambiguity_sensitive
  - multi_agent_handoff
  - destructive_action
inputs:
  - target repository or project name and proof that the lane is truly greenfield or baseline-only
  - project purpose and baseline scope for Project Overview
  - exact required skill names that already exist in the current library
  - concrete toolchain choices and versions for Toolchain Expectation
  - concrete packages, paths, entrypoints, and other locatable structure for Structural Invariants
  - measurable quality targets and concrete sensing assertions for Quality Thresholds and Acceptance Criteria
outputs:
  - review-ready greenfield blueprint.md using the locked blueprint v1 section order
  - stop-and-ask feedback when required skills are missing, structure is abstract, or the request is in the wrong lane
  - a contract that python-project-init-greenfield can consume without schema translation or guessed locators
use_when:
  - a new or baseline-only Python repository needs its first review-ready blueprint.md
  - the task is to author or repair a greenfield blueprint before execution starts
  - the contract must stay inside the locked blueprint v1 shape already consumed by python-project-init-greenfield
do_not_use_when:
  - the repository already has meaningful structure, migration pressure, or retrofit conflict surfaces; use python-retrofit-plan-authoring
  - the task is to execute a valid blueprint; use python-project-init-greenfield
  - the task is to review or approve an existing blueprint
  - the request lacks tool choices, verifiable acceptance targets, or locatable structural details that cannot be derived safely from explicit intent or the repository name
---

# Purpose
Turn greenfield Python repository intent into a review-ready `blueprint.md` that `python-project-init-greenfield` can consume without reinterpretation.

# Trigger / When to use
Use this skill when:
- a new or baseline-only Python repository needs its first review-ready `blueprint.md`
- the task is to author or repair a greenfield blueprint before execution starts
- the workflow needs exact-name `Required Skills` validation, concrete `Structural Invariants`, and explicit stop-and-ask handling for ambiguity
- the authored contract must stay inside the locked blueprint v1 shape already used by `python-project-init-greenfield`

Do not use this skill when:
- the repository already has meaningful structure, migration pressure, or retrofit conflict surfaces; use `python-retrofit-plan-authoring`
- the task is to execute a valid blueprint; use `python-project-init-greenfield`
- the task is to review or approve an existing blueprint
- the request lacks tool choices or verifiable acceptance targets, or lacks package names or other locatable structural details that cannot be derived safely from explicit intent or the repository name; if a package name is derived, record the concrete derived name in the authored blueprint before handoff

# Inputs
- the target repository or project name and proof that the lane is truly greenfield or baseline-only
- the intended project purpose and baseline scope for `## Project Overview`
- exact required skill names that already exist in the current library
- concrete toolchain choices and versions for `## Toolchain Expectation`
- concrete packages, paths, entrypoints, and other locatable structure for `## Structural Invariants`
- measurable quality targets and concrete sensing assertions for `## Quality Thresholds` and `## Acceptance Criteria`
- explicit human clarification whenever the request is abstract, contradictory, missing a locatable detail, or routed to the wrong lane

# Process
1. Confirm lane fit first.
   - Use this skill only for new or baseline-only Python repositories.
   - If the request is really retrofit planning, route to `python-retrofit-plan-authoring`.
   - If the request is execution or review, hand off to `python-project-init-greenfield` or reviewer flow instead of absorbing those roles.
2. Reuse the locked blueprint v1 contract exactly.
   - Author only the heading order already consumed by `python-project-init-greenfield`.
   - Do not invent a new section, alias, compatibility layer, or alternate block format.
3. Validate `Required Skills` before drafting the final contract.
   - Check every named skill against the current library using exact directory names.
   - Treat `_` versus `-`, case changes, guessed aliases, and invented placeholders as invalid.
   - If any named skill is absent, stop and ask instead of normalizing or deferring the problem downstream.
4. Write the blueprint in the locked section order:
   1. `## Project Overview`
   2. `## Required Skills`
   3. `## Toolchain Expectation`
   4. `## Structural Invariants`
   5. `## Quality Thresholds`
   6. `## Acceptance Criteria`
5. Write `## Project Overview` as concise human-readable baseline intent.
   - Summarize the repository purpose and baseline goals.
   - Do not hide missing structural decisions behind general prose.
6. Write `## Required Skills` with exact current-library names and explicit roles.
   - Keep each listed skill locatable as `skills/<skill-name>/` in the active library.
   - Preserve an optional marker only as `(Optional)` after the exact skill name when truly needed.
7. Write `## Toolchain Expectation` and `## Structural Invariants` with concrete, executor-usable detail.
   - Name real tools, versions, package names, paths, and entrypoints.
   - If the request says only “modern layout”, “good defaults”, or similar abstract goals, stop and ask.
   - If structural details are contradictory or cannot be located in the filesystem, stop and ask.
8. Write `## Quality Thresholds` and `## Acceptance Criteria` as verifiable contract surfaces.
   - Under `## Acceptance Criteria`, place a fenced `yaml [sensing-assertions]` block immediately below the heading.
   - Every assertion record must include `kind`, `target`, and `expected`.
   - Keep human explanation outside the machine-readable block.
9. Run the authoring self-check before handoff.
   - Confirm section order, assertion-block placement, exact-name skill validation, locatable structure, and greenfield lane fit.
   - Confirm the draft stays upstream-authoring-only and does not widen into executor changes.
10. Stop at `review-ready`.
    - Do not approve the blueprint.
    - Hand the draft to reviewer flow once the contract is complete.

# Examples
- Positive: Author a greenfield `blueprint.md` for an empty weather repository that lists `sense-env-scaffold`, `python-testing-pytest`, and `python-type-hints-strict` by exact library name, declares `src/weather_service/main.py`, and puts a `yaml [sensing-assertions]` block immediately under `## Acceptance Criteria`.
- Negative: Draft a blueprint for an existing repository that needs migration, guess a missing skill as `python_testing_pytest`, or write `Structural Invariants` as “use a modern src layout with good defaults”.

# Outputs
- a review-ready greenfield `blueprint.md` using the locked blueprint v1 section order
- exact stop-and-ask feedback when required skills are missing, structure is abstract, or the request is in the wrong lane
- a contract that `python-project-init-greenfield` can consume without schema translation or guessed locators

# Validation

## Required Checks
- all six blueprint v1 sections are present in exact order: Project Overview → Required Skills → Toolchain Expectation → Structural Invariants → Quality Thresholds → Acceptance Criteria
- every schema v1 field is populated with concrete, executor-usable values; no section is left empty or abstract
- no TBD placeholder or abstract style words (e.g. "modern", "sensible", "clean") appear in any locked field
- `## Acceptance Criteria` starts with a parseable `yaml [sensing-assertions]` block immediately below the heading
- every sensing assertion includes `kind`, `target`, and `expected`
- every named required skill matches a real current-library directory name exactly

## Quality Checks (best effort)
- naming conventions are consistent across package names, paths, and entrypoints
- toolchain dependency choices are justified or accompanied by rationale notes
- `## Project Overview` is concise and hides no missing structural decisions behind general prose
- sensing assertions cover the main structural invariants declared in `## Structural Invariants`

## On Soft Fail
- mark blueprint as INCOMPLETE at the top of the draft
- list every missing or abstract section explicitly
- do not block output; deliver the partial draft with gaps flagged so the reviewer can act

# Failure Handling

## Missing Context
- BLOCKED — if project intent, package name, or key structural decisions are not provided and cannot be safely derived from explicit context, stop and ask before proceeding
- list the specific missing inputs explicitly; do not fabricate locators, package names, or sensing assertions to fill gaps

## Ambiguous Requirement
- note the assumption explicitly as a sub-bullet under an existing section of the blueprint (e.g., under `## Implementation Notes`)
- proceed with best-effort draft using the stated assumption
- flag the assumption clearly so the reviewer and `python-project-init-greenfield` consumer can evaluate it before handoff

## Execution Limitation
- if the schema v1 reference (`references/blueprint-contract.md`) cannot be read, note the limitation explicitly in the draft
- fall back to the known locked section order and block placement rules embedded in this skill's Process
- do not invent new sections or omit required ones to work around the limitation

# Verification
- confirm the section order is exactly Project Overview -> Required Skills -> Toolchain Expectation -> Structural Invariants -> Quality Thresholds -> Acceptance Criteria
- confirm `## Acceptance Criteria` starts with a parseable `yaml [sensing-assertions]` block
- confirm every sensing assertion includes `kind`, `target`, and `expected`
- confirm every named required skill matches a real current-library directory name exactly
- confirm package names, paths, entrypoints, and tool choices are concrete enough for executor consumption
- confirm greenfield-only lane fit is explicit and retrofit requests are rerouted instead of absorbed
- confirm the skill stays in authoring scope and does not imply executor or reviewer approval

# Red Flags
- the request mixes “create the first baseline” with “preserve and migrate these existing files”
- a named required skill does not exist in `skills/`
- `Structural Invariants` contain only style words such as “clean”, “modern”, or “sensible”
- acceptance prose appears before the `yaml [sensing-assertions]` block
- the request tries to make `python-blueprint-authoring` choose execution-time behavior or modify the executor schema

# Common Rationalizations
- “The executor can normalize the skill name later.”
- “We can leave the structure abstract because greenfield repos are easy.”
- “This repo mostly exists already, but blueprint authoring is close enough.”
- “The sensing assertions can be added after init works once.”
- “A missing required skill can stay as a placeholder for now.”

# Boundaries
- Do not execute the blueprint.
- Do not approve the authored blueprint.
- Do not invent a new blueprint schema or widen the executor contract.
- Do not normalize, alias, or silently replace missing skill names.
- Do not invent package names, paths, entrypoints, tool choices, or sensing assertions when the request is abstract.
- Do not absorb retrofit planning, runtime routing, or reviewer responsibilities.

# Local references
- `examples.md`: layered blueprint-authoring scenarios, stop-and-ask cases, and lane-mismatch examples
- `checklist.md`: repeatable review-ready checks for this higher-risk authoring skill
- `references/blueprint-contract.md`: locked blueprint v1 section order, block placement, and parser-facing authoring rules
- `references/required-skills-validation.md`: exact-name library validation rules, optional-item handling, and blocking missing-skill behavior
- `references/greenfield-lane-boundaries.md`: greenfield-only fit rules and rerouting boundaries versus retrofit or execution
- `references/structural-invariants-locatability.md`: concrete locatability rules for packages, paths, entrypoints, and stop-and-ask triggers
