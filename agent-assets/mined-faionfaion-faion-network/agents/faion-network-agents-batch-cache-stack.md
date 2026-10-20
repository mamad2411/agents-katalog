# Batch API + Prompt Caching Stack

## Summary

**One-sentence:** Sends non-real-time agent workloads through the provider's Message Batches API with cache_control on the longest stable prefix — stacks the 50% batch discount with the 90% cache-read discount for ~5% of synchronous-uncached cost on cached portion.

**One-paragraph:** Overnight pipelines, eval harnesses, content backfills, dataset labelling — none of these need synchronous latency, but most still send synchronous uncached requests and pay 20× what they could. This methodology wires two stacking optimisations: (1) submit through Message Batches / Batch Mode (50% off, 24h SLA); (2) pin `cache_control` on the longest byte-identical prefix shared across batch items (90% off prefill on cache reads). Output is a config block + reference code that an engineer applies to an existing pipeline.

**Ефективно для:** Команд, де щоночі AI-pipeline жере $400 OpenAI/Anthropic — без батчей і без кешу; правильно зібраний stack зрізає це до $20-$40 за один день переробки.

## Applies If (ALL must hold)

- Workload is asynchronous (24h turnaround acceptable).
- ≥100 items per batch (cache amortisation requires volume).
- A stable prefix exists across items (system prompt + tools + canonical instructions).
- Provider supports batch + caching (Anthropic, OpenAI, etc).
- A finance / cost owner is interested in the savings.

## Skip If (ANY kills it)

- Workload is user-facing real-time (sub-second).
- Each item has a unique prefix (no caching opportunity).
- Batch size <50 (overhead exceeds savings).
- Provider doesn't support both batch and caching.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Workload sample | jsonl with prompts | Pipeline owner |
| Provider model + version | string | Tech lead |
| Cost dashboard | URL | Finance |
| Batch endpoint credentials | API key | Ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/prompt-cache-prefix-order/AGENTS.md` | Prefix ordering rules for cache hits. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: batch route, prefix byte-identical, cache_control marker, monitor hit rate | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the batch+cache config | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: async? → volume? → stable prefix? → install/skip | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_prefix` | haiku | Mechanical. |
| `verify_byte_identical` | haiku | Mechanical diff. |
| `tune_cache_marker_position` | sonnet | Per-pipeline judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the config. |
| `templates/output.example.json` | Filled example. |
| `templates/batch_with_cache.py` | Python skeleton for batch submission with cache_control. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the config. | Before pipeline switch. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[prompt-cache-prefix-order]] — prefix ordering rules.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is the workload async (24h ok)? (2) is per-batch volume ≥100? (3) is there a byte-identical stable prefix? Leaves point to "install stack", "use batch only / cache only", or "skip".
