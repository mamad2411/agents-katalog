---
name: hibernate-n-plus-one
description: >-
  Diagnose and fix the N+1 select problem in Hibernate / Spring Data JPA code.
  Use this skill whenever code lazily loads a `@OneToMany`/`@ManyToOne`/`@ManyToMany`
  association inside a loop or a stream, whenever a repository/query returns entities
  whose associations are later touched per-row, or whenever the user mentions "N+1",
  "N + 1", "select N+1", lots of repeated SELECTs, slow list/page endpoints, lazy
  loading, `JOIN FETCH`, `@EntityGraph`, `@BatchSize`, `LazyInitializationException`,
  or "why is this query firing hundreds of times". Trigger it even when the user only
  says "make this repository faster", "reduce the number of queries", "review this JPA
  code for performance", or pastes an entity + a loop over its collections. Also use it
  when the user wants to find N+1 problems from a running application's transaction
  profile via the Axelix MCP server (the `getApplicationTransactionsProfile` tool).
---

# Fixing the Hibernate N+1 Select Problem

The N+1 problem is the single most common performance defect in JPA code. You run **one**
query to load a list of root entities, then Hibernate silently runs **one more query per
row** to lazily initialize an association you touch — 1 + N queries where a single join
would do. It hides well: the code reads like plain object graph navigation, and it only
hurts once the list grows in production.

Your job with this skill is twofold: **confirm it's actually N+1**, then **pick the
right fix**. The fixes are not interchangeable — the "obvious" one (`JOIN FETCH`) is
outright wrong in two common situations, and picking blindly either explodes the heap or
throws at runtime. Walk the decision procedure below rather than reaching for the first
option.

Throughout this skill the examples assume this domain model:

```java
@Entity
@Table(name = "orders") // "order" is a reserved word in SQL; pluralizing is safer
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "order_date", nullable = false)
    private LocalDateTime orderDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<OrderStatusHistory> statusHistory = new HashSet<>();

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();
}

@Entity
@Table(name = "order_items")
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "product_name", nullable = false)
    private String productName;

    @Column(nullable = false)
    private Integer quantity;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal price;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;
}
```

---

## Step 0 — Let the application point you at the problems (Axelix MCP)

Before hunting for N+1 by reading code, check whether the **Axelix MCP server** is
connected in this session. If it is, it exposes a tool named
`getApplicationTransactionsProfile` that returns a feed of the transactions the running
application actually executed, each annotated with the persistence problems observed
inside it. This beats a static scan: it reports what genuinely happened at runtime, so you
fix real N+1s instead of guessing from the code shape.

**When to use it.** Whenever the tool is available and you're diagnosing N+1 (or the user
asks to "find the N+1s", "review this service for N+1", etc.), call it first to get the
list of offenders, then jump straight to the offending methods. If the Axelix MCP server
is **not** connected, skip this step and diagnose from the code starting at Step 1.

**How to call it.** The tool needs the application's GAV coordinates, found in the build
file (`pom.xml`, `build.gradle`, or `build.gradle.kts`):

- `groupId` (**required**) — the G of the GAV coordinate.
- `artifactId` (**required**) — the A of the GAV coordinate.
- `className` (optional, fully qualified) — narrow to every transactional method of one
  class.
- `methodName` (optional) — narrow to a single method; **only valid together with
  `className`**. With neither, you get the problems for the whole application.

Start broad (whole application), or pass `className`/`methodName` when the user already
pointed you at a specific area.

**What it returns.** A JSON feed of problematic transactions. Each entry carries a
`transactionalKey` (the class + method where the problem lives) and two kinds of problems:

- `nPlusOne` — the N+1 lazy-loading occasions. Each names `ownerEntityClass` (the entity
  owning the lazily loaded association, e.g. `com.example.Order`) and
  `associationPropertyName` (the association loaded N+1, e.g. `items`). An association is
  only reported here when it was lazily loaded **more than once** in the transaction — i.e.
  it's genuinely N+1, so Step 1's confirmation is already done for you.
- `inMemoryPaginatedEntities` — entities whose queries were paginated **in memory**. Treat
  this as a strong signal that pagination is involved in that transaction, which directly
  constrains your fix (see the pagination caveat in Step 2 / §1).

**Turning the feed into fixes.** For each reported problem, open the method named by
`transactionalKey`, locate the association from `ownerEntityClass` /
`associationPropertyName`, then run the decision procedure below to pick the fix. A
`transactionalKey` that also shows up under `inMemoryPaginatedEntities` almost certainly
paginates — lean toward `@BatchSize`/projection rather than a collection `JOIN FETCH`.

---

## Step 1 — Confirm it really is N+1

Don't apply a fix on a hunch. N+1 has a specific shape: **a collection or lazy
association is accessed once per element of an already-loaded list.** Look for:

- A repository/query that returns a `List`/`Page`/`Stream` of root entities, followed by
  a loop, `for`, `.stream().map(...)`, or `.forEach(...)` that reads a `LAZY` association
  (`order.getItems()`, `order.getItems().size()`, `order.getStatusHistory()`, a
  `@ManyToOne` back-reference, etc.).
- Logs showing the same `SELECT ... WHERE fk = ?` firing many times with different
  parameters. Enabling `spring.jpa.show-sql=true` (or `hibernate.SQL` at DEBUG) makes it
  obvious.

If the association is never touched, there is no N+1 — don't add a fetch that pulls data
nobody uses. If you only need an aggregate (a `count`, a `size()`), jump to
[the projection option](#5-dto--aggregate-projection-when-you-dont-need-the-entities);
fetching whole collections just to call `.size()` is wasteful even when it's not N+1.

The canonical offender:

```java
interface OrderRepository extends JpaRepository<Order, Long> {

    List<Order> findAllByStatus(Status status);
}

@Transactional
public void processOrders() {

    List<Order> orders = orderRepository.findAllByStatus(Status.FOR_PROCESSING);

    for (Order order : orders) {
        // getItems() is LAZY → one extra SELECT per order → N+1
        var notification = new OrderProcessingNotification(order.getId(), order.getStatus(), order.getItems().size());
        order.setStatus(Status.PROCESSED);
    }
}
```

---

## Step 2 — Walk the decision procedure

Answer these in order; the first one that fits is your fix.

1. **Does the root query paginate?** (`Pageable`, or `setFirstResult`/`setMaxResults` on
   a `Query`.) → collection `JOIN FETCH`/`@EntityGraph` is unsafe on Hibernate < 7.4.
   Go to [@BatchSize](#4-batchsize-the-safe-fallback) (or a projection).
2. **Does the root query already `JOIN FETCH` (or graph-fetch) another collection?** →
   a second collection fetch means a cartesian product or `MultipleBagFetchException`.
   Go to [@BatchSize](#4-batchsize-the-safe-fallback).
3. **Do you only need an aggregate / a few columns, not the entities?** → prefer a
   [projection](#5-dto--aggregate-projection-when-you-dont-need-the-entities).
4. **Is this exact fetch shape reused in many places?** → [@EntityGraph](#3-entity-graph)
   (ask the user first — see below).
5. **Otherwise** → [JOIN FETCH](#1-join-fetch-the-default). This is the default; reach
   for it whenever none of the caveats above apply.

---

## 1. JOIN FETCH (the default)

`JOIN FETCH` is the canonical fix. It tells Hibernate to load the association **in the
same SQL statement** via a join, collapsing 1+N queries into one:

```java
interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.status = :status")
    List<Order> findAllByStatus(@Param("status") Status status);
}
```

The service code is unchanged — `order.getItems()` is now already initialized.

**Duplicate roots.** Joining a to-many association multiplies the root row once per child.
For a `List` result you'll get the same `Order` repeated. Use `SELECT DISTINCT` (Hibernate
de-duplicates the entities without adding `DISTINCT` to the generated SQL in modern
versions) or have the caller collect into a `Set`. A `Set`-typed association like
`statusHistory` avoids duplicate *children*, but the *root* list still duplicates.

### Two situations where JOIN FETCH is the wrong tool

**Pagination.** If the root query paginates, do **not** collection-`JOIN FETCH` it on
Hibernate older than 7.4. Pagination limits *rows*, but a to-many join produces multiple
rows per entity, so the database `LIMIT` no longer maps to "N entities". Before 7.4
Hibernate handled this by fetching **the entire result set and paginating in memory**
(you'll see `HHH000104: firstResult/maxResults specified with collection fetch; applying
in memory`) — which defeats pagination and can exhaust the heap. From Hibernate 7.4 on it
rewrites the fetch as a sub-select keyed off the paginated roots, which is safe. So:
check the Hibernate version before pairing a collection fetch with pagination.

```java
// UNSAFE on Hibernate < 7.4 — in-memory pagination
interface OrderRepository extends JpaRepository<Order, Long> {
    Page<Order> findAllByStatus(Status status, Pageable pageable);
}
```

The same rule applies to the `EntityManager`/`Query` API — `setFirstResult` /
`setMaxResults` *is* pagination, no different from `Pageable`:

```java
// Also pagination — same caveat applies
entityManager.createQuery("SELECT o FROM Order o WHERE o.status = :status")
    .setParameter("status", Status.FOR_PROCESSING)
    .setFirstResult(0)
    .setMaxResults(10)
    .getResultList();
```

**A second collection fetch.** If the query already fetches one collection, adding
another is almost always wrong:

```java
// Flawed: two to-many fetches → cartesian product
@Query("SELECT o FROM Order o JOIN FETCH o.statusHistory JOIN FETCH o.items WHERE o.status = :status")
List<Order> findAllByStatusWithHistory(@Param("status") Status status);
```

Joining two collections produces `|statusHistory| × |items|` rows per order — a cartesian
product dragged into memory. With two `List`-typed collections Hibernate refuses outright
with `MultipleBagFetchException`; with `Set`s it "works" but still materializes the
product. Either way, when the root query already fetches a collection, don't add a second
collection fetch — fall back to [@BatchSize](#4-batchsize-the-safe-fallback). (Fetching
one collection plus any number of to-**one** associations in the same query is fine — the
cartesian problem is specific to multiple to-**many** joins.)

---

## 2. Choosing between JOIN FETCH and @EntityGraph

They solve the same problem and share the same two caveats (pagination, multiple
collections). The difference is a guarantee: `JOIN FETCH` *is* a join;
`@EntityGraph` only promises the listed attributes are fetched **eagerly**, and lets
Hibernate choose how. It almost always picks a join, but it doesn't contractually promise
one. So the deciding factor is **reuse**, not performance.

---

## 3. Entity Graph

Use a named entity graph when the *same* fetch shape is needed in **many** call sites —
it's the DRY option, defined once and referenced by name:

```java
@NamedEntityGraph(
    name = "Order.withItems",
    attributeNodes = @NamedAttributeNode("items")
)
@Entity
public class Order { /* ... */ }

interface OrderRepository extends JpaRepository<Order, Long> {

    @EntityGraph("Order.withItems")
    List<Order> findAllByStatus(Status status);
}
```

**Ask the user before extracting a graph.** You usually can't tell from one call site
whether this shape is reused. Ask explicitly: *"Is loading `Order` together with its
`items` a common pattern across the codebase, or is it just this one query?"* If it's
common, a named graph pays for itself. If it's a one-off, an inline `JOIN FETCH` is
simpler and keeps the fetch plan next to the query that needs it. Don't add graph
machinery speculatively.

---

## 4. @BatchSize (the safe fallback)

When the caveats rule out both `JOIN FETCH` and `@EntityGraph` — the root query
**paginates**, or it **already fetches another collection** — `@BatchSize` is the fix
that needs **no change to the business logic**. It doesn't eliminate the extra queries;
it *batches* them. Instead of N single-row lookups, Hibernate loads the lazy association
for up to `size` parents at once with an `IN (?, ?, …)`, turning 1+N into
1 + ⌈N/size⌉ queries:

```java
public class Order {

    @BatchSize(size = 50)
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();
}
```

Because it keeps the paginated root query intact and touches only how the *association*
is loaded, it composes with pagination and with an existing fetch where a join can't.

**Before applying it, tell the user why you fell back to it** — name the condition that
ruled out the join (e.g. "the query pages with `Pageable` and you're on Hibernate 6.x, so
a collection `JOIN FETCH` would paginate in memory"), then **ask what batch size to use.**
The right value depends on data shape: too small and you barely cut the query count; too
large and the `IN` list gets unwieldy and you over-fetch. A common starting point is
25–100. There's also a global default, `hibernate.default_batch_fetch_size`, if they'd
rather set it application-wide than per-association — mention it, but let them choose.

`@Fetch(FetchMode.SUBSELECT)` is a related alternative: it loads the association for
*all* parents in the result set with a single sub-select rather than fixed-size batches.
It's a good fit when you routinely process the whole list; offer it if `@BatchSize`'s
tuning knob feels arbitrary for their use case.

---

## 5. DTO / aggregate projection (when you don't need the entities)

If the loop only needs a **scalar or a few columns** — the classic case being
`order.getItems().size()` — loading whole entity collections is wasteful even done in one
join. Ask the database for exactly what you need instead:

```java
// Only the count is needed → let the DB count
public record OrderSummary(Long orderId, Status status, long itemCount) {}

interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("""
        SELECT new com.example.OrderSummary(o.id, o.status, COUNT(i))
        FROM Order o LEFT JOIN o.items i
        WHERE o.status = :status
        GROUP BY o.id, o.status
        """)
    List<OrderSummary> summariesByStatus(@Param("status") Status status);
}
```

This sidesteps N+1 entirely, moves the aggregation to the database, and pages cleanly
(there's no collection to multiply rows). The trade-off: you get a DTO, not a managed
entity, so it's read-only — not usable when the same code path also **mutates** the
entities (like the `order.setStatus(...)` in the running example). Use projections for
read/report paths; use a fetch strategy when you need managed entities to write back.

---

## Quick reference

| Situation | Fix |
|---|---|
| Plain list, association touched per row | **JOIN FETCH** |
| Same fetch shape reused across many call sites | **@EntityGraph** (confirm reuse with user) |
| Root query **paginates** (Hibernate < 7.4) | **@BatchSize** / projection |
| Root query **already fetches a collection** | **@BatchSize** |
| Loop needs only a count / a few columns | **DTO projection** |
| Two to-many joins in one query | Never — split into one fetch + **@BatchSize** |

Bottom line: default to `JOIN FETCH`; step down to `@EntityGraph` only for reuse; fall
back to `@BatchSize` (explaining why, and asking for the size) when pagination or a
second collection makes a join unsafe; and prefer a projection whenever you don't
actually need the entities.
