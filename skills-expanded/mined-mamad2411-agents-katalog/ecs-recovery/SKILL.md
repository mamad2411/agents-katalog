---
name: ecs-recovery
description: Controlled ECS node recovery workflow for Docker and ECS restart, NAT verification, and optional drain operations on EC2-backed ECS clusters. Use when tasks are stuck, Docker NAT is suspect, or awslogs failures require node-by-node recovery with durable evidence.
---

# ECS Recovery

Use this skill for controlled recovery on EC2-backed ECS clusters.

## Use when

- ECS tasks are stuck in `PENDING` or `ACTIVATING`
- Docker NAT or port-publish behavior is suspect
- Docker `awslogs` is failing on specific nodes
- Docker and ECS must be restarted on one node at a time
- you need durable evidence for before/after recovery state

## Do not use when

- the cluster is already stable and you only need read-only monitoring
- the environment is Fargate-only
- you need broad parallel restart across many nodes

Use `ecs-monitoring` first for read-only watch and flap detection.

## Recovery rules

- work on one node at a time
- prefer `DRAINING` before restart when permissions allow it
- if you do not have `ecs:UpdateContainerInstancesState`, do not fake drain behavior
- verify Docker NAT after restart
- stop if service counts worsen and do not recover promptly
- write evidence to a durable temp path outside chat context

## Main scripts

### Restart Docker and ECS on one node

```bash
bash scripts/restart-docker-ecs-one.sh \
  <instance_id> <profile> <region> [output_dir]
```

This script:
- captures before state
- restarts `docker`
- waits briefly
- restarts `ecs`
- captures after state
- verifies:
  - `docker=active`
  - `ecs=active`
  - Docker NAT chain exists

If `output_dir` is not provided, it writes to:

```bash
~/.AGENTS-temp/agent-skills/ecs-recovery/restart-<timestamp>-<instance_id>
```

### Resolve ECS container instance ARN from EC2 ID

```bash
bash scripts/resolve-container-instance.sh \
  <cluster> <profile> <region> <ec2_instance_id>
```

### Attempt to set a node to DRAINING

```bash
bash scripts/drain-container-instance.sh \
  <cluster> <profile> <region> <ec2_instance_id> [output_dir]
```

This script is useful only when the caller has:

- `ecs:UpdateContainerInstancesState`

If the permission is missing, treat that as a real blocker and stop.

## Recommended workflow

1. Use `ecs-monitoring` first to confirm which services and nodes are unstable.
2. Prefer drain over restart if permissions allow it.
3. If drain is blocked, restart only one node at a time.
4. After each restart, verify:
   - `docker` active
   - `ecs` active
   - Docker NAT chain present
   - service counts stable or recovering
5. Stop immediately if:
   - a critical service stays degraded
   - NAT chain does not return
   - Docker or ECS does not come back

## Evidence

Keep evidence outside the repo in:

```bash
~/.AGENTS-temp/agent-skills/ecs-recovery/
```

## Related skills

- use `ecs-monitoring` before this skill for read-only diagnosis
- later pair with `awslogs-investigation` when the issue is logging-specific
