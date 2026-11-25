---
name: coding-architecture
description: Guide maintainable frontend implementation and refactoring through semantic reuse, composition, clear boundaries, and justified abstractions. Use for non-trivial UI, state, design-system, or frontend data-boundary changes; do not use for backend-only architecture or cosmetic edits.
---

# Coding Architecture

Improve maintainability without turning a focused change into an architecture project.

## Scope and precedence

- Follow the user's request and repository instructions before this skill's preferences.
- Preserve the project's established framework, design system, directory conventions, state approach, and test strategy unless changing them is requested or concretely necessary.
- Prefer the smallest cohesive change that satisfies the request and preserves behavior. Do not reorganize unrelated modules.
- Treat the guidance below as decision criteria, not a requirement to introduce every listed pattern.

## Decide in this order

Use this as a decision preference, not a mandatory pipeline:

**Reuse → Compose → Extract → Abstract**

1. Inspect the relevant code and identify the current conventions, primitives, dependencies, data shapes, state ownership, and tests.
2. Search for semantically equivalent components, hooks, utilities, types, schemas, services, and adapters.
3. Reuse or extend an existing implementation when its contract fits. Do not merge concepts merely because they look similar.
4. Compose existing parts when their responsibilities remain clear and consumers need flexible arrangement.
5. Extract behavior or knowledge when it meaningfully repeats, changes for the same reasons, obscures a component's responsibility, or benefits from an independent test boundary.
6. Introduce an abstraction only to solve a concrete problem such as dependency isolation, multiple real implementations, complex business rules, replacement, or testability.

Component size, prop count, visual similarity, and hypothetical future reuse are signals to investigate, not sufficient reasons to extract or abstract.

## Apply patterns when the signal is present

| Signal | Preferred response |
| --- | --- |
| An equivalent framework or design-system primitive exists | Reuse, wrap, or extend it instead of rebuilding it. |
| Related UI parts need independent arrangement or extension | Use composition; consider compound components only when consumers benefit from controlling the parts. |
| Stateful behavior meaningfully repeats or makes rendering hard to understand | Extract a focused hook or composable. |
| An external or untrusted data shape would spread beyond its entry boundary | Validate and normalize it into a canonical application model through a parser or adapter. |
| A business rule is meaningful independently of the UI | Move it to an explicitly named domain function or service with a testable API. |
| State belongs to one component or subtree | Keep it local and derive values when possible. Normal prop passing is acceptable; introduce context or a store only for genuine coordination. |
| Code is only superficially similar or reuse is speculative | Keep it separate until a shared semantic contract emerges. |

## Preserve boundaries

- Keep components cohesive rather than optimizing for a line-count limit. Simple view logic may stay near rendering; meaningful business rules should not be buried in dense UI conditionals.
- Keep one source of truth for state. Prefer derived values over synchronized copies, and use effects primarily to synchronize with external systems.
- Keep raw vendor responses and external implementation details behind their entry boundary when they would otherwise leak through the application.
- Keep feature-specific code with its owning feature until reuse is demonstrated. Put shared code behind a small, semantic public API.
- Prefer explicit domain names over generic `utils`, `helpers`, `common`, or prematurely universal components.
- Before adding a dependency, verify that the framework, UI library, standard library, or an existing dependency does not already solve the problem.

## Before finishing

Check that the implementation:

- stays within the requested scope and follows repository conventions;
- reuses existing primitives where their semantics fit and does not create a duplicate concept;
- gives every new hook, service, adapter, context, store, or shared component a concrete responsibility;
- avoids duplicated synchronized state and unintended vendor-type leakage;
- covers important new business rules, parsers, adapters, or state transitions with tests proportional to their risk;
- handles loading, empty, error, responsive, and accessibility behavior when the changed UI requires them;
- passes the repository's relevant checks and leaves a final diff without accidental scope expansion.

Keep routine pattern choices silent. For a material architectural change, briefly report what boundary or abstraction changed and its concrete reason. State any intentional deviation from repository conventions.
