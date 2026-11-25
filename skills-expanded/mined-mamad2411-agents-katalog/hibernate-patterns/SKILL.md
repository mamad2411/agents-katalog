---
name: hibernate-patterns
description: "When to activate: Hibernate, session, query optimization, batch processing, second level cache, envers, auditing, Hibernate statistics"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: java-kotlin
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Hibernate Patterns

## Session & Persistence Context

```java
// EntityManager wraps Hibernate Session
@PersistenceContext
private EntityManager em;

// Access underlying Session for Hibernate-specific APIs
Session session = em.unwrap(Session.class);

// States: transient → persistent → detached → removed
User user = new User("Alice");          // transient
em.persist(user);                       // persistent — tracked by context
em.detach(user);                        // detached — no longer tracked
em.merge(user);                         // re-attach detached entity
em.remove(em.find(User.class, 1L));     // removed
```

## Batch Processing

```java
// Batch insert — prevent OutOfMemoryError with large datasets
@Transactional
public void bulkInsert(List<UserDto> dtos) {
    int batchSize = 50;
    for (int i = 0; i < dtos.size(); i++) {
        User user = mapper.toEntity(dtos.get(i));
        em.persist(user);
        if (i % batchSize == 0) {
            em.flush();   // execute SQL
            em.clear();   // free memory
        }
    }
}

// application.properties
// spring.jpa.properties.hibernate.jdbc.batch_size=50
// spring.jpa.properties.hibernate.order_inserts=true
// spring.jpa.properties.hibernate.order_updates=true

// StatelessSession for bulk — bypasses persistence context entirely
StatelessSession stateless = session.getSessionFactory().openStatelessSession();
try (stateless) {
    ScrollableResults<User> scroll = stateless.createQuery("FROM User", User.class)
        .setFetchSize(50).scroll(ScrollMode.FORWARD_ONLY);
    while (scroll.next()) {
        User u = scroll.get();
        u.setProcessed(true);
        stateless.update(u);
    }
}
```

## Query Optimization

```java
// Named queries — parsed at startup, cached
@NamedQuery(name = "User.findActiveByRole",
    query = "SELECT u FROM User u WHERE u.role = :role AND u.isActive = true")

// Scroll large result sets — don't load all into memory
try (ScrollableResults<Order> scroll = em.createQuery("FROM Order o WHERE o.status = 'PENDING'", Order.class)
        .setHint(QueryHints.HINT_FETCH_SIZE, 100)
        .scroll(ScrollMode.FORWARD_ONLY)) {
    while (scroll.next()) {
        process(scroll.get());
    }
}

// Multi-load — single query for multiple IDs
List<User> users = session.byMultipleIds(User.class)
    .multiLoad(List.of(1L, 2L, 3L, 4L, 5L));

// Native SQL with entity mapping
List<User> users = em.createNativeQuery(
    "SELECT * FROM users u JOIN user_tags t ON u.id = t.user_id WHERE t.tag = :tag",
    User.class)
    .setParameter("tag", "vip")
    .getResultList();
```

## Second-Level Cache (L2)

```java
@Entity
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class Product {
    @OneToMany
    @Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
    private Set<Tag> tags;
}

// Query cache
List<Product> products = em.createQuery("FROM Product p WHERE p.featured = true", Product.class)
    .setHint("org.hibernate.cacheable", true)
    .setHint("org.hibernate.cacheRegion", "featured-products")
    .getResultList();

// Cache statistics
Statistics stats = sessionFactory.getStatistics();
log.info("L2 hit ratio: {}", stats.getSecondLevelCacheHitCount() /
    (double)(stats.getSecondLevelCacheHitCount() + stats.getSecondLevelCacheMissCount()));
```

## Hibernate Envers (Audit History)

```java
@Entity
@Audited
public class Contract {
    @Id private Long id;
    @Audited private String content;
    @NotAudited private byte[] cachedPdf;  // skip large blobs
}

// Query audit history
AuditReader reader = AuditReaderFactory.get(em);

// All revisions
List<Number> revisions = reader.getRevisions(Contract.class, contractId);

// Entity at specific revision
Contract atRev3 = reader.find(Contract.class, contractId, 3);

// Entities changed in revision
List<Object[]> changed = reader.createQuery()
    .forRevisionsOfEntity(Contract.class, false, true)
    .add(AuditEntity.id().eq(contractId))
    .add(AuditEntity.revisionNumber().gt(5))
    .getResultList();
```

## Optimistic vs Pessimistic Locking

```java
// Optimistic — @Version field, conflict detected on commit
@Version private Long version;  // auto-incremented by Hibernate

// Pessimistic — DB-level lock
User user = em.find(User.class, id, LockModeType.PESSIMISTIC_WRITE);
// SELECT ... FOR UPDATE

// Lock on query
em.createQuery("FROM User u WHERE u.id = :id", User.class)
    .setParameter("id", id)
    .setLockMode(LockModeType.PESSIMISTIC_READ)
    .getSingleResult();
```

## Hibernate Statistics & Tuning

```properties
# Enable statistics
spring.jpa.properties.hibernate.generate_statistics=true
spring.jpa.properties.hibernate.session.events.log.LOG_QUERIES_SLOWER_THAN_MS=100

# Show formatted SQL (dev only)
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# Batch size for collections
spring.jpa.properties.hibernate.default_batch_fetch_size=20
```

## Key Rules
- `em.flush()` + `em.clear()` in batch loops — without it, the persistence context grows unbounded and causes OOM
- `READ_WRITE` cache strategy handles concurrent updates; `NONSTRICT_READ_WRITE` is faster but allows stale reads briefly
- Envers creates `_AUD` shadow tables — run schema migration to create them before enabling `@Audited`
- Pessimistic locking (`PESSIMISTIC_WRITE`) holds a DB row lock for the transaction duration — use sparingly to avoid contention
- Enable `hibernate.generate_statistics` in staging to detect N+1 queries before they hit production
