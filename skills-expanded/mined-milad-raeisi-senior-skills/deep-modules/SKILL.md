---
name: deep-modules
description: Software design for codebases that stay easy to change, for humans and agents alike. Use when designing a new module, service, class, or API, refactoring a tangled area, deciding where logic belongs or where to split code, reviewing architecture, or when the user mentions maintainability, coupling, abstraction, layering, testability, or "this code is a mess". Applies deep modules (small interface, rich hidden behavior), information hiding, seams, and explicit states, and refactors in safe, behavior-preserving steps.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Deep Modules

Complexity is what makes software hard to change, and it accumulates in small increments: one more parameter, one more pass-through layer, one more place that knows a detail it shouldn't. Good design fights it by **hiding complexity behind simple interfaces** so that most of the code never has to think about it. Ideas here draw on John Ousterhout's *A Philosophy of Software Design*, Michael Feathers' work on seams, and the functional-core / imperative-shell pattern.

## Vocabulary

- **Module**: anything with an interface and an implementation: a function, class, package, or service.
- **Interface**: everything a caller must know to use the module correctly. That covers signatures, but also ordering rules, error modes, invariants, and performance characteristics.
- **Deep module**: lots of useful behavior behind a small interface. Unix file I/O (`open`, `read`, `write`, `lseek`, `close`) hides caching, devices, and permissions behind five calls.
- **Shallow module**: an interface nearly as complex as its implementation. Pass-through wrappers, getter/setter classes, and "manager" classes that forward every call.
- **Seam**: a place where behavior can be changed without editing the code there, such as a parameter, an interface, or a configuration point. This is where tests and alternate implementations plug in.

## Principles

1. **Make modules deep.** Before adding a module, ask what complexity it hides. If callers still need to understand everything inside, it isn't earning its keep.
2. **Hide information.** Each design decision (a file format, a caching strategy, a vendor API) should live in one module. When a decision leaks into many places, changing it means changing all of them.
3. **Pull complexity downward.** It's better for the module to handle a hard case once than for every caller to handle it. Sensible defaults beat required configuration.
4. **Define errors out of existence where you can.** An API where "delete a missing key" is simply a no-op is easier to use correctly than one that throws.
5. **Make illegal states unrepresentable.** Use types that only allow valid combinations (see `state-machine-hunter`).
6. **Functional core, imperative shell.** Keep decisions in pure functions that take data and return data; keep I/O at the edges. The core becomes trivially testable and the shell stays thin.
7. **Accept dependencies, don't construct them.** Pass the clock, the HTTP client, and the repository in. It's the cheapest seam there is.
8. **One adapter is a hypothetical seam; two is a real one.** Don't create an interface "in case we swap databases". Create it when the second implementation (often the test fake) exists.
9. **Different layer, different abstraction.** If two adjacent layers have the same methods with the same parameters, one of them is probably a pass-through that should go.
10. **Names are interface.** A name that needs a comment to explain it is a design smell. If you can't name a module simply, its responsibility probably isn't simple.

## Red flags

| Smell | What it suggests |
|---|---|
| A change requires edits in many unrelated files | Information leakage; a decision isn't localized |
| A function needs 6+ parameters or boolean flags | Several responsibilities fused together, or complexity pushed up to callers |
| Classes named `*Manager`, `*Helper`, `*Util`, `*Service` with grab-bag methods | Missing domain concepts |
| Tests need heavy mocking of your own code | Logic tangled with I/O; missing seam |
| Same conditional repeated across the codebase | A missing abstraction or an implicit state machine |
| A comment repeats what the code says | The code isn't expressing intent; rename or restructure |

## The deletion test

Imagine deleting a module and inlining it into its callers. If complexity vanishes, it was a pass-through; inline it as part of your refactor (or propose removing it, if it isn't code you're already changing). If complexity reappears in many places, it's earning its keep.

## Refactoring safely

1. Pin current behavior with tests at the module's public interface; add characterization tests if needed.
2. Change structure in small, behavior-preserving steps (extract, inline, move, rename), running the tests after each.
3. Keep refactors and behavior changes in separate commits, so a reviewer can verify each on its own.
4. Stop when the change you actually needed has become easy. Refactoring is in service of a goal, not a goal in itself.

## Designing for agents (AX)

Code that's easy for agents to change is code that's easy for anyone to change: one obvious place for each concept, greppable names that match the domain, explicit types and states, small modules with clear entry points, and fast tests at stable interfaces. When a design decision isn't obvious from the code, write it down next to the code (a short README in the module, or an ADR).
