# AutoGen-Style Conversational Multi-Agent Pattern

## Summary

**One-sentence:** Generates an AutoGen-style conversational multi-agent runner with capped sliding-window context, dual termination (phrase + max_turns), and per-turn budget audit.

**One-paragraph:** Two or more agents take sequential turns in a free-form conversation. Each agent receives a sliding window of recent turns (default last 3) plus the previous message, produces a reply, and the loop continues until a termination phrase appears or `max_turns` is reached. The pattern matches the AutoGen GroupChat / v0.4 event-driven core for tasks where the approach cannot be decomposed upfront — interactive debugging, negotiation, Socratic verification. This methodology ships a `ConversationalAgents` class with both guards wired and a per-turn token audit.

**Ефективно для:** інженера, який запускає інтерактивний дебаг / Socratic-перевірку — конверсація замість заздалегідь зафіксованого пайплайну.

## Applies If (ALL must hold)

- Dynamic task where approach cannot be decomposed upfront (debugging, negotiation, Socratic).
- Adversarial verification — one agent proposes, another critiques, conversation converges.
- Open-ended exploration where the conversation path itself is the output.
- Agents need to negotiate a shared understanding before acting.
- A semantic termination signal can be defined (phrase, JSON flag, or output-shape check).

## Skip If (ANY kills it)

- Task has a known sequential pipeline — use `sequential` or `hierarchical` instead.
- Production audit requires structured per-step decision logs — conversational turns are harder to parse.
- Latency budget tight — free-form runs always risk hitting `max_turns`.
- Agents need shared mutable state beyond message history — use `collaborative` workspace pattern.
- Two agents on identical model + identical system prompt — degenerates to monologue.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Validated multi-agent spec | YAML with `pattern: conversational` | `multi-agent-basics` |
| Agent roster (≥2) | list of `{name, model, system_prompt}` | spec |
| `termination_phrase` | string (e.g. `"TASK COMPLETE"`) | spec.termination |
| `max_turns` | int (≤30) | spec.termination |
| Per-turn token budget | int | spec.budget |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/multi-agent-basics` | Upstream spec. |
| `geek/ai/ai-agents/schema-version-pinning` | Turn entries carry `schema_version`. |
| `geek/ai/ai-agents/record-replay-debugging` | Conversation traces feed into record/replay. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: dual termination, sliding window cap, termination check on output, per-turn budget audit, distinct identities | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for `ConversationalAgents` config + turn entry shape | ~650 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing phrase, missing max_turns, full-history prompt, identical agents, no budget audit | ~700 |
| `content/04-procedure.xml` | medium | 5-step build: config → start → turn loop with checks → emit trace → final extraction | ~700 |
| `content/06-decision-tree.xml` | essential | Pick conversational vs sequential vs hierarchical from decomposability and audit needs | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Per-turn response | sonnet | Reliable structured turn generation. |
| Critique role (adversarial) | opus or different family | Stronger reasoning to surface objections; different family breaks echo. |
| Termination detector | haiku | Cheap string + shape check on each output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conversational_agents.py` | Reference runner with sliding window, dual termination, per-turn audit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-agent-conversational.py` | Validates a conversational config (dual termination present, max_turns ≤30, sliding window cap set, distinct identities). | Pre-merge of any conversational-pattern PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[multi-agent-basics]] — upstream spec.
- [[multi-agent-hierarchical]] — alternative when you have a plan.
- [[multi-agent-collaborative]] — alternative for parallel ideation.
- [[record-replay-debugging]] — replay conversational traces deterministically.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether conversational beats sequential/hierarchical: pick conversational when the path is unknowable upfront AND audit can tolerate prose turns. Otherwise pick sequential (known DAG) or hierarchical (manager + workers). Run it before scaffolding to avoid wrong-pattern cost.
