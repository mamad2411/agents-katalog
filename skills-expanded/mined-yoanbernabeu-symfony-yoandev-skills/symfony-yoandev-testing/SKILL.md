---
name: symfony-yoandev-testing
description: >-
  Write and run PHPUnit tests on a Symfony project the TDD way: the test first, run
  red, then the code — with the test pyramid (TestCase for business rules,
  KernelTestCase for repositories, WebTestCase for HTTP wiring), database isolation
  through dama/doctrine-test-bundle, Doctrine fixtures with named references and groups,
  and native
  test doubles (in-memory mailer, MockHttpClient, in-memory Messenger, MockClock)
  instead of hand-rolled mocks. Use this skill whenever someone says "write a test
  for", "add tests", "test this service", "my test fails", "my test passes but the
  code is broken", "how do I test this", "the test suite is red", "test a controller
  or an API endpoint", "test a console command", "test a voter", "test form or DTO
  validation", "check my validation constraints", "load fixtures in tests", "my tests
  pollute the database", "tests pass alone but fail together", "mock the mailer or the
  HTTP client", "freeze time in a test", or asks for a regression test before fixing a
  bug. Also use it before writing any production code on a project that follows this
  standard, because the test comes first.
---

# Testing

> **Tier: core** — the loop, the pyramid and DAMA apply to every project. The mutation check applies to every declarative behaviour you claim to have tested. Query-count tests are `symfony-yoandev-performance`'s and on demand.

The test is written first, run first, and seen failing first. Everything else in this
skill exists to make that possible on a real Symfony application.

## The loop

```
write the test  →  run it  →  see it RED  →  write the code  →  see it GREEN
```

```bash
vendor/bin/phpunit --filter it_refuses_a_rating_of_zero
```

**The red is the point, not the ceremony.** A test that has never failed is a test you
cannot trust, because there are three ways for it to be green for the wrong reason and
none of them is visible in the code:

- the assertion is inverted, or compares a value with itself;
- the double is permissive — `createStub()` returns whatever the caller asks for, so a
  collaborator that is never called still "works";
- the test never runs at all: wrong namespace, filename not ending in `Test.php`,
  method without `#[Test]`, a directory outside `<testsuites>`.

Seeing red once rules out all three at once. Nothing else does.

A `Class "App\Service\ShelfReader" not found` is a legitimate *first* red — it proves
the test executes. Once the class exists the red must come from an assertion, not from
a fatal error. If you write the class first and the test is green immediately, you have
learned nothing; delete the implementation, watch it fail, put it back.

**Run the failing test alone, not the suite.** `--filter` on the method name gives you
the message in one second and keeps the feedback honest.

## When red-first is impossible: the mutation check

Some things cannot fail before they exist: a validation attribute, an `ORDER BY` in a
repository, a route, `cascade: ['remove']`, a serialization group. The test needs the
code to be there before it can assert anything at all.

The answer is not to skip the proof, it is to move it:

1. write the test, watch it pass;
2. **break the code on purpose** — flip `ASC` to `DESC`, change `min: 1` to `min: 0`,
   delete the constraint;
3. confirm the test goes red;
4. restore, confirm green.

If step 3 stays green, the test measures nothing and it is better deleted than kept —
a test that cannot fail is a comment that costs CI time.

Do this for every declarative behaviour you claim to have tested. It takes fifteen
seconds and it is the only thing standing between "we have a test for that" and
actually having one.

## What each unit must cover

There is no percentage target here. A coverage figure is satisfied by testing getters,
and getters were never where the bugs are. The rule is behavioural: for each unit of
behaviour, ask these five questions and write a test for each answer that exists.

| Question | What it looks like |
|---|---|
| **Nominal** | The case the feature was built for. One test, the happy path. |
| **Boundaries** | The lowest and the highest accepted value, and the first rejected one on each side. Rating 1, 5, 0, 6 — not 3. |
| **Errors** | The precise exception, with `expectException(BookNotFound::class)`. Asserting `\Exception` passes on a `TypeError` and hides a real bug. |
| **Security** | Who may not do this. A rule that is only tested from the allowed side has never been tested. |
| **Side effects** | What else happened: the flush, the email, the message dispatched — and, when the operation can be replayed, that running it twice is not running it twice. |

Boundaries and errors are where `#[DataProvider]` earns its place: one test method, one
provider yielding named cases. The provider must be `static` (PHPUnit 10+).

## The pyramid, and the rule that keeps it honest

| Level | Base class | For | Cost |
|---|---|---|---|
| **Unit** | `PHPUnit\Framework\TestCase` | Business rules, DTO validation, voters, output normalisation | No kernel, milliseconds |
| **Integration** | `KernelTestCase` | Repositories, DQL, mapping, anything that needs a real database | Kernel + database |
| **Functional** | `WebTestCase` | Routing, forms, status codes, redirects, HTML and JSON contracts | Kernel per request |

**A business rule tested through `WebTestCase` is a rule in the wrong place.** If the
only way to check that a rating must be between 1 and 5 is to POST a form, the rule
lives in the controller and should have been a service (`symfony-yoandev-architecture`) or a
DTO constraint. The slow test is the symptom; moving the rule is the fix. The
functional test that remains then asserts what it is actually for: the route exists,
the payload is mapped, the failure is a 422 and not a 500.

The mirror rule: **if you find yourself mocking your own service inside a functional
test, stop.** You are unit-testing through six layers of HTTP. Write the unit test.

## Database isolation: dama/doctrine-test-bundle

`KernelTestCase` and `WebTestCase` talk to a real database, and a test that leaves rows
behind is a test that will fail depending on what ran before it. Every test runs inside
a transaction that is rolled back when it ends, and the bundle is what opens it.

```bash
composer require --dev dama/doctrine-test-bundle
```

Its recipe lives in `recipes-contrib`, so Composer prints `IGNORING` rather than
applying it. Two lines are yours to write. In `config/bundles.php`:

```php
DAMA\DoctrineTestBundle\DAMADoctrineTestBundle::class => ['test' => true],
```

and in `phpunit.dist.xml`:

```xml
<extensions>
    <bootstrap class="DAMA\DoctrineTestBundle\PHPUnit\PHPUnitExtension"/>
</extensions>
```

That is the whole setup. No `setUp()`, no `tearDown()`, no base class to extend: every
test method gets a transaction and gets it rolled back, including everything its HTTP
requests wrote, across as many requests as it makes.

**Write both lines or neither.** The extension registered without the bundle is the
worst configuration this suite knows of: PHPUnit boots it, it finds no static
connection to wrap, every test commits — and the suite stays green while it fills the
database. Measured, on this exact setup. `symfony-yoandev-quality` ships a `phpunit.dist.xml`
with the block already in it, and the CI workflow guards the pairing.

### Why not a manual `beginTransaction()` in `setUp()`

That is what this standard used to say, and it was wrong for a reason that only shows
up in the tests you most want isolated. **A transaction opened in `setUp()` dies on the
second request of a `WebTestCase`.** `KernelBrowser::doRequest()` skips the kernel
reboot for the first request only; on the second the kernel is shut down and rebooted,
the connection is recreated, and the transaction no longer exists. `tearDown()` then
throws `Doctrine\DBAL\Exception\NoActiveTransaction`, and the rows written from the
second request onwards are **committed and left behind** — while the row written by the
first request vanishes with its connection. Isolation disappears exactly where you
believed you had it, and the state you are left with is not even the state before the
test.

DAMA does not have this problem because it does not live in the kernel. It hooks at the
driver level through a PHPUnit extension: the connection is static, it outlives every
reboot, and the transaction is opened and rolled back by PHPUnit's own event system
rather than by your test class.

Nested transactions, tests that genuinely need a commit, and
`dama_doctrine_test.enable_static_connection`: `references/database-tests.md`.

## Test doubles: prefer the ones Symfony ships

Before reaching for `createMock()`, check whether the framework already has a real
implementation that records instead of performing: the in-memory mailer with
`assertEmailCount()` / `assertQueuedEmailCount()`, `MockHttpClient`, the `in-memory://`
Messenger transport, `MockClock`. They exercise your actual wiring — serializer,
transport, template — where a mock only proves you called a method.

For your own collaborators:

- **`createStub()`** when the double is scenery — it feeds a value in and you assert on
  something else.
- **`createMock()`** only when you follow it with `expects()` — the call *is* the
  assertion.

A mock created without any expectation emits a PHPUnit notice from PHPUnit 11 onwards,
telling you to use a stub instead. It is a *PHPUnit* notice, not a PHP one — details
and the exact config flag in `references/test-doubles.md`.

**`$container->set()` is for external boundaries only**: a payment gateway, an SMS
provider, a third-party API you do not want to call. Never for your own services. If a
functional test needs your own service replaced, the rule under test is in the wrong
layer and deserves a unit test instead.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Test green on the first run, before any code | It never ran, or the assertion is trivially true | Break the code and confirm red (mutation check) |
| `rollBack()` throws `NoActiveTransaction` in a `WebTestCase` | A hand-rolled transaction from `setUp()`, killed by the kernel reboot on request 2 | Delete it; DAMA owns the transaction. Do not layer the two |
| Rows survive a test despite DAMA being installed | The PHPUnit extension is registered but the bundle is not in `config/bundles.php` | Add the `['test' => true]` entry; `php bin/console --env=test debug:config dama_doctrine_test` must exit 0 |
| Tests pass alone, fail together | Shared state: rows left behind, a `static`, fixtures loaded once and mutated | Check DAMA is actually active; fetch fixture data by named reference, never `findAll()[0]` |
| `This bundle only works for database platforms that support savepoints` | DAMA on a platform without savepoints | Change engine, or drop DAMA on that connection with `enable_static_connection: {name: false}` |
| Tests write to the **dev** database | On SQLite, `dbname_suffix: '_test'` has no effect — DoctrineBundle documents this | Put an explicit `DATABASE_URL` in `.env.test`, or use `%kernel.environment%` in the DSN |
| `The "App\Service\X" service is already initialized, you cannot replace it` | `$container->set()` called after a request instantiated the service | Replace it before the first request — and reconsider, since it is one of your own services |
| Suite green but full of "PHPUnit Notices" | Mocks without expectations | Use `createStub()`; add `failOnPhpunitNotice="true"` so it can never be ignored again |
| `ConstraintDefinitionException` on `Assert\Range` | `minMessage`/`maxMessage` are rejected when `min` **and** `max` are both set | Use `notInRangeMessage` |
| JSON assertion fails on `4` vs `4.0` | `json_encode(['rating' => 4.0])` produces `{"rating":4}` | Assert the decoded value, or type the DTO property `int` if it is one |
| `#[DataProvider]` not found / provider ignored | The provider method is not `static`, or the name is misspelled | Make it `public static`, returning a `\Generator` with named keys |
| Coverage metadata error | `#[CoversClass]` points at a class that does not exist or is not covered | Fix the reference; `#[CoversClass]` on the class under test, `#[UsesClass]` for collaborators |
| Emails never arrive in a functional test | This standard routes `SendEmailMessage` to the async transport | Assert with `assertQueuedEmailCount()`, not `assertEmailCount()` |
| `symfony console ... --env=test` hit the dev database | The Symfony CLI injects Docker variables regardless of `--env` | Use `php bin/console` for anything touching the test database (`symfony-yoandev-local-dev`) |

## Version notes

`vendor/` is the source of truth over anything written here. Where a version matters:

- `static::runCommand()` needs Symfony 8.1+; before that, `CommandTester` by hand.
- `enableAttributeMapping()` on the validator builder is 7.0+; it was
  `enableAnnotationMapping()` before.
- DBAL 4 declares `beginTransaction(): void` — the old `bool` return is gone, and
  nested transactions always use savepoints. That is what lets DAMA's outer transaction
  contain everything a `flush()` opens inside it.
- `dama/doctrine-test-bundle` 8.x is the PHPUnit 10+ line: the extension is registered
  as `<extensions><bootstrap class="…"/></extensions>`, not with the pre-10
  `<extension class="…"/>`. Verified on 8.6.0 with PHPUnit 13.3.2.
- `doctrine/data-fixtures` 2.0 made `getReference()` take the class as a second
  argument: `getReference('book_dune', Book::class)`.

## Out of scope

- **Query-count assertions for N+1** — that is `symfony-yoandev-performance`. `DebugStack` is
  gone from DBAL 4, but `DoctrineDataCollector::getQueryCount()` is alive and is the
  route that skill uses; do not invent a replacement here.
- **PHPStan, deptrac, php-cs-fixer, the CI workflow, and the `phpunit.dist.xml` that
  carries the DAMA extension and `failOnPhpunitNotice`** — `symfony-yoandev-quality`.
- **Getting the database and the mailer running locally** — `symfony-yoandev-local-dev`.

## Reference files

| File | When to read it |
|---|---|
| `references/database-tests.md` | Any test that touches the database: DAMA setup and its failure modes, what the kernel reboot still costs, fixtures, groups, named references |
| `references/test-doubles.md` | Choosing a double, the PHPUnit notice, `$container->set()`, and the native fakes for mailer, HTTP, Messenger and time |
| `references/functional-tests.md` | `WebTestCase`, forms and CSRF, JSON and RFC 7807 assertions, console commands, voters, DTO validation |
