---
name: test-data-factories
description: Generates realistic, maintainable test data with factories instead of brittle shared fixtures — factory libraries (Ruby factory_bot, Python factory_boy/model-bakery, PHP Foundry/Faker, JS Fishery/@mswjs/data/Fabbrica, Java instancio/Java-faker, Go fake) that build valid objects with sane defaults, Faker for realistic values, traits/transient params/variants for state, build vs create (in-memory vs persisted), sequences for unique fields, nested associations and object graphs without combinatorial fixtures, deterministic seeding (Faker.seed/locale pinning) for reproducible CI, idempotent upsert-based DB seeders for dev/E2E that re-run cleanly, and anonymized prod-like data via masking/synthesis — so every test declares only the fields it cares about and stays valid as the schema evolves.
when_to_use: Building test data — replacing shared YAML/SQL fixtures, generating valid model instances for unit/integration/E2E tests, seeding a dev or E2E database idempotently, creating object graphs with associations, or producing anonymized prod-like datasets. Distinct from write-tests (structures the assertions and suite; this generates the inputs they assert on) and validate-data-quality (checks real datasets for nulls/dupes/outliers; this manufactures synthetic data on purpose).
---

## When to Use

Reach for this skill when you need to manufacture valid, realistic test data and the pain is fixtures that rot or tests coupled to a giant shared dataset:

- "Replace our `fixtures/*.yml` — every schema change breaks 200 tests"
- "Give me a valid User/Order with just the 2 fields this test cares about"
- "Build an order with 3 line items, a customer, and an address" (object graph)
- "Seed the dev/E2E database so `db:seed` is safe to re-run"
- "Tests pass locally, flake in CI" (non-deterministic random data)
- "Generate realistic-but-fake names/emails/addresses" (Faker)
- "Make a prod-like dataset for staging without leaking PII" (anonymize)

NOT this skill:
- Structuring the assertions, arrange/act/assert, mocking, coverage, test naming → write-tests (it organizes the suite that *consumes* the data this skill builds)
- Checking a *real* dataset for nulls, dupes, outliers, schema drift → validate-data-quality (it inspects data you didn't generate; this fabricates data on purpose)
- Profiling/exploring an unfamiliar dataset's distributions → profile-dataset
- Generating *inputs to find bugs* by shrinking counterexamples → property-based-testing (it searches the input space; this hands you fixed, named, realistic instances)
- Driving a browser through the app to set up E2E state via the UI/API → write-playwright-e2e (it may *call* this skill's seeder to plant rows directly)
- Stabilizing a flaky test whose data was already non-deterministic → debug-flaky-tests (seed pinning here is one of its fixes)
- Safe schema changes / running the migration the seeder targets → db-migration-safety
- Designing the schema/associations themselves → design-relational-schema

## Steps

1. **Prefer factories over shared fixtures — fixtures are the anti-pattern you're replacing.** A global `users.yml`/seed SQL becomes load-bearing: tests depend on `user(:admin)` having exactly these fields, so any edit ripples across the suite and tests silently couple to unrelated data ("mystery guest"). Factories invert this: a `build(:user)` is valid by default, and each test **overrides only the attributes it asserts on**. Pick the idiomatic library:

   | Stack | Library | Build vs persist |
   |---|---|---|
   | Ruby / Rails | **factory_bot** | `build(:user)` (RAM) · `create(:user)` (DB) · `build_stubbed` (no DB, fake id) · `attributes_for` (hash) |
   | Python / Django | **factory_boy** (`DjangoModelFactory`) or **model-bakery** (`baker.make`/`baker.prepare`) | `.build()` vs `.create()` / `prepare` vs `make` |
   | Python (plain) | **factory_boy** `Factory` + `faker` | `.build()` only |
   | JS / TS | **Fishery** (`.build()`), **@mswjs/data**, **Fabbrica** (Prisma), `@faker-js/faker` | build returns object; persist via your ORM |
   | PHP / Laravel | **Foundry** or Eloquent factories + **fakerphp/faker** | `Model::factory()->make()` vs `->create()` |
   | Java / Kotlin | **instancio**, **easy-random**, **datafaker** (Java-faker successor) | POJO in memory |
   | Go | `go-faker`/`gofakeit` + hand-rolled builder funcs | struct in memory |

2. **Make the default object minimally valid; override per test.** The factory's defaults must pass all model validations on their own so `create(:user)` never fails for an unrelated reason. Then a test passes only what it cares about:

   ```ruby
   # factory_bot
   factory :user do
     name  { Faker::Name.name }
     email { Faker::Internet.unique.email }   # unique → no collisions
     role  { "member" }
   end
   # test asserts on role only:
   admin = create(:user, role: "admin")       # name/email auto-filled, valid
   ```
   ```ts
   // Fishery
   const userFactory = Factory.define<User>(({ sequence }) => ({
     id: sequence,                              // 1,2,3… unique per build
     email: `user${sequence}@example.test`,
     role: 'member',
   }));
   userFactory.build({ role: 'admin' });        // override one field
   ```
   Use the reserved **`example.test`/`example.com`** domains and the `+tag` trick for emails so generated data never hits a real inbox.

3. **Use Faker for realism, but never for fields you assert on.** Faker gives plausible names/emails/addresses/companies so data looks real and surfaces formatting bugs. The discipline: **if a test checks a value, set it explicitly; let Faker fill the rest.** Asserting against a Faker-generated value is a guaranteed flake. Pin locale (`Faker::Config.locale = :en` / `faker.setLocale`) so address/phone formats are stable across machines, and use `unique` generators (`Faker::Internet.unique.email`, `faker.helpers.unique` — note `@faker-js/faker` removed `unique`; use a sequence or `faker.string.uuid` instead) for columns under a UNIQUE constraint.

4. **Sequences for unique/monotonic fields; transient params for build-time knobs that aren't attributes.** Sequences (`sequence(:email) { |n| "user#{n}@example.test" }`) guarantee uniqueness without a global mutable counter. **Transient/transient-params** are inputs that shape the build but aren't columns:

   ```ruby
   factory :order do
     transient { line_item_count { 3 } }       # not a column
     after(:create) do |order, ev|
       create_list(:line_item, ev.line_item_count, order: order)
     end
   end
   create(:order, line_item_count: 5)
   ```
   factory_boy calls these `Params`/`class Params: ...` with `factory.Trait`; Foundry uses `->with()`/states. Reach for them whenever a test wants "an order with N items" without N being an order column.

5. **Model variants with traits, not a forest of sub-factories.** A trait is a named bundle of attribute overrides; compose several in one call. This beats `factory :admin_user`, `factory :suspended_admin_user`, … which explodes combinatorially:

   ```ruby
   factory :user do
     trait(:admin)     { role { "admin" } }
     trait(:suspended) { suspended_at { Time.current } }
     factory :premium  { plan { "premium" } }   # nested for true subtype
   end
   create(:user, :admin, :suspended)            # compose traits
   ```
   factory_boy → `class Params:` + `factory.Trait`; Fishery → `.params()` + transient `transientParams`, or named factory variants; model-bakery → recipes. **One base factory + traits** is the maintainable shape; deep factory inheritance is not.

6. **Build object graphs through associations — don't hand-wire foreign keys.** Declare relations so the factory creates the whole graph and back-references resolve automatically:

   | Lib | Association syntax |
   |---|---|
   | factory_bot | `association :customer` · `customer { create(:customer) }` · `create_list(:item, 3, order:)` |
   | factory_boy | `customer = factory.SubFactory(CustomerFactory)` · `factory.RelatedFactory` (reverse) · `factory.List` |
   | Fishery | `customer: customerFactory.build()` inside the generator, or `associations` param |
   | Foundry | `CustomerFactory::new()` as an attribute; `->many(3)` for collections |

   **Build the minimal graph the test needs** — pulling in 4 levels of associations slows every test and recreates the fixture problem. Use `build`/`build_stubbed` (no DB) for pure-logic tests; reserve `create` for tests that actually query the DB. Guard against accidental N× object creation in `before` hooks.

7. **Seed dev/E2E databases idempotently — upsert, never blind insert.** A seed script that `INSERT`s breaks on the second run (unique-constraint violation) and corrupts state. Make it re-runnable:

   ```ruby
   # Rails: find_or_create_by / upsert on a natural key
   User.find_or_create_by!(email: "demo@example.test") { |u| u.name = "Demo" }
   ```
   ```sql
   INSERT INTO plans (code, name) VALUES ('pro','Pro')
   ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name;   -- idempotent
   ```
   Rules: key every seed row on a **stable natural key** (slug/code/email), not an auto-id; wrap the whole seed in a transaction; make `db:seed` / `prisma db seed` / `php artisan db:seed` safe to run N times with identical end state. Separate **dev seed** (rich demo data, may be large) from **E2E/test seed** (minimal, deterministic, reset between runs via truncate or transactional rollback). For E2E, prefer planting rows via the factory/seeder directly over driving the UI — orders of magnitude faster and less flaky.

8. **Make data deterministic in CI — pin the RNG seed and locale.** Random factory data that flakes is worse than fixtures. Pin a seed so a failing CI run is reproducible:

   | Tool | Seed control |
   |---|---|
   | Faker (Ruby) | `Faker::Config.random = Random.new(RSEED)` |
   | @faker-js/faker | `faker.seed(12345)` (per-suite, in a `beforeEach`/global setup) |
   | faker (Python) | `Faker.seed(0)` / `fake.seed_instance(0)` |
   | factory_boy | `factory.random.reseed_random('seed')` |
   | RSpec / Jest | `--seed`/`config.seed`; Jest `--testSequencer` + faker seed |

   Print the seed on every run and let CI re-run with a fixed seed to reproduce a failure. **Pin the locale too** — default-locale drift changes address/phone formats and breaks format-sensitive assertions. Don't share mutable factory state across parallel test workers; each worker reseeds.

9. **For prod-like datasets, anonymize — synthesize or mask, never copy raw PII.** Staging/perf data that mirrors prod shape without leaking real people: (a) **synthesize** from factories at volume (`create_list(:user, 100_000)` / a Faker loop) when you only need realistic shape; (b) **mask/anonymize** a prod snapshot when you need real distributions — replace names/emails/SSNs with Faker values, **deterministically** (hash the original → same fake every time, so foreign keys stay consistent), null or tokenize free-text, and shift dates by a constant offset. Tools: pg `anon` extension, `pganonymize`, Snaplet/`@snaplet/seed`, `faker` + a mapping table. Never load an un-anonymized prod dump into a lower environment — that's a PII breach. Keep the anonymization mapping out of the lower environment.

10. **Keep factories close to the code and validated.** Co-locate factories with the test suite (`spec/factories`, `test/factories`, `src/test-utils/factories`), auto-load them, and add a CI lint that **`build`s every factory and asserts it's valid** (factory_bot's `FactoryBot.lint`) so a schema/validation change that breaks a factory fails fast instead of in 50 unrelated tests. When a column is added with a NOT NULL/validation, fix it in the **one** factory, not across the suite.

## Common Errors

- **Shared fixtures as source of truth.** One `users.yml` every test secretly depends on → mystery-guest coupling, schema edits break the world. Fix: factories with per-test overrides; delete the global fixture.
- **Asserting against a Faker-generated value.** `expect(user.name).to eq(faker_name)` flakes the moment the seed changes. Fix: set asserted fields explicitly; Faker only fills don't-care fields.
- **Non-deterministic data in CI with no seed.** Intermittent failures no one can reproduce. Fix: pin `faker.seed`/`Faker.seed` and the locale; print and replay the seed.
- **`create` everywhere when `build` would do.** Hitting the DB (and its associations) for pure-logic tests makes the suite slow and order-dependent. Fix: `build`/`build_stubbed`/`prepare` for in-memory; `create` only when you query.
- **Non-idempotent seed script.** Blind `INSERT` → second run violates UNIQUE / duplicates rows. Fix: `find_or_create_by` / `ON CONFLICT DO UPDATE` on a natural key; wrap in a transaction.
- **Sub-factory explosion.** `admin_user`, `suspended_admin_user`, `premium_suspended_admin_user`… Fix: one base factory + composable traits.
- **Over-deep association graphs.** Every `create` drags in 4 levels of records → slow tests and re-coupled data. Fix: build the minimal graph; stub the rest.
- **Duplicate-key collisions from static defaults.** A hardcoded `email: "a@b.com"` default fails the second `create`. Fix: sequences or `Faker::Internet.unique` (or `faker.string.uuid` in @faker-js/faker, which dropped `unique`).
- **Loading raw prod data into staging.** Real PII in a lower environment = breach. Fix: deterministic anonymization/masking or synthesize; keep the mapping out of staging.
- **Locale drift.** Default Faker locale differs by machine/CI → address/phone format assertions break. Fix: pin the locale explicitly.
- **Factories that drift from the schema.** A new NOT NULL column makes every `create` fail cryptically. Fix: `FactoryBot.lint`-style CI check that builds every factory.

## Verify

1. **Factories are valid standalone:** run the lint (`FactoryBot.lint` / build-every-factory test) — every factory and trait `build`s and passes validations with zero overrides.
2. **No fixture coupling:** grep the suite for the old shared fixture references; a test reads only the fields it sets/asserts, and editing an unrelated factory attribute breaks nothing.
3. **Determinism:** run the suite twice with the same pinned seed → identical data and pass/fail; run with two different seeds → still green (no test asserts a Faker value).
4. **Uniqueness holds:** create N rows from a factory with a UNIQUE column in a loop → no constraint violation (sequence/`unique`/uuid working).
5. **Seed is idempotent:** run `db:seed` twice → identical row count and end state, no UNIQUE error; the second run is a no-op or clean upsert.
6. **build vs create honored:** `build`/`build_stubbed` issues zero SQL INSERTs (assert via query log/`assert_no_queries`); `create` persists exactly the intended graph.
7. **Traits compose:** `create(:user, :admin, :suspended)` yields both states; no combinatorial sub-factory needed.
8. **Object graph is minimal and correct:** an order factory creates exactly its declared associations (customer + N items), foreign keys resolve, and no surprise extra records appear.
9. **Anonymized data is safe:** spot-check the prod-like dataset — no real PII, the masking is deterministic (same input → same fake, FKs consistent), and date/format distributions are realistic.

Done = brittle shared fixtures are gone, each test declares only the fields it cares about against a valid-by-default factory, Faker fills the rest with a pinned seed+locale so CI is reproducible, object graphs and traits compose without sub-factory explosion, the dev/E2E seed is idempotent on a natural key, and any prod-like data is deterministically anonymized — all proven by the factory lint, the twice-with-same-seed run, and the double-seed idempotence check.
