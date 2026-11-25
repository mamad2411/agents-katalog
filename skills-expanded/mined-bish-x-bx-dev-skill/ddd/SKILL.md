---
name: ddd
description: "Domain-Driven Design reference for AI coding agents. Strategic (bounded contexts, subdomain triage) + tactical (aggregates, value objects, repositories, domain events) patterns. Strangler Fig legacy preservation. Anti-Corruption Layer heuristics. Per-stack caveats (Python/TS/Go/Rust/mobile/data). Classification decision tree for per-Story architectural decisions. Use when Dev agent implements new business-logic code, refactors domain layer, or integrates with legacy systems. NOT for infrastructure/migrations/config/CRUD/throwaway code — see Section 15 for explicit non-applicability rules."
---

# Domain-Driven Design — Reference for AI Coding Agents

A per-Story reference. Read Section 2 first — the classification decides whether the rest of this document applies at all.

---

## 1. When to Use / When NOT to Use

### Apply when

- New business-logic code (new aggregate, new use-case, new domain service).
- Story mentions aggregates, entities, domain events, invariants, bounded contexts.
- Project's `CLAUDE.md` / `AGENTS.md` has a `## Domain` section or explicit DDD layering.
- Existing code is already DDD-shaped (folders named `domain/`, `application/`, `infrastructure/`; repositories as interfaces; aggregates with private state).
- Rewriting or extending a core-domain module whose correctness depends on business rules, not just data shuffling.

### Do not apply when

- Pure infrastructure (Docker, CI, Terraform, Helm, deploy scripts).
- Database migrations, schema tweaks, index adds.
- Configuration files, feature flags, environment bootstrapping.
- CRUD scaffolding with ≤2 real business rules per entity.
- PoC / MVP / throwaway script expected to live <6 months.
- Data pipelines, ML training code, notebooks.
- Frontend presentation layer (unless it owns a complex domain — rare; see Section 14).
- UI-heavy changes (styling, layout, copy tweaks).

### Does this project need DDD at all?

Seven-question checklist. If 3+ are "yes", DDD is worth the overhead.

1. Are there dense, non-trivial business rules that change on business (not technical) grounds?
2. Is a domain expert available and willing to talk about the model?
3. Is the project expected to live more than 12 months?
4. Does the model itself evolve for business reasons (new policy, new product line, regulatory shift)?
5. Do multiple teams or multiple people own overlapping parts of the codebase?
6. Are bugs in this area high-impact (financial, legal, safety, data integrity)?
7. Would a cleaner model confer real competitive advantage (faster feature turnaround, fewer cross-team collisions)?

2 or fewer "yes" → skip DDD. Use a simpler style (transaction script, CRUD, layered-lite). Forcing DDD here is cosplay, not architecture.

---

## 2. Architecture Classification — Decision Tree

**This is the most-referenced section.** Dev agent answers three questions at Step 0a of the workflow, picks one tag, writes it into the PR description / commit body. Classification is public — Reviewer can challenge it.

### The five tags (exact spelling — plugin re-pointers rely on these strings)

| Tag | Meaning | Behavior |
|---|---|---|
| **DDD-new** | New business-logic module or aggregate in a DDD-shaped project. | Apply full tactical patterns from Sections 5–10. |
| **DDD-existing** | Extending code that is already DDD-shaped. | Follow existing conventions. Do not re-architect. |
| **legacy-preserve** | Touching legacy (non-DDD) code. | Preserve style. Do not refactor toward DDD. See Section 3. |
| **non-domain** | Infra, migration, config, HTTP handler, UI, CI. | DDD not applicable. Ignore this document after classifying. |
| **too-small** | ≤5 lines, trivial bugfix, project <20 files, explicit PoC. | Skip DDD entirely. Do whatever is minimal and correct. |

### Three questions

**Q1 — Nature.** What is this code's job?

- Domain logic (rules, invariants, events) → continue to Q2.
- Application use-case (orchestration, transactions) → continue to Q2.
- Infrastructure (DB, HTTP, message bus, third-party client) → **non-domain**.
- Interface adapter (REST controller, CLI command, GraphQL resolver) → **non-domain**.
- Config, migration, script, one-off → **non-domain** or **too-small**.

**Q2 — State.** What does the surrounding code look like?

- Greenfield module in a DDD-shaped repo → continue to Q3.
- Existing DDD-shaped code → **DDD-existing**.
- Legacy (anemic services, fat controllers, ORM-as-model, no layering) → **legacy-preserve**.
- Project <20 files or explicit throwaway → **too-small**.

**Q3 — Locus.** Where exactly does the change land, and what style does that area use?

- **Extends an area of code that already exists** (new method in an existing file, new file in an existing module, new behavior attached to an existing service). Inherit the area's style:
  - Area is DDD-shaped (aggregates, value objects, repositories present) → **DDD-existing**.
  - Area is legacy (anemic services, fat controllers, procedural handlers, ORM-as-model) → **legacy-preserve**.
  - Mixed area — judge **per file** by the containing module (package / directory) of that file. If the Story touches files across multiple modules, each file carries its own style verdict; see "Multi-file Stories (polyglot PRs)" below for how to fold per-file verdicts into a primary tag + per-file exceptions.
- **Introduces a genuinely new domain concept that no existing area of this project covers** — a new aggregate type, a new bounded context, a new category of business rules — AND the project as a whole leans DDD → **DDD-new**. This is a narrow case. Creating a new file, by itself, is not enough to qualify.
- **Crosses a real semantic or ownership boundary** between new code and legacy — different ubiquitous language, different team, unstable legacy, transport/persistence leakage — see Section 11 (ACL). Stylistic difference alone is NOT a semantic boundary.

### Default extension rules (apply these FIRST, before the matrix)

These rules describe the most common case — extending existing code — and make the matrix a confirmation rather than the primary decision.

- **New method inside an existing file** → inherits that file's style. Do not introduce a DDD-shaped method into an otherwise anemic file; consistency beats local purity.
- **New file inside an existing directory** → follows the directory's majority style. A single new DDD file in a procedural directory is noise, not an improvement.
- **Extension of an existing service or module** → uses that module's patterns, even if they are anemic or procedural. The lift is "extend", not "rewrite".
- **Read-only pure-function legacy getters** → call directly from new code. No wrapper. No adapter. If it returns what you need and has no side effects, using it is correct.
- **A small domain subtlety can live next to legacy** → extracting a single `Money` value object is fine even when the surrounding code is procedural; you are not required to propagate DDD through the whole path.
- **Adding DDD-ish behavior to a legacy path** (e.g. emitting a domain event from a legacy service, extracting one Value Object from a legacy primitive, introducing one repository interface next to a fat controller) — stays `legacy-preserve`. Add the behavior in-place with minimal wrapping. Do NOT introduce a new outbox table, event-bus framework, handler registry, or full repository abstraction layer for a one-off emission. "We needed an event here" is not a mandate to DDD-ify the surrounding code.

Only when none of the above applies does the matrix drive the answer — and even then, prefer `DDD-existing` / `legacy-preserve` over `DDD-new` unless the four-part `DDD-new` gate under the matrix is clearly satisfied.

### Answer matrix

| Q1 Nature | Q2 State | Q3 Locus | Tag |
|---|---|---|---|
| Domain / application | Any | Extends existing DDD area | **DDD-existing** |
| Domain / application | Any | Extends existing legacy area | **legacy-preserve** |
| Domain / application | DDD-leaning project | Genuinely new domain concept, no existing area covers it | **DDD-new** |
| Domain / application | Any | Cross-boundary integration with real semantic/ownership boundary | See Section 11 (ACL) |
| Infra / interface | Any | Any | **non-domain** |
| Any | Tiny / PoC | Any | **too-small** |

**Default bias — inherit the existing area's style.** `DDD-new` is the exception, not the default. Adding a new method, a new file, or a new small module inside an existing area (legacy or DDD-shaped) does NOT justify `DDD-new` on its own. Pick `DDD-new` only when all four hold:

1. The Story introduces a genuinely new domain concept.
2. No existing area of the project covers that concept.
3. The project as a whole leans DDD (majority of touched areas are DDD-shaped) **OR — for greenfield projects with no existing code** — DDD is the deliberate architectural choice, documented in the project's `CLAUDE.md` / `AGENTS.md` / `ARCHITECTURE.md`.
4. Applying DDD here will NOT require wrapping stable legacy in ACL adapters to make the DDD island hermetic. If it will — the honest classification is `legacy-preserve` (extend in legacy style) or `DDD-existing` with a very small, focused ACL (see Section 11).

An unnecessary `legacy-preserve` costs one read of Section 3. An unnecessary `DDD-new` costs days of over-engineering, multiple forced ACL adapters around stable legacy, and a reviewer fight. The asymmetry means: **when uncertain, lean to `legacy-preserve` or `DDD-existing`, not to `DDD-new`**.

### Multi-file Stories (polyglot PRs)

When one Story touches files that would naturally receive different tags — a backend domain file, a DB migration, a frontend Redux slice, a monitoring dashboard — classify by the **primary touched area**: the largest diff volume in domain or application code. Infra / config / migration / monitoring / generated / auto-scaffolded files receive `non-domain` regardless of the primary tag, and you read NO DDD sections for them even when the primary tag is `DDD-new` or `DDD-existing`. If two domain areas in different languages are both significantly touched (e.g. backend Python domain + frontend TS domain) and they have different stacks, use the backend primary tag for backend files and apply Section 14 "Per-Stack Caveats" for the frontend files (frontend usually `legacy-preserve` or `non-domain` per §14 guidance).

### Reporting rule

Dev writes the classification into the first Lead message: `Classification: <tag>` and a one-line justification. The tag flows into the PR description and commit body. Reviewer may challenge; if challenged, re-run the tree and document the final answer.

### Strategic context — Khononov subdomain triage

Classification tags above are **tactical** (per-Story). They map loosely to **strategic** subdomain types from Khononov's "Learning DDD" (2021), but not 1:1:

- **Core subdomain** — where the business differentiates. Strong candidate for **DDD-new** / **DDD-existing**. Full tactical patterns.
- **Supporting subdomain** — necessary but not differentiating. DDD-lite or CRUD with light domain types. Often **DDD-existing** or **legacy-preserve** (do not over-invest).
- **Generic subdomain** — solved problems (auth, billing integration, notifications). Usually **non-domain** wrappers around off-the-shelf solutions.

If the Story text does not say which subdomain it lives in, ask. Wrong subdomain triage causes wasted DDD investment on supporting/generic code.

---

## 3. Strangler Fig — Legacy Preservation Rules

The **invariant**:

> **Legacy = any code that existed before this Story started. Never refactored toward DDD, even if obviously bad. Strangle by addition and replacement of whole capabilities, not by in-place reshaping.**

### Hard rules for `legacy-preserve` scope

- **Never rename** existing types, files, modules, functions, DB columns, API routes.
- **Never move files** into a `domain/` or `application/` folder.
- **Never extract Value Objects** from primitive fields in legacy. `order.customer_email: str` stays a string.
- **Never add DDD decorators / base classes** (`@aggregate_root`, `class Entity:`) to legacy types.
- **Never refactor anemic legacy services** into domain-rich aggregates inside this Story.
- **Never add layering** (ports/adapters, repository interfaces) to a legacy subsystem you are only touching tangentially.
- **Never split a legacy file** because it is too long.
- **Never reshape legacy tests** toward Given/When/Then just because you edited one line near them.
- **Never invent new test infrastructure (fixtures, conftest additions, helpers, mocks-factories, `pytest_plugins` entries) for a single Story.** If the Story's tests need a fixture that does not exist, match the conventions of neighboring test files — use direct object/dict manipulation, in-line setup, or existing fixtures. If NO existing pattern fits, raise it to the Lead as a scope question, do not invent infrastructure unilaterally. Introducing new test infra for one Story creates a slow-to-decay architectural debt: future tests either cargo-cult the new pattern or continue using the old, causing bifurcation. (See also §2 "Default extension rules" — adding DDD-ish behavior to a legacy path stays `legacy-preserve`; the same spirit applies to test plumbing.)
- **Never wrap every legacy call** in an ACL. See Section 11 — ACL only when warranted.

### What you may do in `legacy-preserve` scope

- Add a new function / method that matches the surrounding style.
- Fix the specific bug described in the Story.
- Add tests for the change you just made (in whatever test style the legacy code already uses).
- Add a deprecation comment (`# deprecated — use NewXService for new code`) only if the Story explicitly asks.

### If a reviewer flags legacy as "not DDD"

Out of scope for this Story. Reply with: "Classification is `legacy-preserve`. Refactor toward DDD is a separate Story — file it and continue." Do not negotiate this at review time. Negotiate at planning time.

### Healthy-termination warning

Strangler Fig only works if the legacy shrinks over time. It fails when new features keep flowing into legacy and the "new" side never takes over. Thoughtworks' retrospectives on this pattern identify two common failure modes:

1. **Routing / facade layer becomes its own monolith.** The shim meant to route calls between old and new grows until it is itself a legacy system.
2. **Indefinite coexistence.** Old and new run in parallel forever; teams lose track of which is canonical.

Each `legacy-preserve` classification implicitly carries a sunset responsibility — someone, eventually, writes the Story that kills the legacy path. That Story is not this one.

### Fowler's guidance — cut vertically by capability

Slice the strangle along business capabilities (whole features moved across), not along technical layers (all repositories first, then all services). Vertical cuts keep the system always-shippable. Horizontal cuts produce half-migrated systems that cannot be rolled back cleanly.

### Common reviewer trap

A reviewer sees a legacy file edited in the diff and says "while you're there, clean it up". Politely refuse. The edit is the minimum change. Cleanup is a different Story with different risk.

---

## 4. Ubiquitous Language

One term = one meaning inside one bounded context. Terms come from the **domain expert**, not from the engineer's intuition. Code matches the vocabulary letter-by-letter.

### Rules

- If the business says "shipment", the class is `Shipment`, not `Delivery`, `ShippingRecord`, or `OrderLineDispatch`.
- If the language is not English, preserve it. Russian "накладная" becomes `Nakladnaya`, not `Invoice`, not `BillOfLading`. Translation loses meaning and creates two vocabularies (the business's and the code's).
- Method names read as sentences in the domain language: `order.confirm()`, `account.withdraw(amount)`, `shift.handOver(to: other)`.
- Avoid technical suffixes in domain names: not `OrderManager`, `OrderHelper`, `OrderProcessor` — just `Order` (aggregate) or a verb-named service (`PlaceOrderService`).

### Phrase test — context boundary detector

If a domain term requires qualification ("which kind of order?", "whose customer?", "shipping as in outbound or inbound?"), it lives in **more than one bounded context**. Draw the boundary; pick a name per context.

Example:
- `Order` in the **sales context** = a customer's intent to buy.
- `Order` in the **fulfilment context** = a work instruction for the warehouse.

Two models, two classes, two ubiquitous-language entries. Translation between them is an integration concern (Section 11).

### Working with the glossary

- Every bounded context has a living glossary (a `GLOSSARY.md` in the module, or a section in the README).
- New term introduced in code without a glossary entry → reviewer challenge.
- Term changed in glossary without code rename → out-of-sync → file a Story.

---

## 5. Value Objects

### Defining properties

- **Immutable.** No setters, no in-place mutation. Idiomatic per language: frozen dataclass, readonly class, record, struct with private fields.
- **Equality by value.** Two `Money(100, "USD")` are equal; no identity field.
- **Self-validating.** Constructor rejects invalid states. `Email("not-an-email")` raises at creation, not at use.
- **Whole replacement.** `price = price.add(tax)` returns a new VO; the old one is unchanged.
- **Side-effect-free behavior.** Methods compute and return new VOs, never mutate.

### Common candidates

- Money (amount + currency).
- Email, PhoneNumber, Url, PostalCode.
- DateRange, TimeSlot, Period.
- Address, Coordinate, GeoBox.
- Typed IDs — wrap a UUID/int in `UserId`, `OrderId`. Known as the **newtype pattern**. Prevents `save_user(order_id)` type errors.
- Quantity + Unit (weight, length, volume — never a bare float).

### Python example

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("amount must be non-negative")
        if len(self.currency) != 3 or not self.currency.isupper():
            raise ValueError("currency must be ISO 4217 (e.g. USD)")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)
```

### TypeScript example

```ts
export class Email {
  private constructor(public readonly value: string) {}

  static of(raw: string): Email {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(raw)) {
      throw new Error(`invalid email: ${raw}`);
    }
    return new Email(raw.toLowerCase().trim());
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}
```

### Anti-cues (do not do)

- Public setters on a VO.
- A VO with an `id` field — that is an Entity, not a VO.
- Mutating methods: `money.add(tax)` that changes `money` in place.
- Framework-coupled VOs: a VO that imports SQLAlchemy, Django ORM, or a JSON schema library.

---

## 6. Aggregates

An **aggregate** is a cluster of objects treated as a single unit for mutation and consistency. The **aggregate root** is the only external entry point.

### Rules

- **Single root.** External code holds a reference to the root, never to children.
- **Mutations through the root.** `order.addLine(...)`, never `order.lines.append(...)` from outside.
- **Invariants always hold** after any public operation on the root. If the root cannot enforce an invariant, the boundary is wrong.
- **1 transaction = 1 aggregate.** Atomic mutation of two aggregates in one transaction is forbidden. If the domain seems to require it, either redraw boundaries, or model the second effect as a domain event handled eventually (Section 9).
- **Cross-aggregate reference by ID only.** `order.customerId: CustomerId`, never `order.customer: Customer`.
- **Small is better.** Vernon's heuristic: prefer small aggregates. A 500-line aggregate usually hides two aggregates.
- **Factory** — when aggregate construction is non-trivial (requires cross-aggregate data, policy checks, multi-step assembly, or must enforce multiple invariants at once), place construction in a dedicated `Factory` object or a static `create_*` method on the aggregate. This keeps the aggregate's constructor simple and makes construction policy explicit. A plain constructor is still the default; reach for a Factory only when construction logic starts polluting the caller. (Evans ch. 6.)

### Consistency boundary

Inside an aggregate: strong consistency. Every invariant holds at the end of every operation.

Across aggregates: eventual consistency. A domain event fires, a handler updates the other aggregate in its own transaction. No distributed transaction, no saga as a "hidden single transaction".

### Concurrency — aggregate version

Aggregates use an integer **version** field on the root, incremented on each save. Repositories check version-on-load vs version-on-save; mismatch raises `ConcurrentModificationError` / `OptimisticLockError`. This is the DDD-standard optimistic-lock pattern (Vernon, ch. 10).

Without it, two concurrent mutations silently overwrite each other — the aggregate boundary no longer guarantees consistency in the presence of concurrent writes. ORMs often provide this (SQLAlchemy `version_id_col`, Hibernate `@Version`, Django `select_for_update` + application-level check). If your ORM doesn't, add a `version` column and check-and-increment in the repository `save()`.

Pessimistic locking (SELECT FOR UPDATE) is the fallback when business requires serializable behavior, but it scales worse. Default to optimistic.

### Before / after — god-aggregate refactor

**Before (god aggregate):**

```python
class Order:
    lines: list[OrderLine]
    customer: Customer          # full aggregate nested
    shipping_address: Address
    payment_method: PaymentMethod
    invoices: list[Invoice]     # each invoice has its own lifecycle

    def pay_invoice(self, invoice_id):
        ...   # mutates self.invoices AND self.customer.balance
```

Problems: two lifecycles in one aggregate, two transactions pretending to be one, lock contention on `Order` when only `Invoice` is changing.

**After (two aggregates + ID link):**

```python
class Order:
    id: OrderId
    customer_id: CustomerId
    lines: list[OrderLine]
    shipping_address: Address
    payment_method: PaymentMethod
    # invoices are a separate aggregate

class Invoice:
    id: InvoiceId
    order_id: OrderId
    amount: Money
    status: InvoiceStatus

    def pay(self, payment: Payment) -> InvoicePaid:
        self._ensure_not_already_paid()
        self.status = InvoiceStatus.PAID
        return InvoicePaid(invoice_id=self.id, order_id=self.order_id, at=now())
```

`InvoicePaid` is a domain event (Section 9). A handler in the customer bounded context subscribes and updates customer balance in a separate transaction.

### Common mistakes

- Nesting full aggregates instead of IDs (causes eager-loading, transaction bloat, consistency illusions).
- Modifying two aggregates in one use-case "because it's simpler" — this is the most common source of silent corruption.
- Making the aggregate root expose children directly (`order.lines`) as a mutable list, so callers bypass invariants.
- One huge aggregate per module because "it's all related" — relation is not the same as consistency need.

---

## 7. Repositories

A **repository** gives the domain access to aggregates without leaking persistence concerns.

### Rules

- **Interface in the domain layer, implementation in infrastructure.** Domain depends on an abstraction it owns.
- **Works with whole aggregates.** `save(order: Order)`, not `save_order_lines(...)` or `update_order_status(...)`.
- **Methods named in domain terms.** `OrderRepository.find_unpaid_for_customer(customer_id)`, not `OrderRepository.find_by(field="status", value="unpaid")`.
- **One repository per aggregate root.** No `OrderLineRepository` — you never load an order line alone.
- **No lazy loading across aggregate boundaries.** If you need related data from another aggregate, load it via its own repository.
- **Returns domain objects, not ORM entities / DTOs / rows.** If your ORM entity doubles as the domain object, Section 13 (anti-patterns) applies.

### Minimal interface — Python

```python
from typing import Protocol

class OrderRepository(Protocol):
    def get(self, order_id: OrderId) -> Order: ...
    def save(self, order: Order) -> None: ...
    def find_unpaid_for_customer(self, customer_id: CustomerId) -> list[Order]: ...
```

Implementation lives in `infrastructure/persistence/sqlalchemy/order_repository.py`. It translates between ORM rows and the `Order` aggregate. The domain never sees SQLAlchemy types.

### Query-heavy reads

If the use-case needs a complex read that does not map to an aggregate (dashboard, search, report), do **not** force it through the repository. Use a dedicated read model / query service (CQRS-lite). Keep repositories for write-side aggregate loading.

### Common mistakes

- **Generic repository** (`Repository<T>.findBy(field, value)`) — hides intent, couples the domain to generic query DSL, invites misuse.
- **Repository returning ORM rows or DTOs** — leaks persistence into the domain.
- **Repository on a child entity** — signals that the child should be a separate aggregate or that the parent aggregate is too large.
- **Repository with business logic** (`order_repo.mark_as_shipped(id)` that decides when "shipped" is valid) — that logic belongs on the aggregate.

---

## 8. Domain Services

A **domain service** is a stateless operation that genuinely spans multiple aggregates, or requires external domain data, and does not fit as a method on any single aggregate.

### Rules

- **Stateless.** No fields, no per-instance data.
- **Domain-language name.** Noun-verb, matching vocabulary: `FundsTransferService`, `RoutePlanner`, `PricingService`. Not `OrderManager`, `OrderHelper`.
- **Lives in the domain layer.** Same dependency rules as aggregates: no framework imports, no ORM, no HTTP.
- **Small.** A domain service with 2000 lines is an anemic-model smell — the logic belongs back on the aggregates.

### Correct example — funds transfer

```python
class FundsTransferService:
    def transfer(self, source: Account, target: Account, amount: Money) -> Transferred:
        source.withdraw(amount)        # invariant: non-negative balance
        target.deposit(amount)         # invariant: currency match
        return Transferred(source.id, target.id, amount, at=now())
```

The use-case orchestrates two aggregates. Neither `Account` alone owns the transfer. The service is the right home.

### When it is NOT a domain service

- A 2000-line class called `OrderService` with methods like `createOrder`, `updateStatus`, `calculateTotals`, `sendConfirmation` — that is a god service. Split:
  - Creation / mutation → methods on the `Order` aggregate.
  - Side-effects (email, audit) → application layer or event handlers.
  - Cross-aggregate operations → small, focused domain services.

### Domain service vs application service

- **Domain service** — domain logic, in the domain layer. No framework, no transaction management.
- **Application service** (Section 10) — orchestration, in the application layer. Opens transactions, calls repositories, dispatches events.

Confusing the two leads to business rules leaking into the application layer.

### Specification pattern (Evans ch. 9)

Encapsulate a business rule as a first-class object — `OrderIsOverdue.isSatisfiedBy(order) -> bool` — when the same boolean business question appears in multiple places (aggregate method, repository query, validation, UI filter). Three uses:

1. **Validation** — "is this aggregate in a state where X is allowed?"
2. **Selection** — repositories expose `find_satisfying(spec)` instead of a dozen `find_by_*` methods.
3. **Building** — specs compose via `and_ / or_ / not_` for complex predicates.

A Specification is NOT the right answer when:
- The rule appears in one place (just write the `if`).
- The rule needs translation to SQL/NoSQL — specs with DB-native compilation are powerful but require a compiler layer (Vernon ch. 9 has an example); not worth it for a single query.

Default to inline `if`; escalate to Specification only when duplication forces it.

---

## 9. Domain Events

A **domain event** records that something meaningful happened in the domain. Past tense. Immutable. Part of the ubiquitous language.

### Rules

- **Past tense names.** `OrderPlaced`, `PaymentReceived`, `SpeakerMappingConfirmed`. Not `PlaceOrder`, `ReceivePayment`, `ConfirmMapping` (those are commands).
- **Immutable value object.** Fields: stable event id, timestamp, aggregate id, minimal payload. No references to ORM rows or live aggregates.
- **Published after commit, never before.** If the transaction rolls back, the event must not exist.
- **Part of the ubiquitous language.** Discuss event names with the domain expert. Bad event name = misaligned model.
- **Small payload.** Include only what subscribers need to make decisions. If subscribers need more, they look it up by id.

### Dispatch patterns

| Pattern | Use when | Cost |
|---|---|---|
| **In-process dispatcher** | Monolith, single process, no durability requirement. | Simple. Lost on crash between commit and dispatch. |
| **Transactional Outbox** | Distributed system, durability required, at-least-once delivery. | Extra table, relay process, idempotent handlers. |
| **Event bus (Kafka/NATS/RabbitMQ)** | Cross-service integration. | Infra ownership. Usually downstream of an outbox, not replacing it. |

Two failure modes to avoid:

1. **Publish before commit.** Subscriber acts on an event for a transaction that later rolled back.
2. **Publish and commit separately without outbox.** Transaction commits, process crashes, event never leaves — silent divergence.

### Event vs command

- **Command** — "do this" — imperative, may be rejected. Lives at the application boundary.
- **Event** — "this happened" — past tense, cannot be rejected (you cannot un-happen a fact).

### Event Storming — brief

A workshop format where domain experts and engineers map the domain as a timeline of events on orange sticky notes, then cluster events into aggregates and bounded contexts. Useful at project start or before a major re-modelling. Not a per-Story activity.

### Scope — not covered by this skill

This skill covers **state-based aggregates** (current state stored in tables/rows), **in-process domain events** dispatched after commit, and the **transactional outbox** pattern for durable event delivery.

Out of scope:
- **Event Sourcing** (store events as primary source of truth, rebuild state from event stream). See Vernon ch. 8 if a Story explicitly asks for it.
- **Full CQRS** (separate write-model aggregates and read-model projections with their own schemas). See Fowler's CQRS write-up. A lightweight read model (separate query repository, no projection machinery) is fine and does not count as "full CQRS".

Do NOT introduce either without an explicit Story requirement. Both add significant operational complexity — event replay, projection rebuilding, eventual consistency handling, schema evolution across event versions — that a Story-level change cannot absorb.

---

## 10. Application Layer

The application layer orchestrates use-cases. It is thin. It contains **no business rules**.

### Shape of a use-case

1. Start a transaction.
2. Load the aggregate(s) via repository.
3. Invoke a single method on the aggregate root.
4. Save via repository.
5. Commit the transaction.
6. Dispatch events (outbox or in-process).
7. Translate domain exceptions into application-level results.

### Rules

- **No `if`-about-business.** If you see `if order.status == "paid"` in the application layer, move that logic to `Order.ship()` as an invariant.
- **One use-case = one transaction = one aggregate mutation.** Multi-aggregate coordination uses events.
- **Stateless between calls.** No per-request fields on the service.
- **Translates domain exceptions to results.** Returns `Result.failure("insufficient funds")` or raises an application-level exception. Not HTTP status codes — that is the interface layer's job.
- **Owns transaction boundaries.** The domain does not know transactions exist.
- **Authorization lives here, not on the aggregate.** The aggregate enforces business invariants (what is a valid state transition); the application service enforces policy (is THIS caller allowed to call this use-case?). Pass the `Principal` / `User` / caller identity into the use-case constructor or method; the use-case decides by policy. An aggregate that asks "can this user do this?" has swallowed a concern that doesn't belong to it.

### Python sketch

```python
class PlaceOrder:
    def __init__(self, orders: OrderRepository, uow: UnitOfWork, events: EventBus):
        self._orders = orders
        self._uow = uow
        self._events = events

    def __call__(self, cmd: PlaceOrderCommand) -> OrderId:
        with self._uow:
            order = Order.create(customer_id=cmd.customer_id, lines=cmd.lines)
            self._orders.save(order)
            self._uow.commit()
        for evt in order.pull_events():
            self._events.publish(evt)
        return order.id
```

The aggregate collects events during mutation (`pull_events()` drains them). Events are dispatched only after commit.

### Anti-shape

```python
class PlaceOrder:
    def __call__(self, cmd):
        if cmd.customer_id in self._blocked_customers:      # business rule in app layer
            raise ForbiddenError()
        order_row = self._db.insert("orders", ...)           # persistence leaking up
        if order_row.total > 10000:                          # business rule in app layer
            self._notify_finance(order_row)
        return order_row.id
```

Problems: business rules outside the aggregate, persistence types leaking into application, notification is a side effect of a business fact and should be driven by an event.

---

## 11. Anti-Corruption Layer — When Needed, When Not

An **Anti-Corruption Layer (ACL)** is deliberate isolation between two models that use different vocabularies, have different ownership, or have different stability guarantees. **It is not the default.** It has real cost — extra code, extra latency, extra tests, extra monitoring, extra CI time. Reach for it only when you can point to a concrete reason.

### Default: call legacy directly

Stable, well-named legacy code is a resource, not a problem. New code may call it directly with a one-line conversion if needed. Architectural consistency between new and legacy is NOT a reason to wrap — that is the crutch this section exists to prevent.

### Reasons that warrant an ACL (pick the one that applies, write it as a comment on the ACL class)

1. **Different ubiquitous language.** Legacy says `User`, new domain says `Account`, and the semantic difference is real — different identity rules, different lifecycle, different invariants.
2. **Different team ownership.** Legacy changes without coordination; you need a buffer so their refactor does not ripple through your domain.
3. **Known instability or planned replacement.** Legacy is on a sunset path; ACL isolates the blast radius of the upcoming swap.
4. **Transport / persistence leakage.** Legacy returns ORM rows, HTTP response envelopes, proto messages, or anything carrying infrastructure concerns that would poison your domain model if imported directly.

Any one of those four is enough. Without at least one, do NOT build an ACL.

### Reasons that do NOT warrant an ACL (common traps)

- *"New code is DDD-shaped and I want type-uniformity."* Cosmetic. Use a one-line converter or just accept the shape difference.
- *"I call the legacy function from several places, DRY says wrap."* Extract a plain helper. A helper is not an ACL.
- *"Legacy returns a tuple, my new code uses a dataclass."* One-line conversion, inline. Not an ACL.
- *"Nearby new code is DDD so I should isolate."* This is the crutch. Extending legacy in legacy style is the correct answer when the legacy is stable and well-named.
- *"I want future-proofing in case legacy changes someday."* Speculative. Add the ACL when the change is real, not when it is imagined.

If you catch yourself writing an adapter because "DDD requires it" — stop. DDD does not require wrapping stable, clear, well-named legacy calls. Extending functionality in legacy style is a valid and often preferred answer.

### Sanity check before writing an ACL

Even when one of the four warrant-reasons applies, verify the ACL is not overkill. If ALL four below are true, you are probably overbuilding:

1. Legacy function is stable — `git log -- <path>` shows no meaningful churn in the last 3 months.
2. Call surface is small — ≤ 2 legacy functions, ≤ 3 call sites in the new code.
3. Mapping is trivial — 1:1 fields or ≤ 3 lines without business logic.
4. No real semantic model difference — you are shuffling fields between representations of the same concept.

Under those conditions, a direct call (with a one-line conversion at the call site) is correct. Revisit the "warrant-reasons" list and confirm one truly applies before proceeding.

### What is NOT an ACL

A 5-line DTO mapper is **not** an ACL; it is a mapper. ACLs translate between **semantic models** — different vocabularies, different invariants, different ownership. Mappers translate between representations of the same model.

```python
# NOT an ACL — just a mapper
def to_dto(order: Order) -> OrderDTO:
    return OrderDTO(id=str(order.id), total=float(order.total.amount))
```

```python
# IS an ACL — bridges two models with different vocabularies and transport leakage
class LegacyBillingClient:
    def charge(self, customer: Customer, amount: Money) -> ChargeResult:
        raw = self._legacy.billing.do_charge({
            "cust_id": customer.id.value,
            "amt": int(amount.amount * 100),
            "ccy": amount.currency,
        })
        return self._parse(raw)  # returns a domain ChargeResult
```

### Framing — why ACLs exist

ACLs exist to let two models evolve independently. Without one, changes on the legacy side propagate into the new domain as type changes, naming changes, and invariant leaks. With one, the new domain sees a stable interface shaped by its own language.

The decision is **deliberate isolation vs acceptable coupling**. Both are valid. The cost of unnecessary ACL is over-engineering and reviewer churn. The cost of missing one is domain corruption. Use the warrant-reasons above to pick the side deliberately.

### Cost of an ACL (so you feel it before you write one)

- Extra code to maintain (ACL class, tests).
- Extra latency — usually small, one indirection.
- Contract tests against the legacy side (else the ACL drifts silently).
- Monitoring for translation errors.
- CI time for the above.

When the cost exceeds the benefit, skip it. AWS well-architected guidance, Microsoft Azure Architecture Center, and DDD practitioner consensus all converge: ACL is a targeted pattern, not a default.

---

## 12. Testing Domain Invariants

### Tests express invariants, not method coverage

- **Bad:** `test_service_calls_repo_save` — asserts that a mock was called. Verifies the test setup, not the behavior.
- **Good:** `test_cannot_cancel_shipped_order` — asserts a business rule. Fails if the rule is broken.

### Given / When / Then naming

One test, one invariant, three sections:

```python
def test_given_shipped_order_when_cancel_then_rejected():
    # Given
    order = make_order(status=OrderStatus.SHIPPED)
    # When / Then
    with pytest.raises(CannotCancelShippedOrder):
        order.cancel()
```

### Layer targets

| Target | Test style | Dependencies |
|---|---|---|
| Value Object | Unit, pure | None |
| Aggregate | Unit, pure | None (no DB, no mocks for domain logic) |
| Domain Service | Unit, pure | None for domain logic; fakes if external domain data needed |
| Application Service | Integration OR unit with fake repos | Fake repository (in-memory), fake event bus |
| Repository | Integration with **real DB** | Real DB (testcontainers, ephemeral schema) |
| Controller / HTTP | Integration or contract test | Test client, full stack |

### Mocks vs real DB — repository tests

**Use a real database** for repository integration tests. Mocking the ORM or the SQL layer produces mock/prod divergence: the test passes, production breaks on a type or constraint the mock never enforced. Testcontainers, Docker-backed Postgres, or an ephemeral SQLite (when the dialect matches) are all acceptable. The mock-database is not.

### Architecture tests

Automate layering rules so reviewers do not have to police them manually:

- **Python**: `import-linter` — declare layer contracts (`domain` must not import `infrastructure`).
- **Java / Kotlin**: ArchUnit — layer, package, and dependency checks.
- **TypeScript**: `dependency-cruiser`, `eslint-plugin-boundaries`.
- **Go**: `go-cleanarch` or custom `go vet` rules.
- **C#**: NetArchTest.

These tests run in CI. If the dependency graph drifts, the build fails. Free enforcement.

### What to test per layer

- **VO**: constructor rejects invalid input; equality; behavior methods return correct new VOs.
- **Aggregate**: each invariant has at least one passing and one failing test; each public method either returns an event or raises a domain exception.
- **Domain service**: cross-aggregate coordination yields correct events and correct state on each aggregate.
- **Application service**: given a command, the right aggregate method is called and the right event is dispatched. Use fakes for repository and event bus.
- **Repository**: load → mutate in memory → save → reload → state matches. Round-trip against a real DB.

### Property-based tests for VOs

VOs are pure and total — perfect for property-based testing:

```python
from hypothesis import given, strategies as st

@given(st.decimals(min_value=0, max_value=1_000_000), st.decimals(min_value=0, max_value=1_000_000))
def test_money_addition_is_commutative(a, b):
    m1, m2 = Money(a, "USD"), Money(b, "USD")
    assert m1.add(m2) == m2.add(m1)
```

---

## 13. Anti-Patterns Catalog

| Pattern | Symptom | Fix |
|---|---|---|
| Anemic Domain Model | Entities are plain data bags; all logic lives in services. | Move logic onto entities; services only orchestrate. |
| God Service | `OrderService` with 1000+ lines, every use-case. | Split by use-case or push logic onto the aggregate. |
| Leaky Repository | Repo returns ORM entities or DTOs. | Repo returns domain aggregates only; translate at the edge. |
| Cross-aggregate transaction | One transaction mutates two aggregates. | Redraw boundaries, or use events + eventual consistency. |
| Generic Repository | `Repository<T>.findBy(field, value)`. | Replace with intent-named methods per aggregate. |
| Premature Bounded Contexts | Five contexts on day one, shared nothing. | Start with one; split when language diverges. |
| ORM Entity mis-used as VO | `@Entity` class with `id` used for equality where value equality is needed. | Introduce a real VO; keep the ORM entity for persistence. |
| Present-tense event name | `ConfirmMapping`, `PlaceOrder`. | Rename to past tense: `MappingConfirmed`, `OrderPlaced`. |
| Domain imports framework | `from sqlalchemy import ...` in `domain/`. | Push the import to infrastructure; domain is plain Python / TS / Go. |
| Oversized aggregate | One aggregate with dozens of collections, multiple independent lifecycles. | Split along consistency boundaries; link by ID. |
| Public setters on Entity | `order.status = "shipped"` from outside. | Replace with intent methods (`order.ship(tracking_number)`). |
| Lazy loading across aggregate boundary | Accessing `order.customer.loyalty_tier` triggers a DB query. | Load the other aggregate explicitly by ID; no implicit traversal. |
| Repository on child entity | `OrderLineRepository`. | Remove; load lines via `Order` only. |
| VO with identity | Value Object has `id: UUID`. | Either make it an Entity, or drop the id. |
| Business rule in application layer | `if order.total > 10000: notify_finance()`. | Move the rule to the aggregate; application only orchestrates. |
| "Manager" / "Helper" class | `OrderManager`, `OrderUtils`. | Rename to verb-named service or push methods onto the aggregate. |
| Event published before commit | Subscriber fires before transaction commits. | Collect events, publish after commit (outbox or post-commit hook). |
| DTO-everywhere mapper called "ACL" | Two-line field rename labeled as Anti-Corruption Layer. | Call it a mapper. Use ACL only when Section 11 triggers apply. |
| Strangle fig with indefinite coexistence | New and legacy both accept writes forever. | Set a sunset date; file the cutover Story. |
| Ubiquitous Language translated to English by default | `Nakladnaya` renamed to `Invoice` because English feels "professional". | Preserve original vocabulary; translation loses meaning. |

---

## 14. Per-Stack Caveats

Patterns are universal; idioms are not. Match the language.

### Python

- **FastAPI is neutral.** Keep route handlers thin. Pydantic models live at the HTTP boundary (request / response), not inside the domain. Converting Pydantic ↔ domain happens in the interface layer.
- **Django clashes with DDD.** The ORM uses ActiveRecord — the model class is both the domain type and the persistence type. Real DDD on Django requires explicit conversion in repositories (Django model ↔ domain aggregate). It is expensive. Alternatives: accept the ActiveRecord style and do DDD-lite, or pick SQLAlchemy / pure repositories if the project is DDD-serious.
- **SQLAlchemy works cleanly** with DDD when used in imperative-mapping mode (classical mappers). Domain classes stay pure; mapping lives in infrastructure.
- **VOs** — use `@dataclass(frozen=True)` or `pydantic.BaseModel` with `model_config = {"frozen": True}`. Prefer `dataclass` inside the domain (no runtime dependency on Pydantic).
- **Typed IDs** — `NewType("UserId", uuid.UUID)` for lightweight, or a small frozen dataclass for self-validating.
- **Architecture tests** — `import-linter` with a layers contract.

### TypeScript

- **Backend (Nest.js, Express, Fastify, Hono)** — DDD works cleanly. Nest.js's module system maps onto bounded contexts naturally. Use `readonly` classes + `equals` for VOs. Prefer classes over plain objects for aggregates (behavior belongs on the type).
- **Frontend (React)** — DDD is usually the wrong frame. Use **Vertical Slice** or **Feature-Sliced Design**. Redux + DDD architecturally conflict: Redux stores flat serializable state and pure reducers; DDD aggregates hold behavior and enforce invariants in-place. Reconciling them is fighting both. Prefer one or the other.
- **Frontend DDD is sometimes right** — complex offline-first apps with their own consistency model, games with complex state machines, canvas/D3-heavy apps with real domain logic (CAD-lite, map editors). Rare.
- **VOs** — readonly class with static factory, private constructor, `equals` method. No primitive obsession — `new PhoneNumber(raw)` not `string`.
- **Architecture tests** — `dependency-cruiser`, `eslint-plugin-boundaries`.

### Go

- **Go does not want Java-style DDD.** The community rejects deep class hierarchies, getters/setters, and event-sourcing-by-default. Three Dots Labs' "DDD Lite in Go" is the canonical shape:
  - Structs with **unexported fields** and behavior-oriented methods.
  - **Constructors that validate** and return `(Type, error)`.
  - **Repository interfaces** in the domain package, concrete in infrastructure.
  - **DB-agnostic domain types** — no `gorm` tags in the domain.
- No aggregate base class, no framework, no magic. Just structs with invariants.
- Event-sourcing exists but is not the default. Reach for it only when history is the domain.
- **VOs** — small structs, value receivers, no setters. Named types on primitives (`type UserID string`) give the newtype pattern.
- **Architecture tests** — `go-cleanarch` or custom tests parsing imports.

### Rust

- **Newtype pattern is a VO by default.** `struct Email(String)` with a private field and a public `try_new` enforces invariants at the type level.
- `#[derive(PartialEq, Eq)]` gives value equality for free.
- **Ownership aligns with aggregate boundaries** — the borrow checker enforces at compile time what DDD enforces at design time (no cross-aggregate mutation while another reference exists).
- Enums + pattern matching are ideal for aggregate state machines (`enum OrderStatus { Draft, Confirmed { at: Instant }, Shipped { tracking: TrackingNumber }, Cancelled }`).
- Error handling via `Result<T, DomainError>` instead of exceptions.
- **Architecture tests** — there is no standard tool yet; custom `cargo test` with `cargo-modules` parsing, or `dep-graph` checks.

### Java / Kotlin / C#

- **Historical home of DDD.** Every pattern in this document applies as described.
- **Kotlin** — `data class` for VOs (equality, `copy()`, destructuring). Sealed classes / sealed interfaces for aggregate states. Companion objects for factory methods that validate.
- **Java (17+)** — records for VOs, sealed interfaces for aggregate states.
- **C#** — records for VOs, `readonly struct` when allocation matters. `EntityFrameworkCore` works with DDD in classical-mapping mode (own entity configurations, private setters on aggregates, private constructors for EF Core).
- **Architecture tests** — ArchUnit (Java), NetArchTest (.NET), Konsist (Kotlin).

### Mobile — iOS / Android

- Use **Clean Architecture**, **MVVM**, or **The Composable Architecture (TCA)**. Structurally similar (domain at the center, UI outside), different vocabulary.
- Full DDD with aggregates and events is rare — mobile apps usually consume a backend that owns the domain.
- If the mobile app has a real offline-first domain (finance tracker, field-ops app, offline editor), DDD-lite patterns apply: pure domain types, repositories, application services.

### Data pipelines / ML / notebooks

- **DDD is an anti-pattern here.** The unit of work is the DataFrame, the DAG, the model artifact.
- Bounded contexts are meaningful at the **data-domain level** (sales data vs inventory data vs marketing attribution) but not at the **pipeline-stage level** (extract / transform / load are not contexts).
- Notebooks are research artifacts, not production domain code. Do not DDD-ify a notebook.
- If a pipeline evolves into a production service with business rules, extract those rules into a domain module and let the pipeline call it. The pipeline itself stays procedural.

---

## 15. When DDD Does Not Apply

Extends Section 1. Explicit non-applicability cases — if the Story lands here, **skip this document entirely**.

- **Pure CRUD.** Entity with ≤2 business rules (typically "required field" and "unique"). Force-fitting DDD adds ceremony without insight.
- **Stable, low-change domain.** Requirements have not moved in years. There is nothing to model.
- **PoC / MVP / throwaway.** Expected lifespan <6 months. Optimize for learning and deletion, not modelling.
- **Single-purpose utility / CLI tool.** A script that converts files, a glue CLI that orchestrates an external tool.
- **Data pipelines / ML training / inference serving.** See Section 14.
- **Infrastructure-as-code.** Terraform, Helm, Pulumi — declarative infra, not domain.
- **Deploy scripts, CI configuration, Dockerfiles.** Non-domain.
- **Frontend presentation layer.** Usually. Exceptions in Section 14.
- **Mobile UI layer.** Usually. Exceptions in Section 14.
- **Notebooks / research / exploration.** Code is a byproduct of thinking, not a product.
- **Reporting / BI / dashboards.** Read-side only, no invariants to enforce.
- **Legacy code you are only touching tangentially.** Classification `legacy-preserve`; do not DDD-ify (Section 3).
- **Bugfix <5 lines.** Classification `too-small`; do the minimum.

If unsure which applies, re-run Section 2's decision tree. The tree is the arbiter.

---

## References

Just URLs and a one-line "what it's for". Paraphrased; no verbatim quotes.

- **Khononov, "Learning Domain-Driven Design" (O'Reilly, 2021)** — modern strategic DDD; subdomain types (Core / Supporting / Generic); context mapping. Start here for strategic framing.
- **Evans, "Domain-Driven Design" (2003)** — the foundational book; ubiquitous language, bounded contexts, tactical patterns. Dense but canonical.
- **Evans, "Domain-Driven Design Reference" (2016, domainlanguage.com)** — short free PDF, author's condensed summary 13 years after the book.
- **Vernon, "Implementing Domain-Driven Design" (2013)** — tactical patterns applied; source of "prefer small aggregates" guidance.
- **Martin Fowler, martinfowler.com/bliki/BoundedContext.html** — short entry on bounded contexts; start point for non-book readers.
- **Martin Fowler, martinfowler.com/bliki/StranglerFigApplication.html** — the original Strangler Fig write-up.
- **Three Dots Labs, threedots.tech — "DDD Lite in Go"** — idiomatic Go DDD without Java ceremony.
- **Khalil Stemmler, khalilstemmler.com — "DDD on the Frontend"** — when frontend DDD works, when it does not; Redux compatibility issues.
- **Shopify engineering — Packwerk** — modular monolith enforcement for Rails; practical bounded-context tooling.
- **Thoughtworks, thoughtworks.com — Strangler Fig retrospectives** — healthy-termination failure modes; routing-layer monolith anti-pattern.
- **Cockburn, alistair.cockburn.us — Hexagonal Architecture (Ports and Adapters)** — the layering model that pairs with tactical DDD.
- **Microsoft Azure Architecture Center — Anti-Corruption Layer pattern** — cloud-provider consensus on ACL cost/benefit framing.
- **AWS Well-Architected — Anti-Corruption Layer** — same pattern from the AWS lens; convergent guidance.
