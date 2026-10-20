---
name: dive-into-design-patterns
description: "Knowledge base from \"Dive Into Design Patterns\" by Alexander Shvets (Refactoring.Guru). Use when applying the 23 GoF patterns, choosing between creational/structural/behavioral patterns, applying SOLID and core OO design principles, disambiguating lookalike patterns (Strategy vs State, Adapter vs Decorator vs Proxy), studying the book, or referencing its concepts."
---

<!-- argument-hint: [pattern name, topic, or chapter number e.g. ch12] -->

# Dive Into Design Patterns
**Author**: Alexander Shvets (Refactoring.Guru) | **Pages**: ~410 | **Chapters**: 25 | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load the core principles + pattern selection logic below.
- **With a pattern/topic** — ask about `decorator`, `SOLID`, `flyweight`, `state vs strategy`; I read the relevant chapter file before answering.
- **With a chapter** — ask for `ch12`; I load that file.
- **Browse** — ask "what chapters do you have?" for the full index.

For pattern *selection* and *disambiguation*, start with [cheatsheet.md](cheatsheet.md). For a one-paragraph spec of each pattern, see [patterns.md](patterns.md).

---

## Core Design Principles (the foundation — Ch03)

Patterns are applications of these. Reach for the principle before the pattern.

- **Encapsulate What Varies** — isolate the parts that change behind a stable interface, so a change in one place doesn't ripple. The motivation behind most patterns.
- **Program to an Interface, Not an Implementation** — depend on abstractions; this is what lets objects be swapped and extended.
- **Favor Composition Over Inheritance** — inheritance multiplies subclasses across dimensions (combinatorial explosion) and is rigid; composition (has-a) is flexible and runtime-swappable. Bridge and Strategy embody this.

**SOLID** (Ch03):
- **S — Single Responsibility**: one reason to change per class.
- **O — Open/Closed**: open for extension, closed for modification. *When you must change tested, in-use code, extend it (subclass/strategy) instead of editing it.*
- **L — Liskov Substitution**: a subtype must be usable anywhere its base is (honor pre/post-conditions and invariants; don't strengthen inputs or weaken outputs).
- **I — Interface Segregation**: many narrow interfaces beat one fat one; clients shouldn't depend on methods they don't use.
- **D — Dependency Inversion**: high-level modules depend on abstractions, not low-level details.

## What a Pattern Is (Ch02)

A **design pattern** is a customizable *blueprint*, not copy-paste code. Scale: **idiom** (language-specific) → **design pattern** → **architectural pattern** (whole app). The 23 GoF patterns split by intent into three groups:

- **Creational** — *how objects get created* (Factory Method, Abstract Factory, Builder, Prototype, Singleton).
- **Structural** — *how objects/classes are assembled into bigger structures* (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy).
- **Behavioral** — *how objects communicate and divide responsibility* (Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor).

## Pattern Selection (fast path)

| Problem | Pattern |
|---|---|
| Creation type decided by subclass | **Factory Method** |
| Families of related products | **Abstract Factory** |
| Step-by-step build / kill telescoping constructor | **Builder** |
| Copy without coupling to class | **Prototype** |
| Exactly one shared instance | **Singleton** |
| Make incompatible interfaces talk | **Adapter** |
| Split class across two dimensions | **Bridge** |
| Part-whole tree, treat nodes uniformly | **Composite** |
| Add behavior at runtime by wrapping | **Decorator** |
| Simple door to a complex subsystem | **Facade** |
| Share state to fit millions of objects in RAM | **Flyweight** |
| Control access to an object | **Proxy** |
| Pass request along handlers | **Chain of Responsibility** |
| Request as object; undo/queue/log | **Command** |
| Traverse without exposing collection | **Iterator** |
| Decouple tangled objects via a hub | **Mediator** |
| Snapshot/restore state | **Memento** |
| Notify many on change | **Observer** |
| Behavior by state; kill big `if`s | **State** |
| Swap algorithm at runtime | **Strategy** |
| Fixed skeleton, vary steps | **Template Method** |
| Add ops to a hierarchy without editing it | **Visitor** |

**Lookalikes** (full table in cheatsheet): Adapter=*different* interface · Decorator=*enhanced* · Proxy=*same*. State's states know each other & transition; Strategy's don't. Strategy=composition/runtime; Template Method=inheritance/compile-time. Factory Method=one product; Abstract Factory=a family.

---

## Chapter Index

| # | Title | Key Content |
|---|-------|----------------|
| [ch01](chapters/ch01-oop-basics.md) | Introduction to OOP | 4 pillars; association/dependency/aggregation/composition |
| [ch02](chapters/ch02-intro-to-patterns.md) | Introduction to Patterns | what a pattern is; classification; GoF history; criticism |
| [ch03](chapters/ch03-design-principles-solid.md) | Software Design Principles | Encapsulate What Varies, Program to Interface, Composition>Inheritance, SOLID |
| [ch04](chapters/ch04-factory-method.md) | Factory Method | Creator, Product, subclass-decides-type |
| [ch05](chapters/ch05-abstract-factory.md) | Abstract Factory | product families, concrete factories |
| [ch06](chapters/ch06-builder.md) | Builder | step-by-step, Director, telescoping fix |
| [ch07](chapters/ch07-prototype.md) | Prototype | clone, Prototype Registry |
| [ch08](chapters/ch08-singleton.md) | Singleton | single instance, lazy init, caveats |
| [ch09](chapters/ch09-adapter.md) | Adapter | object vs class adapter, translation |
| [ch10](chapters/ch10-bridge.md) | Bridge | Abstraction/Implementation split |
| [ch11](chapters/ch11-composite.md) | Composite | trees, Leaf/Container, recursion |
| [ch12](chapters/ch12-decorator.md) | Decorator | runtime wrapping, stacking |
| [ch13](chapters/ch13-facade.md) | Facade | subsystem entry point |
| [ch14](chapters/ch14-flyweight.md) | Flyweight | intrinsic/extrinsic state, factory |
| [ch15](chapters/ch15-proxy.md) | Proxy | virtual/protection/remote/logging/caching |
| [ch16](chapters/ch16-chain-of-responsibility.md) | Chain of Responsibility | handler chain, forwarding |
| [ch17](chapters/ch17-command.md) | Command | request-as-object, undo, invoker/receiver |
| [ch18](chapters/ch18-iterator.md) | Iterator | traversal without exposure |
| [ch19](chapters/ch19-mediator.md) | Mediator | central hub, notify() |
| [ch20](chapters/ch20-memento.md) | Memento | snapshots, originator/caretaker |
| [ch21](chapters/ch21-observer.md) | Observer | publisher/subscriber, subscription |
| [ch22](chapters/ch22-state.md) | State | FSM, transitions |
| [ch23](chapters/ch23-strategy.md) | Strategy | interchangeable algorithms |
| [ch24](chapters/ch24-template-method.md) | Template Method | skeleton + steps/hooks |
| [ch25](chapters/ch25-visitor.md) | Visitor | double dispatch, add ops to hierarchy |

## Topic Index

- **Abstract Factory** → ch05
- **Adapter / Wrapper** → ch09 (Wrapper also ch12)
- **Aggregation / Composition / Association / Dependency** → ch01, ch03
- **Behavioral patterns** → ch16–ch25
- **Bridge** → ch10
- **Builder** → ch06
- **Chain of Responsibility** → ch16
- **Command** → ch17
- **Composite** → ch11
- **Composition over Inheritance** → ch03, ch10, ch23
- **Creational patterns** → ch04–ch08
- **Decorator** → ch12
- **Dependency Inversion (DIP)** → ch03
- **Double Dispatch** → ch25
- **Encapsulate What Varies** → ch03
- **Facade** → ch13
- **Factory Method** → ch04
- **Flyweight** → ch14
- **GoF / classification / history** → ch02
- **Interface Segregation (ISP)** → ch03
- **Iterator** → ch18
- **Liskov Substitution (LSP)** → ch03
- **Mediator** → ch19
- **Memento** → ch20
- **Observer** → ch21
- **OOP pillars** → ch01
- **Open/Closed (OCP)** → ch03
- **Program to an Interface** → ch03
- **Prototype / clone** → ch07
- **Proxy** → ch15
- **Single Responsibility (SRP)** → ch03
- **Singleton** → ch08
- **SOLID** → ch03
- **State** → ch22
- **State vs Strategy** → ch22, ch23
- **Strategy** → ch23
- **Structural patterns** → ch09–ch15
- **Template Method** → ch24
- **Visitor** → ch25

## Supporting Files

- [glossary.md](glossary.md) — all key terms and pattern roles with definitions
- [patterns.md](patterns.md) — all 23 patterns: when / how / trade-offs
- [cheatsheet.md](cheatsheet.md) — selection table, lookalike disambiguation, tells & smells

---

## Scope & Limits

Covers the book's concepts only — language-agnostic pseudocode, not full code samples in a specific language (the book sells those separately per language). For applying a pattern in your codebase, combine with project tooling. Patterns are tools, not goals: the book itself warns against over-engineering — apply one only when a real recurring problem justifies the indirection.
