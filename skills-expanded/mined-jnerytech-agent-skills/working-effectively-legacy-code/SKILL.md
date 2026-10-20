---
name: working-effectively-legacy-code
description: "Knowledge base from \"Working Effectively with Legacy Code\" by Michael C. Feathers. Use when changing untested code safely — seams, characterization tests, breaking dependencies, getting classes into a test harness, taming monster methods — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, technique name, or chapter number] -->

# Working Effectively with Legacy Code
**Author**: Michael C. Feathers | **Pages**: ~458 | **Chapters**: 25 | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `seams`, `characterization tests`, `monster methods`, `singletons in tests`; I find and read the relevant chapter.
- **With a technique** — name any of the 24 dependency-breaking techniques (e.g. `Extract Interface`, `Subclass and Override Method`); see ch25.
- **With a chapter** — ask for `ch13`; I load that file.
- **Browse** — ask "what chapters do you have?" for the index.

When you ask about something not in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**Legacy code = code without tests.** However well-written, untested code can't be changed with confidence. The whole book is about getting code under test so you can change it safely.

**The Legacy Code Change Algorithm** — the spine of the book; run it for every change:
1. **Identify change points** → 2. **Find test points** → 3. **Break dependencies** → 4. **Write tests** → 5. **Make changes and refactor.**
Each programming episode delivers a feature *and* its tests; tested areas grow like "islands rising out of the ocean."

**Cover and Modify, not Edit and Pray** — change software under a safety net of tests (a *software vise* that fixes behavior in place), not by careful editing and hoping. Care ≠ safety.

**Seam + Enabling Point** *(the central idea, Ch 4)* — a **seam** is a place where you can alter behavior **without editing in that place**; its **enabling point** is where you choose which behavior runs. Three seam types: **object** (preferred in OO), **link**, **preprocessing**. Find seams by asking "where can I change this behavior without editing here?"

**Sensing vs Separation** *(Ch 3)* — the only two reasons to break a dependency: **sensing** (you can't *see* an effect → use a **Fake/Mock**) and **separation** (you can't *run* the code at all → inject via an extracted interface).

**Characterization Test** *(Ch 13)* — the key legacy testing move: a test that documents the code's **actual current behavior**, not its intended behavior. Algorithm: assert a guessed value → let the failure reveal the real behavior → change the assertion to match → repeat. Before "fixing" surprising behavior, check who depends on it.

**Unit test discipline** *(Ch 2)* — must run fast and localize errors. NOT a unit test if it hits a DB, network, filesystem, or needs special env setup.

**Feature-addition techniques** *(Ch 6, 8)* — when you can't get the class under test in time, write new behavior as fresh tested code and call it:
- **Sprout Method / Sprout Class** — new tested code called from untested code.
- **Wrap Method / Wrap Class** — add behavior before/after existing work without growing it (Decorator when many callers).
- **TDD**: failing test → compile → pass → remove duplication. **Programming by Difference**: subclass to add fast, then refactor the inheritance away.

**Safety without tests** *(Ch 23)* — **Lean on the Compiler** (break a declaration on purpose, fix every error it lists), **Preserve Signatures** (copy parameter lists verbatim), **Single-Goal** and **Hyperaware Editing**.

**Design principles invoked**: Single Responsibility (Ch 20), Open/Closed (Ch 21), Dependency Inversion (Ch 7), Liskov Substitution (Ch 8).

**Choosing a dependency-breaking technique** — match the obstacle to the seam available; full catalog of 24 techniques with steps + trade-offs in [ch25](chapters/ch25-dependency-breaking-techniques.md). Most-used: **Extract Interface**, **Subclass and Override Method**, **Parameterize Constructor**, **Extract and Override Factory Method / Getter / Call**, **Introduce Static Setter**.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-changing-software.md) | Changing Software | Four Reasons to Change, behavioral change |
| [ch02](chapters/ch02-working-with-feedback.md) | Working with Feedback | Legacy Code Change Algorithm, software vise, unit test |
| [ch03](chapters/ch03-sensing-and-separation.md) | Sensing and Separation | Sensing vs Separation, Fake/Mock objects |
| [ch04](chapters/ch04-the-seam-model.md) | The Seam Model | Seam, enabling point, seam types |
| [ch05](chapters/ch05-tools.md) | Tools | xUnit, FIT/FitNesse, refactoring/mock tools |
| [ch06](chapters/ch06-i-dont-have-much-time.md) | I Don't Have Much Time | Sprout/Wrap Method & Class |
| [ch07](chapters/ch07-it-takes-forever-to-make-a-change.md) | It Takes Forever to Make a Change | Dependency Inversion, Extract Interface, build time |
| [ch08](chapters/ch08-how-do-i-add-a-feature.md) | How Do I Add a Feature? | TDD, Programming by Difference, LSP |
| [ch09](chapters/ch09-cant-get-class-into-test-harness.md) | I Can't Get This Class into a Test Harness | Constructor/global obstacles → techniques |
| [ch10](chapters/ch10-cant-run-method-in-test-harness.md) | I Can't Run This Method in a Test Harness | Subclass and Override, Extract and Override Call |
| [ch11](chapters/ch11-what-methods-should-i-test.md) | What Methods Should I Test? | Effect sketch, interception/pinch point |
| [ch12](chapters/ch12-many-changes-in-one-area.md) | Many Changes in One Area | Pinch point, higher-level tests |
| [ch13](chapters/ch13-dont-know-what-tests-to-write.md) | I Don't Know What Tests to Write | Characterization Tests |
| [ch14](chapters/ch14-dependencies-on-libraries.md) | Dependencies on Libraries | Skin and Wrap, Responsibility-Based Extraction |
| [ch15](chapters/ch15-application-is-all-api-calls.md) | My Application Is All API Calls | Skin and Wrap vs Responsibility-Based Extraction |
| [ch16](chapters/ch16-dont-understand-the-code.md) | I Don't Understand the Code | Scratch Refactoring, Listing Markup |
| [ch17](chapters/ch17-application-has-no-structure.md) | My Application Has No Structure | Telling the Story, Naked CRC |
| [ch18](chapters/ch18-test-code-is-in-the-way.md) | My Test Code Is in the Way | Test naming/placement conventions |
| [ch19](chapters/ch19-not-object-oriented.md) | My Project Is Not Object Oriented | Link/preprocessing seams in C |
| [ch20](chapters/ch20-class-is-too-big.md) | This Class Is Too Big | SRP, Extract Class, responsibility heuristics |
| [ch21](chapters/ch21-changing-same-code-all-over.md) | Changing the Same Code All Over | Remove duplication, Open/Closed |
| [ch22](chapters/ch22-monster-method.md) | I Need to Change a Monster Method | Bulleted/Snarled, Break Out Method Object |
| [ch23](chapters/ch23-not-breaking-anything.md) | How Do I Know I'm Not Breaking Anything? | Lean on the Compiler, Preserve Signatures |
| [ch24](chapters/ch24-we-feel-overwhelmed.md) | We Feel Overwhelmed | Incremental strategy, morale |
| [ch25](chapters/ch25-dependency-breaking-techniques.md) | Dependency-Breaking Techniques | **Catalog of 24 techniques** |

## Topic Index

- **Characterization test** → ch13
- **Dependency breaking (catalog)** → ch25, ch09, ch10
- **Duplication / Open-Closed** → ch21
- **Effect sketch / pinch point** → ch11, ch12
- **Fakes / Mocks** → ch03
- **Feature addition (Sprout/Wrap)** → ch06, ch08
- **God class / SRP / Extract Class** → ch20
- **Globals / Singletons in tests** → ch09, ch25
- **Lean on the Compiler / safe edits** → ch23
- **Legacy Code Change Algorithm** → ch02
- **Library & API dependencies** → ch14, ch15
- **Monster methods** → ch22
- **Non-OO / C dependency breaking** → ch19, ch25
- **Seams & enabling points** → ch04, ch19
- **Sensing vs separation** → ch03
- **Slow builds / Dependency Inversion** → ch07
- **TDD / Programming by Difference** → ch08
- **Tools (xUnit, FIT)** → ch05
- **Understanding unfamiliar code** → ch16, ch17
- **Unit test definition** → ch02

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — every technique, indexed by problem
- [cheatsheet.md](cheatsheet.md) — decision rules, seam/technique selection, smells

---

## Scope & Limits

Covers the book's content (Java/C++/C-era examples; principles are language-agnostic). For applying these to your codebase, combine with project tools and a test runner. The dependency-breaking catalog (ch25) is the reference the rest of the book points to.
