---
name: optimization-catalog-cutile-dsl
description: >
  Shared optimization guidance plus cuTile Python DSL-specific overlays. Use when: (1) selecting
  optimizations for a cuTile Python DSL kernel, (2) checking cuTile-specific implementation traps,
  (3) deciding whether a profiling finding belongs in shared knowledge or a cuTile overlay,
  (4) updating cuTile Python DSL optimization docs, (5) reviewing how a shared pattern maps to
  cuTile.
---

# cuTile Python DSL Optimization Catalog

## Read Order

1. Start with the shared root catalogs in `docs/knowledge/optimizations/` and `docs/knowledge/anti-patterns/`.
2. Then read cuTile Python DSL-specific overlays in `docs/knowledge/languages/cutile-dsl/` when the implementation depends on cuTile APIs, compiler behavior, or code-generation limits.

## cuTile Overlay Root

- `docs/knowledge/languages/cutile-dsl/optimizations/`
- `docs/knowledge/languages/cutile-dsl/anti-patterns/`

## Typical cuTile-only topics

- `num_ctas`, `occupancy`, or `ByTarget` behavior
- cuTile math and numeric-semantics hints
- code-generation sensitivity tied to `@ct.kernel` lowering
- limits that arise from cuTile's public scheduling model