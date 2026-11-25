---
name: cli-forge
description: "Parent router for the cli-forge skill family: detect the current workflow stage, resume from the earliest incomplete phase, and hand off to the correct child skill."
---

# cli-forge

Use this parent skill when you want one stable entrypoint for the full
`cli-forge` workflow instead of naming a stage skill up front.

This skill does not replace the child skills. Its job is to identify the
current stage, recover the earliest incomplete phase from repo state, and then
route work to the matching child skill.

## Canonical References

- [`../cli-forge-intake/SKILL.md`](../cli-forge-intake/SKILL.md)
- [`../cli-forge-description/SKILL.md`](../cli-forge-description/SKILL.md)
- [`../cli-forge-scaffold/SKILL.md`](../cli-forge-scaffold/SKILL.md)
- [`../cli-forge-extend/SKILL.md`](../cli-forge-extend/SKILL.md)
- [`../cli-forge-validate/SKILL.md`](../cli-forge-validate/SKILL.md)
- [`../cli-forge-publish/SKILL.md`](../cli-forge-publish/SKILL.md)

Read this file first, then move into the child skill that owns the current
phase.

## Parent Role

The parent skill is responsible for:

- classifying the request as `intake`, `description`, `scaffold`, `extend`,
  `validate`, or `publish`
- inspecting the current filesystem state when the request is ambiguous
- selecting the earliest incomplete stage instead of skipping ahead
- routing into the child skill that should do the actual work
- supporting resume flows when the user says only "continue cli-forge" or
  provides partial context

The parent skill should stay thin. It should not duplicate the detailed
instructions already owned by the child skills.

## Stage Selection

Choose the child skill using the request plus the current project state:

1. Route to `intake` when the request is ambiguous, when required inputs are
   missing, or when the correct stage is not obvious yet.
2. Route to `description` when the generated skill's purpose, positioning, or
   user-facing contract must be created or refreshed before implementation.
3. Route to `scaffold` when the user wants a brand-new Rust CLI Skill project
   and the approved description contract already exists.
4. Route to `extend` when a scaffolded project already exists and the requested
   change is exactly `stream` or `repl`, or when description-impacting work
   must continue into feature changes.
5. Route to `validate` when the user explicitly wants an audit or when freshly
   scaffolded or extended work needs verification.
6. Route to `publish` when validation is current and the workflow needs final
   closure, dry-run review, rehearsal, destination-config checks, or the
   documented release path.

If more than one stage seems plausible, inspect the filesystem and route to the
earliest stage that is not clearly complete.

## Resume Rules

- If no target project directory exists yet, resume at `description`, then
  continue into `scaffold`.
- If the directory exists but is missing the scaffold baseline, route back to
  `scaffold` rather than forcing feature or validation work through.
- If the project exists and the request is to add `stream` or `repl`, resume at
  `extend`.
- If scaffold or extend work just completed, always continue into `validate`
  before treating the workflow as done.
- If the user wants release work but validation is stale or missing, route back
  to `validate` first.
- If validation is current and the user did not explicitly ask for a release
  side effect, still continue into `publish` so the flow ends with
  `report_only` closure instead of stopping half-finished.

## Typical Flows

1. New project: `intake` -> `description` -> `scaffold` -> `validate` -> `publish`
2. Add feature: `intake` -> `extend` -> `validate` -> `publish`
3. Description update: `intake` -> `description` -> `extend` -> `validate` -> `publish`
4. Validation request: `intake` -> `validate` -> `publish`
5. Release-oriented request: `intake` -> `validate` -> `publish`, unless
   validation is already current

## Routing Examples

- "Create a new cli-forge skill" -> start with `intake`, then `description`.
- "Add repl to this generated skill" -> inspect the target project, then route
  to `extend` if the scaffold baseline is present.
- "Check whether this skill is compliant" -> route to `validate`.
- "Do a release dry run" -> route to `publish` only after confirming validation
  is current.
- "Continue cli-forge" -> inspect the repo and resume from the earliest
  incomplete stage.

## Done Condition

This parent skill is complete for the current request only when:

- the correct child skill has been selected
- the required inputs for that child skill are assembled or recoverable
- the handoff is explicit enough that work can continue without re-triage
