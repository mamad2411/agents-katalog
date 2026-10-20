# Multi-Agent Design Patterns

## Summary

**One-sentence:** Produces a decision record selecting one of eight canonical multi-agent design patterns (Sequential / Parallel Fan-Out / Hierarchical / Generator-Critic / Loop / Human-in-Loop / Router / Blackboard) with rationale and trade-offs.

**One-paragraph:** Eight reusable design patterns cover the bulk of enterprise multi-agent shapes: Sequential Pipeline (linear DAG), Parallel Fan-Out/Gather (independent subtasks merged), Hierarchical Decomposition (manager + workers + synthesis), Generator-Critic (proposer + reviewer loop), Loop Pattern (iterative refinement with halting criterion), Human-in-the-Loop (mandatory approval gate), Router Pattern (classifier dispatches to specialists), Blackboard Pattern (shared workspace). This methodology produces a pattern-selection decision record — not the implementation — that downstream impl methodologies (`multi-agent-hierarchical`, `multi-agent-conversational`, `multi-agent-collaborative`, `multi-agent-production-bus`) consume.

**Ефективно для:** архітектора, який обирає форму multi-agent системи на старті — щоб не запиляти CrewAI у задачу, що чекає Generator-Critic.

## Applies If (ALL must hold)

- Designing or reviewing a multi-agent system (≥2 agents).
- Pattern choice not yet locked in — still architecting, not implementing.
- Trade-offs (latency, cost, audit, parallelism) can be ranked.
- Decision will be persisted as an SDD design.md / ADR entry.
- At least one downstream impl methodology can consume the chosen pattern.

## Skip If (ANY kills it)

- Single-agent task — pattern overhead with no quality gain.
- Implementation already committed (pattern locked in) — use the relevant impl methodology directly.
- No clear decomposition axes — patterns require some decomposition shape to apply.
- Early PoC where debugging orchestration is not yet warranted.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task description + acceptance criteria | text | product brief |
| Latency / cost / audit constraints | list of ranked priorities | SLO + finance |
| Step decomposability + dependency shape | text | architecture session |
| Per-step expertise needs | text | architecture session |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/multi-agent-basics` | Pattern selection feeds the multi-agent spec. |
| `geek/ai/ai-agents/plan-execute-vs-react` | Sequential / Loop choice overlaps with this axis. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: one named pattern per system, no Blackboard without mutable state, no Router without classifier, HITL on every irreversible action, Generator-Critic needs distinct model families | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for pattern decision record (`pattern, rationale, alternatives_considered, tradeoffs, downstream_methodology`) + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: pattern stacking, Router without classifier, missing HITL, Blackboard without locking, generator and critic on same model | ~700 |
| `content/06-decision-tree.xml` | essential | Top-level tree to pick one of the 8 canonical patterns | ~450 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pattern selection | sonnet | Pattern picking from the tree is structured judgement, not generative. |
| Trade-off authoring | opus | Cross-axis reasoning over latency/cost/audit; opus value here. |
| Decision-record formatting | haiku | Mechanical fill of the schema. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-decision-record.md` | ADR-style decision record skeleton: pattern, alternatives, trade-offs, downstream impl methodology. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-agent-design-patterns.py` | Validates a decision record carries pattern from the 8-canonical set, rationale, ≥2 alternatives considered, and a downstream impl link. | Pre-merge of any multi-agent design.md / ADR. |

## Related

- [[multi-agent-basics]] — downstream spec.
- [[multi-agent-hierarchical]] — impl for Hierarchical pattern.
- [[multi-agent-conversational]] — impl for Loop / Generator-Critic shapes.
- [[multi-agent-collaborative]] — impl for Blackboard shape.
- [[multi-agent-production-bus]] — runtime bus that ships any pattern.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the 8 patterns by orthogonal axes: parallelism, mutable state, halting criterion, audit, classifier, irreversibility. Run it before authoring the decision record so the chosen pattern can be defended in design review.
