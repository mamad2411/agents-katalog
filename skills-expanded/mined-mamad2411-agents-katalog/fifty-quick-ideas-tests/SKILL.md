---
name: fifty-quick-ideas-tests
description: "Knowledge base from \"Fifty Quick Ideas to Improve Your Tests\" by Gojko Adzic, David Evans & Tom Roden. Use when applying their frameworks for test design, key examples, Given-When-Then, testability, async/UI test reliability, coverage, or managing large test suites; studying the book; or referencing its 50 ideas."
---

<!-- argument-hint: [topic, idea name, or chapter number] -->

# Fifty Quick Ideas to Improve Your Tests
**Author**: Gojko Adzic, David Evans & Tom Roden | **Pages**: ~215 | **Chapters**: 4 parts / 50 ideas | **Generated**: 2026-06-30

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference
- **With a topic** — ask about `key examples`, `given-when-then`, `business time`, `coverage targets`, `chaos monkey`; I find and read the relevant chapter
- **With a chapter** — ask for `ch03`; I load that part
- **Browse** — ask "what ideas do you have?" to see the index

When you ask about a topic not in Core Frameworks below, I'll read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

The book groups 50 ideas into 4 parts: **generate ideas → design checks → improve testability → manage the suite.** The most load-bearing ideas:

**Generating test ideas (Ch 1)**
- **Big-picture quality pyramid** — 5 Maslow-style levels (works at all / works well / usable / useful / successful). Quantify each with stakeholders.
- **Explore capabilities, not features** — feature-focused exploration causes tunnel vision; ask what a feature lets users *do* or *prevents*.
- **Always/never heuristic** — list absolutes, then refute them to expose hidden assumptions.
- **SHADED FIGS** — 9 emotional paths beyond happy: Scary, Happy, Angry, Delinquent, Embarrassing, Desolate, Forgetful, Indecisive, Greedy, Stressful.
- **ACC matrix** — Attribute × Component × Capability; stable, risk-scored test plan.
- **Quantify even if you can't measure**; **risk checklists** (5–9 key risks, not steps); **document trust boundaries**.

**Designing good checks (Ch 2)**
- **Focus on key examples** — a few simple examples at the right abstraction beat exhaustive scenario lists (≈40 examples vs 5⁷).
- **Contrast with counter-examples** — vary one input at a time; keep counter-examples close to positives.
- **Given-When-Then in strict sequence** — parameters in `Given`, *one* action in `When`, outcomes in `Then`. It's a design pattern (= Arrange-Act-Assert), not just automation syntax.
- **Describe what, not how** — keep mechanics out of acceptance criteria.
- **Flip equivalence classes** to outputs, not just inputs (validation, audit, alerts). **Write assertions first.** **One test, one topic.** **Treat too many boundaries as a modelling problem.** **Split technical & business checks** (who resolves a failure?).

**Improving testability (Ch 3)**
- **Wait for events, not time** — never `sleep(N)`; block on an event or sample.
- **Wrap sync DB tests in transactions** (roll back, set globally); **set up before async tests, don't clean up after**.
- **Introduce business time** — app clock decoupled from OS clock.
- **Provide atomic external resources** — appearance ⇒ readiness (temp-name → rename).
- **Minimise UI interactions** — pull set-up below the skin; **three-layer automation** (decisions / workflows / technical) when UI driving is unavoidable.
- **Use production metrics for expensive tests** — only ~⅓ of shipped ideas improve their target metric.

**Managing large test suites (Ch 4)**
- **Make developers responsible for checking** — whole team decides *what*, developers automate.
- **Decouple coverage from purpose** — independent dimensions; business-oriented unit tests are fine.
- **Avoid strict coverage targets** — coverage is a *negative* diagnostic; targets get gamed.
- **Organise by business activity, not work items**; **version-control tests with code**; **optimise for reading, not writing**; **name tests for SEO** (no conjunctions); **measure test half-life**; **let the chaos monkey out** (risk-driven mutation).

---

## Chapter Index

| # | Title | Key Ideas |
|---|-------|-----------|
| [ch01](chapters/ch01-generating-test-ideas.md) | Generating Test Ideas | quality pyramid, capabilities, always/never, SHADED FIGS, ACC matrix, risk checklists, trust boundaries, mob testing |
| [ch02](chapters/ch02-designing-good-checks.md) | Designing Good Checks | key examples, counter-examples, Given-When-Then, describe what-not-how, equivalence flip, write assertions first, one test one topic |
| [ch03](chapters/ch03-improving-testability.md) | Improving Testability | DB transactions, async set-up, business time, atomic resources, wait for events, minimise UI, three-layer automation, production metrics |
| [ch04](chapters/ch04-managing-large-test-suites.md) | Managing Large Test Suites | developers own checking, coverage vs purpose, no coverage targets, organise by activity, VCS, half-life, SEO names, chaos monkey |

## Topic Index

- **ACC matrix** → ch01, ch04
- **Acceptance criteria** → ch02
- **Always/never** → ch01
- **Asynchronous testing** → ch02, ch03
- **Atomic resources** → ch03
- **Business time** → ch03
- **Capabilities** → ch01
- **Chaos monkey / mutation** → ch04
- **Counter-examples** → ch02
- **Coverage (targets, diagnostic)** → ch04
- **Cross-team test design** → ch04
- **Database tests** → ch03
- **Describe what, not how** → ch02
- **Equivalence classes** → ch02
- **Exploratory testing** → ch01, ch04
- **Given-When-Then** → ch02
- **Half-life of tests** → ch04
- **Key examples** → ch02
- **Mob testing** → ch01
- **Naming tests** → ch04
- **Production metrics** → ch01, ch03
- **Quality pyramid** → ch01
- **Risk checklists** → ch01
- **SHADED FIGS** → ch01
- **Tables (prefer smaller)** → ch02
- **Three-layer automation** → ch03
- **Trust boundaries** → ch01
- **UI test minimisation** → ch03
- **Version control of tests** → ch04
- **Wait for events not time** → ch03
- **Write assertions first** → ch02

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all 50 techniques as When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, tells & smells, quick fixes

---

## Scope & Limits

Covers the book only. It assumes you know testing basics (exploratory testing, automation, unit vs integration) — it's about *improving* testing, not setting it up. For hands-on implementation in your codebase, combine with project tools and unit-testing skills (e.g. [[khorikov-unit-testing]], [[art-of-unit-testing]], [[specification-by-example]]).
