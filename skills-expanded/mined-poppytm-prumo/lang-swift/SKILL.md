---
name: lang-swift
description: Swift 6 strict concurrency, Actor isolation, Sendable boundary checks, value semantics, and safe memory management.
---

# Swift 6 Strict Concurrency Contract

## 1. Concurrency & Actor Isolation
- Enable Swift 6 language mode with complete concurrency checking (`-Xfrontend -strict-concurrency=complete`).
- Shared mutable state must be protected by an `actor` or isolated to `@MainActor`.
- Cross-actor message parameters must conform to `Sendable`.

## 2. Value Semantics
- Prefer `struct` and `enum` over `class` to guarantee thread-safe value semantics.
