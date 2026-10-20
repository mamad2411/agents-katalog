---
name: khorikov-unit-testing
description: "Knowledge base from \"Unit Testing Principles, Practices, and Patterns\" by Vladimir Khorikov. Use when applying Khorikov's frameworks for the four pillars of a good test, mocks vs stubs, test fragility, integration testing, managed vs unmanaged dependencies, testing styles, or refactoring toward valuable tests — studying the book or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Unit Testing Principles, Practices, and Patterns
**Author**: Vladimir Khorikov | **Pages**: ~305 | **Chapters**: 11 | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `mocks`, `four pillars`, `integration testing`, `database tests`; I find and read the relevant chapter.
- **With a chapter** — ask for `ch05`; I load that chapter file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering. Code is C#, but the principles are language-agnostic.

---

## Core Frameworks & Mental Models

**The goal of unit testing = sustainable growth.** Tests exist to let the project keep growing without slowing down. Code is a liability, not an asset — and so is a test. Every test must earn its keep on a cost-benefit basis. (Ch 1)

**The four pillars of a good unit test** (Ch 4 — the spine of the book). Rate each test and **multiply** them — any pillar near zero makes the test worthless:
1. **Protection against regressions** — does it catch real bugs?
2. **Resistance to refactoring** — does it stay green when behavior is unchanged? **Non-negotiable, binary.** A test that fails on refactoring is a *false positive* and actively harmful.
3. **Fast feedback** — how quickly it runs.
4. **Maintainability** — how cheap it is to read and run.
> You can maximize only 3 of 4. **Lock resistance + maintainability; trade between protection and speed.** Eradicate brittleness (false positives) first — accuracy is signal-to-noise.

**Classical vs London school** (Ch 2). The **classical (Detroit)** school isolates *tests* from each other and uses real collaborators, mocking only **shared** dependencies. The **London (mockist)** school isolates the *class* with mocks everywhere. **Prefer classical** — London's pervasive mocking produces brittle tests (low resistance to refactoring). A unit test verifies a **unit of behavior**, not a class or method.

**Observable behavior vs implementation details** (Ch 5). Assert **only** on observable behavior (the public contract a client cares about). Asserting on implementation details is the root cause of test fragility. Mocks are fine for *outgoing* commands to external systems; never for internal mechanics.

**Mock vs stub** (Ch 5). A **stub** supplies canned inputs (queries) — **never assert on a stub** (that's overspecification). A **mock** verifies outgoing interactions (commands). Follow **Command Query Separation**.

**What to mock — managed vs unmanaged dependency** (Ch 8). The key integration-testing decision:
- **Managed** (only your app touches it, e.g. the application database) → **use the real thing**, assert final state.
- **Unmanaged** (visible to other apps: message bus, SMTP) → **mock it** to protect the observable contract.

**Three styles of unit testing** (Ch 6), best → worst for quality: **output-based** (pure function, assert return value) > **state-based** > **communication-based** (mocks). Get there with **functional architecture — functional core, mutable shell**: pure decision-making core returns instructions; a thin shell applies side effects.

**Types-of-code quadrant** (Ch 7) — complexity/domain-significance × number of collaborators:
- **Domain model & algorithms** (high complexity, few collaborators) → **unit-test thoroughly**, highest value.
- **Trivial code** (getters/setters) → **don't test**.
- **Controllers** (orchestration) → **integration-test**.
- **Overcomplicated code** (high complexity, many collaborators) → **refactor away** via the **Humble Object pattern** — split into domain + controller. Empty this corner.

**Coverage metrics are negative indicators only** (Ch 1). Low coverage signals a problem; high coverage proves nothing. Never a target.

**Test Pyramid** (Ch 4, Ch 8): many fast unit tests, fewer integration, fewest end-to-end. Flatten toward integration for simple CRUD apps.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-goal-of-unit-testing.md) | The Goal of Unit Testing | sustainable growth, coverage as negative indicator, cost-benefit |
| [ch02](chapters/ch02-what-is-a-unit-test.md) | What Is a Unit Test? | classical vs London school, dependency taxonomy, TDD styles |
| [ch03](chapters/ch03-anatomy-of-a-unit-test.md) | The Anatomy of a Unit Test | AAA, Given-When-Then, fixtures, parameterized tests |
| [ch04](chapters/ch04-four-pillars.md) | The Four Pillars of a Good Unit Test | four pillars, false +/−, trade-off triangle, test accuracy |
| [ch05](chapters/ch05-mocks-and-test-fragility.md) | Mocks and Test Fragility | mock vs stub, observable behavior, hexagonal arch, CQS |
| [ch06](chapters/ch06-styles-of-unit-testing.md) | Styles of Unit Testing | output/state/communication styles, functional architecture |
| [ch07](chapters/ch07-refactoring-toward-valuable-tests.md) | Refactoring Toward Valuable Unit Tests | types-of-code quadrant, Humble Object, CanExecute/Execute |
| [ch08](chapters/ch08-why-integration-testing.md) | Why Integration Testing? | managed vs unmanaged deps, Test Pyramid, fail fast |
| [ch09](chapters/ch09-mocking-best-practices.md) | Mocking Best Practices | mock at system edges, mock types you own, spies |
| [ch10](chapters/ch10-testing-the-database.md) | Testing the Database | migration-based delivery, test data life cycle, Object Mother |
| [ch11](chapters/ch11-unit-testing-anti-patterns.md) | Unit Testing Anti-patterns | private methods, code pollution, Ambient Context, time as dep |

## Topic Index

- **AAA / Arrange-Act-Assert** → ch03
- **Ambient Context / testing time** → ch11
- **Classical vs London school** → ch02
- **Code pollution** → ch11
- **Command Query Separation (CQS)** → ch05
- **Controllers / orchestration** → ch07, ch08
- **Coverage metrics** → ch01
- **Database testing** → ch10
- **Dependencies (shared/private/out-of-process)** → ch02, ch08
- **End-to-end tests** → ch02, ch08
- **Fail fast** → ch08
- **False positives / negatives** → ch04
- **Four pillars** → ch04
- **Functional architecture (core/shell)** → ch06
- **Hexagonal architecture** → ch05
- **Humble Object pattern** → ch07, ch11
- **Implementation details vs observable behavior** → ch05
- **Integration testing** → ch08, ch10
- **Managed vs unmanaged dependency** → ch08
- **Migration-based DB delivery** → ch10
- **Mock vs stub / test doubles** → ch02, ch05
- **Mocking best practices / spies** → ch09
- **Object Mother / Test Data Builder** → ch10
- **Output/state/communication styles** → ch06
- **Resistance to refactoring** → ch04, ch05
- **Sustainable growth (goal)** → ch01
- **Test fixtures** → ch03
- **Test Pyramid** → ch04, ch08
- **Types-of-code quadrant** → ch07
- **Unit of behavior** → ch02, ch03

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and patterns (AAA, functional architecture, Humble Object, mocking rules, DB testing)
- [cheatsheet.md](cheatsheet.md) — decision rules: what to mock, which style, the quadrant, test smells

---

## Scope & Limits

Covers the book's content only (C# / .NET examples; principles are language-agnostic). For hands-on test writing in your codebase, combine with project-specific test frameworks. For broader testing topics beyond this book, ask directly.
