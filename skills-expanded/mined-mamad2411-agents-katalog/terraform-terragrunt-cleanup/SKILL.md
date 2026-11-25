---
name: terraform-terragrunt-cleanup
description: Execute cleanup for Terraform/Terragrunt-owned infrastructure using owning stack commands, with clear approvals, evidence output, and IAM-retain-by-default safety.
---

# Terraform/Terragrunt Cleanup Runner

Use this skill when review is finished and cleanup execution is approved.

## Default

This skill only calls owning stack tooling:

- Terraform stacks where ownership is explicit and code path is known.
- Terragrunt stacks where `terragrunt` and stack context are already defined.

Do not invent or execute one-off AWS mutation scripts.

## Use when

- cleanup candidates are accepted in `RESULT.md` from `aws-ec2-ami-cleanup-inventory`
  or another review skill.
- AMI Factory cleanup includes EC2/EBS/AMI/snapshot candidates and needs execution
  through the owning repository command path.
- TrustDev, cleanup, or infra lanes need a safe, repeatable delete path.

## Read first

- repo `AGENTS.md`
- repo `SPEC.md` if present
- `/home/dev/.codex/AWS.md`
- owning repo cleanup/runbook and stack paths

## Evidence root

Use:

```text
~/.AGENTS-temp/<repo>/terraform-terragrunt-cleanup/<YYYYMMDD-HHMMSS>/
```

Include command logs and outputs from stack execution.

## Minimum execution contract

If using Terraform directly:

- capture a destroy plan artifact for approved resource scope.
- use stack/dir lock scope and variable files used by that repo.
- only apply after explicit cleanup approval text exists.

If using Terragrunt:

- use the owning stack `terragrunt` path and `--terragrunt-non-interactive`.
- keep the target stack scope narrow; do not run repo-wide `destroy` unless approved.

No AWS mutation should happen outside repo-owned stack code or clearly documented
repo-owned cleanup command wrappers.

## Safety

- Shared IAM roles/policies that are zero-cost or reused across accounts should
  stay `retain` unless explicit delete approval is written in the request.
- Do not touch `retain-protected` buckets from review tables unless owners and
  approval text are explicit.
- `PUBLIC`-facing or exposure-changing cleanup is a separate approval gate.
- if account/profile/env is unclear, stop and record a blocker in `RESULT.md`.

## Output

Write `RESULT.md` with:

- stack(s) used and the owning repo path
- approved resource list and bucket mapping
- exact command sequence run (or command template if blocked)
- approvals required/completed
- residual risk notes, blockers, and follow-up
- rough cost/savings note if available (non-management-grade estimate only)

Keep chat summary short and point to `RESULT.md`.
