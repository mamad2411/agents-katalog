---
name: swift-design-patterns
description: >-
  Apply Gang of Four design patterns in Swift. Use when implementing, choosing,
  refactoring toward, or explaining a design pattern in Swift/iOS code — e.g.
  "which pattern fits this?", "refactor this giant switch", "show me Strategy in
  Swift", "decouple this with a pattern", or any mention of Strategy, Factory,
  Observer, Decorator, Adapter, Singleton, Builder, Visitor, etc. in a Swift
  context.
---

# Swift Design Patterns

This skill ships a curated catalog of all 23 GoF patterns with idiomatic,
compile-checked Swift examples. Prefer it over recalling patterns from memory —
the examples are verified against the Swift 6 toolchain and stay consistent.

## Reference files (in this skill's folder)

- **`references/catalog.md`** — index of every pattern grouped by category
  (Creational, Structural, Behavioral): id, intent, related patterns, and
  **"Reach for it when"** cues. Read this to browse or to recommend.
- **`references/patterns/<id>.md`** — full reference for one pattern: intent,
  problem, solution, applicability, participants, conceptual + real-world Swift
  examples, pros/cons, related patterns. Ids are kebab-case
  (`abstract-factory`, `chain-of-responsibility`, `template-method`, …).
- **`references/conventions-template.md`** — starter template for a project's
  architecture & conventions file.

## How to work

0. **Honor the project's conventions first.** When working inside a real
   project, look for a conventions file — in order: `.swift-architecture.md`,
   `.claude/swift-architecture.md`, `.claude/swift-conventions.md`,
   `ARCHITECTURE.md` at the project root. If one exists, treat it as
   authoritative: use the team's architecture, layering rules, DI style,
   naming, and any team-specific or banned patterns — *over* the generic
   catalog. If a pattern you'd suggest conflicts with it (e.g. they ban
   Singletons), follow the conventions and say so. If none exists, proceed with
   framework-neutral defaults and you may offer to scaffold one
   (`/swift-conventions init`).
1. **Choosing a pattern.** When the user describes a symptom rather than naming
   a pattern, read `references/catalog.md` and rank candidates by how well the
   problem matches each pattern's intent and "Reach for it when" cues. Then
   read `references/patterns/<id>.md` for the top candidate to confirm fit
   before proposing it. Say briefly *why* it fits and note the trade-offs (the
   pattern's cons) — don't oversell.
2. **Implementing a named pattern.** Read its reference file to ground your code
   in the catalog's idiomatic structure, then adapt it to the user's actual
   types and naming. Don't paste the example verbatim — fit it to their
   codebase.
3. **Explaining.** Use the pattern's intent/problem/solution and participants;
   show the conceptual example for the shape and the real-world example for
   practical context.

## Judgment

- Patterns are a means, not a goal. If a Swift-native feature is simpler — a
  closure instead of a single-method Strategy, an `enum` instead of a State
  hierarchy, protocols/generics instead of boilerplate — say so and prefer it.
- Match the surrounding code's conventions when writing into an existing
  project. Value types and protocol-oriented design are usually the Swift-idiomatic
  default.
- Mention related patterns when a neighbor (Strategy vs State, Adapter vs
  Bridge, Factory Method vs Abstract Factory) might be the better fit.
