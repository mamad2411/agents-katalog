---
name: dive-into-refactoring
description: "Knowledge base from \"Dive Into Refactoring\" by Alexander Shvets (Refactoring.Guru). Use when identifying code smells, choosing a refactoring technique, applying Extract Method / Move Method / Replace Conditional with Polymorphism / type-code refactorings, studying the book, or referencing its concepts."
---

<!-- argument-hint: [smell name, refactoring name, or chapter number] -->

# Dive Into Refactoring
**Author**: Alexander Shvets (Refactoring.Guru) | **Pages**: ~336 | **Chapters**: 11 (grouped) | **Generated**: 2026-07-04

## How to Use This Skill

- **Without arguments** — load the smell→refactoring map and core mental models below
- **With a smell** — ask about `Feature Envy`, `Primitive Obsession`, etc.; I find and read the covering chapter
- **With a refactoring** — ask about `Extract Method`, `Replace Type Code with Subclasses`, etc.
- **With a chapter** — ask for `ch08`; I load that file
- **Browse** — ask "what chapters do you have?"

When you ask about something not in Core below, I read the relevant chapter file first.

---

## Core Frameworks & Mental Models

**The book has two halves:** Part 1 = **Code Smells** (how to *recognize* dirty code, Ch 1–5), Part 2 = **Refactoring Techniques** (how to *fix* it, Ch 6–11). Every smell links to specific refactorings; every refactoring lists which smells it eliminates.

### The 5 smell families (Ch 1–5)
- **Bloaters** — Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps.
- **OO Abusers** — Switch Statements, Temporary Field, Refused Bequest, Alternative Classes w/ Different Interfaces.
- **Change Preventers** — Divergent Change (one class, many reasons to change) vs Shotgun Surgery (one change, many classes); Parallel Inheritance Hierarchies.
- **Dispensables** — Comments, Duplicate Code, Lazy Class, Data Class, Dead Code, Speculative Generality.
- **Couplers** — Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man (+ Incomplete Library Class).

### The 6 refactoring families (Ch 6–11)
- **Composing Methods** — Extract/Inline Method, Extract Variable, Replace Temp with Query, Replace Method with Method Object, Substitute Algorithm.
- **Moving Features** — Move Method/Field, Extract/Inline Class, Hide Delegate/Remove Middle Man, Introduce Foreign Method/Local Extension.
- **Organizing Data** — Self/Encapsulate Field, Encapsulate Collection, Replace Data Value/Array with Object, Change Value⇄Reference, Replace Type Code with Class/Subclasses/State-Strategy, Replace Magic Number.
- **Simplifying Conditionals** — Decompose/Consolidate Conditional, Guard Clauses, Replace Conditional with Polymorphism, Introduce Null Object/Assertion.
- **Simplifying Method Calls** — Rename/Add/Remove Parameter, Separate Query from Modifier, Preserve Whole Object, Introduce Parameter Object, Replace Constructor with Factory Method, Replace Error Code with Exception.
- **Dealing with Generalization** — Pull Up/Push Down, Extract Subclass/Superclass/Interface, Collapse Hierarchy, Form Template Method, Replace Inheritance⇄Delegation.

### Highest-leverage rules
- **Extract Method is the gateway** — most refactorings start with it. If you'd comment inside a method, extract+name instead.
- **See `switch` on a type → think polymorphism.** Type code decision: no behavior → *Class*; behavior + immutable → *Subclasses*; behavior + runtime-changing → *State/Strategy*.
- **Fight Long Parameter Lists with objects**, not more primitives (Preserve Whole Object / Introduce Parameter Object).
- **Feature Envy → move behavior to its data** ("things that change together belong together").
- **Guard clauses** flatten nested conditionals; **Tell-Don't-Ask** replaces type-branching with polymorphism.
- **Pull up to share, push down to specialize.** Prefer **delegation** for flexibility/Liskov, **inheritance** only when delegating to *all* methods.
- Many refactorings come in **inverse pairs** (anti-refactorings) — pick the direction the structure needs and reverse later.
- Refactoring **changes structure, not behavior** — lean on tests; step small; each smell entry has "When to Ignore" cases.

---

## Chapter Index

| # | Title | Key Content |
|---|-------|----------------|
| [ch01](chapters/ch01-bloaters.md) | Bloaters (smells) | Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps |
| [ch02](chapters/ch02-oo-abusers.md) | OO Abusers (smells) | Switch Statements, Temporary Field, Refused Bequest, Alternative Classes |
| [ch03](chapters/ch03-change-preventers.md) | Change Preventers (smells) | Divergent Change, Shotgun Surgery, Parallel Inheritance Hierarchies |
| [ch04](chapters/ch04-dispensables.md) | Dispensables (smells) | Comments, Duplicate Code, Lazy/Data/Dead Code, Speculative Generality |
| [ch05](chapters/ch05-couplers.md) | Couplers (smells) | Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man |
| [ch06](chapters/ch06-composing-methods.md) | Composing Methods | Extract/Inline Method, Replace Temp with Query, Method Object, Substitute Algorithm |
| [ch07](chapters/ch07-moving-features.md) | Moving Features | Move Method/Field, Extract/Inline Class, Hide Delegate, Foreign Method/Local Extension |
| [ch08](chapters/ch08-organizing-data.md) | Organizing Data | Encapsulate Field/Collection, Type Code refactorings, Value⇄Reference, Magic Number |
| [ch09](chapters/ch09-simplifying-conditionals.md) | Simplifying Conditionals | Guard Clauses, Replace Conditional with Polymorphism, Null Object, Assertion |
| [ch10](chapters/ch10-simplifying-method-calls.md) | Simplifying Method Calls | Rename/Add/Remove Param, Separate Query from Modifier, Parameter Object, Factory Method, Exceptions |
| [ch11](chapters/ch11-dealing-with-generalization.md) | Dealing with Generalization | Pull Up/Push Down, Extract Subclass/Superclass/Interface, Template Method, Inheritance⇄Delegation |

## Topic Index

- **Data Class / anemic model** → ch04, ch08
- **Delegation vs inheritance** → ch05, ch11
- **Duplicate Code** → ch04, ch06, ch11
- **Encapsulation** → ch08
- **Extract Method** → ch06 (feeds ch01, ch09, ch10)
- **Factory Method** → ch08, ch10
- **Feature Envy / Move Method** → ch05, ch07
- **Guard Clauses / nested conditionals** → ch09
- **Long Method / Long Parameter List** → ch01, ch06, ch10
- **Null Object** → ch09
- **Parameter Object / Preserve Whole Object** → ch01, ch10
- **Polymorphism (Replace Conditional)** → ch02, ch08, ch09
- **Primitive Obsession** → ch01, ch08
- **Reference vs Value** → ch08
- **Shotgun Surgery / Divergent Change** → ch03, ch07
- **Switch Statements** → ch02, ch08, ch09
- **Template Method** → ch11
- **Type Code (Class/Subclasses/State-Strategy)** → ch08 (+ ch02, ch09)

## Supporting Files

- [glossary.md](glossary.md) — all smells, refactorings, and principles defined
- [patterns.md](patterns.md) — every refactoring with When / How / Trade-off
- [cheatsheet.md](cheatsheet.md) — smell→fix table, decision trees, inverse pairs, triggers

---

## Scope & Limits

Covers the Java edition of *Dive Into Refactoring* — smell catalog + refactoring catalog. Companion to design patterns (Shvets' *Dive Into Design Patterns* / the `dive-into-design-patterns` skill) and Fowler's *Refactoring* (`fowler-refactoring` skill), which shares much of the same catalog with deeper mechanics. For applying refactorings in a real codebase, pair with tests and project tooling.
