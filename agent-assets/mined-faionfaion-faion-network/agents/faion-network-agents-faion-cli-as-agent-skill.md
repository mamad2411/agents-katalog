# Faion CLI as Agent Skill

## Summary

**One-sentence:** Produces a tool-definition + system-prompt scaffold that wires `faion search` and `faion get-content` into a custom agent as a reasoning tool, with bounded budgets and tier-aware fallback.

**One-paragraph:** Faion ships a CLI; most teams want to call it from their own agent (Claude SDK, OpenAI Assistants, LangGraph). This methodology produces the two artefacts they need: a JSON tool definition (`faion_search`, `faion_get_content`) with bounded args + cost ceilings, and a system-prompt skeleton that teaches the agent when to call which tool, how to interpret the response, and what to do on 403 tier_required. Default budget: ≤3 tool calls per user turn, ≤2k tokens per content fetch.

**Ефективно для:** p7-llm-agent-developer wiring Faion into a domain agent, ml-engineer integrating methodology lookups into a multi-step planner, AI engineers shipping `faion`-aware copilots, vendors building integrations.

## Applies If (ALL must hold)

- Building or modifying an agent that should consult methodology corpora at reasoning time.
- The agent runtime supports JSON tool-use (function calling).
- `faion-cli` is installed on the agent host OR available via subprocess/HTTP.
- A tier (free/solo/pro/geek) is assigned to the agent's CLI credentials.

## Skip If (ANY kills it)

- Agent has no tool-use loop (single-shot completion) — methodology can't fire.
- Faion CLI not in scope (licensing, isolation) — embed the corpus directly instead.
- Tier is unset/anonymous — every call will 401; resolve auth first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Agent runtime + tool schema | JSON Schema or provider spec (OpenAI/Anthropic/LangGraph) | host project |
| Faion CLI version + login token | `faion --version`, `~/.config/faion/token.json` | local install |
| Per-turn budget | int tool-calls + int content-tokens | host product spec |
| Tier capability matrix | from `tier-manifest.json` | faion-network repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[gateway-adapter-template]]` | Same shape: tool-defn + retry + tokenizer pinning. |
| `geek/ai/llm-integration/AGENTS.md` | Tool-use vocabulary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: budget cap, structured args, 403→preview path, idempotent calls, no PII, observability | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for `tool-defs.json` + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: unbounded fan-out, missing tier handling, content paste-into-prompt, log leakage | ~600 |
| `content/04-procedure.xml` | recommended | 6 steps: pick provider format → declare tools → write system prompt → wire 403 → meter → smoke-test | ~700 |
| `content/06-decision-tree.xml` | essential | Tool-call decision branches | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate JSON tool-defs | haiku | Schema fill. |
| Write system-prompt skeleton | sonnet | Bounded wording, examples. |
| Trace-replay tool-use loop check | sonnet | Pattern-match against rules. |
| Multi-provider port (Anthropic↔OpenAI) | opus | Cross-format synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-defs.json` | OpenAI/Anthropic-compatible tool definitions for `faion_search` + `faion_get_content`. |
| `templates/system-prompt.txt` | System-prompt skeleton with placeholders. |
| `templates/dispatcher.py` | Subprocess dispatcher wrapping the CLI with budget + 403 fallback. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-faion-cli-as-agent-skill.py` | Validate tool-defs + system prompt against the contract. | Before agent ships. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[gateway-adapter-template]]` — adapter shape for any LLM/RAG endpoint
- `[[hallucination-attribution-checklist]]` — what to log when the agent hallucinates while using `faion_get_content`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters preconditions, then routes: tool-use loop yes/no → tier set yes/no → declare tools and emit system prompt or skip.
