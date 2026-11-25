---
name: testing-data
description: "Test data that keeps tests readable and independent: factories and builders, the minimum data each test needs, unique values, seeded randomness, controlling time, golden files, large datasets for performance tests, and never using real personal data. Read before creating fixtures, factories or seed data for tests."
---

# Test data that stays readable

The naive way: one big fixtures file (`fixtures.json`, `seed.sql`) that every
test leans on, so changing one user breaks forty tests; objects with thirty
fields spelled out in every test; `test@test.com` shared by all; Faker
without a seed, so a failure cannot be replayed; `new Date()` inside the
data; and rows copied from production with real names in them. This skill:
factories with valid defaults, only what matters visible in the test,
unique values, seeded randomness, fixed time, golden files, volume for
performance tests, and no real personal data. Principles in `testing`.

## 1. Factories over shared fixtures

- A factory builds a valid object with boring defaults; each test overrides
  only what it is about: `orderFactory.build({ status: "paid" })`.
- A shared static fixture couples tests: they depend on one record's
  fields, break when someone edits it, and hide what they rely on. Keep
  static data only for reference data that never changes per test
  (currencies, countries, plans).
- `build` in memory for unit tests; `create` (persisted) only for tests that
  need rows.

| Stack | Use |
|---|---|
| TypeScript | fishery, or a plain `makeOrder(overrides)` function; `@faker-js/faker` for values |
| Python | factory_boy (`DjangoModelFactory`, `SQLAlchemyModelFactory`), model_bakery for Django, polyfactory for pydantic and dataclasses |
| Ruby | factory_bot: `build`, `create`, `build_stubbed`, traits |
| Java and Kotlin | test data builders; Instancio to fill whole objects; Kotlin default arguments |
| .NET | builders; Bogus for values; AutoFixture |
| Go | a helper with functional options |
| Rust | `Default` with struct update syntax (`Order { status: Paid, ..Default::default() }`); the `fake` crate |
| PHP (Laravel) | model factories with states: `Order::factory()->paid()->for($customer)->create()` |

```ts
import { Factory } from "fishery";

export const userFactory = Factory.define<User>(({ sequence }) => ({
  id: `usr_${sequence}`,
  email: `user${sequence}@example.test`,
  name: "Test User",
  role: "member",
  createdAt: new Date("2026-01-15T09:00:00Z"),
}));
export const adminFactory = userFactory.params({ role: "admin" });

const owner = userFactory.build({ name: "Ana" }); // params are merged over the defaults
```

```python
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    status = "pending"
    total_cents = 1500

    class Params:
        paid = factory.Trait(status="paid", paid_at=datetime(2026, 9, 29, 10, tzinfo=UTC))

# OrderFactory(paid=True), OrderFactory.build(total_cents=0)
```

```go
func newOrder(t *testing.T, db *sql.DB, opts ...func(*Order)) Order {
	t.Helper()
	o := Order{ID: newID("ord"), Status: "pending", TotalCents: 1500, CustomerID: newCustomer(t, db).ID}
	for _, opt := range opts {
		opt(&o)
	}
	insertOrder(t, db, o)
	return o
}

paid := newOrder(t, db, func(o *Order) { o.Status = "paid" })
```

## 2. Only what matters, in the test

- A value the test asserts on is set in the test, even when the default
  already has it. Defaults are noise; overrides are the signal.
- No mystery guest: nothing the test depends on is found by id `42` in a
  seed file. It is created in the test or in a fixture named for it
  (`givenAPaidOrder()`, `aCustomerIn("Europe/London")`).
- Defaults stay boring and valid, and no test relies on them silently.
  Change a default: the tests that fail were relying on it, so make them set
  the value.
- Factories stay valid as models change: `FactoryBot.lint`, or one test that
  builds each factory once.

## 3. Unique values and relationships

- Unique fields (email, username, slug, external id) come from sequences or
  UUIDs, so parallel workers and reruns never collide:
  `user${sequence}@example.test`, `factory.Sequence(...)`, `sequence(:email)`,
  `uuid4().hex`, `crypto.randomUUID()`. A sequence is per process: with
  several workers on one database, add the worker id or use a UUID.
- Addresses from reserved names (RFC 2606 and 6761: `example.com`,
  `example.org`, `.test`, `.invalid`), so nothing mails a real person.
  `faker.internet.email()` produces real domains such as `gmail.com`; use
  `faker.internet.exampleEmail()` or your own `@example.test`.
- Phone numbers from ranges reserved for fiction: 555-0100 to 555-0199 in
  North America, 07700 900000 to 07700 900999 in the UK.
- Relationships built explicitly (`userFactory.build({ teamId: team.id })`,
  `SubFactory`, `association`), and only the graph the test needs; not a
  factory that silently creates five related records.
- Never assert on generated ids or on auto-increment values (`id == 1`):
  they change with parallel runs, truncation and retries.

## 4. Randomness, always with a seed

- Random values (Faker) are fine for fields that do not matter, when the run
  can be replayed: a seed per test, printed, and overridable.
- Where a value changes the test's meaning (a quantity that is sometimes 0),
  choose it explicitly; random is for irrelevant fields only.

```ts
// a Vitest setup file: the same data for each test, whatever ran before it
import { faker } from "@faker-js/faker";
import { beforeEach, onTestFailed } from "vitest";

const seed = Number(process.env.TEST_SEED ?? 1234);
beforeEach(() => {
  faker.seed(seed);
  onTestFailed(() => console.error(`faker seed: ${seed} (rerun with TEST_SEED=${seed})`));
});
```

- Python: Faker's pytest plugin gives a `faker` fixture reseeded (to 0, or
  your `faker_seed` fixture) for every test; pytest-randomly reseeds
  `random`, Faker and factory_boy per test from its printed seed
  (`--randomly-seed=<n>` replays); `factory.random.reseed_random(1234)`
  seeds factory_boy directly.
- Go: `rng := rand.New(rand.NewPCG(seed, seed))` from `math/rand/v2`, with
  `t.Logf("seed %d", seed)`. Rust: `StdRng::seed_from_u64(seed)`.
- Property-based tests seed and shrink for you (`testing-unit`).

## 5. Time in the data

- Fixed timestamps in factories (`2026-01-15T09:00:00Z`), never `now()`;
  relative times computed from the frozen clock ("created three days ago"
  is the frozen now minus three days).
- Freeze or inject the clock, and restore it after each test:

| Stack | How |
|---|---|
| Vitest and Jest | `vi.useFakeTimers({ now: new Date("2026-09-29T10:00:00Z") })` or `vi.setSystemTime(...)`; `jest.useFakeTimers({ now })`; real timers in `afterEach` |
| Python | time-machine: `@time_machine.travel(dt.datetime(2026, 9, 29, 10, tzinfo=dt.UTC), tick=False)` or its `time_machine` fixture (`move_to`, `shift`); freezegun: `@freeze_time("2026-09-29 10:00:00")` |
| Java | an injected `Clock.fixed(Instant.parse("2026-09-29T10:00:00Z"), ZoneOffset.UTC)` |
| .NET | an injected `TimeProvider`; `FakeTimeProvider` with `Advance(TimeSpan.FromMinutes(16))` |
| Go | a `Clock` interface or `now func() time.Time` field; `testing/synctest` for timers |
| Rails and Laravel | `travel_to Time.utc(2026, 9, 29, 10)`; `$this->travelTo(...)`, `Carbon::setTestNow(...)` |

- time-machine patches time at the C level, so it also catches libraries
  that bypass Python's `datetime`; freezegun patches Python modules only.
- Store and generate times in UTC with explicit offsets; add cases for a
  +05:30 zone and a DST day where the logic is local (`testing-unit`).
- The database has its own clock: set timestamps explicitly in inserted rows
  when a test depends on them.

## 6. Golden files

For output awkward to assert field by field: generated code, reports,
rendered emails, CLI output, SQL from a query builder. Stored beside the
test, compared exactly (after normalising line endings and volatile
fields), regenerated with a flag, and reviewed like code.

```go
var update = flag.Bool("update", false, "rewrite golden files")

func TestInvoiceText(t *testing.T) {
	got := RenderInvoice(sampleInvoice())
	golden := filepath.Join("testdata", "invoice.golden.txt")
	if *update {
		if err := os.WriteFile(golden, []byte(got), 0o644); err != nil {
			t.Fatal(err)
		}
	}
	want, err := os.ReadFile(golden)
	if err != nil {
		t.Fatal(err)
	}
	if diff := cmp.Diff(string(want), got); diff != "" {
		t.Errorf("invoice mismatch (-want +got):\n%s", diff)
	}
}
```

- Regenerate: `go test ./invoice -update`; Vitest
  `await expect(text).toMatchFileSnapshot("./__snapshots__/invoice.txt")`
  with `-u`; `cargo insta review`; syrupy `--snapshot-update`.
- Go ignores `testdata/` when building packages: the place for inputs and
  golden files.
- A golden file too big to read in review is a snapshot nobody reads: keep
  them small, one concern each.

## 7. Development seeds are not test data

- Development seeds (`prisma db seed`, `bin/rails db:seed`,
  `php artisan db:seed`) fill a local app for people: variety, volume, demo
  accounts. Tests never depend on them; they create their own data. Seed
  scripts may reuse the factories.
- Reference data the app needs (roles, currencies, plans) comes from
  migrations or one seed both run; tests may read it, never change it.
- Seeds are idempotent (upsert by a natural key), so running twice is safe.

## 8. Large datasets for performance tests

Generate volume with the shape of production (row counts, skew, null
ratios, text lengths), not copies of it. In PostgreSQL, set-based and
reproducible:

```sql
INSERT INTO customers (id, email)
SELECT g, 'customer' || g || '@example.test' FROM generate_series(1, 10000) AS g;

SELECT setseed(0.42); -- the same "random" data on every run
INSERT INTO orders (customer_id, status, total_cents, created_at)
SELECT 1 + floor(10000 * power(random(), 3))::int, -- skewed: a few customers own most orders
       (ARRAY['paid', 'paid', 'paid', 'pending', 'refunded'])[1 + floor(random() * 5)::int],
       100 + floor(random() * 50000)::int,
       timestamptz '2026-01-01 00:00:00+00' + random() * interval '270 days'
FROM generate_series(1, 1000000);
```

- Bulk load (`COPY`, multi-row inserts), never one ORM insert per row.
- Keep volume scripts out of the unit and integration suites; they belong to
  a performance job, measured with `EXPLAIN (ANALYZE, BUFFERS)` or the load
  tool.

## 9. Never real personal data

- No production copies in tests, fixtures, cassettes or seeds: names,
  emails, addresses, phone numbers, payment details, health data, and free
  text (which contains all of them). It ends up in git history, CI logs and
  laptops, beyond the purpose it was collected for (purpose limitation under
  GDPR and similar laws).
- A bug that needs production-shaped data is reproduced with generated data
  of that shape. If a real sample is unavoidable, anonymise it
  irreversibly (replace, not mask; mind free text and JSON columns; keep
  references intact) with a tool such as PostgreSQL Anonymizer or
  Greenmask, follow the organisation's policy, and delete it afterwards.
- Secrets never appear in test data: fake keys that are obviously fake
  (`test-api-key`), `Authorization` headers filtered from recordings.

## 10. Cleaning up

- Each test leaves nothing behind: transactions rolled back, truncation or a
  database per test (`testing-integration`); files in temporary directories
  (`tmp_path`, `t.TempDir()`, `fs.mkdtemp`); objects in storage under a
  per-run prefix, removed at the end.
- Cleanup runs in teardown or fixtures, so it also runs when the test fails.
- Correctness never depends on cleanup: with unique values, a test also
  passes when a previous run left data behind.

## Check it

- Read each new test: every value it asserts on is visible in its body.
- Search the test data for real-looking details:
  `grep -rEn "@(gmail|yahoo|hotmail|outlook)\.com" tests/`, and names or
  numbers copied from tickets.
- Run the suite twice without resetting, and with parallel workers: no
  unique-constraint failures.
- Run with another seed (`TEST_SEED=99`, `--randomly-seed=99`): still green;
  a failure prints its seed.

## Avoid

One fixture file every test depends on; every field spelled out in every
test; mystery guests; hard-coded unique values; `test@test.com`; unseeded
randomness; `now()` in factories; assertions on generated ids; golden files
updated without reading the diff; production data or real people's details
anywhere in tests; data left behind for the next test.
