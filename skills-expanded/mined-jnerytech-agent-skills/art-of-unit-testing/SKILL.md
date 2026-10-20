---
name: art-of-unit-testing
description: "Knowledge base from \"The Art of Unit Testing, Third Edition — with examples in JavaScript\" by Roy Osherove. Use when applying Osherove's frameworks for unit tests, stubs vs mocks, isolation frameworks, dependency injection, trustworthy/maintainable/readable tests, TDD, testing strategy, async testing, or legacy code — studying the book or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# The Art of Unit Testing (3rd ed, JavaScript)
**Author**: Roy Osherove | **Pages**: ~289 | **Chapters**: 12 + appendix | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load core frameworks below for reference.
- **With a topic** — ask about `mocks vs stubs`, `dependency injection`, `flaky tests`, `testing strategy`, etc.; I find and read the relevant chapter.
- **With a chapter** — ask for `ch05`; I load that file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**Unit of work, entry point, exit point** (Ch 1) — the foundational model. A *unit of work* is everything that runs between an *entry point* (the public thing your test calls) and its resulting *exit point(s)*. A good test invokes one entry point and checks one exit point.

**The three exit-point types** (Ch 1, Ch 4) — every result is one of:
1. **Return value** → assert the value (value-based test).
2. **State change** → call the SUT, then query state via another entry point (state-based test).
3. **Call to a third party you don't control** → inject a **mock** and assert on the call (interaction test).
Pick the test style from the exit-point type. Use interaction (mock) tests **only** for type 3.

**Stub vs Mock** (Ch 3–4) — a **stub** feeds the SUT canned inputs and you **never assert on it**; a **mock** stands in for a third-party exit point and you **do assert on it**. Rule: many stubs per test OK; **at most one mock per test**. Keep interaction tests to ~2–5% of the suite.

**Arrange-Act-Assert (AAA)** (Ch 2) — structure every test: arrange state, act on one entry point, assert one exit point. More than one Act or unrelated Asserts → split.

**USE naming** (Ch 2, Ch 9) — a test name states **U**nit under test, **S**cenario, **E**xpectation (`verifyPassword_withNoNumbers_returnsFalse`). It's the only clue in a failed CI log.

**Dependency injection = control** (Ch 3) — break dependencies so the *test*, not production wiring, decides behavior. Pick the seam by code style: **parameter injection** (simple values like time), **functional/partial-application** (JS), **constructor/object injection** (OO), **modular injection** (fragile, last-ish resort), **monkey-patching** (true last resort, Appendix). Prefer the cleanest seam available.

**Isolation frameworks** (Ch 5) — Osherove insists on "isolation," not "mocking," framework. Jest is the loose flavor (`jest.fn`, `jest.spyOn`, `jest.mock`, `mockReturnValue`/`mockImplementation`); substitute.js is the typed flavor. Powerful but easy to overspecify — reach for them when handwritten fakes get tedious.

**The three pillars of a good test** (Ch 7–9) — every test should be:
1. **Trustworthy** — green means works, red means broken: no logic in the test, no flakiness, real asserts. *Test the test* by breaking prod once.
2. **Maintainable** — fails only when behavior truly changes. Metric: count **false failures**. Avoid overspecification, private-method tests, brittle exact-string asserts.
3. **Readable** — explains itself: USE name, AAA layout, no magic values, clear assert messages.

**Testing the test** (Ch 7) — after a test goes green, deliberately break the production code; if it stays green it's worthless. Single cheapest trust check.

**Flaky tests: fix → convert → kill** (Ch 7) — fix root cause; else convert to an integration test; else quarantine/delete. Never leave a flaky test in the green build.

**Test recipe & levels** (Ch 10) — choose levels per feature with a *test recipe*. Prefer many fast unit tests, few slow E2E (~1 high-level per ~5 lower-level). Avoid both the E2E-only and unit-only antipatterns. Split **delivery-blocking** from **discovery** pipelines.

**TDD = Red-Green-Refactor** (Ch 1) — failing test → simplest pass → refactor both prod and test. The three core skills: write a good test, write it test-first, design well. TDD is *not* a substitute for writing good tests.

**Legacy = code without tests** (Ch 12) — prioritize components by logic complexity × dependencies × priority. Inexperienced team → easy-first (build confidence); experienced → hard-first (unblock system). Wrap in integration tests *before* refactoring to break dependencies.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-getting-started.md) | Getting started | unit of work, entry/exit points, exit-point types, unit-test checklist, TDD |
| [ch02](chapters/ch02-a-first-unit-test.md) | A first unit test | Jest, AAA, USE naming, factory vs beforeEach, parameterized tests |
| [ch03](chapters/ch03-breaking-dependencies-with-stubs.md) | Breaking dependencies with stubs | incoming/outgoing deps, injection styles, seams, IoC |
| [ch04](chapters/ch04-interaction-testing-mocks.md) | Interaction testing using mock objects | mock vs stub, mock = exit point, overspecification, Extract & Override |
| [ch05](chapters/ch05-isolation-frameworks.md) | Isolation frameworks | jest.fn/mock/spyOn, loose vs typed, substitute.js |
| [ch06](chapters/ch06-async-code.md) | Unit testing asynchronous code | Extract Entry Point, Extract Adapter, fake timers |
| [ch07](chapters/ch07-trustworthy-tests.md) | Trustworthy tests | three pillars, testing the test, flaky fix/convert/kill, no logic |
| [ch08](chapters/ch08-maintainability.md) | Maintainability | false failures, overspecification, DRY vs DAMP, factory setup |
| [ch09](chapters/ch09-readability.md) | Readability | USE naming, magic values, separate asserts from actions, tests as docs |
| [ch10](chapters/ch10-testing-strategy.md) | Developing a testing strategy | test levels, test recipe, delivery vs discovery pipelines |
| [ch11](chapters/ch11-integrating-into-organization.md) | Integrating unit testing into the organization | agent of change, buy-in, guerrilla adoption, metrics |
| [ch12](chapters/ch12-legacy-code.md) | Working with legacy code | test-feasibility table, easy/hard-first, integration safety net |
| [ch13](chapters/ch13-appendix-monkey-patching.md) | Appendix: Monkey-patching functions and modules | monkey-patching, spyOn + restore, last-resort seam |

## Topic Index

- **AAA / Arrange-Act-Assert** → ch02
- **Agent of change / adoption** → ch11
- **Async / promises / fetch** → ch06
- **Constructor injection** → ch03
- **Dependency injection** → ch03, ch04
- **Entry / exit points** → ch01, ch04
- **Exit-point types (return/state/third-party)** → ch01, ch04
- **Factory functions / setup** → ch02, ch08
- **Fake timers** → ch06
- **Flaky tests** → ch03, ch07
- **Integration tests** → ch01, ch10, ch12
- **Isolation frameworks (Jest)** → ch05
- **Legacy code** → ch12
- **Maintainability** → ch08
- **Mock objects / interaction testing** → ch04
- **Monkey-patching** → ch13
- **Overspecification** → ch04, ch08
- **Parameterized tests** → ch02, ch08
- **Readability / naming** → ch09, ch02
- **Stubs** → ch03
- **TDD** → ch01
- **Test levels / strategy / recipe** → ch10
- **Three pillars** → ch07, ch08, ch09
- **Trustworthy tests / testing the test** → ch07
- **Unit of work** → ch01
- **USE naming** → ch02, ch09

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — every technique with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, smells, level & injection tables

---

## Scope & Limits

Covers the book's content only (Jest-based JS examples). For applying these in your codebase, combine with project test tooling. Related skills in this repo: `khorikov-unit-testing` (four pillars, mocks vs stubs), `working-effectively-legacy-code` (seams, characterization tests), `reengineering-legacy-software`.
