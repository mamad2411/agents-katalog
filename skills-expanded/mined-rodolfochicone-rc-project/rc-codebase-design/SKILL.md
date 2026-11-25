---
name: rc-codebase-design
description: "Vocabulary for deep modules — interface, depth, seam, adapter. Use when deciding where an interface goes. Do not use for UI (rc-interface-design)."
model: sonnet
effort: medium
metadata:
  credits: Doctrine adapted from codebase-design (mattpocock/skills), itself drawing on Ousterhout's A Philosophy of Software Design and Feathers' Working Effectively with Legacy Code
  adapted-by: RC — scoped against rc-interface-design (UI craft) and rc-council (system boundaries)
---

# Codebase Design

Shared vocabulary for designing **deep modules**: substantial behaviour behind a small interface,
placed at a clean seam, verifiable through that interface. Reach for it whenever code structure is
being created or reshaped — the goal is **leverage** for the caller and **locality** for the
maintainer.

This is a reference to consult, not a session to run. `rc-tdd` uses *seam* from here to decide where
tests go; `rc-implement` uses *depth* to judge whether a new abstraction earned its place;
`rc-code-review`'s delete-list uses the deletion test. It answers the question those skills come
after: **where should this interface live, and how much should it hide?**

Not this skill: UI and visual craft is `rc-interface-design`; service boundaries, data ownership and
10x/100x scaling are a `rc-council` debate. This one is the everyday module.

## Glossary

The terms are the point. Use them literally — they are chosen to avoid words that arrive
pre-loaded with someone else's model.

| Term | Means | Say this, not |
| --- | --- | --- |
| **module** | anything with an interface and an implementation — deliberately scale-agnostic: a function, a class, a package, a slice spanning tiers | *unit*, *component*, *service* |
| **interface** | everything a caller must know to use it correctly: the type signature **plus** invariants, ordering constraints, error modes, configuration and performance facts | *API*, *signature* — both too narrow |
| **implementation** | the code inside the module | — |
| **depth** | leverage at the interface: how much behaviour a caller or a test can exercise per unit of interface they must learn | — |
| **seam** | a place where you can alter behaviour without editing in that place (Feathers). Where a module's interface *lives* | *boundary* — carries DDD baggage |
| **adapter** | the concrete thing satisfying an interface at a seam. Names a **role**, not a substance | — |
| **leverage** | what the caller gains from depth: capability per unit of interface learned | — |
| **locality** | what the maintainer gains from depth: change, bugs and knowledge concentrate in one place instead of scattering across call sites | — |

## Deep and shallow

A **deep** module shows a small interface over substantial hidden implementation. A **shallow** one
shows a large interface over almost nothing — the interface nearly restates the implementation, so
the caller learns as much as they would have by writing it themselves.

```
deep                       shallow
┌────────────┐             ┌──────────────────────────┐
│ interface  │             │       interface          │
├────────────┴───────┐     ├──────────────────────────┤
│                    │     │      implementation      │
│  implementation    │     └──────────────────────────┘
│                    │
└────────────────────┘
```

Shallow is the default failure mode of code written to be "flexible": every option becomes a
parameter, every step becomes a method, and the caller ends up orchestrating what the module should
have owned.

When a module reads shallow, ask: can it expose fewer methods? Fewer parameters? Can more of the
decision live inside instead of being handed out?

## Principles

1. **Depth is a property of the interface, not the implementation.** A 2000-line module is not deep
   because it is large. A module may hold *internal* seams — private, used by its own tests —
   entirely separate from the external seam it presents.

2. **The deletion test.** Delete the module and inline it at every call site. If the complexity
   simply vanishes, the module was a pass-through and never earned its place. If the complexity
   reappears at each of N callers, it earned it. This is the same instrument the delete-list lens in
   `rc-code-review` uses — here it is applied at design time, before the code exists.

3. **The interface is the test surface.** Callers and tests cross the same seam. If a test has to
   reach *past* the interface — poking at internals, asserting through a side channel, needing a
   test-only accessor — that is information about the design, not about the test. The shape is
   probably wrong.

4. **One adapter is a hypothetical seam; two adapters is a real one.** A seam introduced for a
   variation that does not exist yet is speculative flexibility — the interface with a single
   implementation that YAGNI names. Wait for the second adapter.

## Designing for testability

Testability is not a property you add afterward; it is what these three practices produce:

- **Accept dependencies, do not construct them.** Take the payment gateway as an argument; do not
  instantiate it inside. The seam appears for free.
- **Return results, do not cause side effects.** Return the computed discount; do not reach into the
  cart and mutate it. What is returned can be asserted; what is mutated has to be excavated.
- **Keep the surface small.** Fewer methods means fewer tests; fewer parameters means less setup per
  test. Surface area is paid for once at design time and then repeatedly on every test.

## Two framings to refuse

- **Depth measured as a ratio** of implementation lines to interface lines. It rewards padding the
  implementation, which is the opposite of the goal. Depth is about what the caller has to learn.
- **"Boundary"** as the word for where an interface sits. It arrives carrying DDD's bounded context
  and drags a whole model in with it. Say *seam*, or say *interface*.

## Using it in practice

When a change introduces or reshapes structure, name the pieces with these words before arguing
about them — most design disagreements dissolve once both sides say which *interface* they mean and
whether the disagreement is about depth or about placement.

The two questions worth asking out loud on any new abstraction: **what does the caller no longer have
to know?** (depth) and **has the second adapter actually shown up?** (seam).
