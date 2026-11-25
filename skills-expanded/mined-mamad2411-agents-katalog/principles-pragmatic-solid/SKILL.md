---
name: principles-pragmatic-solid
description: Applies pragmatic SOLID discipline. Invoked when an engineer is designing interfaces, wiring dependency injection, considering mocking strategy, evaluating swappable implementations, or deciding whether a SOLID principle applies. Governs which SOLID principles deliver real leverage vs. which add ceremony.
---

# Pragmatic SOLID Principle

Keep DI, interface segregation, and Liskov substitution — they buy mocking and swapping. No interface-per-class, no premature abstraction; apply S and O only when churn justifies it. KISS/YAGNI break ties.

## Keep

**Dependency Inversion — inject behind interfaces.**
Modules should depend on abstractions, not concretions. Inject dependencies at the boundary (constructor, factory, config) so implementations can be swapped without touching call sites. The payoff is immediate: any injected interface can be replaced with a test double. See `principles-tdd` for how this makes isolation cheap.

**Interface Segregation — small, focused interfaces.**
Prefer narrow interfaces over fat ones. A caller that only needs `read(id)` should not be forced to implement or import `create`, `update`, and `delete`. Small interfaces are easier to mock, easier to satisfy with a stub, and easier to swap. When an interface grows beyond what a single caller needs, split it.

**Liskov Substitution — substitutable implementations.**
Every implementation of an interface must be a true substitute — same pre/post-conditions, no surprises. This is what makes mocking safe: a test double that violates the contract produces a green test suite that lies. Enforce it by designing interfaces around behavior contracts, not implementation convenience.

## Guardrails against ceremony

**No interface-per-class.**
A `UserService` class does not need a `IUserService` interface unless a second implementation exists or a test double is required. An interface with one implementation that never changes is dead weight — it adds an indirection layer for no substitution benefit.

**No premature abstraction.**
Don't extract a shared interface before you have two genuinely different implementations. Speculative abstractions ("we might want to swap this later") lock in the wrong contract. Write the concrete class; extract the interface when the second implementation arrives or when a test double is needed.

**S and O only when churn justifies it.**
Single Responsibility and Open/Closed are refactoring guides, not upfront mandates. Apply SRP when a class has multiple unrelated reasons to change and those changes conflict. Apply OCP when you find yourself repeatedly modifying the same class for new variants. Until then, a cohesive class that grows predictably beats a prematurely fragmented one.

**Avoid abstraction stacks.**
Repository → Service → Facade → Manager chains where each layer adds no logic are a trap. Each layer costs a file, a type, and a mental hop. Flatten when the intermediate layer is a passthrough. See `principles-dry-kiss`.

## Cross-references

- `principles-tdd` — the interface discipline here is the direct enabler of cheap test doubles and clean isolation.
- `principles-ddd` — Dependency Inversion enforces domain/infra separation; injected infra interfaces keep domain logic pure.
- `principles-dry-kiss` — YAGNI governs when to stop adding abstraction layers; KISS breaks ties between two SOLID-compliant designs.
