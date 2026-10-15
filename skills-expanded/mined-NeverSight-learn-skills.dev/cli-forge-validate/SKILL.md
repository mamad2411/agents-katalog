---
name: cli-forge-validate
description: "Validation stage for the cli-forge skill family: run the documented compliance checks for an existing project and report whether it is planning-brief-compliant, usable with warnings, or blocked by errors."
---

# cli-forge Validate

Use this stage when you need a compliance report for an existing Rust CLI Skill
project, or when you have just scaffolded or extended one and need to verify
the result.

## When To Use This Stage

- The user explicitly asked for validation or compliance checking.
- Scaffold work just finished and needs a verification pass.
- Extension work just finished and needs a verification pass.
- Description-stage work just finished and needs the downstream surfaces
  checked for alignment.
- Publish-oriented work is requested, but validation is stale or missing.

## Stage Goal

Produce a validation report that reflects the project's current state and makes
the next action obvious.

## Canonical References

- [`./instructions/validate.md`](./instructions/validate.md)
- [`./planning-brief.md`](./planning-brief.md)

Read `instructions/validate.md` as the exact source of truth for the ruleset,
the output table format, build checks, and runtime-convention checks.

## Required Inputs

- `project_path`

## Workflow

1. Run the pre-checks from
   [`./instructions/validate.md`](./instructions/validate.md): resolve
   the path, confirm it is a directory, and confirm `Cargo.toml` exists.
2. Execute the documented validation rules in order, including:
   - structure
   - naming
   - dependencies and metadata
   - `SKILL.md` contract checks
   - build checks
   - runtime convention checks
   - generated package boundary checks so package-local support assets are
     allowed only when enabled and repository-owned CI automation is not
     misclassified as generated output
3. Return the report in the required markdown table shape with the requested
   summary.
4. Classify the outcome:
   - compliant when all required checks pass
   - usable with warnings when only warning-level gaps fail
   - non-compliant when any error-level check fails
5. Prepare the handoff:
   - compliant or reviewable-with-warnings results continue into `publish`
     so the workflow ends with final release-readiness or no-publish closure
   - non-compliant results route back to the earliest failing phase before
     later work resumes

## Guardrails

- Do not skip checks just because an earlier rule failed unless the instruction
  file explicitly says the remaining check would be impossible or misleading.
- Preserve the exact reporting contract from the instruction file.
- If failures point to broken scaffold fundamentals, route back to the earlier
  phase that owns those surfaces before claiming the workflow is done.

## Done Condition

This stage is complete only when the full validation report and summary have
been produced for the current project state.

## Next Step

- Continue with [`../cli-forge-publish/SKILL.md`](../cli-forge-publish/SKILL.md)
  after every successful validation pass. If no explicit release action was
  requested, enter `publish` in `report_only` mode.
- Otherwise, route back to the earliest failing phase, fix the gaps there, and
  re-run validation.
