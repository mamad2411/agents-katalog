---
name: write-service-code
description: Use when writing OR refactoring/moving/porting code inside a feature — a handler, query, service, event, or integration test. Consolidating or extracting existing code counts (moved-verbatim code must still pass the checklist — precedent listings-api#719 where sequential awaits survived a controller→service move). Control flow, async (Promise.all), query performance (N+1, upsert, joins, indexes), events/SQS, logging, decimal/date libs. Language-agnostic with TS/NestJS examples.
metadata:
  last-updated: 2026-07-30
  author: Ken Nguyễn <ntnpro@gmail.com>
---

## When to use

Reach for this when you're writing the **body** of a handler/service/query/event/test and want the
team's implementation conventions — readability, async, nullability, SQL performance, messaging,
logging, and test shape. For *where files go and what they're named*, use the companion skill
[structure-a-backend-service](./structure-a-backend-service.md).

Each rule: **portable principle** → **▸ Example (TS/NestJS)** (neutral `listing` domain;
`<Entity>`/`<feature>` = rename) → **▸ Other stacks**. Some rules restate global policy; the global
rule stays authoritative (see Related).

## Steps

### 1. Control flow — return early, no manual loops

- **Return (or throw) early; don't nest.** Handle the invalid/empty case first and bail, so the
  happy path stays unindented.
  ```ts
  if (minPrice == null && maxPrice == null) return;     // guard
  if (!items?.length) return null;
  // ...happy path, never more than ~2 levels deep
  ```
- **Transform collections with pipeline functions, not `for`/`while`.** `map`/`filter`/`reduce`/
  `find`/`some`/`every`/`flatMap`. Keep callbacks pure (no mutating the source).
  ```ts
  const coverIds = media.filter((m) => m.type === MediaType.COVER).map((m) => m.id);
  const labelByCode = categories.reduce((acc, c) => { acc[c.code] = c.label; return acc; }, {} as Record<string, string>);
  ```
- **Imperative iteration only for:** side effects (`forEach` / `for...of` to mutate external state,
  dispatch, log) and **sequential async that must be ordered** (`for...of` with `await`, e.g. a
  retry loop). Never `forEach` with an `async` callback. ▸ *Other stacks:* comprehensions /
  streams / `map` equivalents; the principle (declarative transform, imperative only for effects &
  ordered async) is universal. (Matches global *Code Style — Iteration & Collections*.)

### 2. Parallelize independent async with `Promise.all`

Independent awaits run together; only `await` in sequence when one result feeds the next.
```ts
const [detail, owner] = await Promise.all([getDetail(id), getOwner(id)]);       // independent → parallel
const files = await Promise.all(media.map(async (m) => ({ name: m.name, data: await toBase64(m) })));
```
A sequential `await` inside a `map`/loop for independent work is the anti-pattern — it serializes
needlessly. ▸ *Other stacks:* `asyncio.gather`, goroutines + `errgroup`, `CompletableFuture.allOf`.

Cheaper than parallelizing: **don't run what a branch discards.** If some flag/condition zeroes out
or ignores a result, compute that condition FIRST and skip the calls entirely (precedent:
listings-api#719 — an estimate engine ran 2 queries for non-tillable farms whose prices were then
forced to 0). And "moved/ported verbatim" is not an exemption — code you relocate must pass this
section even if its old home didn't.

### 3. Prefer `null` over `undefined`

Use an explicit nullable type for "absent" values; reserve `undefined` for "not provided". This
keeps DB-nullable columns, DTO fields, and return types consistent.
```ts
@Column({ nullable: true }) publishedAt!: Nullable<Date>;         // entity field
async getFile(req: FileReq): Promise<Nullable<FileDto>> { ... }   // return type
```
▸ *Other stacks:* `Optional<T>` (Java), `*T`/`sql.NullString` (Go), `T | None` (Python). The point:
one agreed "absent" value, not a mix of `null` and `undefined`. (TS note: `==`/`!=` against `null`
intentionally matches both `null` and `undefined`.)

**API response defaults:** an absent **array** is `[]` (never `null`/`undefined`); an absent
**scalar/object** is `null` (never `undefined`). `undefined` disappears from JSON and breaks clients
that expect the key. ▸ *Other stacks:* same — empty collection for lists, explicit null for the rest.

### 4. Put private helpers below the public API

A class/file reads top-down: public methods first, then `private` helpers underneath. Helper names
are **verb-led + single responsibility** (`fetchOwnerProfile`, `shouldTriggerReview`, `buildPayload`).
```ts
@Injectable()
export class ListingService {
  async createListing(dto: CreateListingDto) { /* ...delegates to helpers... */ }
  async getListing(id: string) { ... }
  // ── private helpers below ──────────────────────────────
  private async fetchOwnerProfile(listing: Listing) { ... }
  private shouldTriggerReview(listing: Listing): boolean { ... }
}
```
Keep methods to one screenful; extract a focused private method when one covers 3+ concerns.
(Matches global *Code Style — Function Size & Density*.)

### 5. Querying & performance

The repository/query builder is where most performance is won or lost. Apply all of these:

- **Select only the columns you need** — never implicit `SELECT *`.
  ```ts
  .select(['listing.id', 'listing.status', 'listing.price', 'photo'])   // explicit, includes joined alias
  ```
- **Push every filter into the query** (status/type/date/soft-delete) and batch multi-value
  filters with `IN (:...ids)` — never fetch broadly then `.filter()` in code, and never query
  per-item in a loop (that's the N+1). (Matches global *Database & Migration Rules*.)
  ```ts
  .where('listing.isDeleted = false')
  .andWhere('listing.status IN (:...statuses)', { statuses })    // one query, not one-per-status
  ```
- **Load relations in the query**, not lazily per row, to avoid N+1: `leftJoinAndSelect` for
  optional relations you need in the result, `innerJoin` for a required relation you only filter on
  (no select), `Brackets` for grouped `OR`.
  ```ts
  .leftJoinAndSelect('listing.photos', 'photo', 'photo.isDeleted = false')   // eager, optional
  .innerJoin('listing.owner', 'owner')                                       // required, filter-only
  ```
- **One round-trip when you can** — fetch rows + total together (`getManyAndCount`) instead of two
  queries; combine related work rather than looping queries.
  ```ts
  const [rows, total] = await qb.take(take).skip(skip).orderBy(column, direction).getManyAndCount();
  ```
- **Write-or-update in one statement with upsert** instead of select-then-insert/update; it also
  lets you batch insert + update + soft-delete together.
  ```ts
  await this.photoRepo.upsert(
    [...newPhotos, ...unused.map((p) => ({ ...p, isDeleted: true }))],
    ['id'],   // conflict key
  );
  ```
- **Index for your filters + sort, and order deterministically.** Add a composite `@Index` matching
  the common `WHERE` + `ORDER BY`; drive `orderBy` from a typed sort-map constant (not free-text), so
  only indexed columns are sortable.
  ```ts
  @Index('listing_status_createdAt_idx', ['status', 'createdAt'])
  // sort map: enum → { column, direction } ; query: const { column, direction } = listingSortMap[sortBy];
  ```
- **Money & dates go through standard libraries, never ad-hoc math.** Precise/decimal numeric work
  uses a decimal library (floats drift — `0.1 + 0.2 !== 0.3`); date/time uses a date library
  (parsing, timezones, formatting). ▸ *Example:* a `Decimal` type + a `decimal(p,s)` column
  transformer for money; a day/date lib for every date operation. ▸ *Other stacks:* your ecosystem's
  decimal + datetime libs — never hand-roll currency math or timezone arithmetic.

▸ *Other stacks:* the same SQL discipline applies through any ORM/query layer (Django
`select_related`/`prefetch_related`, JPA fetch joins, `sqlc`/`sqlx`); upsert = `INSERT ... ON
CONFLICT` / `MERGE`.

### 6. Events & async messaging (SQS/pub-sub)

- **One event per file under the feature's `events/`**, holding the event class (extends a shared
  `BaseEvent<T>`) **and** its handler; a barrel exports the handler list for batch registration.
- **Emit from the use-case via the bus; never publish externally inline.** The command/query handler
  publishes a domain event; an event handler does the outbound I/O.
  ```ts
  // in a command handler
  this.eventBus.publish(new ListingStatusChangedEvent(listings));

  // events/listing-status-changed.event.ts
  @EventsHandler(ListingStatusChangedEvent)
  export class ListingStatusChangedEventHandler implements IEventHandler<ListingStatusChangedEvent> {
    async handle(event: ListingStatusChangedEvent): Promise<void> {
      await this.publisher.dispatch({
        event: TOPIC.LISTING_STATUS_CHANGED,
        payload: event.data.map((l) => ({ listingId: l.id, status: l.status })),  // mapped subset, NOT the raw entity
      });
    }
  }
  ```
- **Outbound payloads are an explicit mapped subset** (id + the few fields subscribers need), never
  the whole entity — that's a contract you don't want leaking internal columns.
- **Inbound consumers are wired from config + named constants**, not hard-coded URLs/strings. Queue
  URLs are built from a centralized config block; topic/queue/pattern names are constants.
  ```ts
  SqsModule.registerAsync({
    useFactory: (config: ConfigService) => {
      const { region, accountNumber, sqsEndpoint } = config.get(configEvents);
      const consumers = [getQueueName(EVENT_PATTERNS.listing.published)].map((name) => ({
        name, queueUrl: `${sqsEndpoint}/${accountNumber}/${name}`, region,
      }));
      return { consumers };
    },
    inject: [ConfigService],
  });
  // @SqsMessageHandler(queueName, false) async handleMessage(message: Message) { ... }
  ```
- **In a queue (SQS) consumer, never throw — log and return.** An unhandled throw returns the
  message to the queue, where it's re-consumed until it expires — a poison message that can loop
  forever. ▸ *Example:* the handler extends a shared `AbstractEventHandler`; on failure it calls
  `logger.error(...)` then `return`, so the message is acked/deleted while the error still reaches
  alarms. Handle partial-batch failures explicitly (report which records failed). ▸ *Other stacks:*
  ack/commit the message and route the failure to a dead-letter queue — don't let an exception
  trigger blind redelivery.

▸ *Other stacks:* an in-process event bus or outbox emits; a separate consumer/worker handles the
queue. Principle: **use-case → event → handler → broker**, payloads are explicit, names are config.

### 7. Logging

- **Structured metadata, not string concatenation.** A short message string + a context object.
  ```ts
  this.logger.info(`Response from <system> for "${path}"`, { data: maskPii(data), payload: maskPii(payload) });
  this.logger.error("Can't publish listing", { listingId, resError: (error as Error).message });
  ```
- **Mask PII/secrets before logging** (identity numbers, tokens) — pass values through a masker.
- **Levels:** `info` = normal milestones (external call made, status transition), `warn` = recovered/
  fallback paths, `error` = exceptions & failed external calls (include the error message + ids),
  `debug` = detailed tracing. Log every critical branch, fallback, and missing-config path (global
  *Feature Flags & Observability*). Request logging + a global exception filter are wired once
  centrally, not per handler. ▸ *Other stacks:* any structured logger (zap, structlog, SLF4J + MDC) —
  key-value context, not interpolated strings.

### 8. Writing a test (integration layer)

These are **integration tests** — they boot the app and hit the real transport/DB boundary. For the
**isolated unit-test layer** (mocked deps, no DB — fast tests for handlers/services/DTOs) see
[write-unit-tests](./write-unit-tests.md); a repo may run one layer or both (two jest projects).
See [structure-a-backend-service](./structure-a-backend-service.md) step 8 for the harness. Per spec:

```ts
describe('ListingCmdController', () => {
  let client: ClientProxy, app: INestApplication, dataSource: DataSource;
  let factoryCtx: FactoryContext, listingFactory: ListingFactory, listingRepo: Repository<Listing>;

  beforeAll(() => {
    ({ client, app, dataSource } = global.testContext);   // app booted once in the shared setup
    listingRepo = dataSource.getRepository(Listing);
  });
  beforeEach(() => {
    factoryCtx = new FactoryContext(dataSource);
    listingFactory = new ListingFactory(factoryCtx);       // fresh factory per test
  });
  afterEach(async () => {
    jest.restoreAllMocks();
    await listingRepo.delete({});
    await factoryCtx.destroy();                            // clean state between tests
  });

  it('publishes the listing and persists it', async () => {
    // Arrange — seed via factory, mock only externals
    const listing = await listingFactory.build({ status: ListingStatus.DRAFT });
    jest.spyOn(SearchIndexService.prototype, 'index').mockResolvedValue({ ok: true });

    // Act — exactly one action under test, blank line before & after
    const { success } = await lastValueFrom(client.send(PATTERN.listing.publish, msg({ id: listing.id })));

    // Assert — response AND persisted state, with specific expected values
    expect(success).toBe(true);
    const updated = await listingRepo.findOneOrFail({ where: { id: listing.id } });
    expect(updated.status).toBe(ListingStatus.PUBLISHED);   // not toBeTruthy()
  });

  it('fails for an unknown listing', async () => {
    const { success } = await lastValueFrom(client.send(PATTERN.listing.publish, msg({ id: v4() })));
    expect(success).toBe(false);                            // cover the error path too
  });
});
```
- **Structure every test Arrange → Act → Assert**, blank line around the Act, **exactly one Act**
  (one action under test) — the comments above show the shape.
- **Seed with factories + a faker lib for inputs** (realistic random names/emails/numbers/ids),
  never hand-rolled literals; build only the fields the test asserts on. Clean up the rows created
  in *this* test afterward (and only those) so parallel specs don't collide.
- **Mock only what crosses the process boundary** (external services via `spyOn(...prototype)`,
  outbound HTTP via an intercept lib). Use the real DB; assert the persisted row, not just the reply.
- **Assert specific expected values, not just truthiness** — `expect(id).toBe(realId)`, not
  `toBeTruthy()`. Common matchers: `toBe` (string/number), `toMatchObject` (part of an object),
  `toEqual` (whole object/array), `arrayContaining` (array members).
- **Group branch variations with `it.each`** instead of copy-pasting near-identical tests.
- **Cover the success path + the error/edge path**; assert outbound side effects with spy-called-with.
- **Keep specs small and run coverage.** One spec per API when it has many cases (≤ ~300 lines);
  group several small APIs into one spec otherwise. Run the coverage report over what you wrote.
- **Don't write isolated unit tests that bypass the boundary** — if it can't be reached through the
  boundary, skip it (global *HTTP-layer testing rule*).

### 9. Robustness — transactions, event-handler safety, external clients
- **Multi-repo writes go in one transaction; broadcast a compensating event before re-throwing.** Wrap
  related mutations in `dataSource.transaction(em => …)` and pass `em` to each repo op for atomicity.
  In an event-driven flow, if the transaction fails after side effects were signalled, emit a
  **compensating event** (e.g. `OrderCanceled` releasing held inventory) before throwing, so
  downstream can undo:
  ```ts
  await dataSource.transaction(async (em) => {
    const order = await saveOrder(em, dto);
    try { await reserveInventory(em, order); await debitWallet(em, order); return order; }
    catch (e) { await events.publish(new OrderCanceledEvent(order)); throw e; }  // compensate, then roll back
  });
  ```
- **In-process event handlers must not crash the bus.** A CQRS `@EventsHandler` is fire-and-forget;
  one failing handler (missing template, third-party down) shouldn't break sibling handlers. Wrap
  `handle` so it logs + swallows instead of throwing — e.g. a shared `@CatchException()` decorator
  (log + return). (This is the in-process twin of the SQS "don't throw" rule in §6.)
- **External/microservice clients own their lifecycle.** A `ClientProxy` (TCP/microservice client)
  **closes on `OnApplicationShutdown`** (no zombie connections on deploy); retry config (attempts +
  delay) is **env-driven** (exponential backoff + jitter, capped); route every call through one base
  `send()` wrapper that centralizes retries + error mapping (don't scatter `clientProxy.send` across services).
  ```ts
  @Injectable() export class WalletClient implements OnApplicationShutdown {
    constructor(@Inject(walletMs) private readonly proxy: ClientProxy) {}
    onApplicationShutdown() { this.proxy.close(); }
    send<I, R>(pattern: string, data: I) { return this.base.sendAsync<I, R>(this.proxy, pattern, data); }
  }
  ```
- **Scope every read/write to the caller's tenant/permitted set.** For non-admin roles, an
  interceptor auto-injects the caller's allowed scope (e.g. their `locationIds`/`orgId`) into the
  query — or **intersects** a requested scope with the allowed set and drops the rest — so a handler
  can't return or mutate another tenant's data even when asked. Centralize this in one
  interceptor/guard; don't re-check in every handler. ▸ *Other stacks:* a query-scoping middleware or
  DB row-level security.
- **Bulk CSV/spreadsheet import** (streaming parse + per-row error report + chunked upsert) has its
  own skill — see `import-data-from-csv`.
- **Background jobs & caching** (Bull queues, Redis cache) have their own skill —
  see `background-jobs-and-caching`.
▸ *Other stacks:* a DB transaction + outbox/compensation; a global error-swallowing wrapper on async
event handlers; one connection-managed client per dependency with retries centralized.

## Verification

Reviewing a change, confirm:

- **Control flow:** no manual index `for`/`while` for transforms (`grep -nE 'for ?\(' src --include='*.ts'`
  should hit only side-effect/ordered-async spots); guard clauses up top; ≤2 nesting levels.
- **Async:** independent awaits are inside a `Promise.all`; no `await` inside a `.map` used for
  independent work.
- **Nullability:** nullable fields/returns use the nullable type, not `undefined`.
- **Layout of logic:** private helpers sit below public methods; helper names are verb-led.
- **Queries:** every list/detail query has an explicit `.select([...])`, filters are in the SQL
  (`IN (:...)` for lists), relations are joined (no per-item query in a loop), pagination uses one
  count+rows call, writes that can conflict use `upsert`, and sorted/filtered columns are indexed.
- **Events:** outbound payload is a mapped subset (not the raw entity); topic/queue names are
  constants; consumers wired from config.
- **Logging:** message + context-object form (no string-concatenated context); PII masked; errors
  log the cause + ids.
- **Tests:** go through the transport/HTTP boundary, seed via factories, assert persisted state, mock
  only externals, cover an error path.
- **Gates:** lint, build, and the test suite pass (e.g. `pnpm lint` / `pnpm build` / `pnpm test`).

## Related

- [structure-a-backend-service](./structure-a-backend-service.md) — where these files live and how a
  feature is wired (this skill is the *how to write the code inside*; that one is the *where & what*).
- [README](./README.md) — how project skills are organized.
- **Global assistant instructions** (the authority for the do/don't this skill restates): *Code
  Style — Iteration & Collections*, *Code Style — Function Size & Density*, *Database & Migration
  Rules*, *DRY — Parallel flows*, *Feature Flags & Observability*, *Testing Rules / HTTP-layer
  testing rule*, *Root-Cause First*.
