---
name: php-doctrine
description: Use when persisting PHP objects with Doctrine ORM 3 — attribute-mapped entities, EntityManager, DQL/QueryBuilder, associations, migrations, N+1 avoidance.
metadata:
  added: 2026-05-23
  last_reviewed: 2026-05-23
  type: language
  languages: [php]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-23"
  related: [orm-overview, postgres, sql, php-symfony]
---

# Doctrine ORM 3

**Iron Law: one `flush()` per request/transaction, never inside a loop. Default every association to `fetch: LAZY` and kill the resulting N+1 with an explicit fetch join — not EAGER. Entities model the domain; they are not API DTOs and they hold no business decisions.**

**Versions:** ORM `3.6`, DBAL `4`, Migrations `3`. ORM 3 is **attributes-only** — annotations and XML/YAML mapping are gone. PHP 8.1+ enums map natively. This skill is the _dialect_ — for when-to-use-an-ORM, identity-map theory, and cross-language ORM trade-offs, `Skill(devkit:orm-overview)` is the concept owner; don't re-derive it here.

## Attribute-mapped entity

```php
use Doctrine\ORM\Mapping as ORM;
use Doctrine\Common\Collections\{Collection, ArrayCollection};

#[ORM\Entity(repositoryClass: OrderRepository::class)]
#[ORM\Table(name: 'orders')]
#[ORM\Index(fields: ['status', 'createdAt'])]
class Order
{
    #[ORM\Id, ORM\GeneratedValue, ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 50)]
    private string $sku;

    #[ORM\Column(enumType: OrderStatus::class)]   // native PHP enum mapping
    private OrderStatus $status = OrderStatus::Pending;

    #[ORM\Column]
    private \DateTimeImmutable $createdAt;

    /** @var Collection<int, LineItem> */
    #[ORM\OneToMany(targetEntity: LineItem::class, mappedBy: 'order', cascade: ['persist'], orphanRemoval: true)]
    private Collection $items;

    public function __construct(string $sku)
    {
        $this->sku = $sku;
        $this->createdAt = new \DateTimeImmutable();
        $this->items = new ArrayCollection();
    }
    public function getId(): ?int { return $this->id; }
}
```

`?int $id = null` is the standard pattern: null before the first flush, populated by `GeneratedValue` after. Use `DateTimeImmutable` to avoid the shared-mutable-instance trap. Initialise every collection in the constructor — an unset `Collection` throws on access.

## EntityManager, UnitOfWork, identity map

The `EntityManager` (`EntityManagerInterface`, autowired in Symfony) is the front door. It tracks every managed entity in the **identity map**: fetching the same row twice in one request returns the _same object_. The **UnitOfWork** records changes and computes a single change-set at `flush()` — you mutate objects, then flush once; Doctrine emits the minimal `INSERT`/`UPDATE`/`DELETE` batch.

```php
$order = new Order('SKU-1');
$em->persist($order);   // schedule insert; does NOT hit the DB
$order->markShipped();  // tracked automatically — no second persist needed
$em->flush();           // ONE transaction, all pending changes
```

`persist()` only for _new_ entities. Managed entities are auto-dirty-tracked — re-calling `persist()` is a no-op smell. `$em->clear()` detaches everything (drop the identity map) when processing huge batches to bound memory.

## Repositories

```php
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/** @extends ServiceEntityRepository<Order> */
class OrderRepository extends ServiceEntityRepository  // autowirable by type in Symfony DI
{
    public function __construct(ManagerRegistry $registry) { parent::__construct($registry, Order::class); }

    /** @return Order[] */
    public function findShippableWithItems(): array
    {
        return $this->createQueryBuilder('o')
            ->addSelect('i')                          // hydrate items in the same query
            ->leftJoin('o.items', 'i')                 // fetch join → no N+1
            ->where('o.status = :s')->setParameter('s', OrderStatus::Pending)
            ->orderBy('o.createdAt', 'DESC')
            ->getQuery()->getResult();
    }
}
```

Custom repositories own query logic — keep DQL out of services and controllers. Wire via `repositoryClass:` on the entity; inject the repo by type. Query methods return arrays/entities, never `QueryBuilder` (don't leak the builder past the repo boundary).

## DQL + QueryBuilder

DQL queries _entities and properties_, not tables/columns — `SELECT o FROM App\Entity\Order o WHERE o.status = :s`. QueryBuilder is the programmatic form; prefer it for anything conditional. **Always** bind with `setParameter` — string-interpolating a value into DQL is SQL injection (the placeholder syntax is the only safe path). For raw reporting SQL Doctrine can't express, drop to DBAL `$conn->executeQuery(sql, params)` with bound params and map yourself.

## Associations + fetch strategy

| Side                          | Mapping                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| Many rows point to one parent | `#[ORM\ManyToOne]` (owning, holds the FK) + `#[ORM\OneToMany]` (inverse, `mappedBy`) |
| Both collections              | `#[ORM\ManyToMany]` (one side owns the join table via `inversedBy`)                  |
| Exactly one each way          | `#[ORM\OneToOne]`                                                                    |

The **owning side** carries the FK and is what flush persists — set _both_ sides in your domain methods or the inverse goes stale. Default `fetch: LAZY`: associations load on first access via a proxy. **`fetch: EAGER` is almost always wrong** — it loads the relation on _every_ query of the parent, even when unused. Leave it LAZY and add a fetch join where you actually need the children.

## N+1 avoidance — the core failure mode

```php
// N+1: 1 query for orders + 1 per order for items (lazy proxy fires in the loop)
foreach ($repo->findAll() as $o) { count($o->getItems()); }

// Fixed: one query, items hydrated via addSelect + join
$repo->createQueryBuilder('o')->addSelect('i')->leftJoin('o.items', 'i')->getQuery()->getResult();
```

`addSelect('i')` is what turns a filtering join into a _fetch_ join (hydrates the children). For collection-to-collection fan-out that a single join would Cartesian-explode, use `Doctrine\ORM\Tools\Pagination\Paginator` or batched `WHERE IN` loads. See `Skill(devkit:sql)` for join mechanics and `Skill(devkit:postgres)` for index design behind these queries.

## Lifecycle events

```php
#[ORM\HasLifecycleCallbacks]
class Order {
    #[ORM\PreUpdate]
    public function touch(): void { $this->updatedAt = new \DateTimeImmutable(); }
}
```

Lifecycle callbacks (`PrePersist`, `PreUpdate`, `PostLoad`) suit timestamp/derived-field upkeep. For cross-entity reactions use an **event listener/subscriber** service, not a callback — and never `flush()` inside one (re-entrant flush corrupts the UnitOfWork). Real side effects (email, queue) belong in the application layer after a clean flush.

## DBAL 4 types + enum types

DBAL 4 maps PHP↔DB types. Native enum columns use `#[ORM\Column(enumType: Status::class)]` (backed enum required). For custom value objects register a custom `Type` subclass and reference it via `type:` on the column. DBAL 4 tightened type strictness — `DateTimeImmutable` over `DateTime`, and watch implicit string↔int coercions that 3.x tolerated.

## Migrations 3

```bash
bin/console doctrine:migrations:diff      # generate from entity↔schema delta
bin/console doctrine:migrations:migrate   # apply pending, tracked in migration_versions
```

`diff` writes a versioned `up()`/`down()` class from the mapping-vs-database delta — **review it**, don't trust it blind (it can drop columns it doesn't understand). Treat migrations as forward-only in practice; `down()` is a best-effort safety net. Put data backfills in the migration's `up()` body (`$this->addSql(...)`) or a separate console command, never mixed with a slow schema change on a hot table. See `Skill(devkit:postgres)` for online-DDL / lock-avoidance on large tables.

## Flush batching

Inserting thousands of rows: flush in chunks and clear the identity map, or the UnitOfWork grows unbounded.

```php
foreach ($rows as $i => $row) {
    $em->persist(Order::fromRow($row));
    if (($i % 500) === 0) { $em->flush(); $em->clear(); }   // bound memory + change-set size
}
$em->flush();
```

For pure bulk loads where you don't need entities back, DBAL batch `INSERT` is faster than ORM hydration — measure.

## Anti-patterns

- `flush()` inside a loop — one transaction per iteration; batch + flush once (or chunk)
- Using entities as API request/response DTOs — couples wire shape to schema, enables mass-assignment; map to DTOs
- Business decisions inside entities (pricing rules, auth checks) — entities model state; logic goes to services
- `fetch: EAGER` to "fix" N+1 — loads the relation on every query forever; use a fetch join at the call site
- Interpolating values into DQL strings — SQL injection; always `setParameter`
- Forgetting `addSelect` on a join — you joined but didn't hydrate, the proxy still N+1s on access
- Setting only the inverse side of an association — owning side holds the FK; flush ignores the inverse
- `flush()` inside a lifecycle callback or event listener — corrupts the in-flight UnitOfWork
- Never calling `$em->clear()` in a long batch — identity map grows until OOM
- Trusting `migrations:diff` output unreviewed — it can emit destructive DDL

## Red flags

| Thought                                     | Reality                                                                  |
| ------------------------------------------- | ------------------------------------------------------------------------ |
| "I'll flush after each save to be safe"     | one flush per loop = N transactions + N round-trips; batch it            |
| "EAGER fetch is simpler"                    | it loads the relation on every parent query, used or not — LAZY + join   |
| "The entity is basically my API model"      | now schema changes break the API and clients can mass-assign — use a DTO |
| "I'll put the discount logic in the entity" | persistence object now owns a business rule no one can test in isolation |
| "The N+1 is fine, it's only a few rows"     | it's a few rows in dev and ten thousand in prod                          |
| "`diff` generated it, ship it"              | review every migration — diff drops what it can't model                  |

## Hand-off

For the ORM-vs-query-builder decision, identity-map theory, and cross-language comparison: `Skill(devkit:orm-overview)` (the concept owner). For controllers, DI, and wiring the EntityManager into a request: `Skill(devkit:php-symfony)`. For join mechanics, transactions, and isolation: `Skill(devkit:sql)`. For index design, online DDL, and the Postgres engine behind these queries: `Skill(devkit:postgres)`.
