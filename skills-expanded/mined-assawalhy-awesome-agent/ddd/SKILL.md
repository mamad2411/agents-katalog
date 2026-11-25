---
name: ddd
description: Use when organizing, writing, reviewing, or extending backend code that follows Domain-Driven Design with Clean Architecture layering — with or without a CQRS command/query split. Trigger whenever the question is where a piece of code belongs (domain vs application vs infrastructure), how to name a class (Request/Command/Query/UseCase/Handler/Repository/Gateway/Controller/Dao/Dbo/Projection), how to shape an aggregate or bounded context, whether a new context should split reads from writes, whether existing structure is correct, or how to add a use case to an existing service. Also trigger when extending a codebase whose layout differs from the canon and you must decide what to conform to and what not to copy. Language-agnostic at its core; `references/kotlin-spring.md` covers the Kotlin + Spring Boot implementation and `references/cqrs.md` the full command/query split. Fires even when the user never says "DDD" or "CQRS".
---

# Domain-Driven Design + Clean Architecture

Two things are always true, and one thing varies.

**Always:** the system is split into **bounded contexts**, and each context is
**layered** `domain` / `application` / `infrastructure` with dependencies pointing
strictly inward.

**Varies:** whether a context additionally splits into a **command side** and a
**query side** (CQRS). That is a per-context decision, not a law. Codebases
routinely mix split and unsplit contexts in one service.

So: never assume the shape. Read it first.

## 1. Detect before you write

Before creating or moving a single file, establish three facts about the context
you are editing. Do not skip this because the change looks small — putting a file
in the wrong place is the most expensive kind of small mistake here.

```bash
# a) topology — does this context split reads from writes?
find src/main/<lang>/**/<context> -maxdepth 2 -type d

# b) naming variant — singular or plural, Repo or Repository, where do converters live?
find src/main/<lang>/**/<context> -type d | sort

# c) the pattern across siblings, not just this one context
find src/main/<lang>/** -maxdepth 2 -type d | sort
```

Then read **two or three actual files** of the kind you are about to add — an
existing use case, its repository, its converter. Signatures and idiom matter
more than folder names.

**Read several sibling modules before concluding what "the pattern" is.** One
occurrence may be an accident. The same deviation repeated across the service
*is* that service's convention.

## 2. The invariants

These hold in every topology, in every language. Local precedent does **not**
override them — a codebase that breaks one has a defect, not a convention.

1. **Dependencies point inward.** `infrastructure → application → domain`. The
   domain depends on nothing.
2. **The domain layer imports no framework.** No ORM, no HTTP client, no DI
   annotations, no serialization attributes. An ORM import in a domain model
   means the file is in the wrong layer.
3. **Business rules live in the domain.** A business-rule `if` in a use case,
   controller, or repository belongs on the aggregate or in a domain service.
4. **The application layer is orchestration only** — coordinate domain calls,
   own the transaction boundary, return a result. One use case per file, one
   entry point (`execute()`).
5. **Depend on ports, never adapters.** Domain and application code references
   a `...Repository` / `...Gateway` / `...Publisher` interface, never a concrete
   `...Impl`, `...Dao`, `...Dbo`, ORM entity, or HTTP client.
6. **One repository per aggregate root**, never per entity. Children load and
   save through the root.
7. **The models stay distinct.** Wire DTO ≠ application model ≠ domain model ≠
   persistence model. Conversions are explicit, hand-written, and live in
   infrastructure — never in `application/`, never in the domain.
8. **Aggregates stay bounded.** A root holding an ever-growing collection (an
   account with every transaction it ever had) will get slow and can exhaust
   memory. Flag it; consider a narrower boundary.

## 3. Pick the topology

Four shapes are legitimate. Choose per context, on evidence.

| Shape | Layout | Use when |
|---|---|---|
| **Split (CQRS)** | `command[s]/` + `quer{y,ies}/` + `common/`, each layered | Reads and writes genuinely diverge — the read shape isn't the write shape, list/report queries span aggregates, or the two sides scale differently |
| **Command-only** | `command[s]/` + `common/`, no read side | The context only mutates state — driven by schedulers, consumers, or gateways, and exposes no read API |
| **Unsplit layered** | `domain/` + `application/` + `infrastructure/` directly under the context | CRUD-shaped context where reads return roughly the write model; the split would be ceremony |
| **Flat / technical** | no bounded contexts at all | Small single-purpose services (a cron runner, a thin integration proxy) with no real subdomain to model |

**Default for a new context: unsplit layered.** Split when you can name the
divergence, not in anticipation of it. A context that outgrows unsplit is
straightforward to split later; an unnecessary split is dead structure in every
file you touch.

**When the context is already split, read `references/cqrs.md` before writing** —
the split has rules that don't follow from layering alone (the query side has no
domain layer; query code never imports write aggregates; ports sit on different
layers on each side).

**Adding to an existing context: match its shape.** Don't split an unsplit
context to add one query, and don't add an unsplit `application/` beside an
existing `command/`+`query/` pair.

## 4. Where each artifact goes

Keyed by role. The **Lands in** column resolves per topology: `<side>` is
`command[s]/` or `quer{y,ies}/` in a split context, and nothing at all in an
unsplit one (artifacts sit directly under the context).

| Artifact | Layer | Lands in | Notes |
|---|---|---|---|
| Aggregate root, entity, value object | domain | `<side>/domain/model[s]/` — write side only when split | Invariants live here. Prefer validating factories (`MerchantId.of(...)`) |
| Domain service | domain | `<side>/domain/services/` | Business logic spanning models; still domain, not orchestration |
| Domain event | domain | `<side>/domain/events/` | Emitted by aggregates, so a domain artifact — not `application/events` |
| Port / contract | domain (write), application (read) | `<side>/domain/contracts/`; query-side ports in `query/application/contracts/` | Repositories, gateways, publishers |
| Use case | application | `<side>/application/usecase[s]/` | Verb-first names (`CreateShipment`); event handlers suffixed `...Handler` |
| Use-case input/output | application | `<side>/application/model[s]/` | `...Command` or `...Request` in, `...Query` for reads, `...Result` or a named read model out. Data only |
| Access policy | application | `<side>/application/policy/` | Row-level/visibility rules as an injectable component. The use case *calls* it; rules are never inlined |
| Controller / resource | infrastructure | `<side>/infrastructure/controllers/` | Convert in → call use case → convert out. No business logic |
| Repository impl | infrastructure | `<side>/infrastructure/repositories/` | Implements the domain port; owns the transaction boundary |
| Gateway impl | infrastructure | `<side>/infrastructure/gateways/` | Anti-corruption layer over another service; wraps the HTTP client, maps into our models |
| Publisher / listener | infrastructure | `<side>/infrastructure/publishers/` + `listeners/` | Port in `domain/contracts/`, broker specifics in the impl |
| Scheduled job | infrastructure | `<side>/infrastructure/jobs/` | An entry point — as thin as a controller |
| Converter / mapper | infrastructure | `<side>/infrastructure/converters/`, or nested `controllers/converters` + `repositories/converters` | Direction-specific names: `toModel`, `toDto`, `toDomain`, `toDbo`, `toApplication` |
| Persistence entity, DAO, projection, SQL | infrastructure | `common/infrastructure/db/` when split (both sides read it); `infrastructure/db/` when not | See `references/kotlin-spring.md` |
| Exception hierarchy + error codes | — | `common/exceptions/` when split, else `domain/exceptions/` | One hierarchy per context. Never two same-named exception classes in one context |

**`common/` (inside a split context)** holds only what both sides genuinely
share: persistence, shared value objects and enums, the exception hierarchy, the
exception handler, services used by both. It does **not** hold the write
aggregate, converters, or a policy only one side calls.

**`sharedkernel/` (at the service root)** holds what every context may depend on:
cross-cutting value objects and ports, base use-case interfaces, base persistence
classes, centralized HTTP clients and their config, the global exception handler,
framework config. Reusable across contexts → `sharedkernel`; specific to one
context → that context. One context's persistence never belongs here.

## 5. Conform vs. improve

You will find code that doesn't match this document. Sort it into three buckets
and act differently on each. Getting this wrong in either direction is the most
common failure — cementing drift, or refactoring things nobody asked you to touch.

**The test:** *does the difference change what the code can do, or which
invariants hold?*

| Bucket | Examples | What to do |
|---|---|---|
| **Variation** — no, it's an arbitrary choice | `command/` vs `commands/`; `model` vs `models`; `Repo`/`RepoImpl` vs `Repository`/`RepositoryImpl`; suffix (`ShipmentQueryRepoImpl`) vs prefix (`QueryShipmentRepositoryImpl`); extension-function converters vs a mapper class; one controller per endpoint vs one per resource; `db/dao` vs `db/dao/pg`; bare `CreateShipment` vs `CreateShipmentUseCase` | **Conform silently.** Match the module you're in. The only error is introducing a *third* pattern |
| **Defect** — yes, an invariant is broken | ORM annotation in a domain model; business rule in a use case or controller; query code importing the write aggregate; the whole aggregate parked in `common/domain`; converters in `application/`; a command path re-reading state to build its response; application code injecting a `...Dao` directly | **Don't propagate.** Write the new code correctly. Name the surrounding defect once when you hand off. Don't fix it in place unless asked |
| **Typo / degenerate** — just wrong, no argument for it | misspelled packages (`infrastucture`); doubled words (`...CommandsCommandsRepositoryImpl`); singular `gateway/` beside plural `controllers/`; a stray `query/domain/` package | **Don't copy.** Spell new files correctly and mention the existing ones. Never mass-rename as a side effect of another change |

Two rules make this decidable:

- **Frequency decides.** A deviation in one file is an accident — don't imitate
  it. The same deviation across the whole service is that service's convention —
  treat it as canon there, even if this document prefers otherwise.
- **Priority order: correctness of new code > consistency with the module >
  this document.** If staying correct forces you to deviate from the surrounding
  code, do it, and say so in one line when you deliver.

**Propose, don't perform.** Improving structure is a change of its own. Never
bundle a refactor into a feature or bugfix — deliver the feature correctly, then
say what you'd clean up and let the user decide.

## 6. Flows

**Command:** controller receives DTO → `toModel()` → use case `execute()` →
repository port loads the aggregate → aggregate enforces invariants and mutates →
repository saves the root (children cascade) in one transaction → domain events
published → use case returns what it already has → controller converts to DTO.

A command must **not** re-read state through a query path to build its response.
If the response needs the updated resource, the use case returns it from the
aggregate it already loaded. If the body isn't genuinely needed, return none.

**Query (split context):** controller → `toModel()` → use case `execute()` (calls
the policy when access rules apply) → query port → projection / read model →
`toApplication()` → controller → `toDto()`.

**Unsplit context:** same as the command flow for writes; reads go
controller → use case → repository port → domain model or a read projection →
DTO. There is one repository port per aggregate, serving both.

## 7. Adding a feature — order of operations

1. **Which bounded context?** The one owning the closest existing aggregate.
   Don't open a new context for an extension of an existing one.
2. **What's the topology?** Section 1. Decides whether there's a side to pick and
   whether a domain layer is involved.
3. **Mutation or read?** In a split context this picks the side. In an unsplit
   one it picks whether you touch the domain at all.
4. **Contract first** if the service generates its API from a spec — change the
   spec, regenerate, then implement against the generated signature.
5. **Domain** (mutations): new or changed invariants on the aggregate or a domain
   service; consider a domain event.
6. **Application**: the use case and its input/output models; wire in a policy if
   access rules apply.
7. **Infrastructure last**: controller, repository, persistence, converters.
8. **Tests per layer** as you go.

When *changing* behavior, first find which layer owns the logic: business rule →
domain; coordination or transactions → application; how data is fetched, stored,
or exposed → infrastructure. If one rule forces edits in several layers, the
logic is probably in the wrong layer — consider moving it rather than patching
around it.

## Review checklist

Always:

- [ ] Dependencies point inward; domain has zero framework/ORM/HTTP imports
- [ ] Business rules in the domain; application layer is orchestration only
- [ ] One use case per file, single entry point, naming consistent with the module
- [ ] Code depends on ports; no `...Impl`/`...Dao`/persistence entity/client reaching into domain or application
- [ ] One repository per aggregate root; aggregate persisted through the root; no unbounded child collections
- [ ] DTO ≠ application model ≠ domain model ≠ persistence model; conversions hand-written in infrastructure
- [ ] Topology matches the rest of the context — no split introduced into an unsplit context, or vice versa
- [ ] New code follows the module's existing variations; no third pattern introduced
- [ ] No defect or typo from surrounding code copied into the new files
- [ ] No unrequested refactor bundled into this change — improvements named, not performed
- [ ] Each new use case has a unit test; each new endpoint and query has the layer's usual test

If the context is split, also run the checklist in `references/cqrs.md`.

## References

- **`references/cqrs.md`** — the command/query split in full: canonical tree, why
  the query side has no domain layer, projections, per-side ports and policies,
  and the accepted naming variations. **Read this whenever the context splits.**
- **`references/kotlin-spring.md`** — the Kotlin + Spring Boot implementation:
  contract-first OpenAPI generation, persistence entities/DAOs/cascade, native
  SQL, Specifications, gateways over HTTP clients, and the testing tiers.

The core is a structural convention, not a framework. In another language, keep
the layering and the naming and adapt the idioms — interfaces or protocols or
traits for ports, whatever the language uses for conversion.
