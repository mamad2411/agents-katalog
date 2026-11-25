---
name: hibernate-list-backed-many-to-many
description: >-
  Diagnose and fix a `@ManyToMany` association backed by a `java.util.List` in Hibernate /
  Spring Data JPA. A `List`-backed `@ManyToMany` forces Hibernate, on any change to the
  collection, to DELETE every row of the join table for that parent and re-INSERT the
  survivors — turning a one-row change into a full rewrite of the link table. Use this skill
  whenever an entity maps a `@ManyToMany` (or a `@ManyToMany` join table) with a `List`,
  whenever the user mentions "ManyToMany", "many-to-many", "join table", "link table",
  "association table", a `@ManyToMany` that "deletes and re-inserts everything", "why does
  removing one row rewrite the whole join table", switching a collection from `List` to
  `Set`, or the entity `equals`/`hashCode` contract for JPA entities. Trigger it even when
  the user only says "review this `@ManyToMany`", "make this many-to-many mapping efficient",
  or pastes an entity with a `List`-typed `@ManyToMany`. Also use it when the user wants to
  find list-backed `@ManyToMany` mappings from a running application's entities profile via
  the Axelix MCP server (the `getApplicationEntitiesProfile` tool).
---

# Fixing a List-backed @ManyToMany in Hibernate

A `@ManyToMany` mapped with a `java.util.List` is a quiet performance defect. The mapping
works, reads look fine — but the moment you **change** the collection (add or remove a
single element), Hibernate does not issue a surgical `INSERT`/`DELETE` for the one row that
changed. Instead it **deletes every join-table row for that parent and re-inserts the whole
surviving set.** Remove one product from an order that has fifty, and Hibernate runs one
`DELETE FROM order_products WHERE order_id = ?` followed by forty-nine `INSERT`s.

This happens because of `List` semantics. A `List` is an *ordered* collection with
positional identity; Hibernate cannot cheaply tell which rows moved, so for a join table
(which has no dedicated primary key it can target per row) it plays safe and rebuilds the
whole set. A `Set` has no positional identity, so Hibernate can compute the exact delta and
emit a single `INSERT` or `DELETE` for the one link that changed.

**The fix is therefore: change the collection type from `List` to `Set`.** But there is more
to it than swapping the declaration — a `Set` relies on `equals`/`hashCode`, and existing
`List`-based call sites may not survive the type change. Both are covered below; don't stop
at the type swap.

The examples below assume this domain model — an `Order` linked to many `Product`s through
the `order_products` join table:

```java
@Entity
@Table(name = "orders") // "order" is a reserved word in SQL; pluralizing is safer
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // ⚠ List-backed @ManyToMany — any change rewrites the whole join table
    @ManyToMany
    @JoinTable(
        name = "order_products",
        joinColumns = @JoinColumn(name = "order_id"),
        inverseJoinColumns = @JoinColumn(name = "product_id"))
    private List<Product> products = new ArrayList<>();
}

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @ManyToMany(mappedBy = "products")
    private List<Order> orders = new ArrayList<>();
}
```

## Step 1 — Change the collection type from List to Set

This is the core fix. Swap `List` for `Set` (and `ArrayList` for `HashSet`) on **both** ends
of the association:

```java
@Entity
@Table(name = "orders")
public class Order {

    @ManyToMany
    @JoinTable(
        name = "order_products",
        joinColumns = @JoinColumn(name = "order_id"),
        inverseJoinColumns = @JoinColumn(name = "product_id"))
    private Set<Product> products = new HashSet<>(); // was List<Product> / ArrayList<>
}

@Entity
@Table(name = "products")
public class Product {

    @ManyToMany(mappedBy = "products")
    private Set<Order> orders = new HashSet<>(); // was List<Order> / ArrayList<>
}
```

With a `Set`, `order.getProducts().remove(product)` now issues a single
`DELETE FROM order_products WHERE order_id = ? AND product_id = ?`, and adding one product
issues a single `INSERT` — instead of clearing and rebuilding the whole join table.

But a `Set` decides membership and de-duplication through `equals`/`hashCode`, whereas a
`List` does not. So the type swap is only safe once the entity has a **correct**
`equals`/`hashCode` (Step 2) — and once you've checked the existing call sites (Step 3).

---

## Step 2 — Give the entity a correct equals/hashCode

With a `List`, the entity's `equals`/`hashCode` barely mattered. With a `Set`, it decides
whether two elements are "the same" and which bucket each lands in — get it wrong and
elements silently vanish or duplicate. For JPA entities the contract has two subtle
requirements that the naive implementations violate:

1. **Stable across the entity's lifecycle.** An entity is added to a `Set` while *transient*
   (no id yet), then gets an id when it's persisted. If `hashCode` depended on the id, the
   element's bucket would change after flush and the `Set` would "lose" it. So `hashCode`
   must **not** depend on the id.
2. **Proxy-aware.** A lazily loaded association element may be a `HibernateProxy`, whose
   `getClass()` is a generated subclass, not the real entity class. Equality must compare the
   *real* (unproxied) classes, or a proxy and its loaded entity would be considered different.

The canonical implementation that satisfies both — compare by id (with proxy-aware type
check) and derive `hashCode` from the real class only:

```java
import org.hibernate.proxy.HibernateProxy;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // ... fields ...

    @Override
    public final boolean equals(Object o) {
        if (this == o) return true;
        if (o == null) return false;
        Class<?> oEffectiveClass = o instanceof HibernateProxy hp
            ? hp.getHibernateLazyInitializer().getPersistentClass()
            : o.getClass();
        Class<?> thisEffectiveClass = this instanceof HibernateProxy hp
            ? hp.getHibernateLazyInitializer().getPersistentClass()
            : this.getClass();
        if (thisEffectiveClass != oEffectiveClass) return false;
        Product other = (Product) o;
        return getId() != null && Objects.equals(getId(), other.getId());
    }

    @Override
    public final int hashCode() {
        return this instanceof HibernateProxy hp
            ? hp.getHibernateLazyInitializer().getPersistentClass().hashCode()
            : getClass().hashCode();
    }
}
```

What this contract says, precisely:

- **`equals`**: two entities are equal only if they are the **same type** (after unproxying
  both sides) **and** have the same non-null id. A transient entity (id still `null`) is equal
  only to *itself* by reference (`this == o`) — never to another transient instance. This is
  intentional: before an entity has an identity, the JVM object identity is the only thing you
  can trust.
- **`hashCode`**: a **constant** derived from the real entity class, identical for every
  instance of that entity. It deliberately ignores the id so it never changes when a transient
  entity becomes persistent. Yes, all `Product`s share one hash bucket — that's fine for the
  small collections a `@ManyToMany` holds, and correctness beats bucket spread here.

Notes:

- Make both methods `final` so a `HibernateProxy` subclass can't override them.
- `equals`/`hashCode` are shared by every entity, so this is a natural fit for a
  `@MappedSuperclass` base class exposing `getId()` — define it once there and let entities
  inherit it, rather than copy-pasting per entity.
- **Do not** substitute the usual IDE-generated `equals`/`hashCode` (which hash all fields) or
  a `record`-style all-fields equality — both reintroduce the lifecycle-instability bug this
  contract exists to avoid.

---

## Step 3 — Check the existing `List` call sites before you commit

Changing the field type from `List` to `Set` changes the semantics of every place that
touched the collection. Most call sites (`contains`, `remove`, `size`, iteration, `stream()`)
are unaffected. The one to scrutinize is **`add` and anything that depends on ordering or
positional access**:

- `List.add(e)` appends at the end and preserves insertion order and duplicates. `Set.add(e)`
  has **no positional guarantee** and silently drops an element already considered equal.
- Anything positional — `get(index)`, `List`-based indexing, "the first/last element",
  assumptions that iteration order equals insertion order — has **no equivalent** on a plain
  `HashSet`.

So, for each site that mutated the old `List`:

- If the code only ever **adds distinct elements and never relies on their order or position**,
  the `Set.add` behaves equivalently and the change is safe. Proceed.
- If you **cannot be sure** the ordering/positional behavior is irrelevant — e.g. code reads
  `products.get(0)`, renders them in insertion order, or depends on duplicates — **do not try
  to be clever.** Stop and return to the user: explain that the collection is moving from
  `List` to `Set`, point at the specific call site whose ordering/positional assumption you
  can't verify, and ask how they want to handle it. Don't silently paper over it with a
  `LinkedHashSet` or an `@OrderColumn` and hope.

`LinkedHashSet` (preserves in-memory insertion order) and `@OrderColumn` (persists a position
column so the order survives reloads) are legitimate answers when ordering genuinely matters —
but they are the user's call to make once you've surfaced the trade-off, not a default you
reach for to avoid the conversation.

---

## Quick reference

| Situation | What to do |
|---|---|
| `@ManyToMany` mapped with `List` | Change the field to `Set` (and `ArrayList` → `HashSet`) on both ends |
| Entity going into a `Set` | Add the proxy-aware, id-based `equals`/`hashCode` (Step 2) |
| IDE/`record`-generated `equals`/`hashCode` present | Replace it — it hashes mutable/id fields and breaks the lifecycle contract |
| Existing `List.add`, distinct elements, order irrelevant | Safe — `Set.add` is equivalent; proceed |
| Call site relies on ordering / position / duplicates | **Stop and ask the user** — offer `LinkedHashSet` / `@OrderColumn`, let them decide |
| Axelix MCP connected | Call `getApplicationEntitiesProfile`, fix every field flagged `LIST_BACKED_MANY_TO_MANY` |

Bottom line: a `List`-backed `@ManyToMany` rewrites the entire join table on every change.
Switch it to a `Set`, give the entity a correct proxy-aware, id-based `equals`/`hashCode` so
the `Set` behaves, and audit the old `List` call sites — where an ordering or positional
assumption might break, surface it to the user rather than guessing.
