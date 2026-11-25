---
name: cli-forge-scaffold
description: "Scaffold stage for the cli-forge skill family: create a new Rust CLI Skill project from the package templates and prepare it for validation."
---

# cli-forge Scaffold

Use this stage when the work is to create a brand-new Rust CLI Skill project
from this package and the description stage has already approved the generated
skill's description contract.

## When To Use This Stage

- The target project does not exist yet.
- Intake has classified the work as new-project scaffolding.
- The description stage has produced the approved purpose summary and
  positioning contract for the new skill.
- A prior extension attempt revealed that the scaffold baseline is missing.

## Stage Goal

Create a planning-brief-aligned project scaffold that is immediately ready for
validation and reuses the approved description contract across generated
surfaces.

## Canonical References

- [`./instructions/new.md`](./instructions/new.md)
- [`./planning-brief.md`](./planning-brief.md)

Read `instructions/new.md` as the exact source of truth for token expansion,
file layout, required commands, and verification checks.

## Required Inputs

- `skill_name`
- optional `author`
- optional `version`
- optional `rust_edition`
- approved description contract from `description`

## Workflow

1. Follow the pre-checks in [`./instructions/new.md`](./instructions/new.md):
   validate the name, require it when missing, and refuse to overwrite an
   existing target directory.
2. Create the directory structure and expand the templates exactly as the
   instruction file defines, reusing the approved description contract instead
   of inventing new wording during scaffold.
3. Verify that no template tokens remain unresolved.
4. Run the required verification commands from the generated project root:
   `cargo build`, `cargo clippy -- -D warnings`, `cargo fmt --check`, and
   `cargo test`.
5. Confirm the generated project exposes the shared runtime contract surfaces
   described in the instruction file.
6. Confirm the generated package layout stays within the documented boundary:
   baseline generated files plus any package-local support files that a
   supported capability requires. Repository-owned CI workflows, release
   scripts, and release automation stay outside the generated project.

## Guardrails

- Do not improvise a different project structure from the templates.
- Keep the generated project aligned with the planning brief's CLI and text I/O
  rules.
- If any verification step fails, fix the scaffold before handing the work
  forward.

## Done Condition

This stage is complete only when the new project exists, the template expansion
is clean, and the required checks pass.

## Next Step

Continue with [`../cli-forge-validate/SKILL.md`](../cli-forge-validate/SKILL.md)
unless the user explicitly asked to stop after scaffolding.
