---
name: cli-forge-extend
description: "Extension stage for the cli-forge skill family: add the supported stream or repl feature to an existing scaffolded project while preserving the shared runtime contract."
---

# cli-forge Extend

Use this stage when an existing scaffolded Rust CLI Skill project needs one of
the supported optional features: `stream` or `repl`, or when a
description-impacting change must continue into feature work after the
description stage refreshed the contract.

## When To Use This Stage

- Intake classified the work as optional feature extension.
- The description stage already ran when the request changed the skill's
  purpose, positioning, or other user-facing contract.
- The target project already has the scaffold baseline.
- The requested feature is exactly `stream` or `repl`.

## Stage Goal

Apply the requested feature cleanly, keep the project aligned with the
planning brief,
and prepare the result for validation.

## Canonical References

- [`./instructions/add-feature.md`](./instructions/add-feature.md)
- [`./planning-brief.md`](./planning-brief.md)

Read `instructions/add-feature.md` as the exact source of truth for pre-checks,
file patches, required touched files, and post-edit verification.

## Required Inputs

- `project_path`
- `feature` where `feature` is exactly `stream` or `repl`

## Workflow

1. Run the pre-checks from
   [`./instructions/add-feature.md`](./instructions/add-feature.md):
   resolve the path, confirm the scaffolded files exist, validate the feature
   name, and stop if the feature is already present.
2. Expand the matching template into the target project:
   - `stream` -> `src/stream.rs`
   - `repl` -> `src/repl.rs`
3. Apply the required source, help, and documentation updates described in the
   instruction file.
4. Preserve the shared runtime contract while editing:
   plain-text `--help`, structured `help`, runtime-directory docs, and Active
   Context behavior must stay accurate.
5. Keep the generated package within the documented boundary:
   package-local support files may be added when the enabled capability
   requires them, but repository-owned CI workflows, release scripts, and
   release automation must not be copied into the generated skill.
6. Run the required verification commands after the edit:
   `cargo build`, `cargo test`, `cargo clippy -- -D warnings`, and
   `cargo fmt --check`.

## Guardrails

- Do not use this stage on a project that is missing the scaffolded baseline.
  Return to the earlier scaffold phase instead.
- Do not add unsupported features beyond `stream` and `repl`.
- Keep feature-specific changes scoped to the files and behaviors described by
  the instruction file.
- If the request changes the generated skill's public description and feature
  behavior together, treat the approved description contract as an input rather
  than inventing new summaries here.

## Done Condition

This stage is complete only when the requested feature is present and the
required verification commands pass.

## Next Step

Continue with [`../cli-forge-validate/SKILL.md`](../cli-forge-validate/SKILL.md)
to verify the project after the extension work.
