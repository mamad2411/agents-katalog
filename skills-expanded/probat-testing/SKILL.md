---
name: probat-testing
description: Use when the user needs to write or run unit, functional, or integration tests for TLPP code using ProBat (tlppCore's native testing engine) -- covering @TestFixture, @Test, @Setup/@TearDown, @OneTimeSetUp/@OneTimeTearDown, @Skip, @ErrorLog annotations, the full assertion library (assertEquals, assertTrue, assertVector, assertJson, assertIsRegExFull, etc.), SKIPASSERT, and TDD/CI workflows. Also triggers on Portuguese phrasing like "testes unitarios", "criar teste ProBat", "testar rotina TLPP", "cobertura de testes", or requests to add @Test methods to a TLPP class.
---

# ProBat Testing (TLPP)

This skill covers ProBat, the native unit/functional/integration testing engine of tlppCore, used exclusively with TLPP (`.tlpp`) source files -- even when the code under test is legacy `.prw`. It covers the required `#include "tlpp-probat.th"`, the `test.<module>` namespace convention, the full annotation set (`@TestFixture`, `@Test`, `@Setup`, `@TearDown`, `@OneTimeSetUp`, `@OneTimeTearDown`, `@Skip`, `@ErrorLog`), the `tlpp.probat` assertion functions, the class-based execution lifecycle, and `SKIPASSERT` for conditional assertion skipping.

Activate this skill when the user wants to create a new ProBat test fixture, add test methods to cover a routine, set up setup/teardown logic, or understand how ProBat discovers and executes tests (via REST API or the VSCode extension). Concrete test-writing templates live in the sibling patterns file.

It does not cover generating the production TLPP code being tested (see `advpl-code-generation`), reviewing code quality outside of tests (see `advpl-code-review`), or writing embedded SQL used inside test fixtures (see `embedded-sql`).

| Reference file | Read when |
|---|---|
| reference.md | Always -- includes, namespace convention, annotations, assertion function reference, execution lifecycle, and how tests are run |
| patterns-unit-tests.md | Writing a concrete ProBat test fixture and need ready-to-adapt templates/patterns |
