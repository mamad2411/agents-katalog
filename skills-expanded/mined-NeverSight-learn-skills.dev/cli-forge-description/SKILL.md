---
name: cli-forge-description
description: "Description stage for the cli-forge skill family: define or refresh the generated skill description contract before downstream stages change scaffold, feature, validation, or packaging surfaces."
---

# cli-forge Description

Use this stage when the workflow needs one authoritative description contract
for a generated Rust CLI Skill before later stages proceed.

## When To Use This Stage

- Intake classified the work as a new generated skill.
- The requested change alters the generated skill's purpose, positioning, or
  user-facing contract.
- A later stage detects drift between Cargo metadata, `SKILL.md`, README, help
  text, or release-facing summaries.

## Stage Goal

Finish this stage with one approved description contract that downstream stages
must reuse instead of inventing new summaries independently.

## Canonical References

- [`./instructions/new.md`](./instructions/new.md)
- [`./instructions/add-feature.md`](./instructions/add-feature.md)
- [`./planning-brief.md`](./planning-brief.md)

Read the instruction files as the detailed source of truth for how the
description contract is consumed during scaffold or feature work.

## Required Inputs

- classified workflow intent from `intake`
- current or proposed generated skill scope
- any existing description surfaces that must stay aligned
- the target next stage:
  - `scaffold` for new skills
  - `extend` for existing skills whose public contract changes
  - `validate` when only verification is needed after description alignment
  - `publish` only for final summaries after validation is current

## Description Contract Outputs

- approved one-line purpose summary
- approved positioning statement
- inventory of description surfaces that must reuse the same contract
- explicit next-stage handoff and done criteria

## Workflow

1. Confirm whether the work creates a new generated skill or changes the
   user-facing contract of an existing one.
2. Define or refresh the approved purpose summary and positioning statement.
3. Record which downstream surfaces must stay synchronized:
   - `Cargo.toml` package description
   - `SKILL.md`
   - `README.md`
   - help text / structured help summaries
   - packaging or publish-facing summaries
4. Confirm the next stage that is allowed to consume the approved description
   contract.
5. Hand the approved contract forward without letting downstream stages invent
   competing wording.

## Guardrails

- `description` is the authoritative stage for user-facing purpose and
  positioning.
- `scaffold`, `extend`, `validate`, and `publish` consume the approved
  contract; they do not redefine it.
- `publish` may summarize the contract for release readiness, but it must not
  overwrite the approved description surfaces.

## Done Condition

This stage is complete only when every required description surface is named,
the approved summary and positioning are ready for reuse, and the next stage is
explicit.

## Next Step

- Continue with [`../cli-forge-scaffold/SKILL.md`](../cli-forge-scaffold/SKILL.md)
  for new generated skills.
- Continue with [`../cli-forge-extend/SKILL.md`](../cli-forge-extend/SKILL.md)
  when an existing skill's public contract changes alongside feature work.
- Continue with [`../cli-forge-validate/SKILL.md`](../cli-forge-validate/SKILL.md)
  when description alignment is ready for verification.
- Continue with [`../cli-forge-publish/SKILL.md`](../cli-forge-publish/SKILL.md)
  only after validation is current and the workflow needs final closure.
