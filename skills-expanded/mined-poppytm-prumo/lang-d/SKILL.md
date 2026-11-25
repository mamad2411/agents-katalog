---
name: lang-d
description: Dlang systems programming, @safe by default, DIP1000 scope pointer checking, @nogc optimization, pure immutability, and memory safety.
---

# Dlang Safe-by-Default & Scope Pointer Discipline Contract

## 1. Safety Architecture
- **`@safe` by Default**: All module functions must be marked `@safe` (or encapsulated in a `safe:` module-level declaration).
- **DIP1000 Scope Pointers**: Enforce `-preview=dip1000` to prevent pointers or references from escaping their local scope.
- **Unsafe Code Quarantine (`@trusted`)**: `@trusted` functions MUST be small, isolated, and accompanied by formal escape-hatch registration with safety proofs.
- **`@nogc` and `pure`**: Mark critical inner loops `@nogc` to avoid garbage collector latency, and `pure` to guarantee referential transparency.
