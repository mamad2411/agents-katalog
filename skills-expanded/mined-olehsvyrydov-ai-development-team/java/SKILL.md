---
name: java
description: "Java language and JVM engineering standards — records and sealed-type modelling, JSpecify null-safety with NullAway as a build error, immutability, virtual threads and modern concurrency, Error Prone/ArchUnit/PIT build gates, JUnit 6 testing doctrine, and boundary security. Load whenever writing, refactoring, or reviewing Java: any .java file, pom.xml/build.gradle change, javac or test failure, or Java design/test planning — with or without /be or /rev invoked. NOT for Kotlin (that is /be's kotlin reference) and NOT for Spring/API/persistence how-to (that is /be's java-expertise reference)."
---

# Java (language skill)

This is a knowledge skill, not an agent: it loads from context whenever Java is written or
reviewed, and the role agents (`/be`, `/rev`, `/arch`) route into it for the language-level
rules. Framework depth — Spring, persistence, API design, messaging — stays with `/be`
(`../../backend/java/backend-developer/SKILL.md`) and its
`../../backend/java/backend-developer/references/java-expertise.md`; this skill owns the language.

## Trigger

Use this skill when:
- Writing, editing, or reviewing `.java` files
- Changing `pom.xml`, `build.gradle`, `build.gradle.kts`, or `gradle/libs.versions.toml`
- Diagnosing a `javac`, Error Prone, or JVM test failure
- Designing a Java component — domain model, null contract, concurrency topology
- Planning tests for Java code
- Adding a dependency to a JVM build

Do NOT load it for:
- Kotlin — that is `/be`'s kotlin reference
- Spring/API/persistence how-to — that is `/be`'s java-expertise reference

## Context

This skill exists to make Java reviews boring. Illegal states cannot compile, so the
reviewer argues about the domain instead of hunting null checks. Null flows are verified
by a checker at build time, so "can this be null?" has a mechanical answer. Architecture
rules are executable tests, so the layering survives its tenth contributor. Where the
language has moved — records, sealed types, virtual threads, `ScopedValue` — the doctrine
moves with it and states which runtime each piece of advice applies to.

## Documentation Lookup (MANDATORY)

**Before implementing any feature**, check current documentation. Java ships a new release
every six months, preview APIs mutate between releases, and the tooling stack (Error Prone,
NullAway, PIT, ArchUnit) moves independently; recall is not a source.

### Context7 MCP

Use Context7 MCP to retrieve up-to-date documentation for any library or tool:

1. **Resolve library**: Call `mcp__context7__resolve-library-id` with the library name
2. **Query docs**: Call `mcp__context7__query-docs` with the resolved library ID and your question

**When to use:** JUnit 6 APIs, ArchUnit rule syntax, Testcontainers modules, NullAway and
Error Prone flags, pitest configuration, jqwik arbitraries.

**Example queries:**
- "JUnit 6 parameterized test sources"
- "ArchUnit 1.4 layeredArchitecture syntax"
- "Testcontainers Spring Boot ServiceConnection supported containers"
- "NullAway OnlyNullMarked option"
- "pitest incremental analysis configuration"
- "jqwik combinators for recursive records"

### Web Research

Use `WebSearch` and `WebFetch` for anything version- or advisory-shaped:

| Question | Source to check |
|----------|-----------------|
| Is a feature final or preview on the deployed JDK | the JEP page — its status line, not blog posts |
| What changed in a JDK release | the release notes / JEP index for that exact JDK |
| Current version of a library | its repository / Maven Central, at task time |
| Advisory against a dependency | the OSV database |

### Java-specific lookup rules

- **Preview APIs are looked up against the current JEP number, never recalled.** Preview
  features rename between releases — structured concurrency's `Joiner` API changed between
  the JDK 25 preview (JEP 505) and the JDK 26 preview (JEP 525). Code recalled from an
  earlier preview round will not compile on the next JDK; find the JEP that ships with the
  project's JDK and read that one.
- **Framework claims are verified against the deployed major.** Spring Framework 7 is
  JSpecify-annotated and recommends NullAway; Spring 6 used its own null-safety
  annotations. Null-safety, baseline-JDK, and namespace advice all differ by major —
  check which one the project actually runs before asserting anything.

**Rule**: When uncertain about any API, configuration, or best practice — **search first, code second**.

## Versions

| Technology | Version | Notes |
|------------|---------|-------|
| Java | 25 (LTS) | The baseline this skill targets; 26 is non-LTS, 27 expected Sept 2026 |
| `ScopedValue` | final since 25 | JEP 506 |
| Stream Gatherers | final since 24 | JEP 485 — `Stream.gather(...)` |
| FFM | final since 22 | `java.lang.foreign` — the JNI replacement |
| Structured concurrency | **PREVIEW** | JEP 505 (5th preview, 25) → JEP 525 (6th preview, 26, `Joiner` renames); expected final in 27 |
| Virtual-thread pinning fix | JDK 24 | JEP 491 — `synchronized` no longer pins |
| JSpecify | 1.0 | `org.jspecify:jspecify:1.0.0`; Spring Framework 7 is annotated with it |
| Error Prone | ≥ 2.36 | The floor NullAway requires |
| NullAway | 0.12.x | `OnlyNullMarked` mode for incremental adoption |
| JUnit | 6.0.x | GA 2025-09; one version across Platform/Jupiter/Vintage; Java 17 baseline |
| PIT (pitest) | 1.19.4+ | Incremental analysis; JUnit Platform engines (JUnit 6 Jupiter) via the separate `pitest-junit5-plugin` (1.2.x) |
| jqwik | 1.10.x | Property-based testing |
| ArchUnit | 1.4.x | Architecture rules as tests |
| Testcontainers | current | With Spring Boot `@ServiceConnection` |
| OSV-Scanner | current | Dependency CVEs in CI |
| CycloneDX | current | SBOM plugins for Gradle and Maven |

> **Volatility note.** Versions above are current as of **Aug 2026 — re-verify before
> pinning**. Java ships every six months and preview JEPs renumber each release; the
> structured-concurrency row in particular expires when JDK 27 finalizes it.

## The Doctrine — the J-standards (BLOCKING at review)

`/be`'s numbered Engineering Standards 1–7 (facts-only Javadoc, no narration comments,
naming, builder beyond six params, stream-vs-loop, complexity, AOP-for-cross-cutting-only)
apply verbatim and are not repeated here. The J-standards below are the language doctrine
on top of them: each is one rule sentence plus its rationale, enforced at review. A
violation is a review finding, not a style comment.

### Type-driven design

**J1 — Value types are records.** Every value type is a `record`; its compact constructor
validates and defensively copies (`List.copyOf`) so no invalid or externally mutable
instance can exist. A final-fields-plus-getters class that could be a record is a review
flag: it hand-writes the equality and accessors the language now provides, and
hand-written versions drift.

```java
// BAD — hand-rolled value class: the caller's list mutates the "immutable" order later
public final class Order {
    private final List<LineItem> items;
    public Order(List<LineItem> items) { this.items = items; }
    public List<LineItem> items() { return items; }
}

// GOOD — record; the compact constructor validates and copies once, at the boundary
public record Order(OrderId id, List<LineItem> items) {
    public Order {
        Objects.requireNonNull(id);
        if (items.isEmpty()) throw new IllegalArgumentException("order needs items");
        items = List.copyOf(items);
    }
}
```

**J2 — Closed hierarchies are sealed and switched without `default`.** Every domain
variant set is a `sealed interface`, and consumption is `switch` pattern matching with
no `default` branch — so adding a variant breaks compilation at every consumer instead
of falling through silently at runtime. A `default` arm is legitimate only over
non-sealed types you do not control.

```java
// BAD — default arm: a new Refunded variant is silently "unknown" in production
String describe(OrderEvent event) {
    return switch (event) {
        case Created c -> "created";
        case Cancelled c -> "cancelled";
        default -> "unknown";
    };
}

// GOOD — sealed set, no default: adding Refunded breaks the build at every consumer
sealed interface OrderEvent permits Created, Cancelled, Refunded {}

String describe(OrderEvent event) {
    return switch (event) {
        case Created c -> "created";
        case Cancelled c -> "cancelled";
        case Refunded r -> "refunded";
    };
}
```

**J3 — Invariants live in types, not comments.** A status enum plus nullable fields makes
every reader re-derive which fields are legal in which status, and lets no compiler check
the answer. Model one sealed variant per state, each carrying exactly the data that is
legal in that state.

```java
// BAD — which fields may be null in which status? The answer lives in reviewers' heads
public record Payment(PaymentStatus status,
                      @Nullable Instant capturedAt,
                      @Nullable String refundReference) {}

// GOOD — each state carries exactly its legal data; no illegal combination compiles
public sealed interface Payment permits Pending, Captured, Refunded {}
public record Pending(PaymentId id) implements Payment {}
public record Captured(PaymentId id, Instant capturedAt) implements Payment {}
public record Refunded(PaymentId id, Instant capturedAt, String refundReference)
        implements Payment {}
```

**J4 — Domain identifiers are value records.** `record UserId(String value)` with
validation in the compact constructor — never a raw `String` or `long`. Raw identifiers
let any ID fill any parameter, so an argument swap compiles cleanly and corrupts data;
an identifier record turns the same mistake into a type error.

**J5 — Public methods return `Optional`, never `null`.** A `null` return is an invisible
contract every caller must remember; `Optional` puts absence in the signature where the
compiler and NullAway can see it. `Optional` is a return type only — never a field (it
adds a second null-ish state to store) and never a parameter (it forces ceremony an
overload avoids).

### Nullness

**J6 — Every package is `@NullMarked`.** With JSpecify 1.0, non-null is the default and
`@Nullable` the visible, checkable exception — one `package-info.java` annotation per
production package. Spring Framework 7's own APIs are JSpecify-annotated, so the checker
sees through framework calls instead of stopping at them.

**J7 — NullAway runs in the build as an ERROR.** `-Xep:NullAway:ERROR` on Error Prone
≥ 2.36, with `OnlyNullMarked` mode for incremental adoption; the full wiring lives in
`references/build-and-quality-gates.md`. This is prevention, not review-time detection:
an NPE the compiler could have refused should never reach a reviewer, let alone
production.

**J8 — Boundary reads are nullable until proven.** `Map.get`, deserialized DTO fields,
and JDBC/ORM reads return "maybe absent" whatever the annotations claim; handle absence
at the read site — `getOrDefault`, `computeIfAbsent`, `orElseThrow` — not three stack
frames later where the reason is gone.

```java
// BAD — NPE at a distance when the tenant is unknown
var region = regionByTenant.get(tenantId);
applyPolicy(region.policy());

// GOOD — absence decided at the read: default it, or fail naming the cause
var region = regionByTenant.getOrDefault(tenantId, Region.DEFAULT);
var strict = Optional.ofNullable(regionByTenant.get(tenantId))
        .orElseThrow(() -> new UnknownTenantException(tenantId));
```

### Immutability

**J9 — Immutable by default.** Final fields, `List.copyOf` on every exposed collection,
defensive copies of mutable inputs at construction, and no setters on domain types —
evolution is a with-style copy or a builder. Immutable objects are safe to share across
virtual threads and to cache without inventing a locking design.

**J10 — No static mutable state.** The only exception is a deliberately designed cache
with documented eviction and thread-safety. Anything else is a hidden global: it couples
tests to execution order, leaks state across requests, and is invisible at every call
site that depends on it.

### Concurrency

**J11 — Virtual threads are the default for I/O-bound concurrency.** One task, one
virtual thread, blocking code that reads top to bottom. Reactive stacks are justified
only when streaming or backpressure is itself the requirement — not as a general
performance posture. Never pool virtual threads: they cost almost nothing to create, and
pooling reintroduces exactly the starvation they exist to remove.

**J12 — Pinning advice is runtime-versioned.** Since JDK 24 (JEP 491), `synchronized` no
longer pins a virtual thread to its carrier; the remaining pinning sources are native
frames and class initializers. Diagnose with the JFR `jdk.VirtualThreadPinned` event
before touching any code. The old "replace `synchronized` with `ReentrantLock`" advice
applies **only to pre-24 runtimes** — say which runtime you are on before repeating it.

```java
// BAD on JDK 24+ — mechanical rewrite of working code, citing an obsolete rule
private final ReentrantLock lock = new ReentrantLock();
void refresh() {
    lock.lock();
    try { reload(); } finally { lock.unlock(); }
}

// GOOD on JDK 24+ — synchronized does not pin; verify with JFR, not folklore
synchronized void refresh() {
    reload();
}
```

**J13 — `ScopedValue` over `ThreadLocal` for context propagation.** `ScopedValue` is
final since JDK 25 (JEP 506): immutable, bounded to a scope, inherited by structured
subtasks, and impossible to forget to `remove()`. A new `ThreadLocal` requires written
justification in the PR.

**J14 — Structured concurrency for fan-out — as a preview-gated choice.**
`StructuredTaskScope` with a `Joiner` expresses fork/join with correct cancellation, but
it is **preview** (JEP 505 in 25, renamed in 26's JEP 525, expected final in 27). Policy:
preview features are OFF in production unless the project explicitly opts in and records
the decision. The no-preview fallback: submit each subtask individually and consume
completions via an `ExecutorCompletionService` (or a list of futures polled as they
finish) under an explicit deadline; on the first failure, cancel the remaining futures
yourself — note that `invokeAll` cannot do this, since it blocks until every task
finishes and surfaces failures only at `Future.get`. Either way, every fork is joined —
a fire-and-forget submit is a defect.

**J15 — Every blocking external call has an explicit timeout.** HTTP, JDBC, queue,
cache — connect and read timeouts stated at the call site or the client builder, never
inherited from a library default, because the library default is usually "infinite".

**J16 — Modern replacements** (rows, not standards):

| Legacy | Replace with |
|--------|--------------|
| JNI | FFM — `java.lang.foreign` (final since 22) |
| Collect-then-restream pipelines | Gatherers — `windowFixed`, `scan`, `mapConcurrent` (final since 24) |
| `java.util.Date` / `Calendar` | `java.time` |
| Reproducible RNG via `ThreadLocalRandom` | `SplittableRandom(seed)` — `ThreadLocalRandom` cannot be seeded |
| `finalize()` | `Cleaner` |
| `Pattern.compile` per call | Cached `static final Pattern` |
| Service logic `static` on a DI bean | Instance method — substitutable and injectable |

Primitive selection, when shared state or coordination is genuinely needed:

| Concept | Tool | When |
|---------|------|------|
| Thread-safe collections | `ConcurrentHashMap`, `CopyOnWriteArrayList` | Shared mutable state |
| Atomic operations | `AtomicReference`, `VarHandle`, `LongAdder` | Lock-free updates |
| Locks | `ReentrantLock`, `StampedLock`, `ReadWriteLock` | Fine-grained locking |
| Synchronizers | `CountDownLatch`, `Semaphore`, `Phaser`, `CyclicBarrier` | Thread coordination |
| Executors | `newVirtualThreadPerTaskExecutor()`, `ForkJoinPool` | Task scheduling |
| `CompletableFuture` | `thenApply`, `thenCompose`, `allOf`, `anyOf` | Async composition |

### Build hygiene

**J17 — Versions live in exactly one place.** Gradle: the version catalog
`gradle/libs.versions.toml` is the ONLY location a version literal may appear. Maven: BOM
imports plus `<properties>`. A version literal inside a dependency declaration is a
review flag — two locations for one version is how a build ends up running two versions.

**J18 — The quality gate compiles in CI.** Error Prone + NullAway as errors and
`-Xlint:all`, with suppressions only as named annotations at the narrowest scope, each
carrying its justification. A warning nobody fails on is documentation of a defect, not
a gate.

**J19 — Dependency integrity is enforced, not assumed.** Gradle dependency verification
metadata or a Maven lockfile; reproducible builds; OSV-Scanner in CI (preferred over
owasp-dependency-check for its false-positive rate — both are acceptable); a CVSS ≥ 7
finding blocks merge; SBOM published via CycloneDX. Wiring in
`references/build-and-quality-gates.md`.

### Testing

**J20 — JUnit 6.** One version across Platform, Jupiter, and Vintage (Java 17 baseline).
Naming keeps the house convention: `should_<expected>_when_<condition>`, or a
`@DisplayName` sentence about observable behaviour. The unit-test toolkit and shape:
**Mockito 5** (`@Mock`, `@InjectMocks`, `BDDMockito`; mock collaborators, never the type
under test), **AssertJ** fluent assertions (`assertThat().extracting()`,
`assertThatThrownBy()`), Given-When-Then structure with one assertion *concept* per
test, no interdependence between tests (any order, any subset), and test-data builders
over copy-pasted fixture literals. The pyramid holds: many unit tests, fewer
integration/slice tests, few end-to-end — inverted pyramids are slow and flaky where
they are supposed to be cheap and exact.

**J21 — Parameterized tests for input classes; properties for invariants.** Input
partitions get `@ParameterizedTest`; algebraic invariants — round-trips, idempotency,
ordering, merge-commutativity — get jqwik properties, and each property names the
invariant it defends (`serialization_round_trips_any_valid_order`), because a property
that cannot be named is usually not an invariant.

**J22 — Architecture rules are tests.** ArchUnit encodes the layered dependency
direction, no package cycles, domain-packages-import-no-framework, no field injection,
no `java.util.Date`, and a deprecated-symbol freeze. An approved architecture boundary
decision lands as an ArchUnit rule **in the same PR** — the extension-point discipline
of `../../../architecture/solution-architect/references/design-for-predictability.md`
(D6) made executable. Starter class in `references/build-and-quality-gates.md`.

**J23 — Mutation testing gates new code.** PIT 1.19.4+ with the `pitest-junit5-plugin`
(JUnit Platform engines are not built into pitest core) and incremental analysis on PR CI:
mutation score ≥ 75% on new and changed classes, plus a weekly full run to keep the
history honest. Advisory for the first sprint, then blocking. Never chase 100% —
equivalent mutants make it unreachable, and the chase produces assertion noise.

**J24 — Integration tests run the real thing.** Testcontainers-first, with
`@ServiceConnection` under Spring Boot. A mocked repository in an integration test
verifies the mock, not the query, and stays green while the SQL is wrong.

### Security — boundary classes (each names its guard)

**J25 — Bean Validation on every boundary DTO.** Every request object carries constraint
annotations and is validated (`@Valid`) at the controller; an unvalidated request object
reaching a service is BLOCKING at review. The guard is the constraint set plus the test
that rejects an invalid payload.

**J26 — Native serialization of untrusted data is prohibited.** `ObjectInputStream` over
anything an outsider can influence is remote code execution waiting for a gadget chain.
Where legacy makes it unavoidable, the guard is a JVM-wide `ObjectInputFilter` allowlist
(JEP 290/415) — named in the ticket, asserted by a test.

**J27 — Path traversal: resolve, normalize, prove containment.** Every path built from
external input goes through `resolve(...).normalize()` and a `startsWith(baseDir)` check —
including the zip-slip variant, where the hostile name arrives as an archive entry.

```java
// BAD — "../../etc/cron.d/job" in an entry name writes outside baseDir (zip-slip)
Path target = baseDir.resolve(entry.getName());
Files.copy(zip.getInputStream(entry), target);

// GOOD — normalize, then prove the result is still inside the base
Path target = baseDir.resolve(entry.getName()).normalize();
if (!target.startsWith(baseDir)) {
    throw new UnsafeArchiveEntryException(entry.getName());
}
Files.copy(zip.getInputStream(entry), target);
```

**J28 — SSRF: allowlist before fetch.** A client-supplied URL passes a host allowlist and
a deny of loopback, private and link-local ranges (127.0.0.0/8, 10/8, 172.16/12,
192.168/16, 169.254/16, `::1`, `fd00::/8`, `fe80::/10`) **before** any request is made — after DNS resolution, so a hostname pointing
into the private range is caught too. The guard is the checked resolver the HTTP client
is built with.

**J29 — ReDoS: regexes over user input are bounded.** No nested quantifiers or
overlapping alternation over user input; input length bounded before matching; patterns
cached as `static final`. A backtracking regex plus one pathological string is a CPU
denial of service.

**J30 — Secrets never touch code or logs.** Environment or secret manager only; never in
source, never logged. Configuration classes' `toString` redacts secret fields, and a
test asserts the redaction — the test is the guard that survives refactors.

## Deep-dive references (load on demand)

- `references/build-and-quality-gates.md` — the complete build wiring: version catalog,
  Error Prone + NullAway for Gradle and Maven, the `@NullMarked` package template, the
  ArchUnit starter class, PIT configuration, Testcontainers templates, verification
  metadata, OSV-Scanner, CycloneDX. Load when setting up or reviewing build/CI for any
  Java module.

Cross-links (owned elsewhere — do not duplicate here):
- Spring, persistence, API design, messaging — `/be`'s
  `../../backend/java/backend-developer/references/java-expertise.md`; the role skill
  itself is `../../backend/java/backend-developer/SKILL.md`.
- SQL written anywhere in the stack — the sql language skill, `../sql/SKILL.md`.
- Rust components in the same product — the rust language skill, `../rust/SKILL.md`.

## Workflow note

This skill owns no gates. The `workflow-engine` contract and the role agents' gate checks
apply unchanged; this skill supplies the language knowledge inside them. Java-specific
gate triggers to know (they mirror `workflow.yaml` — that file decides):

- New dependencies, new modules, and new service boundaries are **ARCH triggers**
  (`new_dependency`, `new_service`, `cross_boundary`).
- Security-sensitive surfaces — auth, secrets, deserialization, file or URL handling
  fed by external input — are **SECOPS triggers**.

Whether those gates fire is the workflow-engine's decision, not this skill's. What this
skill supplies is the evidence the gates consume: the sealed model, the stated null
contract, the ArchUnit rules, and the green quality gate are what `/rev` and `/verify`
check against.

## Checklist

### Before Implementing
- [ ] Domain model sketched as records and sealed types — illegal states unrepresentable (J1–J3)
- [ ] Null contract stated: which packages are `@NullMarked`, which fields/returns are `@Nullable` (J6–J8)
- [ ] Test list written — behaviour sentences before any implementation (J20–J21)
- [ ] Stack versions confirmed against `## Versions` — re-verified if that table is stale

### Before Commit
- [ ] Error Prone + NullAway clean at ERROR (J7, J18)
- [ ] ArchUnit suite green (J22)
- [ ] All tests green, including Testcontainers integration tests (J24)
- [ ] No version literal outside the catalog / properties (J17)
- [ ] Change verified as landed — behaviour observed, not assumed (the `verify-landed` process skill)

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Boolean-plus-nullable state | Illegal combinations representable; every reader re-derives the legal ones | One sealed variant per state (J2, J3) |
| `default` arm on a sealed switch | New variants are swallowed silently at runtime | Exhaustive switch, no default (J2) |
| `@Autowired` field injection | Hidden dependencies; untestable without a container | Constructor injection; ArchUnit forbids the field form (J22) |
| Raw `String`/`long` domain IDs | Any ID fits any parameter; swaps compile and corrupt data | Identifier records validating on construction (J4) |
| `null` return from a public method | Invisible contract; NPE at a distance | `Optional` return (J5) |
| `Optional` as field or parameter | A second null-ish state in storage; ceremony at call sites | `Optional` as a return type only (J5) |
| `ThreadLocal` for request context | Leaks across carriers; error-prone cleanup | `ScopedValue` (J13) |
| Pooled virtual threads | Reintroduces the starvation virtual threads remove | One task, one virtual thread (J11) |
| Pre-24 pinning advice applied to 24+ | Churn with no effect; hides the real pinning sources | JEP 491 applies; diagnose with JFR `jdk.VirtualThreadPinned` (J12) |
| Version literals in build files | Two locations for one version become two versions | Catalog / BOM + properties only (J17) |
| Mocked repositories in integration tests | Verifies the mock while the SQL is wrong | Testcontainers (J24) |
| Unvalidated boundary DTO | Malformed input reaches domain logic | Bean Validation + `@Valid`, with a rejection test (J25) |
| Native serialization of untrusted input | Gadget-chain remote code execution | Prohibited; legacy behind an `ObjectInputFilter` allowlist (J26) |
| Catching `NullPointerException` as flow control | Hides the defect the checker would have refused | Fix the null contract (J6–J8) |
