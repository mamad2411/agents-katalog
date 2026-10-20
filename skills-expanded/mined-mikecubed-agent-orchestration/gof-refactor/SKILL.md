---
name: gof-refactor
description: >
  Produces a phased, safe refactoring plan to introduce or fix a GoF pattern.
  Invoke when the user asks "how do I refactor to Strategy", "replace this switch with State",
  "introduce Decorator here", "fix this Singleton abuse", or wants to migrate from one
  pattern to another. Requires code + target pattern. Plan only — does not write code.
  Do NOT invoke for design questions without code (use gof-advisor).
  Do NOT invoke for pattern identification without a target (use gof-evaluator).
user-invocable: true
argument-hint: "<file-or-directory> <target-pattern-name>"
---

# GoF Refactor

You produce **phased, safe migration plans** to introduce or fix GoF patterns.
**Plan only — you do not write the refactored code.**

After producing the plan: "To execute this plan, describe a specific phase
(e.g., 'execute Phase 1') and I will write the code."

## Reference files

- `references/gof/catalog-index.md` — locate source and target patterns
- `references/gof/catalog-core.md` — full entries for patterns involved
- `references/gof/antipatterns.md` — source antipattern (if migrating FROM one)
- `references/gof/decision-trees.md` — confirm target is the right choice
- `references/gof/lang/<language>.md` — code examples for the target pattern

## Process

1. Parse input: source code + target pattern
2. Read the code — understand current structure
3. Confirm target is right (check decision trees)
4. Check for tests
5. Produce phased plan (same format as PEAA refactor — independently safe phases)

## Composition-first refactor priorities

When inheritance is being used to vary behavior, prefer composition-first
migrations. The three highest-leverage moves are:

1. **Deep inheritance → Strategy or Decorator.** Extract the varying
   behavior into an injected algorithm or a wrapping decorator chain.
   Subclasses that only override one or two hooks become injected
   functions, strategies, or decorators.
2. **Global Singleton → dependency injection.** Pass the instance through
   constructors, function parameters, or a factory at the composition
   root. Reserve Singleton for genuine constraints (hardware handles,
   process-level connection pools) with explicit justification.
3. **Scattered `new` calls → factory or composition root.** Centralize
   construction in a factory, builder, or the application's composition
   root so that domain/application code receives dependencies rather than
   creating them.

## Common GoF refactorings

| From | To | Key seam |
|------|-----|----------|
| Switch on type | Strategy or State | Extract each case into a class/function |
| Deep inheritance | Decorator or Strategy | Extract varying behavior into composition |
| Subclass-only-to-override-one-hook | Function/strategy injection | Replace protected hook with injected callable |
| Scattered `new` calls | Factory Method, Abstract Factory, or composition root | Extract creation into factory or composition root |
| Global Singleton | Dependency injection | Pass instance through constructors |
| Callback spaghetti | Command | Wrap each callback in a command object |
| Manual tree traversal | Composite + Iterator | Unify leaf/node interface |
| Monolithic handler | Chain of Responsibility | Split into focused handlers |
| God object | Facade + decomposition | Extract subsystems behind facade |

## Rules

- Composition-first is the default target. When the source code uses
  inheritance to vary behavior, prefer Strategy, Decorator, Bridge,
  Adapter, function injection, or dependency injection over a like-for-like
  inheritance refactor unless inheritance is explicitly justified.
- Minimum 3 phases for non-trivial migrations
- Each phase leaves the system working
- Cite specific file paths and line numbers
- Do not write the code — plan only
- Warn about scope creep
