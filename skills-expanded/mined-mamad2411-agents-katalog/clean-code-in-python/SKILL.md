---
name: clean-code-in-python
description: "Knowledge base from \"Clean Code in Python, 2nd Edition\" by Mariano Anaya. Use when applying Anaya's frameworks for Pythonic code, Design by Contract, SOLID in Python, decorators, descriptors, generators/async, unit testing and refactoring, Python design patterns, or clean architecture — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Clean Code in Python (2nd Edition)
**Author**: Mariano Anaya | **Pages**: ~423 | **Chapters**: 10 | **Python**: 3.9+ | **Generated**: 2026-10-09

## How to Use This Skill

- **Without arguments** — load the core frameworks below
- **With a topic** — ask about `descriptors`, `LSP`, `context managers`, etc.; I find and read the relevant chapter
- **With chapter** — ask for `ch06`; I load that chapter file
- **Browse** — ask "what chapters do you have?"

When a question goes beyond the Core Frameworks below, read the relevant chapter file before answering. For quick decisions, read [cheatsheet.md](cheatsheet.md) first.

---

## Core Frameworks & Mental Models

### The thesis: the code *is* the design
Clean code is code that other engineers can read and maintain. Formatting and PEP-8 are **necessary but not sufficient**. Clean code fights **technical debt**: every shortcut accrues interest. Enforce standards with tools (pylint, mypy, black) in a `make checklist` target that CI runs, so they don't depend on good intentions. Skip quality only for code that will truly never be maintained.

### Pythonic code (Ch 2): use the language's protocols, don't fight them
- Prefer **idioms** to ports of C or Java: slices, comprehensions, `:=`, unpacking, `@dataclass`.
- Use **context managers** (`__enter__`/`__exit__`, `@contextmanager`, `ContextDecorator`, `suppress`) for any pre/post logic. Don't return `True` from `__exit__` unless you mean to swallow the error.
- Make objects behave natively through magic methods: `__getitem__`/`__len__` (sequence), `__iter__` (container iterable), `__contains__`, `__getattr__` (it must raise `AttributeError`), `__call__`.
- **Caveats**: no mutable default arguments. Don't subclass built-ins (use `UserDict`/`UserList` or composition). Use `_single` underscore for privacy, never `__double` (name mangling).

### General traits of good code (Ch 3)
- **Design by Contract**: state preconditions, postconditions and invariants. Apply the **non-redundancy principle**: validate each condition in exactly one place, either the client or the function.
- **Defensive programming**: handle errors at the right level of abstraction. Never swallow them (`except: pass`). Chain with `raise X from e`. Assertions mark impossible states: never catch `AssertionError`.
- **Separation of concerns**: aim for **high cohesion and low coupling** to contain ripple effects.
- Acronyms to live by: **DRY/OAOO**, **YAGNI**, **KIS**, **EAFP over LBYL**.
- Favor **composition over inheritance**. Inherit only for a true IS-A relationship that reuses most of the parent. Mixins add behavior through the MRO.
- Treat long parameter lists as a smell: **reify** the concept or pass the owning object. Keep `*args`/`**kwargs` for perfect wrappers. Aim for **orthogonality**: a change in one part shouldn't affect another.

### SOLID, the Pythonic way (Ch 4)
- **SRP**: one reason to change. Find it with the question "does X have to change because Y changed?" Split god objects along partitions of attributes and methods.
- **OCP**: replace `if/elif` over types with polymorphism. Each subclass implements `meets_condition()`, the client iterates `__subclasses__()`, and a **null object** is the fallback.
- **LSP**: a subclass keeps the signature and **never makes preconditions stricter or postconditions weaker**. Let mypy and pylint catch violations, and never `# type: ignore` them.
- **ISP**: keep interfaces small and cohesive, sized by "do one thing". In Python, ABCs or duck typing.
- **DIP + dependency injection**: details depend on abstractions. Inject collaborators through `__init__`, and use `pinject` for large object graphs.

### Decorators (Ch 5)
- `@deco` is `f = deco(f)`. **Always apply `functools.wraps`** to the wrapper.
- Put side effects **inside the wrapper** so they run at call time. The only exception is deliberate import-time registration.
- **Parametrized decorators**: use nested functions or, more readable, a **decorator object** (parameters in `__init__`, logic in `__call__`). Make the parameters keyword-only. For default arguments use the `function=None` + `partial` trick.
- Class decorators replace boilerplate. A coroutine wrapper must itself be `async`. The **universal decorator** (a class with `__get__`) works on both functions and methods.
- A good decorator is **encapsulated, orthogonal, reusable** and has a single responsibility (`log_execution` and `measure_time` stay separate). Apply the **rule of three** before creating one.

### Descriptors (Ch 6)
- **Data** descriptors (`__set__`/`__delete__`) override the instance `__dict__`. **Non-data** descriptors (`__get__` only) are overridden by it.
- In `__get__`, return `self` when `instance is None`. Get the attribute name from `__set_name__`. **Store values in `instance.__dict__[name]`**: not on the descriptor (shared across instances), not with `setattr` (infinite recursion). If you need a mapping, use a `WeakKeyDictionary`.
- Use them for **validated or transformed fields** that repeat across classes. Python itself is built on them: methods are function descriptors, plus `@property`, `classmethod` and `__slots__`. Keep business logic out of descriptors.

### Generators, iterators, async (Ch 7)
- Turn eager builders into **lazy generators**: replace `append` with `yield`, and chain generator expressions with `itertools` (`islice`, `tee`, `chain`). Generators are single-pass, so use a **container iterable** when you need several passes.
- Flatten nested-loop searches with a helper generator plus `next(gen, default)`.
- Coroutine interface: `send` / `throw` / `close`. Prime with `next()` first. `yield from` delegates and returns the sub-generator's value.
- Async: `async def`/`await`, `__aenter__`/`__aexit__`, `__aiter__`/`__anext__`, and async generators. Async leaks through every caller.

### Unit testing & refactoring (Ch 8)
- Unit tests must be **isolated, fast, repeatable and self-validating**. **Testability is a design property**: if a test needs heavy `mock.patch`, refactor toward DI.
- Prefer **pytest**: `parametrize`, fixtures, `conftest.py`. Use `Mock`/`MagicMock` sparingly.
- Treat ~80% coverage as a floor, not a target. Strengthen the suite with **property-based** (hypothesis) and **mutation testing** (mutpy).
- Test boundaries and equivalence classes. TDD: red, green, refactor.

### Design patterns in Python (Ch 9)
- **Patterns emerge; don't force them.** Some are invisible in Python (iterator, decorator syntax, facade via `__init__.py`), some are simpler, and some are still needed.
- Avoid **singletons**. Use a module-level object, a shared-state descriptor or Borg instead. Use **Adapter** through composition.
- Also covered: Composite, Decorator (class or function form), Chain of responsibility, Template method, Command, **State** (reify each state as a class), **Null object**.
- Never name classes after patterns.

### Clean architecture (Ch 10)
- Clean code is the foundation of clean architecture, and **separation of concerns scales up** to components (packages or services).
- **Hexagonal / screaming architecture**: the domain defines APIs, and the ORM, web framework and broker sit behind adapters. Dependencies flow toward the kernel.
- Prefer a **library** to a microservice unless consumers use several languages or deploy independently.
- Get repeatable builds from a pinned baseline: `setup.py` ranges, a compiled `requirements.txt`, and Docker installing only from it.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction-formatting-tools.md) | Introduction, Code Formatting, and Tools | technical debt, PEP-8, docstrings, type hints, mypy/pylint/black, CI checklist |
| [ch02](chapters/ch02-pythonic-code.md) | Pythonic Code | idioms, slices/sequences, context managers, comprehensions, `:=`, properties, dataclasses, iterables, magic methods, caveats |
| [ch03](chapters/ch03-general-traits-good-code.md) | General Traits of Good Code | Design by Contract, defensive programming, cohesion/coupling, DRY, YAGNI, KIS, EAFP, composition vs inheritance, arguments |
| [ch04](chapters/ch04-solid-principles.md) | The SOLID Principles | SRP, OCP, LSP, ISP, DIP, dependency injection, ABCs, pinject |
| [ch05](chapters/ch05-decorators.md) | Using Decorators to Improve Our Code | `wraps`, parametrized/class decorators, universal decorator, side effects, rule of three |
| [ch06](chapters/ch06-descriptors.md) | Getting More Out of Our Objects with Descriptors | data vs non-data, `__set_name__`, `instance.__dict__` storage, validation fields, `__slots__` |
| [ch07](chapters/ch07-generators-iterators-async.md) | Generators, Iterators, and Asynchronous Programming | lazy pipelines, itertools, coroutines, `yield from`, async magic methods, async generators |
| [ch08](chapters/ch08-unit-testing-refactoring.md) | Unit Testing and Refactoring | testability, pytest, fixtures, mocks, coverage, property-based & mutation testing, TDD |
| [ch09](chapters/ch09-common-design-patterns.md) | Common Design Patterns | monostate/Borg, adapter, composite, decorator, facade, chain of responsibility, template method, command, state, null object |
| [ch10](chapters/ch10-clean-architecture.md) | Clean Architecture | SoC at scale, hexagonal/screaming architecture, adapters, packaging, Docker, baselines |

## Topic Index

- **ABCs / virtual subclasses** → ch04
- **Adapter** → ch09, ch10
- **Annotations / type hints / mypy** → ch01, ch04
- **Assertions** → ch03
- **Assignment expressions (`:=`)** → ch02
- **Async / await, async generators** → ch02, ch05, ch07
- **black / yapf / pylint** → ch01
- **Borg / monostate / singleton** → ch09
- **Chain of responsibility / Command / Template method** → ch09
- **Cohesion & coupling** → ch03
- **Composition vs inheritance / mixins / MRO** → ch03, ch09
- **Context managers** → ch02
- **Coverage / mutation / property-based testing** → ch08
- **Dataclasses / properties** → ch02
- **Decorators** → ch05; **Decorator pattern** → ch09
- **Dependency injection / DIP** → ch04, ch08
- **Descriptors / `__slots__` / `__set_name__`** → ch06, ch09
- **Design by Contract / defensive programming / exceptions** → ch03
- **Docstrings / documentation** → ch01
- **DRY, YAGNI, KIS, EAFP/LBYL** → ch03
- **Facade / Composite** → ch09
- **Generators / iterators / itertools / `yield from`** → ch02, ch07
- **Hexagonal / screaming architecture** → ch10
- **Magic methods** → ch02, ch06, ch07
- **Mutable defaults / extending built-ins** → ch02
- **Null object** → ch04, ch09
- **Packaging / Docker / dependencies** → ch10
- **pytest / unittest / mocks / fixtures** → ch08
- **Refactoring / testability** → ch08
- **SOLID (SRP, OCP, LSP, ISP)** → ch04
- **State pattern / reification** → ch03, ch09
- **Technical debt / PEP-8** → ch01

## Supporting Files

- [glossary.md](glossary.md): all key terms with definitions
- [patterns.md](patterns.md): all techniques and design patterns
- [cheatsheet.md](cheatsheet.md): decision rules, thresholds, decision trees, smells

---

## Scope & Limits

This skill covers the book's content only (2nd ed., Python 3.9+). For hands-on implementation in your codebase, combine it with project-specific tools. For newer Python features (3.10+ pattern matching, newer typing syntax), check current docs. Chapter files are synthesized summaries, not the book text.
