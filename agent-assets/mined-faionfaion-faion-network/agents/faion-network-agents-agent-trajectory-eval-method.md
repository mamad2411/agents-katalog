# Agent Trajectory Eval Method

## Summary

**One-sentence:** Evaluation method that scores not just an agent's final answer but the full tool-call trajectory — right tools, right order, redundancy, recovery — and produces a per-run report with trajectory metrics.

**One-paragraph:** Output-only evals miss the half of agent quality that lives in the trajectory: did the agent pick the right tools, in a sensible order, without redundancy, and recover gracefully from tool errors? This methodology defines a three-layer score (system efficiency: latency + tokens + tool calls; session: trajectory exact-match / precision / recall; node: per-tool selection and parameter accuracy) and emits a per-run report that gates promotion. Required for any agent feature that survived first-week sunny-day testing and now needs an honest production readiness signal.

**Ефективно для:** Команд, у яких pass-rate на golden set ≥80%, але в проді агент іноді робить дивне і ніхто не знає чому; метрики траєкторії показують конкретні misselect-tool / redundant-call / no-recovery випадки, які output-only-евали ховають.

## Applies If (ALL must hold)

- Agent is past initial-prototype stage (has ≥1 deployed version).
- Trajectory logs (per-tool call + args + return) are persisted.
- A golden set of ≥30 expected-trajectory examples exists or can be assembled.
- Owner is willing to gate GA promotion on trajectory metrics, not only final-answer metrics.
- An eval harness can replay or fresh-run trajectories (see [[agent-replay-harness-cookbook]]).

## Skip If (ANY kills it)

- Agent is a single-tool wrapper (no trajectory to score).
- Trajectory logs are unavailable and cannot be added (closed harness).
- Final-answer quality alone meets the team's bar and trajectory variation does not affect outcomes.
- Production cost ceiling cannot accommodate the eval run cost.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Golden trajectory set | jsonl `[{task, expected_tools, expected_order}]` ≥30 entries | QA |
| Live trajectory logs | jsonl from observability stack | Datadog / Langfuse / LangSmith |
| Tool registry | JSON name+schema | Tool catalogue |
| Cost ceiling | $ per eval run | Finance |
| Named owner | handle | QA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-replay-harness-cookbook/AGENTS.md` | Harness emits the trajectories this evaluator consumes. |
| `geek/ai/ai-agents/chaos-eval-fault-injection/AGENTS.md` | Chaos-eval extends this with deliberate fault injection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: golden frozen, three-layer scoring, CI reported, judge calibrated, cost capped | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the trajectory-eval report | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (output-only, judge drift, cherry-picked traces, etc.) | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: build golden → score per-layer → aggregate → CI → report | ~1000 |
| `content/05-examples.xml` | medium | Worked example: trajectory report for a code-fixer agent | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: logs available? → golden set? → cost ok? → run/build/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse_traces` | haiku | Structured extraction. |
| `score_trajectory` | sonnet | LLM-as-judge for trajectory quality where rule-based fails. |
| `aggregate_report` | sonnet | Compose final report. |
| `review_regression` | opus | Cross-version drift diagnosis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the trajectory-eval report. |
| `templates/report.example.json` | Filled minimal valid example. |
| `templates/golden-trajectory.jsonl` | Skeleton golden-set with two example entries. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the report against the schema. | After subagent emits report, before promotion gate. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-replay-harness-cookbook]] — replay produces the input traces.
- peer: [[chaos-eval-fault-injection]] — extends trajectory eval with fault injection.
- external: TRACE (arXiv:2602.21230); Vertex AI trajectory_exact_match / precision / recall.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) are trajectory logs available? (2) is a golden set ≥30 examples ready? (3) does cost fit ceiling? Leaves point to "run eval", "build prerequisites first", or "escalate".
