---
name: sequenced-collections
description: >
  Extends agent's knowledge of Java 21 SequencedCollection, SequencedSet, and
  SequencedMap interfaces. Use when you need first/last element access, reversed
  iteration, or add/remove at both ends of a collection.
compatibility: Java 21+
metadata:
  domain: core-java
  level: beginner
  stack: [java-21]
  version: "1.0.0"
---

# Sequenced Collections (JEP 431)

Java 21 introduced `SequencedCollection`, `SequencedSet`, and `SequencedMap` to
unify access to the first and last elements and provide a `reversed()` view.

## Interfaces

- `SequencedCollection<E>` — extends `Collection`, adds `getFirst()`, `getLast()`, `addFirst()`, `addLast()`, `removeFirst()`, `removeLast()`, `reversed()`
- `SequencedSet<E>` — sequenced `Set` (no duplicates, so addFirst/Left are no-ops on existing elements)
- `SequencedMap<K,V>` — extends `Map`, adds `sequencedKeySet()`, `sequencedValues()`, `sequencedEntrySet()`, `putFirst()`, `putLast()`, `pollFirstEntry()`, `pollLastEntry()`, `reversed()`

## Implementations (already implement these interfaces)

- `ArrayList`, `LinkedList` → `SequencedCollection`
- `LinkedHashSet` → `SequencedSet`
- `LinkedHashMap`, `TreeMap` → `SequencedMap`

## Rules

1. Use `getFirst()` / `getLast()` instead of `get(0)` / `get(size()-1)` — clearer, no index math.
2. Use `reversed()` for reverse iteration instead of manual index-based loops.
3. Prefer `LinkedHashSet` / `LinkedHashMap` over `HashSet` / `HashMap` when insertion order matters.
4. `addFirst` / `addLast` on `LinkedList` are O(1); on `ArrayList` they are O(n) — choose accordingly.
5. Use `SequencedMap` in method signatures when order is part of the contract.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- collections-best-practices — List.of(), Map.of(), copyOf()
