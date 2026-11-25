---
name: hibernate-eager-fetching
description: >-
  Diagnose and safely convert EAGER associations to LAZY in Hibernate / Spring Data JPA.
  Use this skill whenever an association is (or resolves to) `FetchType.EAGER`, whenever the user mentions
  "EAGER fetching", "eager loading", "FetchType.EAGER", "make this LAZY", "why is this always
  joined / always loaded", "too many joins", a `@ManyToOne`/`@OneToOne` that loads its target
  unconditionally, `LazyInitializationException` risk when switching to LAZY, or "review this
  entity's fetch types". Trigger it even when the user only says "this query loads too much",
  "reduce what this entity fetches", or pastes an entity with an eager association. Crucially,
  use it when the user wants to find the *real* resolved fetch type — which since JPA 4 can no
  longer be read off the `fetch` attribute of the annotation — from a running application's
  entities profile via the Axelix MCP server (the `getApplicationEntitiesProfile` tool).
---

# Fixing EAGER Fetching in Hibernate

An `EAGER` association is loaded **every single time** its owning entity is loaded, no matter
whether the current code path touches it. Every `findById`, every `findAll`, every derived
query, every `JOIN FETCH` of the entity drags the eager association along — as an extra join
(and, when several eager to-many associations meet, a cartesian product), or as a follow-up
`SELECT`. The cost is invisible in the source: the mapping says `@ManyToOne` and the query
reads innocently, but the database does more work on **every** load, forever, for code paths
that never wanted the data.

`@ManyToOne` and `@OneToOne` default to `EAGER` in JPA, so most eager associations got that way
without anyone choosing it. **The right default is `LAZY`** — load an association only where a
code path actually needs it.

The catch is that you **cannot** just flip `EAGER` → `LAZY` and walk away. Every place that
currently relies on the association being pre-loaded — because it navigates it after the
transaction, or after the entity is detached — will start throwing `LazyInitializationException`
at runtime. The tests may not catch it. So the fix is deliberately **multi-staged**: pick one
association, find where it's loaded, judge how safely you can change it, and re-supply the
association *exactly* where it's genuinely needed with `@EntityGraph`.

The examples below assume this domain model — note the eager `@ManyToOne`:

```java
@Entity
@Table(name = "orders") // "order" is a reserved word in SQL; pluralizing is safer
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status;

    // ⚠ EAGER (the JPA default for @ManyToOne) — loaded on every Order load
    @ManyToOne // fetch defaults to EAGER
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();
}

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;
}
```

---

## Step 0 — Let the application tell you the *real* fetch type (Axelix MCP)

**You cannot determine the eventual fetch type by reading the annotation.** Since JPA 4, the
`fetch` attribute of `@ManyToOne`/`@OneToOne`/etc. is no longer the last word: JPA introduced a
**configurable default fetch mode**, so an association written with no `fetch` (or even one that
looks LAZY) can resolve to something else at runtime depending on configuration. Reading
`@ManyToOne` and concluding "EAGER", or reading `fetch = LAZY` and concluding "LAZY", is now
unreliable. The **real, resolved** fetch type has to come from the running application.

That is exactly what the **Axelix MCP server** provides. If it is connected in this session, it
exposes a tool named **`getApplicationEntitiesProfile`** that reports each entity's associations
annotated with their **actual resolved fetch type** — so you fix associations that are genuinely
eager at runtime, not ones you *guessed* were eager from the source.

**When to use it.** Whenever the tool is available and you're diagnosing eager fetching (or the
user asks to "find the EAGER associations", "which associations load eagerly", "review fetch
types", etc.), call it first and trust its resolved fetch type over the annotation. If the Axelix
MCP server is **not** connected, say so, and fall back to reading the annotations — while warning
the user that on JPA 4+ the annotation may not reflect the real fetch type, so the audit could be
incomplete.

**How to call it.** The tool needs the application's GAV coordinates, found in the build file
(`pom.xml`, `build.gradle`, or `build.gradle.kts`):

- `groupId` (**required**) — the G of the GAV coordinate.
- `artifactId` (**required**) — the A of the GAV coordinate.
- `entityName` (optional) — The name of the entity to inspect (e.g. 'Order').

**What it returns.** A profile of the application's entities. Each association carries its
**resolved `fetchType`** (`EAGER` / `LAZY`); the eagerly-fetched ones are your candidates. Collect
the associations resolved to `EAGER` and present that list to the user — it is the authoritative
starting point for the rest of this skill.

---

## Step 1 — Fix ONE association at a time (ask the user which)

Do **not** convert every eager association in one sweep. Each conversion is a behavioral change
with its own call-site risk, and bundling several into one commit makes the blast radius
impossible to review. Fix them **one by one**, one association per commit.

So, before changing anything, **ask the user which association to fix first.** Present the eager
associations surfaced in Step 0 (owning entity + field) and let them choose. Use `AskUserQuestion`
with the concrete candidates. Everything below applies to that **single** chosen association;
loop back here for the next one.

---

## Step 2 — Find every call site that loads the owning entity

The flip to `LAZY` is one line; the work is making sure nothing breaks. So before touching the
mapping, **enumerate every place the owning entity is loaded**, because each one is a place the
association might be navigated:

- **Spring Data repositories** — this is the common case. Every derived query (`findByStatus`,
  `findById`, `findAll…`), every `@Query`, every `@EntityGraph` method, and every
  `JpaSpecificationExecutor` usage that returns the owning entity.
- **Direct `EntityManager` / `Session` queries** — JPQL/HQL/Criteria that select the entity.
- Any other loader that returns the entity to code which may navigate the association after the
  session closes.

For a large codebase this search is the crux, and doing it by hand loses coverage. **Launch
subagents** (the `Explore` agent) to sweep the repositories and query layers and report back the
full list of methods/queries that load the owning entity. Accuracy here is what keeps you from
shipping a `LazyInitializationException`.

---

## Step 3 — Make the assessment: overcompensate vs. cherry-pick

The exact fix now depends on **how confidently you can change the code without breaking it.**
Judge two things: how many code paths load this entity, and whether the project has **real
integration tests** — tests that boot the Spring context and exercise the repositories against a
database (Testcontainers, `@SpringBootTest`, `@DataJpaTest`), such that a hidden
`LazyInitializationException` would actually surface. Unit tests with mocked repositories catch
**nothing** here.

### Case A — Large surface and/or weak tests → overcompensate, then trim

If the entity is loaded in **many** places and the project has **no sufficient, high-quality
integration tests**, a targeted change is dangerous: you can't prove you found every navigation of
the association, and the tests won't catch the ones you missed. So **overcompensate**. After
flipping the association to `LAZY`, add an `@EntityGraph` that re-fetches it to **every** repository
method (and every direct `EntityManager`/`Session` query) that loads the owning entity. This
re-supplies the association everywhere it used to be present, so nothing that relied on it breaks —
you over-fetch in some paths, but you don't throw at runtime.

Then **trim the over-fetching back down safely.** For **each** repository method where you added the
`@EntityGraph`, launch a subagent to answer one question about that method's call paths:

> Does this code path actually use the `customer` association on the `Order` it loads?

- **Yes** → keep the `@EntityGraph`.
- **No** → remove it; that path now correctly loads the entity without the association.

This converges on the correct state (association fetched only where used) without ever passing
through a broken state.

### Case B — Small surface and/or solid integration tests → cherry-pick

If there are only a **few** code paths that load the entity, **or** the project has **solid
integration tests** that would catch a `LazyInitializationException`, you can afford precision.
Trace the minimal set of code paths — again **using subagents** to explore each path so the
analysis stays accurate — and add `@EntityGraph` **only** to the specific methods whose callers
genuinely navigate the association. Everywhere else, the entity loads lazily, as it should. Then
run the integration tests to confirm nothing throws.

**When unsure which case you're in, treat it as Case A.** Over-fetching is a performance nuisance;
a `LazyInitializationException` in production is an outage. Overcompensate first, then trim.

---

## Step 4 — Apply the fix

**Flip the mapping to LAZY:**

```java
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "customer_id", nullable = false)
private Customer customer;
```

**Re-supply the association where it's needed with `@EntityGraph`.** This is the fix to reach for
here — it declares "load this association eagerly *for this query*" without hard-coding a join into
JPQL, and it reads cleanly on derived queries:

```java
interface OrderRepository extends JpaRepository<Order, Long> {

    // customer is navigated by this method's callers → fetch it here
    @EntityGraph(attributePaths = "customer")
    List<Order> findByStatus(Status status);

    // customer is NOT navigated by this method's callers → leave it lazy (Case A: trimmed; Case B: never added)
    List<Order> findByOrderDateBefore(LocalDateTime cutoff);
}
```

If the same fetch shape recurs across many methods, define it once as a `@NamedEntityGraph` on the
entity and reference it by name (`@EntityGraph("Order.withCustomer")`) instead of repeating
`attributePaths`.

**Caveats to keep in mind** (they mostly bite to-*many* associations, so a `@ManyToOne`/`@OneToOne`
conversion is usually clear of them, but check):

- **Pagination.** An `@EntityGraph` that fetches a **collection** on a `Pageable` query triggers
  Hibernate's in-memory pagination on versions older than 7.4 — see the sibling
  `hibernate-in-memory-pagination` skill. To-one graphs page fine.
- **Multiple collections.** Graph-fetching two to-many associations in one query yields a cartesian
  product (or `MultipleBagFetchException`) — see the sibling `hibernate-n-plus-one` skill for the
  `@BatchSize` fallback.

---

## Step 5 — Verify

Run the project's integration tests — the ones that boot the context and hit a database. This is
the whole point of the assessment in Step 3: the conversion is only safe once something has
actually exercised the changed code paths and *not* thrown `LazyInitializationException`. If the
project has no such tests, say so plainly to the user: the change rests on the Case A
overcompensation, not on a test proving it works. Then commit — just this one association — and
loop back to Step 1 for the next.

---

## Quick reference

| Situation | What to do |
|---|---|
| Determining the real fetch type on JPA 4+ | **Don't read the annotation** — call `getApplicationEntitiesProfile`; the resolved `fetchType` is authoritative |
| Axelix MCP not connected | Fall back to reading annotations, but warn the audit may be incomplete on JPA 4+ |
| Several eager associations to fix | One association per commit — **ask the user which first** |
| Finding where the entity is loaded | Sweep repositories + `EntityManager`/`Session` queries with **subagents** |
| Many call sites, weak/no integration tests | **Case A**: flip to LAZY, add `@EntityGraph` **everywhere**, then trim per-method with a subagent asking "is the association used here?" |
| Few call sites, or solid integration tests | **Case B**: trace paths with subagents, add `@EntityGraph` only where the association is navigated |
| Unsure which case | Treat as **Case A** — over-fetch beats a production `LazyInitializationException` |
| Re-supplying the association | `@EntityGraph(attributePaths = …)` on the methods that need it; `@NamedEntityGraph` if reused |
| Graph fetches a collection under `Pageable` | Watch for in-memory pagination (< 7.4) — see `hibernate-in-memory-pagination` |

Bottom line: `EAGER` loads an association on every entity load whether or not it's wanted; the fix
is `LAZY` **plus** `@EntityGraph` only where the association is genuinely used. But flipping to LAZY
risks `LazyInitializationException`, so work one association at a time: get the *real* fetch type
from Axelix (not the annotation), find every loader with subagents, and choose — overcompensate and
trim when the surface is large or untested, cherry-pick when it's small or well-tested.
