---
name: cli-forge-intake
description: "Triage stage for the cli-forge skill family: classify the request as description, scaffold, extend, validate, or publish, confirm required inputs, load the shared rules, and hand off to the correct next phase."
---

# cli-forge Intake

Use this stage when the current request needs routing or when you want to
resume the cli-forge workflow from the earliest safe phase.

## Stage Goal

Finish this stage with:

- the work classified as `scaffold`, `extend`, `validate`, or `publish`
- the work classified as `description`, `scaffold`, `extend`, `validate`, or
  `publish`
- the required user inputs identified and, when available, assembled
- the shared constraints loaded from the planning brief and the relevant
  instruction document
- an explicit handoff to the next stage skill

## Canonical References

- [`./planning-brief.md`](./planning-brief.md)
- [`./instructions/new.md`](./instructions/new.md)
- [`./instructions/add-feature.md`](./instructions/add-feature.md)
- [`./instructions/validate.md`](./instructions/validate.md)
- [`../cli-forge-publish/SKILL.md`](../cli-forge-publish/SKILL.md)
- [`../cli-forge-publish/planning-brief.md`](../cli-forge-publish/planning-brief.md)
- [`../cli-forge-publish/instructions/release/skill-release-runbook.md`](../cli-forge-publish/instructions/release/skill-release-runbook.md)
- [`../cli-forge-publish/templates/README.md`](../cli-forge-publish/templates/README.md)

## When To Use This Stage

- The user asks for cli-forge help in a high-level way and the correct phase is
  not obvious yet.
- The user wants to create a new project but has not clearly supplied a valid
  skill name.
- The user wants to create a new project and the generated skill's description
  contract has not been approved yet.
- The user wants to add `stream` or `repl`, but the project path or feature is
  still unclear.
- The user wants to update an existing generated skill's purpose, positioning,
  or other user-facing contract.
- The user wants validation, but the target project path still needs to be
  resolved.
- The user wants to publish, do a release dry run, rehearse the destination
  mirror, check destination configuration, or adopt the release automation
  asset pack into a target CLI skill project.

## Required Inputs By Outcome

- `description`: the classified intent, generated skill scope, and the next
  stage that will consume the approved description contract
- `scaffold`: `skill_name`, plus optional `author`, `version`, and
  `rust_edition`
- `extend`: `project_path` and `feature` where `feature` is `stream` or `repl`
- `validate`: `project_path`
- `publish`: release mode (`report_only`, `dry_run`, `rehearsal`, or
  `live_release`), current validation status, and any required destination
  configuration or credential context

## Workflow

1. Read the user request and classify the intent as `description`, `scaffold`,
   `extend`, `validate`, or `publish`.
2. Load [`./planning-brief.md`](./planning-brief.md) before choosing a
   downstream phase so the runtime contract and compliance posture stay in
   scope.
3. Open the matching local instruction document for the likely next stage and use it
   as the detailed source of truth.
4. Confirm the required inputs for that path:
   - For `description`, verify the work creates a new generated skill or
     changes the generated skill's user-facing contract.
   - For `scaffold`, verify the name is present, the approved description
     contract exists, and the work is intended to become a Rust CLI Skill
     project.
   - For `extend`, verify both `project_path` and `feature`.
   - For `validate`, verify `project_path`.
   - For `publish`, load
     [`../cli-forge-publish/planning-brief.md`](../cli-forge-publish/planning-brief.md),
     verify whether the user wants `report_only`, `dry_run`, `rehearsal`, or
     `live_release`, and whether the work should start with validation or can
     proceed directly to the publish stage.
5. Inspect the filesystem when it helps disambiguate the stage:
   - missing target directory usually means `description` followed by
     `scaffold`
   - existing scaffolded project plus feature request means `extend`
   - existing generated skill plus description-impacting request means
     `description` followed by `extend` or `validate`
   - explicit audit or post-change verification means `validate`
   - release, dry-run, rehearsal, destination-config work, or final
     post-validation closure means `publish`
6. Route to the next stage skill and carry forward the resolved inputs.

## Classification Examples

- Create request with no project directory yet -> route to `description`.
- Existing generated skill plus purpose/positioning change -> route to
  `description`.
- Existing scaffolded project plus `stream` or `repl` request -> route to
  `extend`.
- Audit or post-change verification request -> route to `validate`.
- Successful validation with no explicit release action -> route to `publish`
  in `report_only` mode.
- Mixed implementation and release request with unresolved project state ->
  return to the earliest incomplete stage instead of skipping ahead to
  `publish`.

## Done Condition

This stage is complete only when one downstream phase is clearly selected and
the next stage has the inputs it needs.

## Next Step

- Route to [`../cli-forge-description/SKILL.md`](../cli-forge-description/SKILL.md)
  whenever the description contract must be created or refreshed.
- Route to [`../cli-forge-scaffold/SKILL.md`](../cli-forge-scaffold/SKILL.md) for
  new project creation after `description`.
- Route to [`../cli-forge-extend/SKILL.md`](../cli-forge-extend/SKILL.md) for
  `stream` or `repl` work.
- Route to [`../cli-forge-validate/SKILL.md`](../cli-forge-validate/SKILL.md) for
  compliance checking.
- Route to [`../cli-forge-publish/SKILL.md`](../cli-forge-publish/SKILL.md) for
  release, dry-run, rehearsal, or destination-config work.
