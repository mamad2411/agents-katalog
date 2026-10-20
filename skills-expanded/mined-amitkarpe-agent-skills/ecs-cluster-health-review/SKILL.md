---
name: ecs-cluster-health-review
description: Run a read-only ECS-on-EC2 cluster health review with service desired/running checks, active and draining container-instance inventory, canary-lane status, and optional RTK summaries. Use for next-day or next-week ECS health checks, Jira proof, or boss-status snapshots after a canary or node maintenance window.
---

# ECS Cluster Health Review

Use this skill for a bounded, read-only ECS cluster health snapshot.

## Use when

- reviewing ECS cluster health after a canary or maintenance window
- checking whether all services are at desired count
- checking active versus draining ECS container instances
- confirming canary lane still has the expected task footprint
- preparing a small Jira or boss-facing proof

## Workflow

1. Use `rtk aws ...` for broad human-facing AWS reads when output is large.
2. Use raw `aws` plus `jq` for machine-parsed health evidence.
3. Capture:
   - cluster registered/running/pending/active-service counts
   - all services with desired/running/pending/status
   - non-steady services
   - active container instances and task counts
   - draining container instances and task counts
   - canary lane attributes if present
4. If the ask includes CloudWatch Logs or Docker `awslogs`, use
   `awslogs-investigation` after this health snapshot.
5. If any node is unhealthy or task placement is bad, use `ecs-recovery` only
   after the failing node set is known.

## Script

```bash
bash scripts/collect-health.sh \
  <cluster> <profile> <region> [output_dir]
```

If `output_dir` is omitted, the script writes under:

```bash
~/.AGENTS-temp/agent-skills/ecs-cluster-health-review/
```

## Output

- `cluster.json`
- `services.json`
- `service-summary.tsv`
- `non-steady-services.tsv`
- `container-instances-active.json`
- `active-node-summary.tsv`
- `container-instances-draining.json`
- `draining-node-summary.tsv`
- `summary.md`
- optional `rtk-cluster.txt` if `/home/dev/.local/bin/rtk` is available

## Rules

- keep this skill read-only
- do not terminate, drain, restart, or scale resources from this skill
- clearly separate ACTIVE nodes from DRAINING nodes
- do not call a DRAINING zero-task node an incident by itself
- report a DRAINING zero-task node as cleanup/follow-up unless it blocks capacity
