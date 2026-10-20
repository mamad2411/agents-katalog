---
name: awslogs-investigation
description: Investigate ECS Docker awslogs failures on EC2-backed nodes by checking Docker journal errors, container placement, and node-level patterns. Use when CloudWatch Logs are missing for ECS tasks, awslogs stream creation fails, or some nodes appear clean while others do not.
---

# AWSLogs Investigation

Use this skill for Docker `awslogs` failures on EC2-backed ECS nodes.

## Use when

- ECS tasks are not sending recent logs to CloudWatch
- Docker journal shows `awslogs` failures
- some nodes have logs and others do not
- you need a node-by-node matrix of failing versus clean ECS hosts

## Do not use when

- the environment uses Fargate only
- tasks use a different log driver
- you only need generic CloudWatch Logs querying

## Main scripts

### Check one or more nodes for awslogs failures

```bash
bash scripts/check-awslogs-node.sh \
  <profile> <region> <since_timestamp> <instance_id> [instance_id...]
```

This checks Docker journal lines for:

- `awslogs`
- `failed to create Cloudwatch log stream`
- `failed to refresh cached credentials`
- `failed to load credentials`
- `retry quota exceeded`

If errors are present, treat the node as suspect.

### Build a node matrix for an ECS cluster

```bash
bash scripts/check-awslogs-matrix.sh \
  <cluster> <profile> <region> <since_timestamp> [output_dir]
```

This script:
- lists active ECS container instances
- maps them to EC2 IDs
- runs the journal probe per node via SSM
- saves raw outputs to a durable temp path

If `output_dir` is not provided, it writes to:

```bash
~/.AGENTS-temp/agent-skills/awslogs-investigation/matrix-<timestamp>
```

## Investigation rules

- keep this skill read-only
- do not restart Docker from this skill
- treat fresh clean nodes versus older loaded nodes as an important signal
- do not assume a Docker restart is a durable fix for this failure mode
- confirm whether the failure is:
  - cluster-wide
  - limited to older nodes
  - limited to nodes with heavier task density

## Recommended workflow

1. confirm tasks use Docker `awslogs`, not CloudWatch Agent
2. check one known failing node
3. compare it to one known clean node
4. if the pattern is real, build a cluster-wide node matrix
5. hand off to `ecs-recovery` only after the failing-node set is clear

## Known reference

- read `references/DOCKER_AWSLOGS_CREDENTIAL_FAILURE.md` for the known failure pattern and why drain/replacement is safer than assuming restart fixes it

## Evidence

Keep evidence outside the repo in:

```bash
~/.AGENTS-temp/agent-skills/awslogs-investigation/
```

## Related skills

- use `ecs-monitoring` for read-only service/task stability checks
- use `ecs-recovery` only after the failing-node set is known
