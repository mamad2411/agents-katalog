---
name: dependency-injection-principles
description: "Knowledge base from \"Dependency Injection Principles, Practices, and Patterns\" by Steven van Deursen & Mark Seemann. Use when applying their frameworks for Dependency Injection, DI patterns/anti-patterns, Composition Root, object lifetime/lifestyles, interception, SOLID/AOP, and DI Containers (Autofac, Simple Injector, MS.DI), studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, pattern/anti-pattern name, or chapter number] -->

# Dependency Injection Principles, Practices, and Patterns
**Author**: Steven van Deursen & Mark Seemann | **Pages**: ~562 | **Chapters**: 15 | **Generated**: 2026-07-03

## How to Use This Skill

- **Without arguments** — load the core DI patterns, anti-patterns, and principles below
- **With a topic** — ask about `lifestyles`, `service locator`, `composition root`, `decorator`; I find and read the relevant chapter
- **With chapter** — ask for `ch05`; I load that specific chapter file
- **Browse** — ask "what chapters do you have?" for the full index

When you ask about a topic not covered in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**What DI actually is.** Dependency Injection = supplying a class's **Volatile Dependencies** from the outside instead of creating them internally. It is NOT about containers — a container is optional tooling. The purpose is **maintainability** through loose coupling.

**Volatile vs Stable Dependency (the inject-or-not test).** Inject a dependency only if it is *Volatile*: it touches an external resource, is nondeterministic/has side effects, must be swappable, or doesn't exist yet. *Stable* dependencies (`string`, `List<T>`, pure value types) should be `new`ed directly. Injecting stable deps is noise.

**Composition Root.** Compose the entire object graph in **one** place, as close to the entry point as possible (`Main`, `Startup.ConfigureServices`, platform bootstrapper). It is the *only* place that references concrete types or the DI Container. Composing anywhere else leaks coupling.

**The four DI patterns** (Ch 4):
- **Constructor Injection** — the default. Required, static deps → single public constructor → `readonly` fields. The constructor is a compile-time contract of what the class needs.
- **Method Injection** — a per-call value/dependency passed as a method parameter.
- **Property Injection** — an *optional* dependency with a safe **Local Default**. Use sparingly.
- **Composition Root** — where all of the above get wired.
Decision rule: *"When in doubt, Constructor Injection."*

**The four DI anti-patterns** (Ch 5) — recognize and kill:
- **Control Freak** — most common: `new`ing a volatile dependency instead of injecting it.
- **Service Locator** — asking a container/registry for deps at runtime; hides dependencies and couples to the locator.
- **Ambient Context** — reaching a dependency through a static accessor (`DateTime.Now`, static logger).
- **Constrained Construction** — forcing every implementation to share a specific constructor signature.

**Code smells** (Ch 6): **Constructor Over-injection** (>~4 ctor deps ⇒ SRP breach ⇒ extract **Facade Services**); Abuse of Abstract Factories; cyclic dependencies (redesign, don't patch).

**Lifestyles / object lifetime** (Ch 8): **Singleton** (one per container — must be thread-safe), **Scoped** (one per request/scope), **Transient** (one per resolve). **Captive Dependency** is the cardinal sin: never inject a shorter-lived dependency (Scoped/Transient) into a longer-lived one (Singleton) — it outlives its scope.

**Interception & AOP** (Ch 9–11): apply Cross-Cutting Concerns (logging, caching, security, retry) with the **Decorator** pattern — "AOP by design". This honors the **Open/Closed Principle**. Prefer decorators over **tool-based AOP** (dynamic proxies / compile-time weaving), which obscures control flow and adds tool lock-in. **SOLID** (esp. SRP, OCP, DIP) is the driver that makes code decoratable.

**Pure DI vs DI Container** (Ch 12): **Pure DI** = hand-wiring with `new` (formerly "Poor Man's DI") — compile-time safe, debuggable, best for small/medium graphs. Adopt a **DI Container** (Register-Resolve-Release, Auto-Registration) when hand-wiring costs more than the magic it hides. **Resolve only in the Composition Root** — resolving elsewhere is Service Locator.

**Prefer**: loose coupling over convenience · Constructor Injection over Property/Method · design-based AOP over tool-based · Pure DI until a container earns its place · abstractions owned by the consumer (DIP).

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-basics-of-di.md) | The basics of Dependency Injection | Volatile/Stable Dependency, Composition Root, Pure DI |
| [ch02](chapters/ch02-tightly-coupled-code.md) | Writing tightly coupled code | tight coupling, composability, DIP violation |
| [ch03](chapters/ch03-loosely-coupled-code.md) | Writing loosely coupled code | Constructor Injection, DIP, seams |
| [ch04](chapters/ch04-di-patterns.md) | DI patterns | Composition Root, Constructor/Method/Property Injection |
| [ch05](chapters/ch05-di-anti-patterns.md) | DI anti-patterns | Control Freak, Service Locator, Ambient Context, Constrained Construction |
| [ch06](chapters/ch06-code-smells.md) | Code smells | Constructor Over-injection, Facade Services, Abstract Factory abuse |
| [ch07](chapters/ch07-application-composition.md) | Application composition | Composition Root placement, Pure DI per framework |
| [ch08](chapters/ch08-object-lifetime.md) | Object lifetime | Lifestyles (Singleton/Scoped/Transient), Captive Dependency |
| [ch09](chapters/ch09-interception.md) | Interception | Decorator, Cross-Cutting Concerns |
| [ch10](chapters/ch10-aop-by-design.md) | Aspect-Oriented Programming by design | AOP, SOLID |
| [ch11](chapters/ch11-tool-based-aop.md) | Tool-based Aspect-Oriented Programming | Dynamic Interception, Compile-time weaving |
| [ch12](chapters/ch12-di-container-introduction.md) | DI Container introduction | Register-Resolve-Release, Auto-Registration, Pure DI vs Container |
| [ch13](chapters/ch13-autofac.md) | The Autofac DI Container | Autofac ContainerBuilder, lifetime scopes, modules |
| [ch14](chapters/ch14-simple-injector.md) | The Simple Injector DI Container | Simple Injector, Verify(), RegisterDecorator |
| [ch15](chapters/ch15-microsoft-extensions-di.md) | Microsoft.Extensions.DependencyInjection | MS.DI, IServiceCollection, limitations |

## Topic Index

- **Ambient Context** → ch05
- **AOP / Aspect-Oriented Programming** → ch10, ch11, ch09
- **Auto-Registration** → ch12, ch13, ch14, ch15
- **Autofac** → ch13
- **Captive Dependency** → ch08
- **Composition Root** → ch04, ch07, ch12
- **Constrained Construction** → ch05
- **Constructor Injection** → ch03, ch04
- **Constructor Over-injection** → ch06
- **Control Freak** → ch05
- **Cross-Cutting Concerns** → ch09, ch10
- **Cyclic dependencies** → ch06
- **Decorator** → ch09, ch10
- **DI Container** → ch12, ch13, ch14, ch15
- **Dependency Inversion Principle (DIP)** → ch03, ch10
- **Facade Services** → ch06
- **Interception** → ch09, ch11
- **Lifestyles / object lifetime** → ch08
- **Method Injection** → ch04
- **Microsoft.Extensions.DependencyInjection (MS.DI)** → ch15
- **Property Injection** → ch04
- **Pure DI (Poor Man's DI)** → ch01, ch07, ch12
- **Register-Resolve-Release** → ch12
- **Service Locator** → ch05
- **Simple Injector / Verify()** → ch14
- **SOLID** → ch10
- **Tightly vs loosely coupled code** → ch02, ch03
- **Tool-based AOP (proxies, weaving)** → ch11
- **Volatile vs Stable Dependency** → ch01

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — the DI patterns and techniques with when/how/trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules: inject-or-not, pattern picker, smell→fix, lifestyle picker, container API map

---

## Scope & Limits

This skill covers the book (C#/.NET focus). For applying DI in your codebase, combine with project-specific tools and your DI container's docs. For unit-testing patterns that DI enables, see related testing skills (`khorikov-unit-testing`, `art-of-unit-testing`).
