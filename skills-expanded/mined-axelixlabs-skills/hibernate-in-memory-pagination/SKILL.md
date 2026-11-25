---
name: hibernate-in-memory-pagination
description: >-
  Diagnose and fix Hibernate's in-memory pagination problem — when a paginated query
  (`Pageable`, `setFirstResult`/`setMaxResults`) is combined with a collection fetch
  (`JOIN FETCH`, `@EntityGraph`, or a `root.fetch(...)` in the Specification/Criteria API)
  and Hibernate, on versions older than 7.4, loads the entire result set into memory and
  paginates there. Use this skill whenever a `Page<Entity>`/paged query also fetches a
  to-many association, whenever the user mentions "in-memory pagination", "in memory
  paging", the `HHH000104: firstResult/maxResults specified with collection fetch; applying
  in memory` warning, `JOIN FETCH` with `Pageable`, `@EntityGraph` with `Pageable`, OOM /
  heap blowups on a paged endpoint, or "why does this paged query load the whole table".
  Also use it when the user wants to find in-memory pagination from a running application's
  transaction profile via the Axelix MCP server (the `getApplicationTransactionsProfile`
  tool).
---

# Fixing Hibernate's In-Memory Pagination Problem

When a paginated query also fetches a to-many collection, Hibernate older than **7.4**
cannot push the `LIMIT` down to the database: a to-many join multiplies the root rows, so
the SQL row count no longer maps to "N entities". Its workaround is to run the query
**without** the limit, pull **the entire filtered result set into the heap**, and paginate
there. You'll see the tell-tale log line:

```
HHH000104: firstResult/maxResults specified with collection fetch; applying in memory
```

It "works" — the returned page is correct — but it defeats the entire point of
pagination: instead of the ~20 rows the page needs, the application materializes the whole
result set. The result is excessive heap usage, GC pressure, higher latency, and, on large
tables, `OutOfMemoryError`.

> **Version note.** This was fixed in **Hibernate 7.4**: from 7.4 on, Hibernate rewrites
> the fetch as a sub-select keyed off the paginated roots and pages on the database side —
> so this problem *only* applies to projects on Hibernate **older than 7.4** (still very
> common). **Confirm the Hibernate version first.** If they're on 7.4+, there is nothing to
> fix; the collection fetch + `Pageable` is safe.

The examples below assume this domain model:

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

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;
}
```

---

## Step 0 — Let the application point you at the problems (Axelix MCP)

Before hunting for in-memory pagination by reading code, check whether the **Axelix MCP
server** is connected in this session. If it is, it exposes a tool named
`getApplicationTransactionsProfile` that returns a feed of the transactions the running
application actually executed, each annotated with the persistence problems observed inside
it — **including the queries that paginated in memory**. This beats a static scan: it
reports what genuinely happened at runtime.

**When to use it.** Whenever the tool is available and you're diagnosing in-memory
pagination (or the user asks to "find the in-memory pagination", "why is this paged
endpoint slow", etc.), call it first, then jump straight to the offending methods. If the
Axelix MCP server is **not** connected, skip this step and diagnose from the code starting
at Step 1.

**How to call it.** The tool needs the application's GAV coordinates, found in the build
file (`pom.xml`, `build.gradle`, or `build.gradle.kts`):

- `groupId` (**required**) — the G of the GAV coordinate.
- `artifactId` (**required**) — the A of the GAV coordinate.
- `className` (optional, fully qualified) — narrow to every transactional method of one
  class.
- `methodName` (optional) — narrow to a single method; **only valid together with
  `className`**. With neither, you get the problems for the whole application.

**What it returns.** A JSON feed of problematic transactions. Each entry carries a
`transactionalKey` (the class + method where the problem lives) and, among its problems:

- `inMemoryPaginatedEntities` — the entities (tables) whose queries were paginated **in
  memory** inside that transaction. This is exactly the problem this skill fixes: each name
  points you at a paginated query that also fetches a collection.
- `nPlusOne` — N+1 lazy-loading occasions (handled by the sibling
  `hibernate-n-plus-one` skill).

**Turning the feed into fixes.** For each entity listed under `inMemoryPaginatedEntities`,
open the method named by `transactionalKey`, find the paginated query that fetches that
entity's collection, then apply the two-query fix below.

---

## Step 1 — Recognize the shape

In-memory pagination is **a collection fetch + pagination in the same query.** The fetch
can be expressed three ways; the pagination is usually a `Pageable`, but
`setFirstResult`/`setMaxResults` on a `Query` is the same thing.

**1. `JOIN FETCH` + `Pageable`** (the most common form):

```java
interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.status = :status")
    Page<Order> findAllByStatus(Status status, Pageable pageable); // ← in-memory pagination
}
```

**2. `@EntityGraph` + `Pageable`** — a graph that pulls in a to-many collection is a
collection fetch too:

```java
interface OrderRepository extends JpaRepository<Order, Long> {

    @EntityGraph("Order.withItems")
    Page<Order> findAllByStatus(Status status, Pageable pageable); // ← in-memory pagination
}
```

**3. `root.fetch(...)` in the Specification / Criteria API** — rarer, but conceptually
identical: a fetch join alongside a paged `findAll`:

```java
public static Specification<Order> hasStatusWithItems(Status status) {
    return (root, query, cb) -> {
        // Only fetch on the data query, not the count query, or the count breaks
        if (query.getResultType() != Long.class && query.getResultType() != long.class) {
            root.fetch("items", JoinType.LEFT); // ← fetch join + Pageable = in-memory pagination
        }
        return cb.equal(root.get("status"), status);
    };
}

// orderRepository.findAll(spec, pageable) → paginates in memory
```

If a paginated query fetches **no** to-many collection (only to-one associations, or no
fetch at all), there is no in-memory pagination — the `LIMIT` pushes down fine. The problem
is specific to pairing pagination with a **to-many** fetch.

---

## Step 2 — Fix it with two queries (fetch IDs, then fetch entities)

The reliable fix splits the work into two selects so that **pagination happens on the
database** and **the collection fetch happens without pagination**:

1. **Page the IDs.** Run the paginated, filtered query returning only the root **IDs** — no
   collection fetch — so the database applies the `LIMIT` correctly.
2. **Fetch the entities for that page.** Load the full entity graph for just those IDs (a
   bounded `IN (...)` of ~page-size IDs), where a collection fetch is safe because there's
   no pagination.

```java
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    // SELECT 1 — page + filter, IDs only, NO collection fetch → DB applies the LIMIT
    @Query("SELECT o.id FROM Order o WHERE o.status = :status")
    Page<Long> findIdsByStatus(@Param("status") Status status, Pageable pageable);

    // SELECT 2 — full graph for just this page's IDs, NO pagination → fetch is safe
    @EntityGraph("Order.withItems")
    List<Order> findByIdIn(List<Long> ids, Sort sort);
}
```

```java
public Page<Order> getOrdersPaginatedSafely(Status status, Pageable pageable) {

    // SELECT 1: page and fetch ONLY the primary IDs on the database side
    Page<Long> idPage = orderRepository.findIdsByStatus(status, pageable);

    if (idPage.isEmpty()) {
        return Page.empty(pageable);
    }

    // SELECT 2: fetch the full graph only for the ~page-size IDs on this page
    List<Order> orders = orderRepository.findByIdIn(idPage.getContent(), pageable.getSort());

    // Re-wrap into a Page so the caller keeps correct pagination metadata (total, etc.)
    return new PageImpl<>(orders, pageable, idPage.getTotalElements());
}
```

Why this works: SELECT 1 has no collection join, so its `LIMIT`/`OFFSET` maps cleanly to
"N orders" and pages on the database. SELECT 2 fetches the collection for a **fixed, small**
set of IDs, so materializing it is bounded by the page size, not the whole table.

### Details that matter

- **Preserve ordering.** The page's order is established by SELECT 1. Pass the same `Sort`
  into SELECT 2 (as above) so the fully-fetched list keeps that order — a to-many join can
  otherwise reorder rows.
- **Total count.** Take `getTotalElements()` from SELECT 1's `Page` and feed it into
  `PageImpl`, so the returned page reports the correct total without a third query.
- **For the Specification/Criteria case**, apply the same split: a paged
  `findAll(idSpec, pageable)` projecting the ID (or a `JpaSpecificationExecutor` returning
  IDs), then a second call that fetch-joins the collection for `id IN (:ids)` with no
  pagination.

---

## Alternatives — mention, but the two-query split is the default

- **Upgrade to Hibernate 7.4+.** The cleanest fix if it's on the table: 7.4 rewrites the
  fetch as a sub-select and pages on the database, so the original one-query form becomes
  safe. Suggest it when a version bump is realistic, but don't assume it is — the two-query
  split works on every version.
- **`@BatchSize` on the collection.** Keep the paginated root query *without* any collection
  fetch, and annotate the association with `@BatchSize`. Hibernate pages the roots on the
  database, then loads the collection for the page's roots in batched `IN (...)` queries.
  This needs no service-code restructuring and is a good fit when you don't want the
  two-query orchestration — but it trades the guaranteed single fetch for a handful of
  batched selects. See the `hibernate-n-plus-one` skill for `@BatchSize` guidance (and ask
  the user for a batch size).
- **`@Fetch(FetchMode.SUBSELECT)`** — loads the collection for all roots in the page via one
  sub-select. Similar trade-off to `@BatchSize`; offer it when the whole page is always
  processed.

---

## Quick reference

| Symptom | What it is | Fix |
|---|---|---|
| `Page<Order>` query with `JOIN FETCH o.items` | In-memory pagination (Hib < 7.4) | Two-query split (IDs → entities) |
| `@EntityGraph` collection + `Pageable` | In-memory pagination (Hib < 7.4) | Two-query split |
| `root.fetch("items")` + paged `findAll(spec, pageable)` | In-memory pagination (Hib < 7.4) | Split spec: page IDs, then fetch by IDs |
| `HHH000104 ... applying in memory` in logs | Confirmation of the above | Two-query split |
| Same query, but on Hibernate 7.4+ | Safe (sub-select rewrite) | Nothing to fix |

Bottom line: a **to-many fetch + pagination** on Hibernate < 7.4 pages in memory and can
blow the heap. Split it into two queries — page the IDs on the database, then fetch the full
graph for just those IDs — or, if a version bump is realistic, upgrade to 7.4+.
