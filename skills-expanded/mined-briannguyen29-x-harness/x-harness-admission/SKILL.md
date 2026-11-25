---
description: Teach the x-harness admission workflow and completion-card discipline
---

# x-harness-admission

Use this skill when you need to create, update, or verify a completion claim in a repository that uses x-harness.

## What x-harness is

x-harness is a Go-native, file-first admission and readiness harness for AI coding workflows.

- It does **not** run agents.
- It does **not** replace CI.
- It does **not** guarantee that code is correct.

It evaluates whether a completion claim is admissible under repository policy and emits one of two decisions: **accepted** or **withheld**.

## When to create or update completion-card.yaml

Create or update `completion-card.yaml` at the root of the workspace when you finish a task and are ready to propose completion.

Do this **before** claiming the task is done.

The card must be written as YAML and must validate against the repository schema at `schemas/completion-card.schema.json`.

## How to record evidence

Evidence must be explicit and reproducible.

1. **Files changed**: list every file you created or modified.
2. **Command evidence**: record the exact commands you ran, their exit codes, and when they ran.
3. **Manual rationale**: only use this when no command evidence is possible (light tier).
4. **State**: for standard and deep tiers, declare `read_set` and `write_set`.

Do not include:
- hidden network installations
- commands that auto-enable external services
- destructive commands without rollback context

## How to run verify / check

Run the local verify gate before proposing completion:

```bash
./x-harness verify --card completion-card.yaml --strict
```

or

```bash
./x-harness check --card completion-card.yaml --strict
```

Both commands are aliases for the same read-only verify pipeline.

### Interpreting the result

- `outcome: success` and `acceptance_status: accepted` means the claim is admitted.
- Any other outcome means the claim is withheld.

If withheld, read the validation errors, fix the issues, and re-run verify.

## What accepted means

**Accepted** means the completion claim meets the repository admission policy:

- required fields are present
- evidence floor is met for the declared tier
- admission mapping is valid
- no unresolved blockers
- verifier was read-only

Accepted is the only valid end state for a completed task.

## What withheld means

**Withheld** means the claim does not yet meet policy. All non-success outcomes map to withheld:

- failed
- blocked
- skipped
- timeout
- error

Withheld claims must include a valid `handoff` block with `next_action` and `owner`.

## Why the agent must not self-admit completion

An agent may propose completion, but it cannot declare its own claim accepted.

Only the read-only verify gate can emit an accepted decision.

These conditions are **not** sufficient by themselves:

- `claim.fix_status: fixed`
- `verification.status: passed`
- tests passed
- high confidence
- PGV advice says okay
- context acknowledged

The single source of truth is the verify gate output.

## Tier guidance

Use only the canonical tier labels: `light`, `standard`, `deep`.

- **light**: minor changes. Requires `files_changed` and command evidence or manual rationale.
- **standard**: normal changes. Also requires `done_checklist` and `prediction`.
- **deep**: major or security-sensitive changes. Also requires scoped evidence, `state.read_set/write_set`, `untested_regions`, `remaining_risks`, `execution_controls`, and `rollback_policy`.

## Rules

- Verifier is read-only. Do not edit source files during verification.
- PGV advice is advisory-only and never overrides verify.
- Non-success outcomes are always withheld.
- Do not use `small`, `medium`, or `large` as tier labels in active runtime handoffs.

<!-- BEGIN X-HARNESS MANAGED CONTRACT: x-harness-admission-skill-contract -->
<!-- generated-by: x-harness -->
<!-- contract-hash: ec6438371a039c93 -->

## Generated Skill Contract

- Completion is admitted, not claimed.
- Verifier is read-only.
- Success is the only accepted outcome.
- Canonical tiers: light, standard, deep.
- PGV is advisory-only.

## Evidence Floor

- **light**: files_changed + (command_evidence or manual_rationale).
- **standard**: files_changed + command_evidence + done_checklist + prediction.
- **deep**: files_changed + command_evidence + evidence_scope_declared + untested_regions_declared + remaining_risks_declared + execution_controls_present + rollback_policy_present + done_checklist + prediction. Runtime-enforced: verification_artifacts, state.read_set, state.write_set.

## Strict Evidence Provenance

- verify --strict requires command_evidence entries to include command, exit_code, runner, and started_at for standard/deep cards.
- verify --strict requires verification_artifacts entries to include command, exit_code, runner, and started_at for standard/deep cards.

<!-- END X-HARNESS MANAGED CONTRACT: x-harness-admission-skill-contract -->
