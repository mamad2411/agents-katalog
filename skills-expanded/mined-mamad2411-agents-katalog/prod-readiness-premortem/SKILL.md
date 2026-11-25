---
name: prod-readiness-premortem
description: Negative pre-mortem review for production or production-like AWS infrastructure changes. Use when Codex must stress-test DEV evidence, rollout plans, worker results, Terraform/Terragrunt plans, AMI promotions, SSM runbooks, database/auth changes, GitLab/app integrations, or release readiness before PROD approval; especially when the user asks what can go wrong, corner cases, no-go gates, rollback risk, lockout risk, or 30 June style PROD planning.
---

# PROD Readiness Pre-Mortem

## Purpose

Run a hostile readiness review before PROD. Treat green DEV evidence as useful
input, not proof that PROD is safe.

Use this skill to produce a decision-grade risk review, not an execution plan
that quietly assumes approval.

## Inputs

Collect the smallest authoritative set:

- User's intended PROD change and date/window.
- DEV or staging result packets.
- Repo `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, and feature specs when present.
- Terraform/Terragrunt plan summaries or exact stack paths when relevant.
- Current AWS readbacks only when needed and safe.

For AWS private-only, GCC, GovTech, restricted, VPC, endpoint, SG, or public
exposure topics, also apply `aws-private-network-preflight` if the task will
create or change networking/exposure.

## Review Method

1. State the intended PROD outcome in one sentence.
2. Split evidence into:
   - confirmed facts
   - DEV-only proof
   - assumptions
   - missing PROD evidence
3. Assume the rollout fails. Work backward to identify how.
4. Check each failure mode for:
   - customer/app impact
   - lockout risk
   - rollback difficulty
   - detection gap
   - approval or ownership gap
5. Mark each item:
   - `BLOCKER`: must resolve before PROD
   - `NO-GO`: must stop during PROD if observed
   - `RISK`: acceptable only with mitigation/evidence
   - `WATCH`: monitor during or after rollout

## Mandatory Risk Areas

Always cover these for AWS infra/database/app release reviews:

- Account, region, role, and approval boundary.
- Terraform/Terragrunt state, stack path, drift, imports, destroys, and plan
  scope.
- IAM, KMS, SSM Parameter Store, and secret lookup/decrypt paths.
- VPC, subnet, route table, endpoint, private DNS, security group, and public
  exposure.
- DNS/private hosted zone association and resolver behavior.
- AMI ID, AMI ownership/share/copy state, snapshot/KMS launchability, and
  runtime drift from DEV.
- Boot/user-data/idempotency and service restart behavior.
- Database cluster health, stepdown, election, quorum, auth, keyFile, lockout,
  client compatibility, and connection-string behavior.
- Application integration and retry behavior during failover.
- Backup, restore, retention, and backup-host connectivity.
- Observability: logs, metrics, alarms, run-command evidence, and operator
  visibility during the window.
- Rollback: exact trigger, exact command/path, expected data/config state after
  rollback, and rollback proof.
- Cleanup of temporary users, DBs, tokens, test data, EC2s, SG rules, snapshots,
  and stale SSM values.
- Human/operator mistakes: wrong account, wrong instance, wrong SSM path, stale
  AMI pointer, copied DEV value into PROD, incomplete command output, and
  continuing after a no-go signal.

For database auth or keyFile changes, read `references/mongodb-auth-keyfile.md`.

## Output Shape

Keep the review concise but sharp:

```text
PROD readiness status: GO / CONDITIONAL GO / NO-GO

1. Intended PROD outcome
2. What current DEV evidence proves
3. What current DEV evidence does not prove
4. BLOCKERS before PROD
5. NO-GO gates during PROD
6. Risk register
7. Required pre-check evidence
8. Minimum safe execution shape
9. Rollback gaps
10. Open questions for Amit/Ops
11. Recommended next worker goal
```

Use `NO-GO` when missing evidence could cause lockout, public exposure, wrong
account mutation, irreversible state changes, or unbounded outage.

## Guardrails

- Do not run destructive commands.
- Do not apply Terraform, mutate PROD, rotate secrets, restart services, or
  change AWS resources while doing the pre-mortem.
- Do not treat DEV success as PROD readiness unless target-account proof exists.
- Do not expose secret values in prompts, results, logs, or Markdown.
- If execution is needed, stop with an exact approval request and command plan.
