---
name: z-architecture
description: Deep-module design principles and seam analysis. Use when designing new modules, reviewing interfaces, deciding plugin contracts, or eliminating shallow layers.
---

# Z-Architecture Design Protocol

## Deep Modules vs Shallow Modules

- **Deep Module**: Has a small, simple interface that conceals extensive internal complexity (e.g. Unix file I/O: `open`, `read`, `write`, `close`). High leverage, low cognitive cost.
- **Shallow Module**: Has an interface almost as complex as its implementation, offering little value while creating an extra indirection layer.

## Invariant Design Rules

1. **Design It Twice**: For any critical component or boundary seam, sketch 2 distinct interface designs and compare trade-offs before writing implementation code.
2. **Information Hiding**: Details that change together must live together behind the module boundary.
3. **Data Sovereignty**: A module owns its internal data structures. External access occurs strictly through explicit domain contracts or event messages.
4. **Single Direction Dependencies**: High-level policies depend on abstractions, not concrete low-level details. Circular dependencies are forbidden.
