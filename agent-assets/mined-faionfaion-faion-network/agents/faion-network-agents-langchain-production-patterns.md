# LangChain Production Patterns

## Summary

**One-sentence:** Hardens a LangChain chain with fallbacks, retries, configurable fields, batch processing, and pinned deps; emits a hardening decision-record.

**One-paragraph:** A LangChain chain that boots in a notebook breaks in production from model outages, transient network errors, silent dep upgrades, and unbounded retries. This methodology turns a reliability profile (target uptime, latency budget, model providers available, dep policy) into a deterministic hardening plan: which `with_fallbacks` to wire, which retry strategy, which fields to expose for runtime config, and how to pin deps. Output is a JSON decision-record plus a chain-hardening patch.

**Ефективно для:** solopreneur shipping a paid LangChain agent who cannot get woken at 03:00 by a single provider outage.

## Applies If (ALL must hold)

- Chain has paying or SLA-bound users (or imminently will).
- ≥2 LLM providers are available (or you can sign up for one).
- You control the chain wiring and can wrap nodes with `with_fallbacks` / `with_retry`.
- Deploys run from CI, not from a developer laptop.
- Failures cost money (downtime / refunded calls / refused work).

## Skip If (ANY kills it)

- Prototype with ≤10 users; over-engineering kills velocity.
- Single-provider lock-in mandated by contract (cannot wire fallback).
- Chain is ad-hoc Jupyter analysis with no users.
- Latency budget is so tight (<200ms) that retries are useless — use a circuit breaker instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `reliability-profile.yaml` | YAML with `target_uptime`, `latency_budget_ms`, `providers`, `dep_policy` | author writes |
| Chain entrypoint | Python module + symbol | the existing chain to harden |
| `requirements.txt` or `pyproject.toml` | dep manifest | repo root |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[langchain-basics]] | Need to understand chain composition. |
| [[langchain-observability]] | Hardening without tracing is unprovable. |
| [[max-turns-circuit-breaker]] | Retries multiply turns; pair with turn cap. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Migrated production rules (fallback, retry, pin, batch, configurable) | ~1100 |
| `content/02-output-contract.xml` | essential | Hardening-plan schema + examples | ~800 |
| `content/03-failure-modes.xml` | essential | Silent dep upgrade, retry storm, fallback masking, batch order break | ~700 |
| `content/04-procedure.xml` | recommended | 7-step hardening procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Hardening shape by uptime + provider count | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Fallback graph design | sonnet | Tradeoff reasoning. |
| Patch emission | sonnet | Code-shaped. |
| Cross-check vs failure modes | opus | Catches retry storms and silent masking. |

## Templates

| File | Purpose |
|---|---|
| `templates/reliability-profile.yaml` | Input contract. |
| `templates/hardening-plan.md.j2` | Output skeleton — what gets wired, in what order. |
| `templates/hardening-plan.md` | Output skeleton — what gets wired, in what order. Generated from `templates/hardening-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/chain-hardening-patch.py` | Working `with_fallbacks` + `with_retry` patch. |
| `templates/_smoke-test.yaml` | Minimum viable profile. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-langchain-production-patterns.py` | Validates the hardening-plan JSON. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[langchain-observability]] — tracing is non-optional once you wire fallbacks.
- [[max-turns-circuit-breaker]] — retries × tools = turn explosion.
- [[langchain-workflows]] — when hardening becomes a graph, LangGraph wins.

## Decision tree

Lives at `content/06-decision-tree.xml`. Root question: provider count. ≥2 providers → wire `with_fallbacks`. Single → wire `with_retry` with exponential backoff. Then branches on uptime target (>99.5% → demand cross-region fallback + batched warm-pool) and on dep policy (locked → pin exact + hash; floating → at minimum upper-bound minor versions).
