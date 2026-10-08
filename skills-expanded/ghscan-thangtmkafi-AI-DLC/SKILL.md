---
name: kafi-code-review-kotlin
description: Kotlin code reviewer. Invoked by the kafi-code-review router (or directly) to review .kt/.kts files for null safety, coroutine scopes, and idiomatic pitfalls at Stage 14c. Checks detekt, ktlint.
inclusion: manual
---

# Skill: kafi-code-review-kotlin

## Tooling baseline
- **Static:** detekt · **Style:** ktlint
- **Deps:** OWASP dependency-check / gradle versions plugin

## Critical (blocking) checks
- [ ] Null safety — no `!!` non-null assertions on truly-nullable values; prefer `?.`/`?:`/`requireNotNull`
- [ ] Coroutines — launched in a proper `CoroutineScope` (no `GlobalScope`); structured concurrency honored; cancellation cooperative
- [ ] No blocking calls on coroutine dispatchers meant for non-blocking (use `Dispatchers.IO` for blocking)
- [ ] Sealed class / enum `when` is exhaustive (no `else` escape hatch that hides new cases)
- [ ] Exceptions not swallowed; `runCatching` results actually handled
- [ ] SQL parameterized; secrets via config-store

## Advisory (warning) checks
- Prefer `val` over `var`; immutable collections
- Data classes for DTOs; sealed hierarchies for state
- Extension functions over util classes
- Scope functions (`let`/`apply`/`run`) used for clarity, not nesting
- Flow over callback for streams; `StateFlow`/`SharedFlow` for UI state

## Framework hot-spots
- **Android/Compose:** state hoisting · `remember`/`derivedStateOf` correct · no work in composition · lifecycle-aware collection
- **Spring (Kotlin):** same as Java reviewer + nullability annotations bridge

## Output
Per finding: `severity · file:line · rule · what · suggested fix`. Critical → Stage 14c sub-check 1 ✗.

## References
- Router: `kafi-code-review` · Stage 14c: `construction/conformance-audit.md`
