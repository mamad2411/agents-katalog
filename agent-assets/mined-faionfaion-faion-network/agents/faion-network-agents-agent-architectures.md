# Agent Architectures (Memory + Tools + Planning + Reflection)

## Summary

**One-sentence:** Produces a production-ready agent scaffold: memory with embeddings + summarization, typed tool framework, async state machine, planning + reflection loops, and an idle-eviction policy for long-runn...

**One-paragraph:** Production-ready architectures for autonomous agents with memory, tools, planning, and reflection. Covers memory system with embeddings, tool registry framework, async state machine, planner / reflection loop, and long-run summarization. Memory summarization becomes critical for long-running agents: at 50+ iterations raw concatenation overflows context; implement compress step or limit summary_recent() to last 3-5 entries.

**Ефективно для:** production agents running >100 iterations; multi-tool agents with ≥5 callable tools; agents persisting across sessions; agents required to plan before acting and reflect after.

## Applies If (ALL must hold)

- Building or scaling a production LLM agent (not a prototype)
- Agent uses ≥3 tools
- Agent runs for ≥50 iterations or across sessions
- Latency budget allows for planning + reflection loops (≥2s)

## Skip If (ANY kills it)

- Single-turn extraction / classification task — full agent loop is overhead
- Sub-100ms latency budget — planning + reflection blows the budget
- Stateless function call replacing a deterministic API

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool inventory + schemas | JSON Schema | team |
| Vector store (Pinecone / pgvector / Weaviate) | service | infra |
| LLM provider with structured-output support | API key | team |
| Eval suite ≥30 trajectories | JSONL | eval owner |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-observability-stack-blueprint]]` | Trace + cost + eval wiring |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (r1-r5 + skip-methodology) with rationale and source | ~550 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author tool registry | sonnet | Schema generation. |
| Tune reflection threshold | opus | Multi-trajectory reasoning. |
| Author memory summarizer prompt | sonnet | Template application. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent.py.tmpl` | Agent scaffold: FSM + memory + tools + planning + reflection. |
| `templates/tool-registry.py.tmpl` | Schema-validated tool registry. |
| `templates/memory.py.tmpl` | Memory class with summarization. |
| `templates/_smoke-test.py` | Minimal runnable agent stub. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-architectures.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-observability-stack-blueprint]]`
- `[[agent-reasoning-depth-budget]]`
- `[[agent-failure-taxonomy]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-architectures applies: root question — "Is the workload a multi-tool, multi-iteration agent (not a single LLM call)?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
