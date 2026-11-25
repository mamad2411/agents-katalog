---
name: domain-driven-design
description: Applies Domain-Driven Design where it pays off - ubiquitous language, bounded contexts and context maps, aggregates sized around invariants, entities vs value objects, domain events and repositories - and says when DDD is overkill. Use when modelling a complex business domain, splitting a monolith or services along business lines, aggregates or transactions are too large, the same term means different things in different teams, or the user mentions DDD, bounded contexts or aggregates. Not for simple CRUD apps.
license: MIT
---

# Domain-Driven Design

Model the business rules, not the database tables. DDD earns its cost only where the domain is complex and the rules change often; there, the code should use the business's own words, each model should be valid inside one explicit boundary, and every rule that must always hold should be enforced in exactly one place.

## When DDD pays off

| Use DDD (strategic and tactical) | Use strategic DDD only | Skip DDD |
| --- | --- | --- |
| Complex rules that change often (pricing, underwriting, scheduling, logistics) | Several teams or services; terms clash across them; unclear service boundaries | Forms over data, admin panels, reporting, simple CRUD |
| Domain experts are available to talk to | Integration-heavy systems where the main risk is coupling | Prototypes and short-lived tools |
| The domain is a competitive advantage (core domain) | | Generic subdomains you could buy (auth, billing, email) |

Strategic DDD (language, contexts, context maps) is cheap and useful almost everywhere with more than one team. Tactical patterns (aggregates, value objects, repositories) are worth their ceremony only inside complex core domains.

## Workflow

1. **Build the ubiquitous language.** Collect the nouns and verbs domain experts use. Write a glossary per context: term, definition, example, and terms that are *not* synonyms. Use these exact words in code, APIs, tests and conversations. When code and experts disagree on a word, fix the code.
2. **Run a lightweight event storming.** List domain events in past tense on a timeline ("Order Placed", "Payment Captured", "Shipment Dispatched"). For each, add the command that caused it, the actor, and the rules (policies) that must hold. Clusters of events and rules that change together hint at contexts and aggregates.
3. **Classify subdomains.** Core (your advantage: invest, model deeply), supporting (needed, specific to you: keep simple), generic (solved problems: buy or use a library).
4. **Draw bounded contexts.** A bounded context is a boundary within which one model and one language are consistent. The same word may mean different things in two contexts ("Customer" in Sales vs Support): that is expected; don't force one shared model.
5. **Map relationships between contexts** using the context-map patterns below. Make upstream/downstream explicit and choose the translation strategy.
6. **Design aggregates inside complex contexts** (rules below). Start from invariants: rules that must be true after every transaction.
7. **Map contexts to code.** Usually one context = one module (package, namespace, project) in a modular monolith first; split into a service only when independent deployment or scaling is needed. One context may become one service; a service should not contain half of two contexts.
8. **Integrate through explicit contracts**: published APIs or domain events, never shared database tables.

## Context-map patterns

| Pattern | Meaning | Use when |
| --- | --- | --- |
| Shared kernel | Two contexts share a small, jointly owned model/library | Two teams work closely and accept coordinated changes; keep it tiny |
| Customer / supplier | Upstream supplies what downstream needs; downstream's needs influence upstream's plans | Teams can negotiate priorities |
| Conformist | Downstream adopts upstream's model as-is | Upstream won't change for you and its model is acceptable |
| Anti-corruption layer (ACL) | Downstream translates upstream's model into its own at the boundary | Integrating legacy or third-party systems whose model would pollute yours |
| Open host service | Upstream offers a well-defined protocol/API for many consumers | Many downstream contexts integrate with you |
| Published language | A documented shared exchange format (schema, event contract) | Paired with open host; versioned contracts |
| Separate ways | No integration; duplicate the small bit you need | Integration cost exceeds the value |

Default for legacy or external systems: anti-corruption layer. Default for your own platform used by many teams: open host + published language.

## Aggregate rules

An aggregate is a cluster of objects treated as one unit for changes, with one root entity that guards its invariants.

1. **Size aggregates around invariants, not around nouns.** Ask "which rules must be true immediately after this change?" Only data needed to check those rules goes in the aggregate.
2. **Prefer small aggregates.** Often a single entity plus value objects. Large aggregates cause lock contention and slow loads.
3. **Modify one aggregate per transaction.** Rules spanning aggregates are made consistent eventually, via domain events and policies.
4. **Reference other aggregates by ID**, not by object reference. `order.customerId`, not `order.customer`.
5. **All changes go through the root.** External code calls `order.addLine(...)`, never `order.lines.push(...)`. The root enforces the rules.
6. **Load and save whole aggregates** through a repository (one repository per aggregate root, not per table).
7. **Use optimistic concurrency** (a version column) on the aggregate root to catch concurrent modifications.

Example: "An order's total must not exceed the customer's credit limit" spans Order and Customer credit. Options: put credit reservation in its own small aggregate and reserve credit before placing the order (a saga across two transactions), or accept eventual consistency and cancel orders that fail a later credit check. Pick based on how costly a temporary violation is; ask the domain expert.

## Building blocks

| Block | What it is | Rules |
| --- | --- | --- |
| Entity | Has identity that persists across changes (Order #123) | Equality by ID; behaviour lives on it |
| Value object | Defined only by its values (Money, Address, DateRange) | Immutable; equality by value; validates itself on creation; replace instead of mutate |
| Aggregate root | Entity that guards an aggregate's invariants | Only entry point for changes |
| Domain event | Something that happened that domain experts care about | Past tense; immutable; carries IDs and the facts consumers need |
| Repository | Collection-like access to aggregates | Interface in the domain, implementation in infrastructure; returns whole aggregates |
| Domain service | Domain logic that doesn't belong to one entity | Stateless; named in domain language; use sparingly |
| Application service | Orchestrates a use case: load, call domain, save, publish | No business rules; handles transactions and authorization |

Prefer value objects over primitives for domain concepts: `Money(amount, currency)` instead of a bare decimal stops unit and rounding bugs (see the typescript-patterns skill for branded types in TS).

## Layering inside a context

```
api / adapters       -> HTTP controllers, message consumers, ACL translators
application          -> use cases: load aggregate, call method, save, publish events
domain               -> entities, value objects, domain events, repository interfaces
infrastructure       -> ORM mappings, repository implementations, broker clients
```

Dependencies point inward: the domain layer imports nothing from infrastructure or frameworks. Keep ORM annotations out of the domain where the stack allows it cheaply; if it doesn't, accept them but keep the rules in domain methods.

## Domain events in practice

- Raise events inside aggregate methods; publish them after the transaction commits. Use the transactional outbox so events and state changes can't diverge (see the event-driven-architecture skill).
- Distinguish internal domain events (inside a context) from integration events (published contract to other contexts). Integration events are versioned contracts; don't leak internal structure into them.

## Introducing DDD into an existing codebase

Don't rewrite. Move toward the model in small, behaviour-preserving steps (see the legacy-refactoring skill):

1. Write the glossary and context map for the area first; agree on them with the user or domain experts.
2. Put an anti-corruption layer around the legacy or external model you integrate with, so new code speaks the new language.
3. Extract value objects for concepts passed around as primitives (money, email, date ranges, identifiers). This is cheap and catches bugs immediately.
4. Move one invariant at a time from services or controllers into the entity that owns the data, and route all writes through that method.
5. Draw aggregate boundaries once invariants live on entities; split any transaction that modifies several aggregates, using domain events.
6. Extract a module or service per bounded context only after the code inside it no longer reaches into other contexts' tables or classes.

## Mapping contexts to deployment

| Situation | Map each context to |
| --- | --- |
| One team, one deployable, contexts still moving | A module/package in a modular monolith, with enforced boundaries |
| Contexts owned by different teams with different release cadence | Separate services, integrated by APIs and integration events |
| A generic subdomain (auth, email, payments) | A third-party service or library behind an anti-corruption layer |

Boundaries in code come first; a context that isn't separable as a module won't be separable as a service.

## Anti-patterns

- **Anemic domain model** - entities are bags of getters/setters and all rules live in services; invariants get enforced in some code paths and forgotten in others.
- **One model to rule them all** - a single `Customer` class shared by every team, with fields for everyone and rules for no one.
- **Aggregate = table** - mapping every table to an aggregate, or loading a whole object graph to change one field.
- **Multi-aggregate transactions** - updating several aggregates atomically "for convenience"; it creates contention and hides real consistency requirements.
- **Shared database between contexts** - integration through tables couples schemas; any change breaks another team.
- **DDD ceremony on CRUD** - repositories, factories and domain services for a settings page.
- **Technical names** - `OrderManager`, `DataProcessor`, `Handler2`; the code should read like the glossary.

## Done when

- A glossary exists per context, and code names match it.
- Bounded contexts and their relationships are drawn, with the context-map pattern named for each relationship.
- Each aggregate has its invariants listed, is changed only through its root, references other aggregates by ID, and is the only aggregate modified in its transactions.
- Cross-context integration happens through published APIs or integration events, never shared tables.
- Simple subdomains were deliberately left simple.
