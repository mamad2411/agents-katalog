# Chaos-Eval — Fault Injection on Agent Tools

## Summary

**One-sentence:** Injects controlled tool faults (timeouts, 5xx, rate-limits, corrupted returns, MCP disconnects) into eval runs and grades the agent on recovery quality, not sunny-day success.

**One-paragraph:** Standard eval sets run with tools that always succeed; production tools fail. This methodology defines a chaos-eval config (fault classes, injection points, rates) layered on top of a regular eval, and a grading rubric that scores not "did it succeed?" but "did it recover, retry intelligently, escalate when blocked, or produce a confidently-wrong answer?". Output is one report per agent version with per-fault-class recovery scores.

**Ефективно для:** Команд, у яких production agent інколи дає «confidently wrong» відповідь, коли tool тимчасово впав — і eval показує 95%, а реальний uptime 60%; chaos-eval ловить цей клас bugs до релізу.

## Applies If (ALL must hold)

- Agent calls tools that can fail in production (HTTP, MCP, code execution).
- Replay harness exists (see [[agent-replay-harness-cookbook]]).
- Eval set ≥30 examples.
- Owner can run an extended eval cycle (chaos eval is 5-10× longer than normal).
- A grading rubric for recovery quality is available or can be authored.

## Skip If (ANY kills it)

- All tools are deterministic in-process (no network, no MCP).
- No replay harness — can't inject faults reliably.
- Eval already chaos-graded by upstream platform.
- Prototype with no SLA on reliability.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Replay harness | output of [[agent-replay-harness-cookbook]] | Eng |
| Eval set | jsonl ≥30 | QA |
| Tool fault catalogue | per-tool {fault_classes, default_rates} | Tool catalogue |
| Recovery rubric | rubric scoring 0..3 per outcome class | QA |
| Named owner | handle | QA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-replay-harness-cookbook/AGENTS.md` | Harness emits the trajectories chaos-eval mutates. |
| `geek/ai/ai-agents/agent-trajectory-eval-method/AGENTS.md` | Trajectory eval supplies the rubric chaos-eval extends. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: fault catalogue, injection points, grade recovery, baseline first, r1 (run + promotion gate, catalogue complete first), r2 (no harness, no injection), r3 (rubric before grading) | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the chaos-eval report | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: harness? → fault classes? → rubric? → run/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick_fault_classes` | sonnet | Per-tool reasoning. |
| `grade_recovery` | sonnet | LLM-as-judge for recovery quality. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the report. |
| `templates/output.example.json` | Filled example. |
| `templates/chaos-config.json` | Skeleton chaos config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the report. | Before promotion gate. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-replay-harness-cookbook]], [[agent-trajectory-eval-method]].

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is a replay harness available? (2) are fault classes catalogued? (3) does a recovery rubric exist? Leaves point to "run chaos-eval", "build prerequisites first", or "escalate".
