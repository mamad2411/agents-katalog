---
name: functional-architecture
description: "Refactor procedural or class-based TypeScript into an architecture of small pure functions composed with pipes. Use this skill when a file is organised around nouns that have grown into grab-bags of unrelated methods (a Manager, Service, Processor, Converter, Helper, Controller or God object), when a method mutates instance fields so its result depends on call order, when a function takes boolean or mode flags and branches on them, when deep-nested spread ladders update state, when logic can't be unit-tested without constructing objects or stubbing the network, or when someone asks 'how do I make this testable', 'why is this so hard to change', 'can we make this more functional', 'how do I get rid of this class'. Provides a diagnostic for order-dependent code, a six-step refactor ladder from procedure to composition, TypeScript mechanics for pipe and currying, and routes to sibling skills for combining values and for taming side effects."
---

# Functional Architecture

Most hard-to-change TypeScript isn't badly written — it's **organised around nouns instead of contracts**. A class starts as a coherent metaphor (`User`, `Address`, `Repo`), then absorbs whatever needed a home: formatting, validation, geocoding, persistence, dedupe helpers. The metaphor blurs, methods reach into `this`, and every method becomes reachable only through the whole object.

Functional architecture organises around **functions with defined contracts** instead: `a -> b`, no hidden inputs, no hidden outputs. Modularity, testability and reuse follow from that one property, not from the folder layout.

## Diagnose first: is this a procedure or a function?

Ask these four questions about the unit you're refactoring. Each "no" or "it depends" is a specific defect with a specific fix.

1. **Can I run this twice in a row and get the same result?** If not, it holds state or mutates its input.
2. **Does the order I call these in matter?** If yes, they communicate through something other than their arguments.
3. **Does it change other parts of the program?** If yes, it has an output that isn't in its return type.
4. **What does it need in order to run?** If the answer is more than its parameters — instance fields, module globals, a live connection, `Date.now()` — those are undeclared inputs.

A unit that answers *yes / no / no / just its parameters* is already a function; leave it alone. Everything else is a procedure, and the ladder below turns it into a function.

## The refactor ladder

Work top to bottom. Each step is independently shippable, and most code only needs the first three.

1. **Separate the calculation from the effect.** Split every procedure into a pure core that computes a value and a thin shell that performs I/O with it. Read at the top, compute in the middle, write at the bottom. This is the single highest-value move: the core becomes testable with plain values, and the shell shrinks to something you can eyeball.
2. **Promote hidden inputs to parameters.** Instance fields, imported singletons, clocks and config become explicit arguments. The signature now tells the truth about what the function needs — and the function stops caring who calls it first.
3. **Make the data flow one-directional with `pipe`.** A procedure that reassigns a local variable five times is a pipeline in disguise. Name each stage as its own exported function and compose them. Every intermediate value gets a name and a type, and each stage becomes independently testable.
4. **Push configuration to the edges with partial application.** When a stage needs config that the caller of the pipeline knows but the pipeline stage doesn't, curry it: `(config) => (input) => output`. Apply the config once where it's known, and the resulting one-argument function drops into any pipe.
5. **Replace flags and mode branches with composition.** A function taking `{ normalize?: boolean; withTotals?: boolean }` is several functions wearing one hat, and its body pays the branch cost on every call. Extract each behaviour as its own stage and let the caller compose the variant it wants. Callers gain combinations you never anticipated; the function loses its combinatorial test matrix.
6. **Replace mutation with narrowed transformation.** Instead of writing into an existing object, build the next value: `pick` the keys you own, spread the changes, return it. Narrowing to a known key set at the boundary also stops unexpected keys from leaking in from persisted or untrusted input.

## Generalise, but not infinitely

There's a real trade-off, and both ends are wrong:

- **Highly specialised functions** (many flags, many branches) satisfy today's callers exactly, but won't satisfy the next case, resist implementation changes, and give you almost no reuse.
- **Highly generalised functions** are reusable and easy to reimplement, but push assembly work onto every caller — and a pipeline of ten tiny stages can be harder to read than the loop it replaced.

Favour composable functions, **mostly**. Generalise a function when a second caller actually needs the variation, not in anticipation of one. A concrete named wrapper around a general core (`formatUserRow = pipe(normalize, toRow, withTotals)`) gives you both: the general pieces stay reusable, and callers get one obvious entry point.

## TypeScript mechanics that matter

- **`pipe` typings degrade.** Most libraries' `pipe` overloads run out around ten functions, and inference collapses to `any` past that. Break long pipelines into named sub-pipelines — better types *and* better names.
- **Annotate the stage, not the pipe.** Give each stage an explicit `(input: A) => B` signature. Then a mismatch is reported at the broken stage instead of as one unreadable error at the `pipe` call.
- **Point-free has a readability ceiling.** `pipe(prop('items'), map(prop('id')))` is clear; three levels of curried combinators is not. When a stage needs a name to be understood, give it one.
- **Currying manually beats a curry helper.** `(config: Config) => (input: Input): Output => …` types perfectly and needs no `curryN` cast. Reach for a variadic `curry` only for genuinely arity-polymorphic utilities.
- **Keep one `fp` barrel.** Re-export the handful of combinators the codebase actually uses from a single module, alongside your own (`isDefined`, `identity`, `noop`). Deep per-function imports (`ramda/es/pipe`) keep bundles tree-shakeable; the barrel keeps call sites uniform.

## Where to go next

This skill covers turning procedures into composed functions. Three neighbouring problems have their own skills — use them rather than re-deriving the pattern here:

| The code you're looking at | Use |
|---|---|
| A family of objects that vary by a `type` / `kind` / `__class__` field | `entity-factory` |
| An accumulation loop, an awkward `reduce`, several reducers to merge, or a deep-nested update | `algebraic-composition` |
| Throwing, `try/catch`, `async` I/O, or logic you can't test without stubbing the world | `effects-as-values` |

`references/refactor-recipes.md` has before/after TypeScript for each rung of the ladder — class to module, imperative loop to pipeline, flag parameter to composition, and mutation to transformation. `references/composition-in-typescript.md` covers typing `pipe`, curried factories, generic stages, and the readability limits of point-free style.

## When NOT to use it

- **A class with real identity and a lifecycle** — a long-lived connection, a subscription hub, something the DOM holds a reference to. Encapsulated mutable state behind a narrow interface is the right tool; make the *logic it calls* pure instead.
- **Hot loops over typed arrays.** Allocating an intermediate array per stage in a per-frame or per-row path is a measurable cost. Keep the loop, and keep the function it calls per element pure.
- **Framework-shaped code.** Component lifecycles, decorators and DI containers have their own idioms; fighting them costs more than it returns.
- **Code that is already a function.** If it answers the four diagnostic questions cleanly, it doesn't need a pipeline — leave it.
- **A refactor with no test to hold it still.** Get the current behaviour under test first; every rung above is behaviour-preserving only if something checks.
