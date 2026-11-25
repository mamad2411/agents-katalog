---
name: agentdb-causal-explain
description: Walk the causal graph in AgentDB to explain why two memories are connected, or trace a root cause. Use when the user asks "why did X happen", "what led to Y", or after an incident.
---

# Causal Explain

Given a target memory (an episode, a failed test, an outgoing change), traverse the causal graph backwards through edges to surface the chain of preceding events that explain it.

## When to use

- "Why did this fail?"
- "What led to the regression?"
- "Trace the dependency chain for X."
- Incident postmortem — surface every step + decision that contributed.

## API

```
agentdb_causal_explain(
  targetMemoryId:  <id>
  maxDepth?:       3
  minConfidence?:  0.5
  edgeWeights?:    'uplift' | 'confidence' | 'product'   // ranking strategy
)
```

Returns a path or DAG of `(node, edge, node)` tuples ranked by combined `confidence × |uplift|`. Each step carries the relation (`caused`, `supersedes`, `depends-on`, etc.) so the explanation reads naturally.

## Output shape

```
Why did "deploy-2026-05-04 failed migration" happen?

  ┌─ skill[migrate-add-not-null-column]   confidence 0.92
  │     ─[supersedes]→ skill[v1: migrate-with-default]
  │     ─[caused]→     episode[long-running migration on 50M rows]
  │                          ─[caused]→ episode[deploy-2026-05-04 failed migration]
  │
  └─ adr[ADR-046: zero-downtime migration policy]   confidence 0.78
        ─[depends-on]→ skill[migrate-add-not-null-column]
```

## Use the investigator agent

For complex traces, dispatch the `agentdb-investigator` agent (this plugin) — it walks deeper, cross-references with hierarchical memory, and writes a postmortem-shaped report.

## Don't

- Don't traverse with `maxDepth > 5` casually — graph fan-out gets exponential and the bandit's confidence weights don't compensate.
- Don't ignore the `confidence` column. A high-uplift edge with confidence 0.3 is gossip, not evidence.
