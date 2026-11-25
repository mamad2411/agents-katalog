---
name: cwalina-framework-design
description: "Knowledge base from \"Framework Design Guidelines, 3rd Edition\" by Krzysztof Cwalina, Jeremy Barton & Brad Abrams. Use when applying their guidelines for designing .NET libraries/APIs — naming, type & member design, extensibility, exceptions, usage, async/Dispose/factory patterns, and breaking changes — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, guideline, pattern, or chapter number] -->

# Framework Design Guidelines (3rd Edition)
**Authors**: Krzysztof Cwalina, Jeremy Barton, Brad Abrams (+ .NET annotators) | **Pages**: ~626 | **Chapters**: 9 + Appendices A/D | **Generated**: 2026-07-03

## How to Use This Skill

- **Without arguments** — load the core guidelines below for reference.
- **With a topic** — ask about `naming`, `exceptions`, `async`, `Dispose`, `enums`, `Span`, `breaking changes`, etc.; I find and read the relevant chapter.
- **With a chapter** — ask for `ch05`; I load that specific chapter file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about a topic not covered below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**Guidelines are graded, not absolute.** Read every rule as one of: **DO** (always), **DO NOT** (never), **CONSIDER** (default; deviate with reason), **AVOID** (usually bad). They are guidelines because framework design is trade-offs.

**Scenario-Driven Design (the #1 principle).** Write the *client code* for the top 5–10 scenarios first, then design the object model to support it. Standard OO methodologies optimize implementation maintainability, not API usability — invert that. Scenarios ≈ end-user use cases.

**Pit of Success.** Make the most natural usage correct, secure, and fast; make misuse hard. Low barrier to entry (≤1 `new`, minimal init, good defaults, clear exceptions); self-documenting object models (reserve the best names for the most-used types; strong typing; optimize for IntelliSense); layered architecture (low-level power + high-level convenience).

**Consistency is the whole book's theme.** "You can always add; you cannot ever remove" — prefer cutting/deferring over shipping a wrong shape. Simplicity is a feature.

**Type design.** Favor **classes over interfaces** (interfaces are frozen once shipped; classes evolve without breaking subclasses). Most types = classes; structs only for small, immutable, single-value, rarely-boxed types. Decouple contract from impl with an **abstract class in a separate assembly**, not an interface. Enums: zero value (`None`), `[Flags]`+powers-of-2 for flags, no sentinels/reserved values.

**Member design.** Property = cheap data access; method = action / expensive / non-idempotent / side-effecting / returns-array. Overload short→long, only the longest virtual. All instance fields **private**. Prefer enums over bool params; descriptive types over tuples. Validate args high on the stack. Prefer strong typing.

**Extensibility ladder (cheapest→most powerful):** unsealed class → protected members → events/callbacks → virtual members → abstractions. Pick the cheapest that works — you can add extensibility later but never remove it. Public members non-virtual, routing to a `protected virtual XxxCore` (**Template Method**). Treat protected as public for security.

**Exceptions.** Throw for all failures; **never return error codes**. Usage error (caller bug) → existing framework exception + great message; program error → maybe custom; system failure → `Environment.FailFast`. Throw the most-derived type; don't swallow generic exceptions; prefer try-finally/`using`; empty `throw;` preserves the stack. Hot failing paths → Tester-Doer or Try (`bool Try...(out T)`).

**Key patterns.** Task-Based Async Pattern (`Async` suffix, `Task`/`ValueTask<T>`, trailing `CancellationToken`, `ConfigureAwait(false)` off UI); Basic Dispose Pattern (`Dispose()`→`Dispose(bool)`+`SuppressFinalize`, non-finalizable public types via `SafeHandle`); prefer constructors over factories; `Span<T>`/`ReadOnlySpan<T>` for buffers (`Memory<T>` for storage/async).

**Usage rules.** Public APIs return `Collection<T>`/`ReadOnlyCollection<T>`/interfaces — never `List<T>`/`Dictionary`. `DateTimeOffset` by default for points in time. Don't implement `ICloneable`. Implement `IEquatable<T>` on value types; override `Equals`+`GetHashCode` together. `Uri` not `string` for URLs.

**Breaking changes** (App. D): adding < changing < removing; names/identity (rename, class↔struct, seal, remove member) are ❌; adding members to concrete types, unsealing, `[TypeForwardedTo]` are ✅.

---

## Chapter Index

| # | Title | Key Topics |
|---|-------|-----------|
| [ch01](chapters/ch01-introduction.md) | Introduction | 7 qualities of a well-designed framework, consistency, trade-offs |
| [ch02](chapters/ch02-fundamentals.md) | Framework Design Fundamentals | scenario-driven design, Pit of Success, low barrier, layering |
| [ch03](chapters/ch03-naming.md) | Naming Guidelines | Pascal/camel casing, acronyms, type/member/namespace names |
| [ch04](chapters/ch04-type-design.md) | Type Design | class vs struct vs interface, enums, static classes, strongly typed strings |
| [ch05](chapters/ch05-member-design.md) | Member Design | overloading, property vs method, constructors, events, fields, operators, params |
| [ch06](chapters/ch06-extensibility.md) | Designing for Extensibility | unsealed/protected/events/virtual/abstractions, base classes, sealing |
| [ch07](chapters/ch07-exceptions.md) | Exceptions | throwing, standard types, custom exceptions, Tester-Doer, Try pattern |
| [ch08](chapters/ch08-usage.md) | Usage Guidelines | arrays, attributes, collections, DateTime, Equals/GetHashCode/ToString, Uri, Xml |
| [ch09](chapters/ch09-patterns.md) | Common Design Patterns | aggregate components, TAP async, Dispose, factories, LINQ, variance, Template Method, Span |
| [ch10](chapters/ch10-appendix-a-csharp-style.md) | Appendix A: C# Coding Style | braces, spacing, modifiers, `var`, naming, comments |
| [ch11](chapters/ch11-appendix-d-breaking-changes.md) | Appendix D: Breaking Changes | runtime/compile/recompile/reflection breaks, BCL acceptability |

## Topic Index

- **Abstractions / base classes** → ch04, ch06
- **Aggregate components / factored types** → ch09
- **Arrays** → ch08
- **Async / Task / CancellationToken / ValueTask** → ch09
- **Attributes** → ch08
- **Breaking changes** → ch11
- **Casing / capitalization** → ch03, ch10
- **Class vs. interface vs. struct** → ch04
- **Collections** → ch08
- **Constructors** → ch05
- **Covariance / contravariance** → ch09
- **DateTime / DateTimeOffset** → ch08
- **Dependency properties** → ch09
- **Dispose / IDisposable / finalizers** → ch08, ch09
- **Enums** → ch03, ch04
- **Equality / Equals / GetHashCode / operators** → ch05, ch08
- **Events** → ch03, ch05, ch06
- **Exceptions** → ch07
- **Extension methods** → ch05
- **Extensibility / sealing / virtual** → ch06
- **Factories** → ch09
- **Fields** → ch03, ch05
- **LINQ / IQueryable / Query Pattern** → ch09
- **Naming (assemblies, namespaces, types, members, params)** → ch03
- **Optional Feature Pattern** → ch09
- **Parameters / validation / passing** → ch05
- **Pit of Success / scenario-driven / layering** → ch02
- **Properties vs. methods** → ch05
- **Span / Memory / buffers** → ch09
- **Static classes** → ch04
- **Strongly typed strings** → ch04
- **Template Method** → ch06, ch09
- **Tester-Doer / Try pattern** → ch07
- **Timeouts** → ch09
- **Tuples** → ch05
- **Uri** → ch08
- **XAML** → ch09

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns (When/How/Trade-offs)
- [cheatsheet.md](cheatsheet.md) — decision rules and quick-reference tables

---

## Scope & Limits

This skill covers the book's guidelines for designing **.NET libraries/frameworks** (public API surface). It assumes C#/.NET knowledge and does not teach OOP or the CLR basics. For implementation in your codebase, combine with project-specific tools. Some legacy guidance (Classic/Event-Based async, serialization, obsolete naming) was moved to the book's Appendix B and is only summarized here.
