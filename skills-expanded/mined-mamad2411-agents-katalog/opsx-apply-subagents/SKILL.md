---
name: opsx-apply-subagents
description: Orchestrates dependency-aware parallel subagents for OpenSpec workflows, supporting OPSX commands, legacy openspec commands, and Codex CLI prompt aliases. Use when running /opsx:apply, /openspec:apply, or any opsx command with multiple independent tasks that can be parallelized.
---

# OpenSpec Parallel Agents

Orchestrates concurrent subagents for OpenSpec — one subagent per independent task, serial execution for dependency chains. Supports OPSX, legacy `openspec:*`, and Codex CLI `prompts:*` aliases.

See [REFERENCE.md](REFERENCE.md) for the full command compatibility matrix and round summary template.

## Trigger conditions

Enable when any of these are true:
- 2+ changes can run independently
- `/opsx:apply` (or alias) has multiple pending non-conflicting tasks
- Batch archiving or `/opsx:bulk-archive` is needed

## Concurrency rules

1. **One subagent per task** — never group tasks
2. Only dependency-free nodes run in parallel; chains run serially
3. No parallel writes to overlapping file regions — downgrade to serial if conflict risk detected
4. Wait for all subagents before summarizing

## `/opsx:apply` workflow

1. Run `openspec instructions apply --change "<name>" --json` → get tasks + context files
2. Analyze dependencies — identify independent vs chained tasks
3. Spawn one subagent per independent task (strictly parallel)
4. Wait for all → mark completed tasks (`- [x]`) sequentially to avoid conflicts
5. Repeat for next unblocked batch

## Legacy command mapping

| Legacy | OPSX equivalent |
|--------|----------------|
| `/openspec:proposal` | `/opsx:new` + `/opsx:ff` |
| `/openspec:apply` | `/opsx:apply` |
| `/openspec:archive` | `/opsx:archive` |
