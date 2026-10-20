---
name: architecture-review
description: Runs a structured architecture-quality review of a system's module/service boundaries, coupling, data ownership, communication patterns, resilience, structural scalability, extensibility, documentation, pattern consistency, and versioning — evaluating structural soundness and evolvability of the design, not line-level code correctness and not measured runtime performance — then reports the results as one table (check, area, status, evidence, recommendation). Covers domain-aligned vs. arbitrary module boundaries, circular dependencies between modules/packages/services, coupling (does a change in one module ripple into unrelated ones), layering violations (a lower layer reaching up, or a domain layer importing from presentation), data ownership per service vs. shared-database distributed-monolith anti-patterns, cross-boundary consistency (sagas, eventual consistency, distributed transactions), sync-vs-async communication choices and single-points-of-failure created by synchronous call chains, event/message contract versioning, resilience patterns (timeouts, retries with backoff, circuit breakers, bulkheads, graceful degradation), structural/design scalability (independent scaling of components, shared-state bottlenecks, partitioning), extensibility and change cost (blast radius of a typical new feature, god-classes/god-modules), architecture decision records (ADRs), whether diagrams/READMEs describe the actual current structure or a stale one, inconsistent architectural patterns for equivalent problems, and backward-compatibility/versioning strategy for externally-consumed contracts (public APIs, event schemas, shared libraries). Use this whenever the user asks for an "architecture review", "architecture audit", "system design review", "systemdesign prüfen", "architekturreview", "architektur-review", "architekturprüfung", "architektur-check", "softwarearchitektur prüfen", "review the architecture", "is this architecture sound", "is this well-architected", "microservices review", "monolith vs microservices", "modulgrenzen prüfen", "servicegrenzen prüfen", "service boundaries check", "coupling check", "kopplung prüfen", "circular dependency check", "zirkuläre abhängigkeiten finden", "dependency graph review", "abhängigkeitsgraph prüfen", "layering violation", "schichtenarchitektur prüfen", "schichtenverletzung", "data ownership check", "datenhoheit prüfen", "distributed monolith", "verteilter monolith", "resilience review", "resilienz prüfen", "circuit breaker check", "single point of failure", "spof check", "skalierbarkeit der architektur", "structural scalability", "god class", "god module", "blast radius of a change", "architecture decision records", "adr review", "architekturentscheidungen dokumentieren", "technology consistency check", "architectural pattern consistency", "api versioning strategy", "event schema versioning", "abwärtskompatibilität der architektur", "backward compatibility at the architecture level" — even if they only name one or two specific items (e.g. "check for circular dependencies" or "do we have ADRs") rather than asking for a full architecture review.
---

# Architecture Review

A structured, evidence-based review of a system's structural design and evolvability: how its
modules/services are bounded, how they depend on and talk to each other, how they own data, how
they fail (or don't), and how cheaply the system can change. It is a peer to two other skills and
deliberately does not re-cover their ground:

- **code-review** owns line-level correctness, error-handling quality, readability, and test
  coverage *within* a module. If you notice a correctness bug while tracing a dependency, note it
  exists in one line and point the user at `code-review` — don't build it out as a full finding
  here.
- **performance-audit** owns *measured* runtime performance and resource efficiency — actual
  latency, N+1 queries, memory/CPU usage, autoscaling config. This skill only looks at whether the
  design *structurally allows* independent scaling and avoids shared-state bottlenecks; it never
  claims to know how fast or expensive something actually is at runtime. Same treatment: a
  one-line pointer, not a full finding.

This skill's lane is: are the boundaries drawn along the right lines, is coupling loose where it
should be, does data ownership and cross-boundary consistency make sense, is the system resilient
to a dependency failing, can components evolve and scale independently, and is that design
documented and applied consistently.

## Ground rules

- **Evidence or it didn't happen.** Every row needs a concrete pointer — a `file:line`, an actual
  `import`/`using`/`require` statement, a dependency-graph trace you actually walked, a grep match,
  or (for something code can't answer) an explicit note that it needs human/business judgment.
  Never write "the architecture looks clean" or "boundaries seem reasonable" — either you traced
  the actual imports/calls and they hold up, or they don't get a ✅.
- **Separate what the codebase can prove from what needs human judgment.** An actual circular
  import between two packages, an actual synchronous HTTP/gRPC call crossing a boundary the system
  claims is async, a table written to by two different services' code — these are objective,
  demonstrable facts once you've traced them. Whether microservices vs. a monolith is the *right*
  choice for this team's size, whether a given bounded context is drawn correctly for the business,
  or whether a documented eventual-consistency window is acceptable to the business — these are
  judgment calls the codebase alone can't settle. Present the structural evidence, then mark those
  ⚠️ **needs review** rather than asserting your own opinion as fact.
- **Stay in your lane, but don't pretend the other lanes don't exist.** See the scope note above —
  defer correctness bugs to `code-review` and measured performance/cost questions to
  `performance-audit` with a one-line pointer, rather than building full findings for them here.
- **Don't invent scope you can't check, and don't silently drop scope either.** A single-deployable
  monolith with no service boundaries at all → the cross-service checks (data ownership per
  service, sync/async between services, SPOF from a shared service) are `➖ N/A` — but say so
  explicitly and instead apply the equivalent checks at the module/package level, since a monolith
  can still have well- or badly-drawn internal boundaries. No ADRs directory and no architecture
  doc at all → that's a `❌`, not a silent skip. Every check in this skill gets a row.
- **A stale diagram is worse than no diagram.** Never take a README's architecture diagram, a
  `docs/architecture.md`, or a service-boundary description at face value — spot-check its claims
  against the actual imports/calls you traced in step 1 of the workflow. A mismatch is itself a
  finding (documentation check), independent of whether the actual structure underneath is good or
  bad.
- **Be genuinely thorough.** A dependency graph that "looks fine" from the folder structure alone
  is not verified — actually open the files and read the import statements for anything you're
  about to mark ✅. Don't stop at the first two or three modules; a circular dependency or a
  layering violation buried in a less-obvious pair of modules is exactly the kind of thing this
  review exists to surface.

## Workflow

1. **Map the actual system structure first.** Identify the services/modules/packages that exist and
   their *declared* boundaries: separate repos or separate deployables (real service boundaries),
   or folders/projects/packages within one deployable (module boundaries) — check solution files,
   `package.json`/workspace configs, `go.mod`, Maven/Gradle modules, Docker Compose/Kubernetes
   manifests (one deployment per service is real evidence of a service boundary; one deployment for
   everything means "services" in a diagram may just be folders).
2. **Draw the real dependency graph by reading imports, not by trusting a diagram.** For each
   module/service pair that a diagram, README, or folder structure claims is separate, grep the
   actual `import`/`using`/`require`/`from ... import` statements (and, for services, actual
   outbound HTTP/gRPC/message-client calls) to confirm what really depends on what. Build this graph
   before working the checklist — most of the checks below are verified against it.
3. **Work through the checklist below**, grouped by theme — every check gets a row, marked
   ✅/❌/⚠️/➖, grounded in the graph from step 2 and direct file reads, never in the diagram alone.
4. **Cross-check any existing diagram/ADR/README against what you actually found** in step 2 — this
   feeds directly into the Architecture Documentation checks (AR17–AR18).
5. **Report as one table**, most severe/most-confident-❌ findings first within each area, followed
   by the prioritized punch list and needs-review list.

## Module & service boundaries, coupling

**AR1 — Boundaries follow business capability, not accident.** Look at what each
module/service actually contains: is it organized around a business capability/domain (orders,
billing, inventory) with a cohesive reason to change together, or around a technical layer/artifact
type that cuts across every feature (a global "utils", "helpers", "common", or "shared" module that
half the codebase imports, or a split purely by technical tier — "controllers", "services",
"repositories" — with no domain grouping underneath it)? Cite the actual module list and what each
one's responsibility is; a module whose name and contents don't obviously map to one business
concept is the flag.

**AR2 — Circular dependencies.** For every module/service pair in your dependency graph, check
whether A imports/calls B *and* B imports/calls A (directly, or through a chain — A→B→C→A is still
circular). Grep both directions explicitly:

```bash
# does module A reference module B, and does B reference A back?
grep -rn "from ['\"]@app/moduleB" src/moduleA/
grep -rn "from ['\"]@app/moduleA" src/moduleB/
```

(adjust the import syntax to the language — `using ModuleB` in C#, `require('../moduleB')` in
older Node, `import moduleb` in Python). A build/lint tool that already detects this
(`madge --circular`, `dep-cruiser`, NDepend, `go vet` for import cycles — Go's compiler rejects
cycles outright) is faster and more complete than manual grepping if one is already configured;
run it if available, but still spot-verify at least one flagged cycle by reading the actual import
lines. No cycles found after checking the real graph → ✅, and say which tool/method you used.

**AR3 — Coupling is loose where it should be.** Pick two or three modules that the system's
boundaries claim are independent, and check: does a plausible single-purpose change (adding a field
to one domain's model, changing one module's internal storage) require edits in another module, or
does it stay contained? Concretely, look for a shared mutable data structure/class passed by
reference across the boundary, a module reaching into another's internal/private namespace instead
of its public interface, or a shared database table two modules both write to (also covered in
AR5). Cite the actual coupling point found, not a general impression.

**AR4 — Layering violations.** If the system claims a layered architecture (presentation/API →
application/business → domain → infrastructure/data, or similar), grep for imports that go the
wrong direction: a domain/business-logic file importing anything from a controller/view/UI
namespace, or a lower layer (data access, infrastructure) importing from a higher layer it's meant
to be agnostic of (e.g. a repository class referencing a web-framework request/response type). A
good layering has arrows pointing one way only (typically inward toward the domain, per
dependency-inversion); a bad one has at least one file importing "up" or "sideways" across a layer
it shouldn't know about. No layered architecture claimed anywhere in the system → `➖ N/A`, state
that explicitly rather than forcing the check.

## Data ownership & consistency

**AR5 — Each service/module owns its data store.** For a system with more than one deployable
service, check whether each service's code is the only code that reads/writes its own
database/tables — grep for connection strings/ORM contexts/table references from more than one
service pointing at the same schema or database. Multiple services directly reading or writing the
same tables (rather than going through the owning service's API) is the classic
"distributed monolith" anti-pattern: it looks like microservices at the deployment level but is
tightly coupled at the data level, so a schema change in one service silently breaks another. Cite
the actual connection config/table reference for each offending pair. Single-deployable monolith
with one shared database by design → ✅ or `➖ N/A` as appropriate, since the anti-pattern only
applies once there's a claimed service boundary.

**AR6 — Cross-boundary consistency is an explicit decision.** If more than one data store exists
across service/module boundaries, find how consistency between them is actually handled: a
saga/choreography pattern, an outbox pattern, eventual consistency via events, or a distributed
transaction (2PC) — or nothing at all (a "hope both writes succeed" pattern with no compensating
action on partial failure). Check whether this is a documented, deliberate choice (an ADR, a
comment, a design doc) or something that emerged by accident with no failure-mode handling. A
missing compensating action for a multi-step operation that can partially fail is a concrete ❌;
an undocumented-but-present pattern is a ⚠️ (works today, but the next engineer won't know why it's
built that way, or when it's safe to change).

## Communication patterns

**AR7 — Sync vs. async choice, and cascading-failure risk.** Trace the actual communication
between services: HTTP/gRPC client calls (synchronous, caller blocks and fails if the callee is
slow/down) vs. a message queue/event bus publish (asynchronous, decoupled). For each synchronous
call, ask whether the caller's own success genuinely depends on an immediate answer (e.g. "is this
payment authorized" — yes) or whether it's a synchronous call standing in for something that could
be async (e.g. "send a confirmation email" done as a blocking call in the request path). Flag chains
of three or more services calling each other synchronously in sequence — the response time and
failure probability of the whole chain is the product of every link, and any one link failing fails
the whole chain, not gracefully.

**AR8 — Single point of failure from a synchronously-called-by-everything service.** Identify any
service/module that a large share of the others call synchronously (grep outbound client
instantiations pointing at one shared service — an auth service, a shared "core" API, a config
service). If that one service goes down or slows down, does everything that calls it fail/degrade
in lock-step? This is a structural risk regardless of how reliable that service happens to be
today — cite how many callers you found and whether any of them have a fallback (cached
credentials, a circuit breaker, a default config) versus a hard dependency.

**AR9 — Message/event contract versioning.** For any message queue/event bus/pub-sub usage, check
whether published event schemas carry a version (a `version`/`schemaVersion` field, a versioned
topic/subject name, or a schema registry) that lets a consumer detect and handle an old vs. new
shape, or whether producers and consumers are implicitly coupled to "whatever shape the code
currently produces" with no way to evolve one without breaking the other. No messaging/eventing in
the system at all → `➖ N/A`.

## Resilience patterns

**AR10 — Timeouts on outbound calls.** For each outbound HTTP/gRPC/DB client call between
components, check whether an explicit timeout is configured (not the language/library's default,
which is often "wait forever" or an unreasonably long default) — an HTTP client created with no
timeout, or a DB command with no `CommandTimeout`, means a slow downstream dependency can hang the
caller indefinitely and exhaust its thread/connection pool.

**AR11 — Retries with backoff, and idempotency.** Where a retry exists around a cross-component
call, is it capped (not unbounded), and does it back off (exponential/jittered) rather than
hammering a struggling dependency at a fixed interval? Separately: is the retried operation
idempotent, or can a retried non-idempotent write (a payment, an order creation) create a duplicate
side effect? No retry logic anywhere in cross-component calls → flag as a gap if calls are
synchronous with no resilience at all (❌), or `➖ N/A` with a one-line reason if genuinely nothing
in the system warrants one (e.g. everything is fire-and-forget async with dedup downstream).

**AR12 — Circuit breakers, bulkheads, and graceful degradation.** For a call chain identified in
AR7/AR8 as a risk (synchronous, chained, or single-point-of-failure), check whether a circuit
breaker (Polly, resilience4j, a hand-rolled failure-counting wrapper) exists to stop calling a
failing dependency and fail fast instead of piling up blocked callers; whether failure/latency in
one dependency is isolated from others (separate connection pools/thread pools per dependency —
bulkheads — rather than one shared pool a single slow dependency can exhaust); and whether the
caller degrades gracefully (serves cached/default data, disables one feature) when a non-critical
dependency is unavailable, versus the whole request failing. Cite the specific chain this was
checked against, not a generic "resilience seems present/absent."

## Structural scalability

**AR13 — Independent scaling.** Can a component that's expected to see disproportionate load
(the busiest service, a hot module) be scaled on its own, or does the deployment unit it's bundled
into force scaling everything alongside it? Check deployment config (separate
Kubernetes Deployments/services vs. one monolithic deployment; separate serverless functions vs.
one function handling every route) against which components would actually be the ones under load.
A monolith isn't automatically wrong here — flag it only when there's a clearly identifiable
hot component bundled with cold ones, since that's the case where the *design*, not just the
current traffic, forces wasteful or impossible scaling.

**AR14 — Shared-state bottlenecks baked into the design.** Look for a single shared
cache/database/queue instance with no partitioning/sharding strategy that every
component/tenant/request funnels through by design (not as a current capacity number — that's
performance-audit's territory — but as an architectural choice with no partitioning path at all,
e.g. one global lock, one singleton in-memory cache in a system meant to run multiple instances, one
queue with no partition/consumer-group concept for parallel consumption). Cite the actual
shared-resource reference and who all depends on it.

## Extensibility & change cost

**AR15 — Blast radius of a typical change.** Pick one or two representative recent
features/integrations (from git log or changelog if available) and trace how many
modules/services actually needed to change to ship them. A well-bounded system keeps most feature
work inside one or two modules; a system where a typical feature routinely touches five-plus
unrelated modules is a sign the boundaries don't align with how the system actually changes (this
is the practical, checkable proxy for AR1's boundary-quality judgment). Cite the actual commit/PR
and the file list if git history is available; if no history is available to sample, reason from
the current dependency graph instead (how many modules would a plausible one-capability change
have to touch, given who depends on what) and mark the row ⚠️ since it's an estimate rather than an
observed instance.

**AR16 — God-classes/god-modules.** Identify any single class/module/package with an
unusually large number of inbound dependencies (grep for how many other files import it) relative
to the rest of the system — a "core", "utils", "manager", or "context" object that half the
codebase directly depends on. This isn't inherently wrong (some shared kernel is normal), but flag
it when it also has high *outbound* fan-out or frequent churn (many unrelated changes touch it),
since that combination means it's both a single point of coupling and a magnet for merge conflicts
and ripple effects. Cite the actual import count/dependents found, not an impression of "there's
probably a god class somewhere."

## Architecture documentation

**AR17 — ADRs or equivalent exist for significant past decisions.** Look for an `adr/`,
`docs/decisions/`, `docs/architecture/` folder, or equivalent (even informal design-doc links in a
wiki/README) recording *why* a significant structural choice was made (why this data store, why
this messaging pattern, why split this service out). Their absence isn't just "no docs" — it means
the next engineer can't tell a deliberate choice from an accident, which directly affects several
other checks above (AR6, AR9). No such records anywhere → ❌, not a silent pass; note what you
searched for.

**AR18 — Diagrams/READMEs describe the actual current structure, not a stale or aspirational
one.** Take any existing architecture diagram or descriptive README section and spot-check its
specific claims (which services exist, which one talks to which, sync vs. async arrows) against the
dependency graph you built in workflow step 2. Cite at least one concrete match or mismatch — e.g.
"diagram shows Service A calling Service B via a queue; actual code in
`src/serviceA/client.ts` makes a direct HTTP call" — rather than asserting the diagram is
current/stale without checking a specific claim. No diagram/architecture doc exists at all →
that's itself the ❌ for this check (there's nothing to compare, which is its own documentation
gap) — don't conflate it with AR17, which is about decision *rationale* rather than structural
description.

## Technology & pattern consistency

**AR19 — Consistent architectural patterns for equivalent problems.** Look for the same *kind* of
problem solved in noticeably different architectural ways across the codebase — e.g. three
different integration patterns for calling external services (one via a shared HTTP client wrapper,
one with `fetch` calls scattered inline, one via a message queue) with no documented reason
(a migration in progress, a deliberate per-case tradeoff noted somewhere) for the divergence. This
is different from C18 in `code-review` (function-level parameter/return convention drift) — this
check is about structural/integration-pattern choices, not local code style. Cite the specific
instances found; if a migration-in-progress note explains the inconsistency, that's a ✅ or ⚠️
(documented transition) rather than a ❌.

## Versioning & backward compatibility (architecture level)

**AR20 — Externally-consumed contracts have a versioning/compatibility strategy.** For every
contract another team, another service, or an external customer depends on — a public/partner API,
an event/message schema (see AR9), or a shared library published to an internal/external package
registry — check whether there's an explicit strategy that lets producer and consumer evolve
independently: API versioning in the URL/header, additive-only schema evolution with a schema
registry, semantic versioning with a documented deprecation window for a shared library. Its
absence means every change to that contract is a potential breaking change for every consumer
simultaneously, and the fix has to happen everywhere at once rather than on each side's own
schedule. No externally-consumed contract exists at all in this system → `➖ N/A`, state what you
checked for.

## Output format

Start with 2-3 sentences: what was reviewed (the actual services/modules/packages identified in
workflow step 1), how the dependency graph was built (which imports/configs you actually read),
and the ground-rule caveat that this is a structural/design review based on static investigation —
not a runtime measurement (see `performance-audit` for that) and not a line-level correctness pass
(see `code-review` for that).

Then ALWAYS use this exact table — one row per check, none omitted:

| # | Check | Bereich/Area | Status | Befund/Evidence | Empfehlung/Recommendation |
|---|---|---|---|---|---|
| 1 | ... | Boundaries/Data/Communication/Resilience/Scalability/Extensibility/Docs/Consistency/Versioning | ✅/❌/⚠️/➖ | file:line, import statement, or traced call | only if not ✅ |

(Match the table's language to the conversation's language — the column names above are
illustrative, not fixed vocabulary. Keep evidence concrete: a path+line and a quoted
import/call, an actual dependency-graph edge, or "not found — checked X, Y, Z.")

Status legend:
- ✅ Pass — traced the actual imports/calls/config and the design holds up
- ❌ Fail — a concrete structural problem was found (a real circular import, a real shared-table
  write from two services, a real missing timeout on a chained synchronous call)
- ⚠️ Needs human/business judgment — the codebase shows the structural facts, but whether they're
  the *right* choice depends on team size, business context, or a tradeoff only the team can weigh
  (e.g. "is a monolith right for this team," "is this eventual-consistency window acceptable")
- ➖ N/A — this check's surface doesn't exist in this system (state why in one clause, e.g. "single
  deployable, no service boundaries — see module-level checks instead")

End with a **prioritized punch list**: every ❌, ordered by blast radius/cascading-failure risk
first (a circular dependency or shared-database write that couples the whole system), then
resilience gaps, then documentation/consistency gaps — each with the one-line fix. Follow it with a
**needs-review list**: every ⚠️, since those are exactly the items that need a human with business
context to close out, not a mechanical fix.
