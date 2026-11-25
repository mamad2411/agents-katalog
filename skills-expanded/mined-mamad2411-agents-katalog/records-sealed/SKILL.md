---
name: records-sealed
description: >
  Extends agent's knowledge of Java 21 records, sealed interfaces, and pattern
  matching with exhaustive switch. Use when modeling algebraic data types, replacing
  DTO classes with records, or writing type-safe switch expressions.
compatibility: Java 21+
metadata:
  domain: core-java
  level: intermediate
  stack: [java-21]
  version: "1.0.0"
---

# Records, Sealed Interfaces & Pattern Matching

Records provide compact immutable data carriers. Sealed interfaces restrict which
classes can implement them. Together they model algebraic data types with
exhaustive pattern matching.

## Concepts

- `record Point(int x, int y) {}` — auto-generates constructor, equals, hashCode, toString
- `sealed interface Shape permits Circle, Rectangle {}` — closed type hierarchy
- `switch` on sealed types is exhaustive — no `default` needed
- Record patterns (JEP 440): `case Circle(var x, var y, var r) -> ...`
- `non-sealed` permits further extension at a leaf

## Rules

1. Use records for all value objects and DTOs — never write boilerplate getters/equals/hashCode.
2. Use sealed interfaces when the set of implementations is fixed and known.
3. Always use exhaustive switch on sealed types — the compiler enforces completeness.
4. Use record patterns to destructure records inline in switch cases.
5. Keep records shallow — no deep nesting; compose with other records.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- switch-patterns — instanceof pattern matching, guarded patterns
- immutability — defensive copying, with-er methods
