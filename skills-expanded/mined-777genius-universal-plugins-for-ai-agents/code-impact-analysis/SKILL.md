---
name: code-impact-analysis
description: Safely analyze code impact before refactors, behavior changes, API changes, and cross-module edits.
execution_mode: docs_only
supported_agents:
  - codex
  - claude
---

# Code Impact Analysis

## What it does

Builds a verified impact set before changing shared behavior, public interfaces, state stores, routes, API DTOs, database models, feature flags, or memory/transcription flows.

## When to use

Use this before any refactor or behavior change where missing one caller could break the product.

## How to run

1. Locate the definition with Serena or `rg`.
2. Find exact callsites with `rg`.
3. Find type-aware references with Serena.
4. Ask CGC for callers, callees, and complexity.
5. Use Semble to find similar patterns that exact search may miss.
6. Decide the minimum edit set.
7. Run focused tests, typecheck, or app verification.

Useful commands:

```bash
rg -n "symbolName\\(" .
uvx --from semble==0.2.0 semble search "similar usage of symbolName" .
cgc analyze callers symbolName --context "$(basename "$PWD")"
cgc analyze calls symbolName --context "$(basename "$PWD")"
cgc analyze complexity --limit 20 --context "$(basename "$PWD")"
```

## Constraints

- If `rg` and Serena disagree, inspect both results. Generated code, dynamic dispatch, and framework magic can explain the difference.
- If CGC disagrees with `rg` or Serena, treat CGC as incomplete until verified.
- If Semble finds a pattern outside exact symbol search, inspect it before concluding the impact set is small.
- If a change crosses modules or user-facing workflows, add or update tests near the affected behavior.
- Stop and ask for direction only when unrelated dirty user changes block a safe edit, the change requires a product decision, or no reasonable verification is possible.
