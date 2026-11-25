---
name: principles-dry-kiss
description: Applies DRY, KISS, and YAGNI principles. Invoked when an engineer encounters duplication, is considering an abstraction, suspects over-engineering, wants to keep it simple, or is weighing whether to generalize code. Also referenced by the UX agent for design decisions.
---

# DRY / KISS Principle

Single source of truth; KISS over cleverness; YAGNI. Apply the rule of three — duplicate twice before you abstract. The simplest thing that works wins ties.

## Duplication: incidental vs meaningful

**Incidental duplication** — two code paths happen to look similar but represent independent concepts that will evolve separately. Extracting a shared abstraction couples them artificially; leave them alone.

**Meaningful duplication** — the same rule, formula, or business fact appears in multiple places. A change to the rule requires updating every copy. That is the duplication DRY targets.

Wait for a third instance before reaching for an abstraction. One occurrence is a fact; two might be coincidence; three is a pattern worth naming.

## Premature abstraction

Abstractions that arrive before the shape of a problem is clear lock in the wrong interface. The cost: every future use-case fights the abstraction rather than fitting it. Prefer concrete, specific code while the domain is still being discovered.

Signs of premature abstraction: a base class with one subclass, a strategy pattern with one strategy, a config flag that one path ever reads, a generic helper used once.

## Prefer deletion

The best code is code that doesn't exist. Before extracting, ask whether the feature, branch, or parameter earns its place. Deleting a code path is always cheaper than maintaining it. When in doubt, inline first and see if the duplication even matters.

## Cross-references

- `principles-pragmatic-solid` — Single Responsibility keeps units small enough that duplication is easy to spot and extraction is cheap when the time comes.
- `principles-ddd` — ubiquitous language names the meaningful duplicates worth eliminating.
- `principles-tdd` — tests constrain refactors that collapse or extract abstractions, making cleanup safe.
