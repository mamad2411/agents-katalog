---
name: architecture-design
description: Designing module, service, and layer boundaries for applications. Use when starting a new project or feature area, restructuring code, deciding monolith vs services, defining layers (API/service/data), or when the user says "architecture", "structure", "refactor the design", "how should I organize", or "design this system's components".
---

# Architecture Design

Architecture is deciding **what is allowed to know about what**. Good architecture makes the change you'll make next month cheap; bad architecture makes every change touch everything. Optimize for cost-of-change, not for diagrams.

## Method: boundaries from change, not from nouns

1. **List the forces first.** Before drawing anything, write down: the 3–5 most likely future changes (new payment provider? new tenant type? mobile app?), the team size, and the hard constraints (compliance, latency, budget). Architecture answers these; without them you're decorating.
2. **Draw boundaries where change is isolated.** Things that change together live together (one module); things that change for different reasons get a boundary between them. "User service / Order service" split by noun is often wrong; "pricing rules change weekly, ledger rules never" is a real boundary.
3. **Make dependencies one-way.** Pick a direction (e.g., API → service → data; domain never imports web). Enforce it: a lower layer importing an upper layer is a build error in your head even when the compiler allows it.
4. **Define each boundary as a contract**, not a folder: what operations, what data shapes, what errors, what invariants the caller may rely on. If you can't state a module's contract in five lines, the boundary is wrong.

## The default that is usually right

**A modular monolith with strict internal boundaries**, one database, boring synchronous calls — until you have *measured* evidence (scaling limits, team contention, isolation requirements) demanding otherwise. Distribution converts function calls into failure modes: network errors, partial failures, versioning, eventual consistency. Take that cost only when paid for.

Signs you've earned a service split: independent scaling profiles (CPU-bound worker vs I/O web), independent deploy cadence blocking teams, a hard fault-isolation or security boundary. "It might need to scale someday" is not a sign.

## Layering rules (server apps)

- **Transport layer** (routes/controllers): parse, authenticate, authorize, call one service function, shape the response. Zero business logic. If you see an `if` about money or state here, move it down.
- **Service layer**: all business logic and transaction boundaries. One service function = one use case = one transaction. Services don't know HTTP exists.
- **Data layer**: models/queries. No business decisions; no knowledge of use cases.
- **Cross-cutting** (config, errors, auth primitives) lives in a core module both sides may import; it imports neither.
- External systems (SMS, email, payments, storage) go behind an **adapter interface with a mock implementation**, selected by config. This is the single highest-ROI architectural habit: it buys testability, dev-without-credentials, and provider swaps for free.

## Decisions: record them or repeat them

For every non-obvious choice, write a 5-line ADR (in `docs/adr/` or the PR description): *context → options considered → decision → consequences accepted.* The purpose is not bureaucracy; it's that six months later, you (or an AI model) will "fix" the design because nobody wrote down why it's shaped that way.

## Review checklist for a proposed design

- Can you state, for each component, what it must NOT know about? (If everything may know everything, there is no architecture.)
- Walk the top 3 likely changes through the design: how many components does each touch? >2 is a smell.
- Where is each invariant enforced — exactly once, at the boundary that owns it? Duplicated enforcement drifts; missing enforcement corrupts.
- What happens when each external dependency is down or slow? Every arrow crossing a process boundary needs a failure answer (timeout, retry policy, degraded mode).
- Is there exactly one source of truth for each piece of state? Every cache/copy/denormalization must name its invalidation story.
- Could a new developer (or AI model) find where code for feature X goes without asking? Predictability beats cleverness.

## Anti-patterns to refuse

- **Speculative generality**: plugin systems, generic "engines", abstraction layers with one implementation and no concrete second use in sight. YAGNI is an architecture rule.
- **Distributed monolith**: services that must deploy together or share a database's tables — all of the cost of microservices, none of the benefit.
- **Business logic in the database or the UI** (triggers with rules, fat frontend that computes prices): logic hidden where tests and reviews don't look.
- **The Big Rewrite** as the answer to messy code. Strangle instead: draw the boundary, put new code behind it, migrate old callers incrementally, delete last.
