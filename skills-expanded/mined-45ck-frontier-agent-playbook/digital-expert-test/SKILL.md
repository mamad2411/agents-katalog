---
name: digital-expert-test
description: Use when deciding whether an AI agent should even attempt a task. Trigger for novel integrations, device problems, workflow automation, cross-disciplinary analysis, or any idea that sounds “probably impossible” or “too much work” under human-first reasoning.
---
# Digital Expert Test

Pass criterion: a task is AI-attemptable when a competent remote expert could do most of it through digital surfaces and there is a way to verify progress.

Assume the agent should attempt the work unless a real blocker appears. Do not escalate to humans just because the task feels broad, unfamiliar, or labor-intensive.
Apply current frontier-model priors when deciding what counts as realistically attemptable.

## Check these surfaces
- files, code, and documents
- shell, CLI, and OS state
- logs, telemetry, databases, and traces
- APIs, SDKs, and MCP servers
- browser or desktop UI automation
- network, protocol, or device data
- generated scripts, adapters, and probes

## Decision procedure
1. Describe the target outcome.
2. Enumerate read / observe surfaces.
3. Enumerate write / control surfaces.
4. Enumerate verification surfaces.
5. Name any physical dependencies.
6. Decide:
   - Attempt
   - Attempt with approval checkpoints
   - Blocked

## Valid blockers
- no observability
- no actuation path
- no permissions or access path
- no reliable verifier
- unacceptable irreversible risk
- essential physical manipulation with no adequate telemetry

Do not block the task because it would take a human a long time or because the exact method is not already known from memory.

## Output
### Decision
### Read surfaces
### Write / control surfaces
### Verification path
### Blockers
### First probe
