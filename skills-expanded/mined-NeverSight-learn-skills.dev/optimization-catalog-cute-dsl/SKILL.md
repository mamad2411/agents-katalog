---
name: optimization-catalog-cute-dsl
description: >
  Shared optimization guidance plus CuTe Python DSL overlays. Use when: (1) selecting
  optimizations for a CuTe Python DSL kernel, (2) deciding whether a finding is shared or
  cute-dsl-specific, (3) recording CuTe Python DSL implementation notes, (4) reviewing the
  knowledge layout for cute-dsl work, (5) mapping shared patterns to a CuTe Python DSL
  implementation surface.
---

# CuTe Python DSL Optimization Catalog

## Read Order

1. Start with the shared root catalogs in `docs/knowledge/optimizations/` and `docs/knowledge/anti-patterns/`.
2. Then read or add CuTe Python DSL overlays under `docs/knowledge/languages/cute-dsl/` when the implementation details depend on that surface.

## Overlay Root

- `docs/knowledge/languages/cute-dsl/optimizations/`
- `docs/knowledge/languages/cute-dsl/anti-patterns/`

## Current State

The overlay directories are intentionally sparse at first. Add entries only when a finding is genuinely specific to the CuTe Python DSL surface rather than a shared algorithmic rule.