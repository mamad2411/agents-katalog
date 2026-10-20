---
name: architecture-essentials
description: Use when making architecture decisions — GoF patterns as vocabulary, SOLID with sharp opinions, hexagonal isolation, modular monolith as the default.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [architecture-event-driven-cqrs, refactoring, debugging]
---

# Architecture Essentials

**Iron Law: composition over inheritance. Modules with clear boundaries beat clever class hierarchies. Start with a modular monolith; split when boundaries prove themselves.**

## SOLID — sharp opinions

Five principles from Robert C. Martin. **Two transcend OO (SRP, DIP); three are situational (OCP, LSP, ISP).**

| Principle                        | Hold?                                                      | When over-applied                                                                 |
| -------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **SRP** — one reason to change   | Universal. Every scale.                                    | Rarely. Holds even when "single responsibility" is hard to pin.                   |
| **OCP** — open/closed            | Concrete first, abstract on the 3rd variant                | Speculative extension points for variations that never come                       |
| **LSP** — Liskov substitution    | Important when you inherit                                 | Inherit less; problem shrinks. Square-extends-Rectangle is the classic violation. |
| **ISP** — many small interfaces  | Sound. Don't over-fragment                                 | One-method-per-file gets you tooling pain                                         |
| **DIP** — depend on abstractions | Universal at boundaries (external systems, swap-for-tests) | `IConsoleWriter` to wrap `console.log` is theater                                 |

**SRP read:** the reasons this code changes come from _one stakeholder/concern_. `InvoicePDFRenderer` (PDF designer) ≠ `InvoiceTaxCalculator` (tax rules).

**DIP read:** business logic doesn't import `psycopg2`; it imports an interface. The whole hexagonal pattern (next section) is industrial-strength DIP.

**Rule of three for OCP:** implement the concrete thing first. Second variant, copy and adapt. **Third variant, abstract.** Speculative OCP is "framework instead of code."

## GoF — vocabulary, not a checklist

Use GoF names to communicate intent. Don't reach for patterns because they exist.

| Reaching for…           | Consider modern alternative                    |
| ----------------------- | ---------------------------------------------- |
| Singleton               | DI with single-instance scope                  |
| Factory                 | Plain function or class method                 |
| Strategy                | Higher-order function                          |
| Observer                | Reactive lib, event bus, signals               |
| Template Method         | Composition with hooks/callbacks               |
| Visitor                 | Pattern matching, tagged unions                |
| Builder                 | Named args, dataclass + validation             |
| Iterator                | Language built-in; don't name it               |
| Command                 | Closure + queue (still useful for undo stacks) |
| Chain of Responsibility | Middleware. List of functions.                 |
| Mediator                | Event bus, pub/sub (risk: god-object)          |
| Memento                 | Immutable snapshots; event sourcing            |

**Still pulls weight:** Adapter (bridges interfaces), Composite (trees), Decorator (logging/caching wrappers), Facade (well-named module _is_ a facade), Proxy (lazy/remote/access), State (when implicit state >3 modes — formalize).

**Smell of pattern-itis:** more `*Factory*` / `*Manager*` / `*Strategy*` classes than business concepts; `Singleton` impossible to test; 4-deep inheritance "for future variations" that never come; Builder for 2-field objects.

## Hexagonal (ports & adapters) — domain at the center

```
   HTTP   CLI   Worker         (driving adapters)
     \    |    /
      \   |   /
       [ DOMAIN ]              (pure: entities, use cases, ports)
      /   |   \
     /    |    \
   DB   Stripe  SES            (driven adapters)
```

- **Domain** at the center. Pure business logic. No imports from frameworks, DBs, HTTP, I/O.
- **Ports** are interfaces _the domain owns and depends on_ (`OrderRepository`, `PaymentGateway`).
- **Adapters** implement those ports against real tech (Postgres, Stripe, SendGrid).
- I/O (HTTP, CLI, consumers) are _driving adapters_ that call into the domain.

**The dependency arrow points inward only.** A grep for `import psycopg2` in `domain/` returns zero. Forever.

### When hexagonal pays

- Non-trivial domain logic worth protecting (financial, scheduling, pricing, regulated).
- Multiple driving channels reusing the same use cases (HTTP + gRPC + CLI + worker).
- Need fast tests (domain runs in-memory at thousands/sec).
- Will swap infrastructure during the system's lifetime.

### When hexagonal is overkill

CRUD apps where `entity.field = value; entity.save()` _is_ the domain. Throwaway scripts. Spike code. Tiny services where the whole thing is 500 lines.

The cost is more code, more files, more indirection. Worth it when the domain is the asset; wasted when the database is the domain.

## Modular monolith — the default

A single deployable unit, organized as explicit modules with **enforced boundaries**. Default for ~95% of systems.

**Most "microservice benefits" (clear ownership, replaceability, independent reasoning) come from modularity, not network boundaries.** Modular monolith gives you those without the distributed-systems tax.

### What "modular" means

1. **Explicit public API** — module exposes a small set; internals not importable.
2. **Stable inter-module contracts** — refactoring inside doesn't break callers.
3. **Enforced boundaries** — tooling (linters, imports, build rules) blocks violations.
4. **One owner per module** — a team or person.
5. **Cohesive vocabulary inside, translated at the boundary** — `customer` in `billing` ≠ `customer` in `support`.

### Enforcement (toolchain, not docs)

| Language   | Tools                                                          |
| ---------- | -------------------------------------------------------------- |
| Python     | `import-linter`; underscore-prefix conventions                 |
| TypeScript | Package per module (Nx, Turborepo); `eslint-plugin-boundaries` |
| Go         | `internal/` packages; `go vet`                                 |
| Java       | JPMS, ArchUnit                                                 |
| Rust       | Crate per module, `pub(crate)`, `pub use`                      |
| Any        | CI check that fails the build on forbidden imports             |

"We agreed not to import that" decays in weeks. CI or it didn't happen.

### Module shape

Domain-oriented, not technical:

- **Good:** `billing`, `inventory`, `customer`, `notifications`, `auth`.
- **Bad:** `controllers`, `services`, `repositories`, `models`. (That's layers, _inside_ a module.)

Each module owns: domain + use cases + persistence + its API surface + tests.

### Modules own their tables

`billing.invoices`, `inventory.stock_items`, `customer.profiles`. **No cross-module direct DB reads.** Use schemas, prefixes, or restricted DB users to enforce. Lose JOINs across modules — that's a feature; it forces explicit contracts.

### When to split into a service

Genuine reasons: independent scale (100× CPU on one module), independent deploy cadence, different runtime needs (Python ML + Go everything else), compliance isolation, team coordination cost.

**Bad reasons:** "microservices are best practice", "feels cleaner", "we _might_ need to scale later", resume-driven development.

Test: _can you point to a concrete pain that splitting eliminates within 6 months?_ If not, stay monolithic.

A well-modularized monolith is a microservice waiting to happen _if needed_. A tangled monolith is a multi-quarter migration.

## Anti-patterns

- Design pattern bingo — `AbstractSingletonProxyFactoryBean`
- Microservices from day one
- Mixing concerns across module boundaries (shared tables, deep cross-module imports)
- `IXyz` interface with one implementation in one place (speculative DIP)
- 5-deep inheritance "for future extensibility"
- One `service.py` with 2000 lines (god-object)
- Interface with 40 methods (ISP violation)
- Domain imports `psycopg2` / ORM / framework
- ORM entities used as domain entities (map at the adapter boundary)
- Modules organized by team org chart (reorg-fragile)
- Cross-module DB JOINs
- "Common" / "core" module that everything depends on and contains business logic

## Common rationalizations

| Excuse                                       | Reality                                                                       |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| "We need it abstract for future flexibility" | YAGNI. Concrete; abstract on variant 3.                                       |
| "Inheritance is faster than composition"     | For 5 minutes. Then refactoring eats the win.                                 |
| "Microservices scale better"                 | Bad modularity in a monolith → bad modularity in microservices, plus network. |
| "We don't need DI; just import it"           | Until you write the test, then mock-everything-everywhere starts.             |
| "Hexagonal is over-engineering"              | For CRUD, yes. For a domain you'd write a book about, no.                     |
| "Module boundaries slow us down"             | They slow you down _less_ than tangled-everything debugging.                  |

## Hand-off

For async between modules and read/write splits: `Skill(architecture-event-driven-cqrs)`. For migrating away from violations: `Skill(refactoring)`. For SOLID applied to code review: `Skill(code-review)`.
