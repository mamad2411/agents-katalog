---
name: close-test-risk-gaps
description: >-
  Load this skill when a feature works and is about to be called done: triage what a passing suite
  misses (concurrency, contract drift, performance, authorization, migrations). Trigger on "is this
  ready", "before I open the PR", "race condition".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the target project's own test runner already working (`pytest` via `uv run`, or
  `vitest` via `bun`). The performance-regression class additionally needs a benchmark plugin
  (`pytest-benchmark`, `vitest bench`), and the migration class needs a reachable database
  instance. None of these is assumed installed - skip the class instead.
license: Apache-2.0
---

# Close Test Risk Gaps

Unit, integration, and E2E tests all ask the same question: given this input, is the output right?
Five important failure classes are invisible to that question — they depend on _timing_, on _who is
asking_, on _what a different process expects_, on _how long it took_, or on _what data and which
code version were already there_.

This is a triage gate, not a checklist to complete. Run it when a feature is working and about to be
called done. **For each class: does the trigger fire? If no, skip it and say so.** Adding tests
whose trigger did not fire is ritual, and it is how a suite becomes slow and ignored.

The task is done when all five classes have a verdict and every class that fires has its tests
written and passing.

## What waits for a request

Writing and running the tests for each class that fires is part of calling the feature done, so the
classes below apply without being asked. Only a slow or paid run waits for a request: the full
suite, a benchmark harness run, a migration against a restored production-sized copy, or repeated
passes over the whole suite. When one of those would help and was not requested, name the command
and what it would reveal, and state what stays unverified.

## Procedure

### 1. Concurrency and idempotency

**Trigger fires if any of:** two requests can touch the same row; a read-modify-write happens outside
a transaction; there is a retry, webhook, queue consumer, or cron; a counter, balance, or sequence is
incremented; a "check then insert" exists; a background job shares state with a request path.

**The two tests:**

```python
# a) same operation twice — the retry that every queue and webhook will eventually send
async def test_charge_is_idempotent(client, order):
    key = {"Idempotency-Key": "k-1"}
    first = await client.post(f"/orders/{order.id}/charge", headers=key)
    second = await client.post(f"/orders/{order.id}/charge", headers=key)
    assert second.status_code == first.status_code
    assert await count_charges(order.id) == 1  # the invariant, not the response


# b) N at once — assert the invariant, not the individual results
async def test_concurrent_redeem_never_oversells(client, coupon):  # stock = 1
    results = await asyncio.gather(
        *(client.post(f"/coupons/{coupon.id}/redeem") for _ in range(20)),
        return_exceptions=True,
    )
    assert (
        sum(r.status_code == 200 for r in results if not isinstance(r, Exception)) == 1
    )
    assert await stock_of(coupon.id) == 0  # never negative
```

Assert the **invariant** (a count, a balance, a uniqueness constraint), never the individual
responses — which one wins is legitimately nondeterministic, but "exactly one" is not.

If it passes on the first run, run it 20 times before believing it. A race that reproduces one time
in ten is still a race.

---

### 2. Contract drift

**Trigger fires if:** you changed a shape that crosses a process boundary — an HTTP response body, an
event or message payload, a stored JSON column, a public function signature in a library, or a
database column another service reads.

**The test:** assert the response against the published schema, not against a hand-written dict — a
hand-written expectation drifts along with the code and never fails.

```python
def test_order_response_matches_published_schema(client, order):
    body = client.get(f"/orders/{order.id}").json()
    OrderResponseV1.model_validate(body)  # the schema consumers were given
    assert set(OrderResponseV1.model_fields) <= set(body)  # no field silently dropped
```

Removing or renaming a field, tightening a type, or making an optional field required is a
**breaking change** for anyone already consuming it. Adding an optional field is not. If the change
is breaking and consumers exist, the test is not the fix — versioning is; flag it rather than
quietly updating the schema.

For messages and events, pin one real payload per event type as a fixture and validate it. A
consumer that deserializes strictly will break on a producer's "harmless" rename.

When the consumer is a service you also own, the schema check upgrades to a **consumer-driven
contract**: the consumer's expectations are the fixture, and the producer's suite runs against them,
so the producer's CI goes red rather than the consumer's production. Contribute the consumer's
recorded payload to the producer's test fixtures — that captures most of the value without adopting
a broker (Pact, Spring Cloud Contract), which is a tooling decision to raise rather than make
silently.

---

### 3. Performance regression

**Trigger fires if:** the change is on a request-serving hot path; a loop iterates something
unbounded or caller-supplied; a query runs inside a loop (the N+1 shape); a new `await`, network
call, or file read landed in a request path; an index was dropped or a `WHERE` clause changed.

**The test: assert a countable bound, never a wall-clock duration.** Timing assertions are flaky on
shared CI and get deleted within a month.

```python
def test_order_list_does_not_n_plus_one(client, query_counter, orders_factory):
    orders_factory(50)
    with query_counter as q:
        client.get("/orders")
    assert q.count <= 3  # constant in the number of orders — this is the real bug
```

Count queries, HTTP calls, or allocations — those are deterministic and they are what actually
regressed. If you must assert on time, use a benchmark harness with a baseline
(`pytest-benchmark`, `vitest bench`) and a ceiling wide enough that only a real regression trips it,
never a bare `assert elapsed < 0.5`.

The highest-value single assertion here is the N+1 count check. Add it once per list endpoint.

---

### 4. Authorization

**Trigger fires if:** an endpoint accepts a user-supplied identifier; a response contains data owned
by someone; there are roles, tenants, teams, or permissions; anything is admin-only.

**The test: the authz matrix.** Functional tests are written from the happy path — the owner
requesting their own resource — so the case that ships broken is always _another user's resource_.

```python
@pytest.mark.parametrize(
    "actor,target,expected",
    [
        ("owner", "own", 200),
        ("owner", "other_user", 404),  # the one that is always missing
        ("teammate", "own", 200),
        ("anonymous", "own", 401),
        ("member", "admin_only", 403),
    ],
)
def test_order_access_matrix(client, actor, target, expected):
    assert client.get(url_for(target), headers=auth(actor)).status_code == expected
```

Three rules the matrix encodes:

- **Not-yours returns 404, not 403** — a 403 confirms the resource exists, which leaks the ID space.
- **Test the object, not just the route.** Route-level auth passes while the handler happily loads
  any ID it is given. That is the whole IDOR class.
- **Cover write and delete, not only read.** They are usually pasted from the read handler, minus
  the ownership check.

Add one matrix per resource type, not per endpoint: the ownership rule belongs to the resource, so
per-endpoint matrices repeat the same cases.

---

### 5. Migration and rollout compatibility

**Trigger fires if:** the change ships a schema migration or a data backfill; a column is renamed,
dropped, or made `NOT NULL`; a stored format or enum gains or loses a value; a cache key or
serialized payload shape changes. The tests pass because they run against an empty database created
by the migration itself, on one process, with no old code running.

**The three tests:**

```python
def test_migration_round_trips(alembic_runner):
    alembic_runner.migrate_up_one()
    alembic_runner.migrate_down_one()  # the down path nobody runs until an incident
    alembic_runner.migrate_up_one()


def test_backfill_is_idempotent(seeded_db):  # it will be re-run after a timeout
    run_backfill()
    first = snapshot(seeded_db)
    run_backfill()
    assert snapshot(seeded_db) == first


def test_old_code_still_reads_new_schema(seeded_db):
    # during a rolling deploy both versions run at once
    assert PreviousOrderModel.query_all(seeded_db)  # no exception, no missing column
```

Three rules the tests encode:

- **Expand, then contract — in separate deploys.** Add the new column, backfill it, ship code writing
  both, and only then drop the old one. A rename in a single migration breaks every instance still
  running the previous release, which during a rolling deploy is half of them.
- **Run it against prod-shaped data, not fixtures.** A restored copy or a generated table at
  production row count is where the lock and the timeout appear. `ALTER TABLE` on 50M rows is a
  different operation from the same statement on 50.
- **Backfill in batches, and make it resumable.** Assert that a partial run followed by a full run
  leaves the same state as one clean run — because that is what happens when the first attempt is
  killed.

If the migration is not reversible (a dropped column, a lossy type change), say so explicitly and
name the recovery path — restore from backup is an answer, but only if someone has confirmed it.

---

## Output

State the verdict for all five classes, including the skips — a silent skip is indistinguishable
from an oversight:

```
Concurrency  — FIRES: /coupons/{id}/redeem decrements shared stock. Added 2 tests.
Contract     — FIRES: OrderResponse dropped `legacy_total`. Breaking; needs v2, flagged not fixed.
Performance  — FIRES: GET /orders loads customer per row. Added query-count test (was 51, now 3).
Authorization— skipped: no user-supplied IDs, endpoint is unauthenticated and public.
Migration    — skipped: no schema change, no backfill, no stored-format change.
```

If nothing fires, say that explicitly. "All five skipped, none apply" is a legitimate and useful
result — it means the risk was considered, not ignored.
