---
name: domain-modeling
description: Models a business domain so code uses the business's words and enforces its rules - bounded contexts, invariants, aggregates. Triggers - code and business use different words, entity or value object, where do these business rules belong, DDD, bounded context, aggregate.
---

# Domain Modeling

When code and business speak different languages, every conversation needs
translation, and every translation loses a rule. The symptom is a codebase
where the same concept appears as `Customer`, `User`, `Account` and `Party`,
each slightly different, and where a business rule lives in four places that
have quietly diverged.

## When to use

- The domain has real rules (eligibility, pricing, state machines, compliance)
- The same noun means different things to different teams
- Business logic keeps leaking into controllers, jobs and UI
- You are about to split a system and don't know where the seams are

**When not to use:** CRUD over a handful of tables with no invariants, or a
thin integration layer. Modeling ceremony on a domain with no rules produces
indirection and nothing else.

## Step 1 — Language before structure

Collect the words the business actually uses, from them, in their order.
Write a glossary with one definition per term, agreed out loud.

Rules that make it real:

- **One term, one meaning, one context.** If "order" means a shopping cart in
  one place and a fulfillment job in another, those are two contexts, not one
  ambiguous term.
- **The code uses the glossary word.** Not a synonym, not an abbreviation. If a
  class is named something the business would not recognize, the model is wrong
  or the name is.
- **A term the business never says is a smell.** `OrderManager`, `DataHelper`,
  `ProcessorService` describe code mechanics, not the domain.

## Step 2 — Find the bounded contexts

A bounded context is a boundary inside which a term has exactly one meaning.

Detect them by listening for the same word carrying different data:

| Word | Sales context | Fulfillment context | Billing context |
|---|---|---|---|
| Order | Cart, discounts, upsells | Pick list, address, weight | Line items, tax, invoice state |

Three models, not one. Forcing them into a single `Order` class produces a
30-field object that is half-invalid in every use — the single most common
cause of unmaintainable domain code.

Between contexts, define the relationship explicitly: shared kernel (rare,
expensive), customer/supplier, anti-corruption layer (translate their model at
your edge — the default for anything external).

## Step 3 — Invariants first, structures second

An invariant is a rule that must **never** be false. Start here, not with class
diagrams.

> "An order cannot be shipped before it is paid."
> "Booked seats never exceed capacity."
> "A refund never exceeds the amount captured."

Each invariant must have exactly one place responsible for enforcing it. That
place is the aggregate.

## Step 4 — Building blocks

| Block | Test | Notes |
|---|---|---|
| **Value object** | Two with the same values are interchangeable; no identity; immutable | `Money`, `DateRange`, `EmailAddress`. Most primitives should be these. |
| **Entity** | Has identity that outlives its attribute values | `Order`, `Customer` |
| **Aggregate** | A consistency boundary: the unit that is saved and loaded together, enforcing an invariant | Keep them small |
| **Domain event** | A fact that happened, past tense, immutable | `OrderPlaced`, `PaymentCaptured` |
| **Domain service** | Behavior that belongs to no single entity | Rare; usually a missing value object |
| **Repository** | Collection-like access to aggregates | One per aggregate root, not per table |

### Aggregate sizing

The most consequential decision in the model.

- One transaction modifies **one** aggregate. If you need two, you either have
  the boundary wrong or you need eventual consistency between them.
- Reference other aggregates **by id**, not by object. Object references invite
  loading half the database.
- Small aggregates with eventual consistency beat large ones with lock
  contention, in every system that grows.
- If an aggregate has a collection that grows unboundedly (an order with 10,000
  lines, a customer with every event), the collection is a separate aggregate.

## Step 5 — Push rules inward

| Where a rule ends up | Why it's wrong |
|---|---|
| Controller / handler | Bypassed by every other entry point (job, CLI, admin) |
| Database constraint only | Enforced, but the reason is invisible and the error is unusable |
| Frontend validation only | Not enforcement at all |
| Scattered `if` statements | Diverges silently |

Rules live in the domain type that owns them, and are enforced at construction:
an object that exists is valid. **Make illegal states unrepresentable** — a
`Money` that cannot be negative, an `Email` that cannot be malformed, a state
machine that has no transition from `Cancelled` to `Shipped`.

## Anti-patterns

| Pattern | Cost |
|---|---|
| Anemic model (data class + service doing everything) | Rules scatter; the object guarantees nothing |
| One model for the whole company | Every field optional; validity is unknowable |
| Database schema as the domain model | Storage concerns leak into business rules |
| Primitive obsession (`string userId`, `float price`) | Nothing prevents passing the wrong string |
| Entity per table | Aggregates get sized by the ORM instead of by invariants |

## Exit checklist

- [ ] Glossary exists; the business recognizes every term in it
- [ ] Bounded contexts named, with the relationship between them stated
- [ ] External models are translated at the boundary, not adopted wholesale
- [ ] Every invariant has exactly one enforcing aggregate
- [ ] Aggregates reference each other by id
- [ ] No transaction spans two aggregates
- [ ] Domain types reject invalid construction
- [ ] No business rule lives only in a controller, job, UI or migration
