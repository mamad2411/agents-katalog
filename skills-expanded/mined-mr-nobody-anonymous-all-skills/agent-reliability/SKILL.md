---
name: agent-reliability
description: "Make agents reliable under failure: retries with jitter, timeouts per tool, idempotency, checkpointing, loop detection and graceful degradation."
type: procedural
category: agents
domain: agents
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - agent stuck in loop
  - tool call retry policy
  - agent timeout handling
  - agent partial failure recovery
  - make agent deterministic
aliases:
  - agent-resilience
keywords:
  - reliability
  - retries
  - timeouts
  - idempotency
  - checkpoint
  - loop-detection
mcp_servers:
  - filesystem
  - github
source: custom
enabled: true
---

# Agent Reliability

## Purpose

Make agents reliable under failure: retries with jitter, timeouts per tool, idempotency, checkpointing, loop detection and graceful degradation.

## When to Use

- An agent loops, retries forever, or fails halfway through a multi-step task.
- Tool failures surface as confusing final answers instead of clear errors.
- A run must be resumable without repeating side effects.

## When NOT to Use

- The task is a single deterministic call.
- The instability is in the model provider and cannot be engineered around.
- A human is in the loop for every decision anyway.

## Capabilities

- Bound every tool call with a timeout, retry policy and budget.
- Detect loops by state signature, not by step count alone.
- Make side-effecting actions idempotent with keys.
- Checkpoint state so a failed run resumes instead of restarting.
- Degrade explicitly: return partial results with a stated limitation.

## Inputs

- The step graph and which steps have side effects.
- Failure budgets: max retries, max wall-clock, max cost per task.
- The acceptable behaviour when a dependency is down.

## Workflow

1. Classify each step as pure, idempotent or side-effecting.
2. Give every external call a timeout, bounded retries with jitter, and a fallback.
3. Hash the observable state each step and abort on repeats.
4. Write checkpoints after side-effecting steps; resume from the last one.
5. Return structured partial success with the failed step named.
6. Fault-inject: kill a tool, add latency, return malformed output — and confirm behaviour.

## Tools

- python
- tenacity
- pytest
- opentelemetry

## Examples

- `Exponential backoff with full jitter prevents a retry storm when a dependency blinks.`
- `Without a checkpoint, a 20-step run that fails at step 19 repeats 18 side effects.`

## Safety

- Never retry a non-idempotent write without a dedupe key.
- Circuit breaking must fail closed for security actions and open for read-only ones.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/agents/agent-reliability`). First-party skill, maintained in this repository.

## Notes

- Step count is a bad loop detector: a legitimate long task trips it.
- Log the reason for each retry; unexplained retries hide systemic faults.
- Pairs with: `agent-observability`, `human-in-the-loop-design`.
