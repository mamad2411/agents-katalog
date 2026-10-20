---
name: switch-patterns
description: >
  Extends agent's knowledge of Java 21 pattern matching in switch, including
  instanceof patterns, guarded patterns, and null handling. Use when replacing
  instanceof-if chains, adding type-based dispatch, or handling null in switch.
compatibility: Java 21+
metadata:
  domain: core-java
  level: beginner
  stack: [java-21]
  version: "1.0.0"
---

# Switch Pattern Matching

Java 21 (JEP 441) allows `instanceof` patterns directly in `switch` cases.
This replaces verbose type-check-and-cast chains with concise, compiler-checked
pattern matching. Guarded patterns (`when` clauses) add arbitrary conditions.

## Concepts

- `case String s -> ...` — type pattern with binding variable
- `case String s when s.length() > 5 -> ...` — guarded pattern
- `case null -> ...` — explicit null handling (Java 21)
- `case Circle c when c.radius() > 0 -> ...` — domerguard + binding
- Dominance: a more general pattern (e.g., `CharSequence`) dominates a more specific one (e.g., `String`); order from most specific to least specific or the compiler will reject

## Rules

1. Replace all `if (x instanceof T) { T t = (x) ... }` chains with `switch` pattern matching.
2. Handle `null` explicitly with `case null` — don't let it silently fall through.
3. Use `when` guards for additional conditions on a matched type.
4. Order cases from most specific to least specific; the compiler will flag dominance violations.
5. Always include a `default` for non-exhaustive switches.
6. Combine with sealed types for compiler-verified exhaustiveness (see records-sealed skill).

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- records-sealed — sealed interfaces + exhaustive switch
- exception-strategy — domain exceptions for unhandled types
