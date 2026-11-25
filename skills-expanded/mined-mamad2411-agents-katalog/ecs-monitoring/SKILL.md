---
name: ecs-monitoring
description: Read-only ECS cluster and service monitoring workflow for watching service counts, task churn, and unstable services, with reusable bash helpers that save outputs to durable temp paths.
---

# ECS Monitoring

Use this skill for read-only ECS monitoring and diagnosis.

## Use when

- watching ECS service counts over time
- checking whether services are steady or flapping
- collecting task stop reasons
- saving durable watch evidence outside chat context

## Main script

### Cluster watch

```bash
bash scripts/watch-cluster.sh \
  <cluster> <profile> <region> <duration_seconds> <interval_seconds> [output_dir] [focus_services_csv]
```

Arguments:
- `cluster`
- `profile`
- `region`
- `duration_seconds`
- `interval_seconds`
- optional `output_dir`
- optional `focus_services_csv`
  - comma-separated service names for task-level detail
  - example:
    - `api-server-pro,api-monitor-pro,cohort-browser-pro`

If `output_dir` is not provided, the script writes to:

```bash
~/.AGENTS-temp/agent-skills/ecs-monitoring/watch-<timestamp>
```

## Output

The script saves:
- service snapshots
- running/stopped task snapshots for focused services when provided
- a rolling `watch.log`
- a final flap summary

## Rules

- keep this skill read-only
- do not use it for Docker or ECS restarts
- prefer this skill before using `ecs-recovery`
