---
name: memory-fragment-sizing-for-llm-input
description: Chunk memory into fragments respecting LLM token budget, per-file and per-session limits
category: data-pipeline
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [evolver, data-pipeline, llm, context-budget]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 22773782475cecf43dc9c1af264bf5f9cacc28bc
source_project: evolver
source_paths:
  - src/evolve.js
imported_at: 2026-04-18T00:00:00Z
---

# Multi-cap memory fragment builder

Feeding agent memory into an LLM requires a *global* context budget and *per-source* caps — without both, one chatty file monopolizes the window.

## Three-cap scheme (config-driven)

- `TARGET_BYTES` — global budget (e.g., 120_000).
- `PER_FILE_BYTES` — max bytes from any single file (e.g., 20_000).
- `PER_SESSION_BYTES` — max bytes from any single session (e.g., 20_000).

Sort sources by recency. Greedily include each, trimming to the per-source cap before accounting against the global budget. Stop when the global budget is exhausted.

## Mechanism

```js
function buildFragments(sources, caps) {
  const out = [];
  let used = 0;
  for (const s of sources.sort(byRecencyDesc)) {
    const slice = s.body.slice(0, caps.perFile);
    if (used + slice.length > caps.target) break;
    out.push({ ref: s.ref, body: slice });
    used += slice.length;
  }
  return out;
}
```

## When to reuse

Any RAG or agent pipeline that assembles context from heterogeneous sources and must stay within a hard token/byte cap.
