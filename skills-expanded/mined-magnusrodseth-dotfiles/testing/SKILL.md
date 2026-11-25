---
name: testing
description: "Verifies changed behavior through meaningful assertions and appropriate boundaries. Use when designing or reviewing tests."
---

# Testing changed behavior

Read AGENTS.md and the repository's docs for language/framework, fixtures, commands,
container/integration requirements and CI ownership. Do not apply a Python recipe
to Kotlin, frontend or infrastructure work.

Read [external-contract assertions](change-detectors.md) when deciding whether
a constant guard is meaningful.

1. State the behavior and a failure scenario before choosing a test seam. The
   assertion must distinguish a defect from the intended behavior; an exact
   mirror of an implementation or a reversible prose edit rarely needs a test.
2. Exercise the public contract at the nearest meaningful boundary. Mock external
   failures deliberately, not the code being claimed as verified. Locking,
   transactions, migrations and composed wiring require their actual relevant
   boundary; in-memory substitutes cannot establish database concurrency.
3. Use existing fixtures and bounded local checks. Follow the repository's split
   between fast local and full CI/integration suites. Keep data deterministic
   across parallel workers and isolate cross-test state.
4. Run the relevant check, repair in-scope failures and repeat until it passes.
   Preserve assertions and enforcement. Report environment/access blockers and
   failed or unrun checks precisely; do not weaken tests to obtain green output.
