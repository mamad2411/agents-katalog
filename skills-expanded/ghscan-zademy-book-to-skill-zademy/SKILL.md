---
name: tudose-spring-data-hibernate
description: "Knowledge base from \"Java Persistence with Spring Data and Hibernate\" by Cătălin Tudose. Use when applying Tudose's frameworks for JPA/Hibernate mapping, Spring Data repositories, transactions & locking, fetch strategies, Querydsl, Spring Data JDBC/MongoDB/REST, or persistence testing."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Java Persistence with Spring Data and Hibernate
**Author**: Cătălin Tudose | **Pages**: ~618 | **Chapters**: 20 | **Generated**: 2026-07-26

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `optimistic locking`, `fetch plans`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch11`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### The Paradigm Mismatch (Ch1)
ORM exists to bridge 5 object/relational mismatch problems: **granularity, inheritance, identity, associations, data navigation**. The #1 performance lever is **minimizing database requests** — watch for the two classic failures: **n+1 selects** and the **Cartesian product** (never eager-fetch two collections at once). The stack: **JPA = spec, Hibernate = implementation, Spring Data = convenience layer** over both.

### Lazy-Global Fetch Discipline (Ch8, Ch12)
**Make every association LAZY globally**, then opt into eager loading per query. `@ManyToOne`/`@OneToOne` default to EAGER — override to `FetchType.LAZY`. Separate the three concepts: **fetch plan** (what to load), **fetch strategy** (how: join/select/subselect/batch), **fetch profile** (named, reusable plan). Fix n+1 with a `JOIN FETCH` query, an **entity graph**, `@BatchSize(N)`, or `@Fetch(SUBSELECT)` — not by flipping the mapping to EAGER.

### Concurrency Default: READ_COMMITTED + @Version (Ch11)
Use **READ_COMMITTED isolation + optimistic locking with a numeric `@Version`** as the default recipe; it prevents lost updates without holding locks. Escalate only when needed: `OPTIMISTIC_FORCE_INCREMENT` for aggregate roots, `PESSIMISTIC_WRITE` (→ `SELECT … FOR UPDATE`) for hot rows. Spring `@Transactional` defaults to `REQUIRED`; use `REQUIRES_NEW` for audit logs that must survive a rollback, and `rollbackFor` to roll back on checked exceptions.

### Entity States & Business-Key Equality (Ch10)
Four states: **transient, persistent, removed, detached**. The **persistence context** is dirty-checking + first-level cache + identity scope (watch OOM on bulk loads). `merge()` returns a *new* managed instance — use its return value. **Implement `equals()`/`hashCode()` on a business key**, never on the generated id (null before flush) and never on all fields.

### Identifier & Value-Type Mapping (Ch5, Ch6)
Always use **surrogate keys** with wrapper types (`Long`, not `long`). Prefer the **enhanced-sequence generator** (allows JDBC batching) over `IDENTITY`. Map value types up the **type-adaptation ladder**: built-in type → `AttributeConverter` → `@Embeddable` → `CompositeUserType`. Use `@Enumerated(STRING)`; enforce nullability with `@Column(nullable=false)` (Bean Validation `@NotNull` alone does not shape DDL).

### Inheritance Decision Rule §7.7 (Ch7)
- No polymorphism / no polymorphic queries → **TABLE_PER_CLASS**
- Polymorphism + only behavior varies → **SINGLE_TABLE** (nullable columns)
- Polymorphism + subclass data / need NOT NULL → **JOINED**

### Technology Selection (Ch14–19)
- Full JPA power / custom queries → **Spring Data JPA** (or a **DAO with `@PersistenceContext(EXTENDED)`** when you must bypass Spring Data).
- Aggregates, no lazy/dirty-checking overhead → **Spring Data JDBC** ("Spring Data JPA minus the persistence context"; its own annotations, not JPA's).
- Repository → hypermedia HTTP API → **Spring Data REST** (`@Version` doubles as **ETag**; PATCH = partial, PUT = full replace; lock down with `exported=false`).
- Document store, same repository model → **Spring Data MongoDB** (`@DBRef` = raw pointer, no cascading; enable `auto-index-creation`).
- Portable, type-safe, readable queries → **Querydsl** (Q-types via APT; its DML **ignores cascades & 2nd-level cache**).
- NoSQL behind JPA, switch backend by config only → **Hibernate OGM**.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-understanding-orm.md) | Understanding Object/Relational Persistence | Paradigm mismatch, n+1, Cartesian product |
| [ch02](chapters/ch02-starting-a-project.md) | Starting a Project | Persistence unit, EMF, persistence context, JPQL |
| [ch03](chapters/ch03-domain-models-metadata.md) | Domain Models & Metadata | Transparent persistence, POJO, static metamodel |
| [ch04](chapters/ch04-working-with-spring-data-jpa.md) | Working with Spring Data JPA | Repository hierarchy, derived queries, QBE, projections |
| [ch05](chapters/ch05-mapping-persistent-classes.md) | Mapping Persistent Classes | Surrogate keys, enhanced-sequence, @Immutable |
| [ch06](chapters/ch06-mapping-value-types.md) | Mapping Value Types | Type-adaptation ladder, AttributeConverter, @Embeddable |
| [ch07](chapters/ch07-mapping-inheritance.md) | Mapping Inheritance | 4 strategies, decision rule §7.7 |
| [ch08](chapters/ch08-collections-entity-associations.md) | Collections & Entity Associations | Lazy discipline, cascades, bag vs list |
| [ch09](chapters/ch09-advanced-entity-associations.md) | Advanced Entity Associations | Shared PK, link entity, join table |
| [ch10](chapters/ch10-managing-data.md) | Managing Data | Entity states, persistence context, business-key equals |
| [ch11](chapters/ch11-transactions-concurrency.md) | Transactions & Concurrency | READ_COMMITTED + @Version, propagation, pessimistic locks |
| [ch12](chapters/ch12-fetch-plans-strategies-profiles.md) | Fetch Plans, Strategies & Profiles | LAZY-global, join fetch, entity graph, @BatchSize |
| [ch13](chapters/ch13-filtering-data.md) | Filtering Data | Cascade→one op, callbacks, Interceptor, Envers, dynamic filters |
| [ch14](chapters/ch14-integrating-jpa-hibernate-spring.md) | Integrating JPA/Hibernate with Spring | DAO pattern, EXTENDED context, GenericDao |
| [ch15](chapters/ch15-spring-data-jdbc.md) | Spring Data JDBC | Aggregates, @MappedCollection, no persistence context |
| [ch16](chapters/ch16-spring-data-rest.md) | Spring Data REST | HATEOAS, @Version=ETag, PATCH vs PUT, lockdown |
| [ch17](chapters/ch17-spring-data-mongodb.md) | Spring Data MongoDB | MongoRepository, @DBRef, MongoTemplate, indexing |
| [ch18](chapters/ch18-hibernate-ogm.md) | Hibernate OGM | JPA over NoSQL, config-only backend switch, uuid2 |
| [ch19](chapters/ch19-querydsl.md) | Querydsl | Q-types, type-safe queries, DML caveats |
| [ch20](chapters/ch20-testing.md) | Testing | Integration tests, @Transactional rollback, leak detection |

## Topic Index

- **AttributeConverter** → ch06
- **Bag / collections** → ch08
- **Business key (equals/hashCode)** → ch10
- **Cascading** → ch08, ch13
- **Cartesian product** → ch09, ch12
- **DAO / EXTENDED context** → ch14
- **Derived queries / @Query** → ch04
- **Dynamic filters** → ch13
- **Embeddable** → ch05, ch06
- **Enhanced-sequence generator** → ch05
- **Entity graph** → ch12
- **Entity states** → ch10
- **Envers (auditing)** → ch13
- **ETag / optimistic locking** → ch11, ch16
- **Fetch plan / strategy / profile** → ch12
- **Inheritance strategies** → ch07
- **Interceptor (audit)** → ch13
- **JPQL** → ch02
- **Join fetch** → ch12
- **Link entity (many-to-many)** → ch09
- **MongoTemplate / @DBRef** → ch17
- **n+1 selects** → ch01, ch12
- **Optimistic / pessimistic locking** → ch11
- **Paradigm mismatch** → ch01
- **Persistence context** → ch02, ch10
- **Projections** → ch04, ch16
- **Querydsl / Q-type** → ch19
- **Query by Example (QBE)** → ch04, ch17
- **Repository hierarchy** → ch04
- **REST events / excerpt projection** → ch16
- **Spring Data JDBC / aggregate** → ch15
- **Surrogate key** → ch05
- **Transaction propagation** → ch11
- **Type-adaptation ladder** → ch06
- **@Version** → ch11, ch16

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions and chapter references
- [patterns.md](patterns.md) — 15 concrete techniques (identifier generation, locking recipes, DAO, auditing, aggregates, testing)
- [cheatsheet.md](cheatsheet.md) — decision rules, fetch/locking/inheritance selection tables, thresholds

---

## Scope & Limits

This skill covers the book's content only — Spring Data + Hibernate persistence patterns as taught by Tudose. For hands-on implementation in your codebase, combine with project-specific config and schema. For topics beyond this book (e.g. reactive R2DBC, Hibernate Reactive), check related skills or ask the agent directly.