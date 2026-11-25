---
name: opentofu-1-plan-review
description: Reviews OpenTofu 1.x plans for risk, including creates, updates, replacements, destroys, state operations, drift, provider changes, and apply readiness. Use when the user asks about tofu plan output, destroy detection, saved plans, apply readiness, state moves/imports, drift, or upgrades.
license: MIT
compatibility: Requires OpenTofu 1.x for command execution. Plan JSON summaries require jq when using bundled shell scripts.
---

# OpenTofu 1.x Plan Review Skill

This skill focuses on safe review of OpenTofu plans, state operations, drift-sensitive changes, destroy detection, and 1.x upgrades.

## Use This Skill When

- Reviewing `tofu plan` output.
- Creating a saved plan for review.
- Summarizing or risk-scanning plan JSON.
- Preparing a controlled `tofu apply`.
- Investigating drift.
- Planning state moves, imports, or backend changes.
- Upgrading within the OpenTofu 1.x release line.

## Safety Boundaries

- Do not run `tofu apply`, `tofu destroy`, `tofu import`, `tofu state *`, `tofu force-unlock`, or workspace deletion without explicit user approval.
- Do not use `-auto-approve` unless explicitly required by the user for a controlled automation context.
- Treat plan files and JSON as sensitive.
- Prefer speculative plans for code review and saved plans for apply handoff.
- Treat any `delete`, `replace`, `-/+`, `-destroy`, or `-replace` as high-risk until reviewed.

## Workflows

- `workflows/plan-review-workflow.md`: Use for routine plan generation and review.
- `workflows/state-change-workflow.md`: Use for imports, moved resources, state operations, or backend changes.
- `workflows/upgrade-1x-workflow.md`: Use for OpenTofu 1.x minor or patch upgrades.

## Resources

- `resources/plan-review-checklist.md`: Review checklist for creates, updates, replacements, destroys, IAM, stateful resources, and provider changes.
- `resources/state-safety-checklist.md`: Checklist for state mutation and backend migration.

## Scripts

Run scripts with `--help` before use.

- `scripts/summarize-plan.sh`: Summarizes a saved plan file by action type using `tofu show -json` and `jq`.
- `scripts/detect-plan-risk.sh`: Flags destructive or high-risk actions in a saved plan.

## Examples

- `examples/tofu-test-example.md`: Example OpenTofu test file structure and assertions.
