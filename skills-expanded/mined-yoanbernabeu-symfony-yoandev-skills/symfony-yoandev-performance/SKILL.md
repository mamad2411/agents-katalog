---
name: symfony-yoandev-performance
description: >-
  Make a slow Symfony page fast and prove it stays fast: measure with the profiler and
  Stopwatch before touching anything, kill N+1 queries with explicit joins and SELECT NEW
  projections into read DTOs, and lock the result behind an integration test that counts
  the SQL queries an endpoint executes. Also covers HTTP caching with #[Cache]
  (expiration vs validation, and why public:true on a page holding personal data leaks it
  through the shared cache), the application cache with tag invalidation placed in an
  #[AsDecorator] decorator rather than in the service holding the rule, and Doctrine's
  query and result caches. Use this skill whenever someone says a page is slow, "this
  takes forever", "it times out", "why is this taking so long", "too many queries", "the
  shelf takes four seconds to load", asks to add caching or a cache layer, asks about
  N+1, lazy loading or eager loading, wants to profile or benchmark an endpoint, wants to
  assert a query count in a test, needs to iterate over tens of thousands of rows without
  exhausting memory, or asks why a cached page keeps showing stale data. Not for server
  tuning — OPcache, preload, autoloader and container settings belong to
  symfony-yoandev-deployment.
---

# Performance

> **Tier: on demand** — every rule here follows a measurement. Nothing in this skill is done pre-emptively, including the query-count test, which is written for a list that has been seen to grow.

Measure, fix the query, then write the test that stops it coming back.

Everything in this skill assumes the ordering. A cache added before a measurement does
not make an application fast; it makes it fast *and wrong*, because the slow query is
still there and now it also serves stale data. Caching is the last move, not the first.

## Measure first

The profiler is the whole toolbox. Load the page, open the toolbar, click the
**Doctrine** panel: number of queries, time per query, the SQL itself, and — because
`profiling_collect_backtrace` is on in debug — the line of code that triggered each one.

Read it in this order, because the answer is almost always in the first line:

1. **How many queries?** 3 is a page. 60 is an N+1.
2. **Are they the same query with different parameters?** That is the signature.
3. **Only then, how long does one query take?** A missing index is a real problem, but
   it is rarer than the loop above it.

For code that is slow without being SQL-bound, `symfony/stopwatch` narrows it down:

```php
$this->stopwatch->start('isbn_lookup', 'shelf');
$data = $this->isbnClient->fetch($isbn);
$this->stopwatch->stop('isbn_lookup');
```

Named events appear in the profiler timeline. One caveat worth knowing before you inject
it: **`symfony/stopwatch` is a `require-dev` package in the Symfony skeleton**, and
FrameworkBundle only registers `debug.stopwatch` when the class exists. A service that
type-hints `Stopwatch` therefore fails to compile the container on
`composer install --no-dev`. Instrument, measure, remove — or move the package to
`require` if the instrumentation is meant to stay.

## The query-count test

Every list endpoint gets an integration test that counts the SQL queries it executes.
`symfony-yoandev-doctrine` makes a relation bidirectional only where the inverse side is
genuinely read — and wherever one exists, N+1 is one dot away: a template that touches
`book.reviews` is enough to reintroduce it by accident. An untested rule is a wish, so
the rule gets a test.

```php
$this->seed(1);
$small = $this->countQueriesFor($this->client, 'GET', '/livres');

$this->seed(9);
$large = $this->countQueriesFor($this->client, 'GET', '/livres');

self::assertSame(2, $small, 'shelf with one book:'.$this->queryLog());
self::assertSame($small, $large, 'the query count grew with the row count:'.$this->queryLog());
```

**Assert on both an exact number and on the absence of growth.** The exact number pins
today's cost; the second assertion is the actual definition of N+1 and it survives
someone legitimately adding a third query later. An upper bound alone
(`assertLessThan(10, …)`) is the weakest form and has a nasty failure mode described
below.

The counting itself is `references/query-counting.md` — read it before writing the
test, because two of the four moving parts are not obvious and one of them makes a
broken test pass silently.

Two facts worth carrying, both verified against Symfony 8.1.5 / doctrine-bundle 3.3.1 /
DBAL 4.4.4:

- `DebugStack` is gone from DBAL 4. Query collection now goes through a DBAL
  `Driver\Middleware` feeding `doctrine.debug_data_holder`.
- `$client->getProfile()->getCollector('db')->getQueryCount()` **does** exist and works.
  It lives on `Symfony\Bridge\Doctrine\DataCollector\DoctrineDataCollector`, which
  doctrine-bundle's collector extends.

## N+1: three rules

| Rule | Why |
|---|---|
| **Never iterate an entity collection outside a repository.** `foreach ($book->getReviews() as …)` in a service or a template is a lazy load per book. | The collection is a `PersistentCollection`; touching it issues a `SELECT` you never wrote and cannot see from the call site. |
| **List queries join explicitly.** `->leftJoin('b.reviews', 'r')->addSelect('r')` in the repository method, not lazy loading at render time. | One query with a join costs one round trip. The same data lazily loaded costs one per row, and the cost is invisible until production has rows. |
| **Never `count($book->getRatings())`.** Add `countForBook(Book $book): int` to the repository. | `PersistentCollection::count()` only issues a `COUNT` query when the association is mapped `fetch: 'EXTRA_LAZY'`. Otherwise it falls through to `Collection::count()`, which **initialises the whole collection** — you hydrate 4 000 entities to display the number 4 000. |

`EXTRA_LAZY` is the escape hatch Doctrine offers for the third rule, and it works. It is
rejected here for the same reason the charter puts all DQL in repositories: it hides a
SQL query behind a `count()` call in a Twig template, where no reader and no static
analyser will find it. The repository method is one line longer and says what it does.

Diagnosing a specific N+1, choosing between `leftJoin` and `WITH`, and the paginate-then-
join trick that avoids the duplicated-row problem: `references/queries.md`.

## Hydrate less: SELECT NEW into a read DTO

A list that displays three columns has no business hydrating full entities, each of
which is tracked by the UnitOfWork for the rest of the request.

```php
public function findShelfRows(): array
{
    return $this->createQueryBuilder('b')
        ->select(\sprintf('NEW %s(b.id, b.title, b.status, b.lastReadAt)', ShelfRow::class))
        ->orderBy('b.title', 'ASC')
        ->getQuery()
        ->getResult();
}
```

`ShelfRow` is a `final readonly` class in `src/Dto/Read/` with promoted constructor
properties. Verified: `SELECT NEW` runs the DBAL type conversion, so a column mapped
with `enumType:` arrives as the enum and a `date_immutable` column as a
`\DateTimeImmutable` — and the identity map stays empty. The service then normalises
Read → Output; if the projection already matches the API contract, project straight into
the Output DTO and skip the layer.

For result sets too large to fit in memory at all, `toIterable()` plus a periodic
`$em->clear()`: `references/queries.md`.

## HTTP caching: nothing by default

`#[Cache]` goes on a page whose slowness has been *measured*, and only then.

Premature HTTP caching is worse than no caching, for two reasons that compound. It hides
the real problem — the page is still slow, you just stopped looking at it — and it
introduces stale-content bugs, which are the hardest class of bug to reproduce because
the reproduction depends on a timer you cannot see.

When it is justified, the two mechanisms answer different questions:

- **Expiration** (`smaxage`, `maxage`) — "do not ask me again for an hour". No request
  reaches PHP. Fastest, and wrong until the TTL expires.
- **Validation** (`etag`, `lastModified`) — "ask me, I will answer 304 if nothing
  changed". Verified: the attribute evaluates the ETag on `kernel.controller_arguments`
  and short-circuits **before the controller runs**, so a 304 costs a routing pass and
  nothing else. That is what makes it useful on a page that is slow to *render*.

Two things that bite:

- **`public: true` on a response containing personal data is a leak.** A shared cache
  will serve one user's page to the next visitor. The rule has no exception: if the
  response varies per user, it is `private`.
- **Touching the session makes the response private anyway.** Verified: any session
  usage — a flash message, the security token, `_csrf` — makes `SessionListener` (which
  runs at priority `-1000`, after the `#[Cache]` attribute) force
  `private, max-age=0, must-revalidate`. `#[Cache(public: true, smaxage: 3600)]` on such
  a page emits contradictory headers and caches nothing. Silent, and a common waste of
  an afternoon.

Full treatment, including `Vary`, `stale-while-revalidate` and the reverse-proxy
question: `references/caching.md`.

## Application cache: in a decorator, invalidated by tags

Two constraints, and they are architectural rather than technical.

**The cache does not go in the service holding the rule.** It goes in a decorator. The
business service stays unit-testable with no cache in sight, and the cache can be
deleted by removing one class — as opposed to being unpicked from the middle of a method
nobody wants to touch.

```php
#[AsDecorator(ShelfReading::class)]
final readonly class CachedShelfReader implements ShelfReading
{
    public function __construct(
        #[AutowireDecorated] private ShelfReading $inner,
        private TagAwareCacheInterface $cache,
    ) {
    }
}
```

`TagAwareCacheInterface` autowires to `cache.app.taggable` with no configuration.
Verified consequence of this suite's "services are `final`" rule: **you cannot decorate
a final concrete class.** `lint:container` rejects it outright — *argument 1 of
`BookController::__construct()` accepts `ShelfReader`, `CachedShelfReader` passed*.
Introducing the cache is therefore also the moment you extract an interface and repoint
consumers at it. That is a real cost; it is also the honest one.

**Invalidate by tag, not by TTL.** A TTL says "this may be wrong for up to an hour". A
tag says "this is wrong now" — the service that modified the book calls
`$this->cache->invalidateTags(['book_'.$book->getId()])` and the entry is gone. Keep a
TTL as well, as a safety net for the invalidation you forgot to write.

Key naming, stampede protection, and what belongs in `cache.app` versus `cache.system`:
`references/caching.md`.

## Doctrine's own caches

Four distinct caches, worth very different amounts:

| Cache | Verdict |
|---|---|
| **Metadata** | Already on. Nothing to do. |
| **Query cache** (DQL → SQL parsing) | Configure it in `prod`. It costs nothing and removes a parse on every request. Pool: `cache.system`, because it is invalidated by a deploy, not by data. |
| **Result cache** | Opt-in per query, `->enableResultCache(3600, 'shelf_rows')`. Only for a query that is genuinely expensive and genuinely tolerant of staleness. Pool: `cache.app`, because it holds data. |
| **Second-level cache** | Not used. It is opt-in per entity, subtle to invalidate, and every problem it solves is better solved by fixing the query. |

Configuration and the caveat about caching a query whose result you then modify:
`references/caching.md`.

## Not in this skill

- **OPcache, `opcache.preload`, `--optimize-autoloader`, container inlining** →
  `symfony-yoandev-deployment`. They are deploy-time settings, not code.
- **Writing repository methods in general** → `symfony-yoandev-doctrine`.
- **Logs, alerting, health checks** → `symfony-yoandev-observability`. The profiler and Stopwatch
  are development instruments and belong here; finding out *in production* that something
  broke or stalled is that skill's.
- **Test structure, fixtures, isolation** → `symfony-yoandev-testing`. This skill only adds the
  query-count assertion.
- **AssetMapper and HTTP/2** → `symfony-yoandev-frontend`. HTTP/2 is a prerequisite there, not
  an optimisation here.

## Symptom → cause

| Symptom | Cause |
|---|---|
| The Doctrine panel shows 60 near-identical `SELECT`s | An entity collection is being iterated outside a repository, usually in a Twig template |
| A page is fine with 10 rows, unusable with 1 000 | N+1. Query count is proportional to rows — the growth assertion catches this and a fixed threshold does not |
| A query-count test passes but the page is obviously slow | `APP_DEBUG=0` in the test run. Profiling is off, the collector returns **0**, and `assertLessThan()` passes for the wrong reason. See `references/query-counting.md` |
| The count is high on the first test in a file and correct afterwards | The kernel is not rebooted before the *first* request, so the test's own fixture queries are counted. Reset the data holder before measuring |
| `Cache-Control: max-age=0, must-revalidate, private, s-maxage=3600` | The session was touched. The shared cache is disabled; `public: true` did nothing |
| A cached page shows old data after an edit | TTL-only invalidation. Tag the entry and invalidate it from the service that writes |
| Out of memory exporting a large table | `getResult()` hydrates everything. `toIterable()` + `$em->clear()` |
| PHPStan cannot type `$profile->getCollector('db')` | It returns `DataCollectorInterface`. Narrow it with `assertInstanceOf` |

## Reference files

| File | When to read it |
|---|---|
| `references/query-counting.md` | Writing or fixing a test that asserts a query count — read before, not after |
| `references/queries.md` | Diagnosing an N+1, writing a fetch join, projecting into a read DTO, iterating a large result set |
| `references/caching.md` | Adding any cache: HTTP, application, or Doctrine result cache |
