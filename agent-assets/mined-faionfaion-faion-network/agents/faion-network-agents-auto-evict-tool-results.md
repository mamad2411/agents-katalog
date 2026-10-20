# Auto-Evict Tool Results at Token Threshold

## Summary

**One-sentence:** Runtime middleware that auto-evicts any tool result over N tokens (default 20k) to disk and substitutes {path, preview, total_tokens, evicted:true} into the agent's message history before the LLM ever sees the oversized payload.

**One-paragraph:** LLMs cannot reliably self-truncate large tool returns; the result is context corruption, blown context windows, and incoherent later turns. This methodology installs the enforced sibling of voluntary "filesystem as memory": a deterministic decorator wraps the agent's tool runtime, checks token count on every return, persists oversized payloads to a scratch directory keyed by tool_call_id, and feeds a typed pointer into the agent. The agent recovers slices via a paired `read_file(path, lines)` tool. Output is one config artifact + middleware reference embedded in the agent harness.

**Ефективно для:** Команд, де агент іноді отримує 200k токенів з одного tool call і потім весь run йде нанівець; middleware вирішує цей клас bugs раз і назавжди — не людська дисципліна, а runtime constraint.

## Applies If (ALL must hold)

- Agent calls tools that occasionally return very large payloads (file reads, web scrape, DB query, log search).
- Long-horizon runs (>5 iterations) where one oversized return blows multiple subsequent turns.
- Scratch storage (local disk, S3, in-process content store) is available.
- A paired read-file tool can be added to the agent's toolbelt.
- Token counter is available for the model in use.

## Skip If (ANY kills it)

- Tools have hard size caps in the tool definition (e.g. always returns ≤2k).
- Short single-turn agents where the result is consumed immediately.
- Agent has no filesystem-equivalent storage available.
- No paired read tool can be added (model not allowed to access scratch).

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Tool registry | JSON list of tools | Tool catalogue |
| Token counter | callable token_count(text) → int | Provider SDK |
| Scratch storage path | URL / local path | Ops |
| Threshold N | int (default 20000) | Tech lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/filesystem-as-working-memory/AGENTS.md` | Voluntary sibling pattern. |
| `geek/ai/ai-agents/file-reference-passing/AGENTS.md` | Pointer-passing convention used by the evict decorator. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 rules: middleware, deterministic write, paired read tool | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the eviction config + the evicted pointer shape | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: wire middleware → expose read tool → test → tune N → ship | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: large payloads possible? → storage available? → read-tool addable? → install/skip | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `instrument_token_counter` | haiku | Mechanical. |
| `tune_threshold_N` | sonnet | Per-agent tuning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the eviction config. |
| `templates/output.example.json` | Filled example. |
| `templates/evict-middleware.py` | Python middleware skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate eviction config. | After wiring, before ship. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[filesystem-as-working-memory]] — voluntary sibling.
- peer: [[file-reference-passing]] — pointer convention.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) can any tool return >N tokens? (2) is scratch storage available? (3) can a paired read-tool be exposed? Leaves point to "install", "raise hard tool caps instead", or "skip — not applicable".
