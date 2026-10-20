---
name: modularity
description: Operational reference for module boundaries, coupling, cohesion, and abstraction depth. Use when designing new modules or components, splitting large files or classes, evaluating dependencies between parts of a system, deciding what to expose in a public interface, naming things well, evaluating whether an abstraction is shallow or deep, or investigating why changes ripple unexpectedly. Covers coupling types (Content through Data), cohesion types (Coincidental through Functional), structural dependency signals (load-bearing modules, instability mismatches, cycles), naming and abstraction depth (Ousterhout), and SOLID as diagnostic signals.
---

# Modularity

Good module design is not about file count or folder structure. It is about making the right things easy to change and the wrong things hard to change accidentally.

For coupling types and signals see [coupling-types.md](coupling-types.md).
For cohesion types and signals see [cohesion-types.md](cohesion-types.md).
For structural dependency signals see [coupling-types.md](coupling-types.md) (structural signals section at the end).
For naming, abstraction depth, and information hiding see [naming-and-abstraction.md](naming-and-abstraction.md).

## Core question

Before evaluating coupling or cohesion, ask: **what is this module's reason to change?**

A module has good boundaries when it changes for one reason. It has poor boundaries when it changes for multiple unrelated reasons, or when changing it forces changes in modules that conceptually should not care.

## SOLID as diagnostic signals

SOLID principles are most useful as signals that something is wrong — not as rules to follow mechanically.

**Single Responsibility** — If you cannot state the module's responsibility in one sentence without "and", it likely has too many. The signal: the module changes for unrelated reasons across different releases.

**Open/Closed** — If adding a new variant requires modifying existing code (not just adding new code), the abstraction boundary is in the wrong place. The signal: every new feature requires editing the same file.

**Liskov Substitution** — If a subtype requires the caller to check what type it actually is before using it, the hierarchy is broken. The signal: `if isinstance(x, SubClass)` in calling code.

**Interface Segregation** — If consumers depend on methods they never call, the interface is too broad. The signal: stub implementations that throw `NotImplemented`.

**Dependency Inversion** — If a high-level module imports directly from a low-level implementation (not an abstraction), changes in the implementation force changes in the policy. The signal: the import graph flows from policy to detail.

Use these to ask "what is wrong here" — not to grade code against a checklist.

## Dependency Structure Matrix

For systems too large to reason about by inspection, a Dependency Structure Matrix (DSM) visualises coupling. Rows and columns are modules; a mark at (row, column) means row depends on column. Clusters of marks off the diagonal indicate hidden coupling. Marks on both sides of the diagonal indicate cycles.

Cycles in the dependency graph are always a structural problem — they prevent independent deployment, testing, and reasoning about modules.
