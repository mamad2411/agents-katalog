# Agent Patterns

## Summary

**One-sentence:** Picks the right control-flow pattern (ReAct, Plan-and-Execute, Reflexion) for an autonomous agent task and locks it in with iteration caps and a termination signal.

**One-paragraph:** Different agent tasks require different control flow patterns. ReAct (Reason + Act) loops are general-purpose for tool-driven investigation. Plan-and-Execute creates a structured plan upfront for known multi-step projects. Reflexion wraps an inner agent with self-critique and retry for tasks where success is objectively checkable (code, math, structured extraction). This methodology produces a single decision record naming the chosen pattern, max iterations/attempts, the termination signal, and the rationale for not picking the other two patterns.

**Ефективно для:** Ситуацій, де агентний цикл ще не визначено, але є зрозуміла мета і набір інструментів — методологія за 10 хвилин обмежує простір рішень до однієї перевіреної архітектури плюс жорсткі ліміти, замість «спробуємо ReAct і подивимось».

## Applies If (ALL must hold)

- Task requires ≥2 tool calls or ≥2 reasoning steps (not a single-shot prompt).
- The task has either a verifiable success signal or a bounded scope of subtasks.
- Tool access is available (HTTP, filesystem, code execution, or MCP server).
- The owner can budget at least 5 LLM round-trips for the task.
- A human reviewer is named for the final output before it is acted upon.

## Skip If (ANY kills it)

- Single-step retrieval or classification — pattern overhead is wasted.
- Latency budget < 2 seconds end-to-end — patterns add round-trips.
- No verifiable success criterion exists (Reflexion has no termination signal).
- No tools accessible — ReAct collapses into plain chain-of-thought.
- Strict budget of < 5 LLM calls — patterns spend iterations.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Task description | natural-language brief, ≤500 chars | Operator / parent agent |
| Tool inventory | JSON list of `{name, description, schema}` | Tool registry / MCP catalogue |
| Success criterion | Either a test command, a JSON schema, or a checklist | Owner of the downstream artefact |
| Budget caps | `max_iterations` + `max_attempts` (ints) | Operator (cost policy) |
| Pattern preference (optional) | one of `react|plan-and-execute|reflexion` | Operator override |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/autonomous-agents/AGENTS.md` | Provides the broader autonomous-agent vocabulary (planner/executor/critic). |
| `geek/ai/ai-agents/ai-agent-patterns/AGENTS.md` | Sibling overview — clarifies when CoT vs full agent loop is needed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (caps, idempotent tools, terminal condition, model choice, observability, human-in-loop) | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision record + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (loops, plan staleness, runaway Reflexion, context overflow, fabricated tools) | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: classify task → pick pattern → fix caps → wire signals → emit record | ~1100 |
| `content/05-examples.xml` | medium | Worked examples for each pattern (research / code-fix / build-feature) | ~1100 |
| `content/06-decision-tree.xml` | essential | Binary decision tree: success-signal? → bounded-subtasks? → ReAct/Plan/Reflexion leaf | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task_shape` | haiku | Cheap structured classification of task vs tool inventory. |
| `pick_pattern` | sonnet | Per-instance judgment — applies decision tree to task features. |
| `author_decision_record` | sonnet | Composes the final JSON output with rationale. |
| `review_for_high_stakes` | opus | Used only when task is irreversible or production-facing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.json` | JSON Schema for `agent-patterns` output decision record. |
| `templates/decision-record.example.json` | Filled minimal valid example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-patterns.py` | Validate a decision-record file against the JSON Schema. | After subagent returns, before downstream agent reads it. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[ai-agent-patterns]] — overview of all named patterns including framework choices.
- peer: [[autonomous-agents]] — broader autonomous-agent operating context.

## Decision tree

See `content/06-decision-tree.xml`. The tree asks three observables in order: (1) is there a deterministic success signal? (2) are subtasks enumerable up-front? (3) is the action irreversible? Leaves point to ReAct, Plan-and-Execute, Reflexion, or `escalate-to-human`. Used when the operator hasn't pre-specified a pattern; never overrides an explicit operator choice.
