---
name: opentofu-1-quality
description: Runs safe OpenTofu 1.x quality, validation, security, state-secret, and command-safety checks. Use for formatting, validation, tests, plan readiness, secret/state risk review, and local verification before code review.
license: MIT
compatibility: Requires OpenTofu 1.x. Optional scripts may require jq and Python 3.
---

# OpenTofu 1.x Quality Skill

This skill provides safe local quality gates for OpenTofu 1.x repositories.

## Use This Skill When

- Running formatting or validation checks.
- Preparing a pull request for OpenTofu code.
- Checking whether a plan is ready for review.
- Looking for state or secret leakage risks.
- Reviewing dangerous OpenTofu command proposals.
- Running `tofu test` where tests exist and the user accepts provider-side effects.

## Safety Boundaries

- Quality checks must not run `apply`, `destroy`, `import`, or state mutation.
- `tofu test` can create real infrastructure. Only run it when the test files and provider credentials are understood.
- Do not commit state, plan files, plan JSON, crash logs, provider credentials, or generated secrets.
- Run scripts with `--help` before using them.

## Workflows

- `workflows/quality-gate-workflow.md`: Use for local formatting, initialization, validation, optional tests, and plan-readiness checks.
- `workflows/security-review-workflow.md`: Use for secrets, state, outputs, providers, backends, and destructive-change review.

## Resources

- `resources/quality-command-matrix.md`: Matrix of safe, conditional, and high-risk OpenTofu commands.
- `resources/security-baseline.md`: Security checklist for state, secrets, providers, outputs, and plans.

## Scripts

Run scripts with `--help` before use.

- `scripts/opentofu-1-check.sh`: Safe local quality checks: fmt, optional init, validate, optional test, optional plan.
- `scripts/guard-tofu-command.py`: Antigravity hook helper that asks before dangerous `tofu` or Terraform CLI commands.
- `scripts/scan-state-secret-risk.py`: Scans repository files for local state files and obvious secret-output risks.
- `scripts/final-verification-reminder.py`: Optional disabled hook helper that injects a final verification reminder.

## Examples

- `examples/local-checks-example.md`: Example commands for running the quality gate locally.
