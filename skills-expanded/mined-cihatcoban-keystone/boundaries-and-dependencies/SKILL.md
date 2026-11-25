---
name: boundaries-and-dependencies
description: Structures modules and dependency direction so changes stay local - ports and adapters, the dependency rule, coupling, cycles. Triggers - one change touches twenty files, circular dependency, where should this new code live, everything is coupled, hexagonal or clean architecture, layering.
---

# Boundaries and Dependencies

Architecture is mostly about what is allowed to know about what. A system where
any module may call any other has no architecture — it has a dependency graph
that grows until every change is a risk. The observable symptom: a one-line
behavior change requires edits in eight files across four concerns.

## The dependency rule

**Dependencies point inward, toward policy. Nothing in the core knows about the
outside.**

```text
        ┌──────────────────────────────────────┐
        │  Frameworks, drivers, I/O            │   ← replaceable details
        │  ┌────────────────────────────────┐  │
        │  │  Adapters (HTTP, DB, queue)    │  │   ← translate outside↔inside
        │  │  ┌──────────────────────────┐  │  │
        │  │  │  Application (use cases) │  │  │   ← orchestration
        │  │  │  ┌────────────────────┐  │  │  │
        │  │  │  │  Domain            │  │  │  │   ← rules, no imports out
        │  │  │  └────────────────────┘  │  │  │
        │  │  └──────────────────────────┘  │  │
        │  └────────────────────────────────┘  │
        └──────────────────────────────────────┘
                  dependencies point ⟶ inward
```

Concretely: the domain imports no web framework, no ORM, no HTTP client, no
cloud SDK. It defines the interfaces (ports) it needs; the outer layers
implement them (adapters). This is what makes the core testable without
infrastructure and survivable across framework churn.

**The pragmatic version:** you do not need four rings. You need *one* line the
dependencies never cross, drawn around the code that encodes business rules.
Everything else is detail arrangement.

## Placing new code

Ask in order:

1. **Is it a business rule?** → domain. No I/O, no framework types.
2. **Does it orchestrate a use case** (load, apply rule, persist, emit)? →
   application. Depends on domain and on ports, never on concrete adapters.
3. **Does it talk to the outside world?** → adapter. Contains no business rule;
   translation only.
4. **Is it a framework concern** (routing, serialization, DI wiring)? →
   outermost. Should be almost mechanical.

If the answer is "a bit of both", the function is doing two things. Split it.

## Coupling: which kind you have

| Kind | Example | Verdict |
|---|---|---|
| Data (pass a value) | `send(email)` | Best |
| Stamp (pass a whole object for one field) | `send(user)` to read `user.email` | Minor smell |
| Control (pass a flag that changes behavior) | `save(data, validate=false)` | Split the function |
| Common (shared mutable global) | Global config mutated at runtime | Fix |
| Content (reach into another module's internals) | Import a private helper | Fix now |
| Temporal (must be called in a specific order) | `init()` then `configure()` then `run()` | Encode the order in types or a builder |

**Cohesion** is the mirror: a module is cohesive when its parts change for the
same reason. `utils/`, `helpers/`, `common/` are the standard names for modules
with no cohesion at all — they become dumping grounds whose changes ripple
unpredictably.

## Cycles

A cycle between modules means they are one module pretending to be two. Fixes,
in order of preference:

1. **Dependency inversion** — the lower-level module defines an interface the
   higher-level one implements; the dependency flips.
2. **Extract the shared part** into a third module both depend on (only if that
   part is genuinely cohesive — not a `common/` dump).
3. **Move the code** so the relationship is one-directional.
4. **Events** — A emits, B subscribes; the compile-time edge disappears. Use
   deliberately: you traded a visible dependency for an invisible one.

Enforce acyclicity mechanically. Most ecosystems have a tool
(`import-linter`, `dependency-cruiser`, ArchUnit, `go list`). Add it to CI;
a rule not enforced by a machine decays within a quarter.

## Boundary sizing

| Signal | Boundary is too small | Boundary is too large |
|---|---|---|
| Change pattern | Every feature touches many modules | Every feature touches one giant module |
| Interfaces | Chatty, fine-grained calls between them | No internal structure |
| Tests | Mostly mocks, little real behavior | Slow, need everything running |
| Ownership | Two teams edit the same module constantly | One module owned by nobody |

Start with fewer, larger boundaries. Splitting a module later is mechanical;
merging two that were split wrongly (especially across a network) is not.

## Distribution is a boundary decision, not a scaling decision

Extracting a service converts a function call into a network call: partial
failure, versioning, latency, deployment coupling, distributed debugging.
Justify it with one of — independent scaling need, independent deployment
cadence, strict team ownership, isolation requirement — not with "cleaner
architecture". A modular monolith with enforced internal boundaries gets you
most of the benefit at a fraction of the operational cost, and makes a later
extraction straightforward because the seam already exists.

## Exit checklist

- [ ] One dependency rule is written down and one tool enforces it
- [ ] Domain code imports no framework, ORM, HTTP or cloud SDK
- [ ] External models are translated at the adapter, not passed inward
- [ ] No cycles between modules
- [ ] No `utils`/`common`/`helpers` module accumulating unrelated code
- [ ] New code's placement follows from the four questions, not convenience
- [ ] Any new network boundary has a written justification beyond tidiness
