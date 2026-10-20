# Collaborative Agents with Shared Workspace

## Summary

**One-sentence:** Generates the implementation scaffold for a shared-workspace collaborative multi-agent pattern with capped iterations, independent synthesizer, and per-run token budget.

**One-paragraph:** Each agent in the group produces an initial contribution, then iteratively reads and builds on others' contributions recorded in a shared append-only workspace. After a hard-capped number of iterations a separate coordinator (different agent + ideally different model family) synthesizes the best elements from all contributions in a single call. This methodology ships the `CollaborativeGroup` Python class, the iteration prompt template, and a budget guard so the N×M call pattern cannot silently blow up cost.

**Ефективно для:** солопрейнера на креативних завданнях (strategy, design, narrative), де потрібна різноманітність точок зору, а одна модель збігається на власному prior.

## Applies If (ALL must hold)

- Creative or strategy work where genuinely diverse perspectives improve quality.
- Problem has no single correct answer; coverage matters more than convergence speed.
- Hard iteration cap and per-run token budget are acceptable (you can afford N×M LLM calls).
- Quality bar tolerates extra latency (5x-20x a single-agent call).
- Synthesizer can be an independent agent from the contributors.

## Skip If (ANY kills it)

- Latency budget < 30 s — collaborative pattern is the slowest of the multi-agent shapes.
- Task has a single correct answer — agents converge to the same answer (echo chamber) regardless of iteration count.
- Token budget is rigid (< 20k) — N×M call pattern blows budget faster than any other.
- Deterministic pipeline preferred — sequential is simpler and cheaper.
- Need fine-grained shared mutable state — workspace is append-only by design.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Validated multi-agent spec | YAML with `pattern: collaborative` | `multi-agent-basics` |
| Agent roster + system prompts | list of `{name, role, model, system_prompt}` | spec |
| Per-run token budget | int | `spec.budget.total_tokens` |
| Iteration cap | int (default 5) | spec |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/multi-agent-basics` | Upstream spec this implementation consumes. |
| `geek/ai/ai-agents/schema-version-pinning` | Workspace entries carry `schema_version` for evolvability. |
| `geek/ai/ai-agents/role-specialized-models` | Synthesizer should be on a different model family than contributors. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: capped iterations, budget guard after each round, independent synthesizer, append-only workspace, structured JSON contributions | ~750 |
| `content/02-output-contract.xml` | essential | JSON Schema for the `CollaborativeGroup` config + workspace entry shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: synthesizer-is-contributor, prompt inflation, no budget guard, all-same-model echo, race condition on workspace | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: configure → run initial brainstorm → iterate (with budget check) → synthesize → emit trace | ~700 |
| `content/06-decision-tree.xml` | essential | Pick collaborative vs hierarchical vs debate based on convergence-needed vs coverage-needed | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Per-iteration contribution | sonnet | Reliable structured ideation; cheap enough for N×M calls. |
| Synthesizer | opus (or different family) | Final synthesis needs strongest reasoning; different family breaks echo. |
| Budget audit per iteration | haiku | Numeric check; not generative. |

## Templates

| File | Purpose |
|------|---------|
| `templates/collaborative_group.py` | Reference `CollaborativeGroup` class with shared workspace, iteration loop, budget guard, and independent synthesizer. |
| `templates/iteration-prompt.txt` | Per-round prompt showing agent its own last contribution + others' latest only (no full history) to prevent prompt inflation. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-agent-collaborative.py` | Validates a collaborative-group config against the contract (iteration cap, budget guard wired, synthesizer != contributor, structured workspace entries). | Pre-merge of any collaborative-pattern PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[multi-agent-basics]] — upstream spec.
- [[multi-agent-hierarchical]] — alternative when convergence > coverage.
- [[multi-agent-conversational]] — alternative for open-ended free-turn shape.
- [[role-specialized-models]] — pick synthesizer model.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether collaborative is the right pattern. Pick it when the task is open-ended with no single correct answer (creative/strategy/design); pick hierarchical when convergence + auditability matter more than coverage; pick debate when adversarial verification dominates. Run it before instantiating the class to avoid wrong-pattern cost.
