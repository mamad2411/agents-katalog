---
name: ecs-mixed-ami-canary
description: Plan and validate a mixed-AMI ECS canary lane with one cluster, separate stable and canary ASGs, separate launch templates, and isolated service placement. Use for safe AMI or CIS-fix calibration on EC2-backed ECS without letting the main workload land on the new lane by default.
---

# ECS Mixed AMI Canary

Use this skill for the repeated operator workflow around one ECS cluster with:

- stable lane on known-good AMI capacity
- canary lane on one new AMI

## Use when

- testing a new AMI beside the old AMI in the same ECS cluster
- calibrating CIS fixes on one canary node before wider rollout
- verifying separate launch template / ASG / capacity provider shape
- freezing rollback-safe rollout notes before a prod window

## Core model

- `1` ECS cluster
- `2` launch templates
- `2` ASGs
- `2` AMIs
- separate ECS capacity providers when possible
- main service stays on stable lane first
- canary service stays on canary lane first

## Validate in this order

1. Confirm stable lane is healthy.
2. Confirm canary ASG joins the same ECS cluster.
3. Confirm canary node is:
   - EC2 healthy
   - SSM online
   - Docker healthy
   - ECS agent healthy
4. Confirm canary service placement is isolated to the canary lane.
5. Validate app health, forwarding, restart, and drain behavior on the canary
   lane only.
6. Only then consider a very small mixed scheduling experiment.

## Save as durable evidence

- cluster name
- stable ASG / LT / capacity provider / AMI
- canary ASG / LT / capacity provider / AMI
- instance attributes or placement constraints in use
- rollback steps
- before/after service counts

Write evidence under:

```bash
~/.AGENTS-temp/<repo>/ecs-mixed-ami-canary/<timestamp>/
```

## Rules

- do not let the main service land randomly on the canary node by default
- prefer a dedicated canary service over one mixed service first
- keep rollback simple:
  - stop canary scheduling
  - drain canary tasks
  - scale canary ASG to zero
- use `ecs-monitoring` for read-only watch
- use `ecs-recovery` only if the canary node degrades

## Related skills

- `ecs-monitoring`
- `ecs-recovery`
- `cis-ssm-apply-validate`
