---
name: specification-by-example
description: "Knowledge base from \"Specification by Example: How Successful Teams Deliver the Right Software\" by Gojko Adzic. Use when applying Adzic's process patterns for executable specifications, living documentation, acceptance testing, BDD/ATDD, deriving scope from goals, specification workshops, or referencing the book."
---

<!-- argument-hint: [topic, pattern name, or chapter number] -->

# Specification by Example
**Author**: Gojko Adzic (Manning, 2011) | **Pages**: ~295 | **Chapters**: 18 (in 12 files) | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load the core process patterns below for reference
- **With a topic** — ask about `specification workshops`, `living documentation`, `automation layer`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch07`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not in Core Patterns below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### The central idea
**Specification by Example (SBE)** — capture requirements as concrete, realistic **examples** that both describe and verify the system. Collaborate to derive them, automate them into **executable specifications**, validate them frequently, and keep them as a single source of truth: **living documentation**. One artifact does three jobs — spec, test, and documentation. The umbrella over Agile Acceptance Testing, ATDD, BDD, and Example-Driven Development.

### The four key benefits (Ch 1) — why teams adopt it
1. **Implementing changes more efficiently** — shared understanding cuts rework loops.
2. **Higher product quality** — examples expose gaps/ambiguity *before* coding.
3. **Less rework** — build the *right* thing once, not the thing built right twice.
4. **Better work alignment** — everyone (business, dev, test) works off the same examples.

### The 7 key process patterns (Ch 2 → chapters 5–11) — the method's spine
Run these as a cycle, not a waterfall:
1. **Deriving scope from goals** (Ch 5) — start from the business *goal* and *who* benefits; let the team propose scope. Spec the *why*, not the solution. → "Ask how something would be useful", "Ask for an alternative solution".
2. **Specifying collaboratively** (Ch 6) — build specs together, not handed down. Pick a model by team maturity/domain: **big all-team workshops** (starting out) → **Three Amigos** small workshops → **pair-writing** (mature) → **informal conversations**.
3. **Illustrating using examples** (Ch 7) — good examples are **precise, complete, realistic, easy to understand**. Use *real* customer data; avoid invented/abstract equivalence classes; don't explore every combinatorial case.
4. **Refining the specification** (Ch 8) — turn raw examples into a focused, self-explanatory spec. **Scripts are not specifications.** Use a descriptive title + short goal paragraph; **Given-When-Then**; push setup defaults into the automation layer; keep it in **domain language**, decoupled from UI/code.
5. **Automating validation without changing specifications** (Ch 9) — three layers: **specification (business language) → automation layer (glue/fixtures) → system under test**. The spec never bends to the tool. Don't replicate business logic in the automation layer; automate **below the skin of the application**, along system boundaries — not through the UI.
6. **Validating frequently** (Ch 10) — run executable specs continuously so documentation stays *alive*. Fight unreliability: "Find the most annoying thing, fix it, repeat"; dedicated CI validation env; **wait for events, not elapsed time**; separate quick vs slow packs.
7. **Evolving a documentation system** (Ch 11) — keep living docs **easy to understand, consistent, organized for access**. Organize by stories → functional areas; evolve a ubiquitous language; **listen to your living documentation** (pain in the docs signals design pain).

### Living documentation (Ch 3) — the long-term payoff
Documentation derived from continuously-validated executable specs is **authoritative** (can't drift — it fails the build if it lies) and **cheap to maintain**. This is what makes SBE pay off long after the project, distinguishing it from plain ATDD/BDD.

### Key distinctions to keep exact
- **Goal vs scope vs solution** — derive scope from goals; don't accept solutions disguised as requirements.
- **Key example** — the minimal set of illustrative examples that pins down a rule (not exhaustive combinations).
- **Executable specification** — a spec a machine can run as a test, written in business language.
- **Specification workshop / "Three Amigos"** — business + dev + tester refine examples together.
- **Boomerang / shotgun surgery / just-in-case code** — adoption warning signs (Ch 4).

---

## Chapter Index

| # | Title | Key Patterns |
|---|-------|--------------|
| [ch01](chapters/ch01-key-benefits.md) | Key benefits | Four key benefits, right-product vs product-right |
| [ch02](chapters/ch02-key-process-patterns.md) | Key process patterns | The 7 patterns, free-delivery example |
| [ch03](chapters/ch03-living-documentation.md) | Living documentation | Documentation-centric model, executable specs as docs |
| [ch04](chapters/ch04-initiating-the-changes.md) | Initiating the changes | Adoption patterns, sign-off/traceability, warning signs |
| [ch05](chapters/ch05-deriving-scope-from-goals.md) | Deriving scope from goals | Goal→scope, ask-how-useful, alternative solution |
| [ch06](chapters/ch06-specifying-collaboratively.md) | Specifying collaboratively | Workshops, Three Amigos, pair-writing, prep patterns |
| [ch07](chapters/ch07-illustrating-using-examples.md) | Illustrating using examples | Precise/complete/realistic/clear, QUPER, nonfunctional |
| [ch08](chapters/ch08-refining-the-specification.md) | Refining the specification | Given-When-Then, scripts≠specs, domain language |
| [ch09](chapters/ch09-automating-validation.md) | Automating validation | Three-layer model, below-the-skin, automation layer |
| [ch10](chapters/ch10-validating-frequently.md) | Validating frequently | Reliability, faster feedback, managing failing tests |
| [ch11](chapters/ch11-evolving-documentation-system.md) | Evolving a documentation system | Understandable/consistent/organized, ubiquitous language |
| [ch12](chapters/ch12-case-studies.md) | Case studies & concluding thoughts | uSwitch, RainStor, Iowa, Sabre, ePlan, Songkick |

## Topic Index

- **Acceptance testing / ATDD / BDD** → ch01, ch02, ch03
- **Adoption / change management** → ch04
- **Automation layer / fixtures** → ch09
- **Below the skin of the application** → ch09
- **Case studies** → ch12
- **Collaboration models** → ch06
- **Continuous validation / CI** → ch10
- **Deriving scope from goals** → ch05
- **Domain language / ubiquitous language** → ch08, ch11
- **Examples (qualities of good)** → ch07
- **Executable specifications** → ch02, ch03, ch09
- **Given-When-Then** → ch08
- **Key examples** → ch02, ch07
- **Living documentation** → ch03, ch11, ch12
- **Nonfunctional requirements / QUPER** → ch07
- **Refining specifications** → ch08
- **Sign-off & traceability** → ch04
- **Specification workshops / Three Amigos** → ch06
- **Test reliability / flaky tests** → ch10
- **User interface testing** → ch09
- **Warning signs (boomerang, shotgun surgery)** → ch04

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all named process patterns with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, tells, and quick-reference tables

---

## Scope & Limits

Covers the book's process patterns and case studies only. The book is tool-agnostic — for a specific tool (Cucumber, FitNesse, SpecFlow, Concordion), combine with that tool's docs. For hands-on automation in your codebase, pair with project-specific testing skills.
