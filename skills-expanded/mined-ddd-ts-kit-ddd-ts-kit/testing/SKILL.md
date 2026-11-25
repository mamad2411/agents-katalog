---
name: testing
description: >-
  Use when writing or reviewing a test, turning it.todo into tests, when a test needs data
  setup or a shared arrangement, when tempted by vi.mock, vi.fn or a spy, for an acceptance
  scenario, or on a test/* rule. Given / when / then, fakes, builders, worlds, contract
  suites, end-to-end.
allowed-tools:
  - Read
  - Edit
  - Bash(npx ddd-ts-kit generate *)
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit list *)
  - Bash(npm test *)
  - Bash(npm run lint *)
  - Bash(npm run test:coverage)
  - Bash(npm run test:e2e *)
  - Bash(npx ddd-ts-kit acceptance *)
---

# Tests

A test reads as a business rule: what was true, what was asked, what happened. Examples use
Vitest, the default; with Jest the same rules hold. Every generated spec holds one passing
test and `it.todo` entries naming the behaviours to prove: replace each, never delete one.

## Levels

| Level | What runs | Doubles | Where |
|---|---|---|---|
| domain | aggregates, value objects, domain services | none | `test/unit/` (`<module>/test/unit/` in a context with modules) |
| application | the real handler through the buses, with its permission | fakes of every port, fixed clock, sequential ids | `test/unit/` |
| adapter | one adapter against its real dependency, and the contract suite | none | `test/integration/` (`<module>/test/integration/`) |
| end to end | the whole application through HTTP and the event bus | none; generated seeded data | `test/e2e/` at the project root |
| acceptance | a story as its client sees it, written before its code | none; generated seeded data | `test/acceptance/` at the project root |

## No mocks

No `vi.mock`, `vi.fn`, `vi.spyOn`, their `jest` twins or a mocking library in a context's
tests (`test/no-mocks`): they assert calls, not outcomes, and break on refactoring.

| Need | Use |
|---|---|
| a repository | its fake in `test/fakes/`, or `<module>/test/fakes/` beside its repository (extends `InMemoryRepository`); assert `findById` or `all()` |
| another port | its fake, a working in-memory class recording what it received; an object literal fits too, a port being a shape |
| time, identifiers | `application.clock` (`advance`), sequential ids (`idPrefix`) |
| published events | `application.eventBus.published`; domain events of the command, heard once its handler has returned: `application.domainEvents.on('<name>', ...)` before executing; what `after-commit` handlers threw: `application.domainEvents.afterCommitFailures` |
| logs, metrics, unexpected failures | `application.logger.entries`, `metrics.samples`, `errors.reports` |
| a failing dependency | a method on the fake: `payments.failNextWith(new PaymentDeclined())` |
| a scheduled job | `application.jobs.runNow('<context>.<job>')` |
| the database | the real one in the adapter's integration spec, never a mocked driver |

A fake stays honest because it passes the same contract suite as the real adapter
(`@ddd-ts-kit/testing/contracts`); `generate port|repository` writes both.

## Aggregate specs: given / when / then

```ts
given(anOrder().withLine(aLine()).build())
  .when((order) => order.pay(clock.now()))
  .thenEvents([{ name: 'ordering.order.paid' }]);

given(anOrder().paid().build())
  .when((order) => order.pay(clock.now()))
  .thenError('ORDER_ALREADY_PAID', { orderId: 'order-1' });
```

An event-sourced aggregate starts from its history, without a database, and its snapshots are
proven once:

```ts
givenEvents((id, history) => Order.rehydrate(id, history), [placed, lineAdded])
  .when((order) => order.pay(clock.now()))
  .thenEvents([OrderPaid]);

expectSnapshotEquivalence({ events, rehydrate, policy: orderSnapshots, state: (order) => order.toState() });
```

One intention per test. Assert events, errors, and state through the public API only. A
refusal is asserted by its code and its facts, never by a message or the class of one error:
`thenError(code, facts)` on an aggregate, `expectRefusal(subject, code, facts)` on an action
(`() => Email.create(raw)`, the factory of a value object that throws), a `Result` or a caught error, `expectProblem(response, { status, code, facts })` end to end.

## Handler specs

Generate the world of the context first (`generate test-world <ctx>`, below): a handler, query,
job, background job or process timeout spec generated after it arranges through it, `arrange()`
being one call of the world.
Generated before it, `arrange()` builds a test application from the platform test module, the
context (`contextModule('<context>', declarations)` or its module) and the fakes, and under a
container a comment says the world would shorten it. A world the generator cannot read (it looks
for `export function a<Context>World` and its `<Context>WorldOptions`) is said so, never forced. Either way `holdersOf(permission)` of `@ddd-ts-kit/auth/testing`
gives the actor holding the permission and the authorizer granting it (to the system actor of a
job too): `const { holder, authorizer } = holdersOf(billingPermissions['invoice.issue'])`, the
authorizer handed to `authorizationModule` or `authorizationMiddleware`. Execute
through `application.commandBus` or `queryBus` with an actor built by `anActor()`. Cover: the
happy path, each failure by its error code, nothing saved or published on failure, and the
refusal of an actor without the permission (generated). Reactions: dispatch the event and
assert the command's effect; an integration event handler run twice changes state once.
A reaction or a controller alone is given a `RecordingCommandBus` (or `RecordingQueryBus`) of
`@ddd-ts-kit/kernel/testing` and asserts `executed`; a controller or a route is sent its
request by `routeOf(controller).send(...)` of `@ddd-ts-kit/http/testing`, guards included, as
the generated specs do; the phase of a reaction is the kernel's to prove, never a spec's.

Always assemble the context from its generated file: it is what registers what each
constructor is injected, so neither the test nor the handler lists a dependency. To test one
class alone, take it from that file,
`contextModule('<context>', { PlaceOrderHandler: declarations.PlaceOrderHandler })`, never
from its own import: a class handed over alone has no dependency list
(`WiringError MISSING_DEPENDENCIES`). Every port a class of the assembled context takes is
bound by the platform test module or by a `fake(Port, aFake)`, read models of projections
included.

## Worlds

The arrangement the specs of a context share (the same test application or buses, the same
fakes) is a world, generated once instead of copied or written as a helper:
`npx ddd-ts-kit generate test-world <ctx> [Name]` writes `test/worlds/<name>.world.ts` (`shared/test/worlds/` in a context divided into modules of the model). The one
named after the context is the one the generators of use cases and jobs arrange through.

```ts
const { application, orderRepository } = await anOrderingWorld({
  modules: [holders],
  now: NOW,
  given: async (fakes) => {
    await fakes.orderRepository.save(anOrder().build());
  },
});
```

It builds every fake of the context (`test/fakes/`, and `<module>/test/fakes/` of each module) and returns each under the name of its port; `given`
stores the starting state before the application wires the fakes, so the events recorded while
building it are not announced; `fakes` takes the fake of a port it cannot build alone (a reader
that answers what the spec gives it). The permission, the data and the facts a spec listens to
stay in the spec. Run it again with `--force` once the context has a new fake: a use case whose
spec needs a fake the world lacks is generated without the world, and the output says so. Nothing else goes in
`test/unit/` or `test/integration/` but specs (`test/helper-placed`): an arrangement is a world,
test data a builder, an in-memory port a fake.

## Builders

One per aggregate in `test/builders/`, or `<module>/test/builders/` in the module of its aggregate (`generate builder [--module]`, written with the aggregate):
valid defaults, methods named in the ubiquitous language (`paid()`, not
`withStatus('PAID')`), built through the aggregate's public API so an invalid state cannot be
built. A test states only what its rule depends on. Generated with `--birth "<Fact>"`
(`generate aggregate <ctx> <Name> --birth "Invoice Issued"`), the builder takes the instant of
the birth by its fact (`issuedAt(at)`) and the spec proves the event.

## End to end

For an end-to-end spec (`npx ddd-ts-kit generate e2e <ctx> <UseCase>`), read [end-to-end.md](end-to-end.md) first: the baseline cases, `settled()`, `publish`, `runJob`, `runDueJobs`.

## Acceptance of a story, before its code

For the acceptance spec of a story, read [acceptance.md](acceptance.md) first: criteria, `pending(...)`, `--lock`, and what to do with a scenario that seems wrong. A locked scenario is never changed to make code pass.

## A fix, before its code

A defect is repaired by skill `ddd-ts-kit:fix` (`/ddd-ts-kit:fix <code>`): the spec that reproduces it is written, run to fail, locked and committed before any code, and never changed to make the fix pass.

## Shape

Held by `npm run lint`, on every test file of the project:

- `describe` names the unit in the words of the glossary, as the generators write it: `Invoice line`,
  `Issue invoice`, `POST /invoices`, `When invoice issued`, a policy by its question (`Who may cancel
  an invoice`); `it` states the rule, in lower case, after the rows and the
  criterion it cites: `refuses to pay an order twice`, `#US5.02 AC1 a customer places an order`;
  never `should`, `test`, `works`, nor a method or a class (`test/title-states-a-rule`).
- Arrange, act, assert separated by blank lines; no `if`, no loop, no `try` (`test/no-logic`):
  `it.each` for the boundaries of a value object, a builder or a fake for a decision.
- Every test asserts an outcome (`test/assertion-present`); a refusal by its code and its facts,
  `thenError`, `expectRefusal`, `rejects.toMatchObject({ code })`, `expectProblem`, never
  `toThrow('message')` (`test/refusal-by-code`); no snapshot (`test/no-snapshot`).
- Every test runs: no `.only`, `.skip`, no `.skipIf` on a constant (`test/no-only-no-skip`). What is not proven
  yet is an `it.todo` named after it, which `story --gate close` refuses while it is the story's.
- No shared mutable state; never read a private field.

A coverage rate says that code ran under a test, never that the test asserts anything: write
the spec for the behaviour, and let the rate follow. The thresholds of `ddd-ts-kit.config.json`
are a floor per context and layer, not a goal; a test written to move a number proves nothing.

Each spec file is held to the time budget of its level, five seconds for a unit spec and thirty for an
integration spec by the reference: the runner names the slowest at the end of a run and warns over the budget, failing once the project sets `"enforce": true`. A slow unit spec is a world to share or a fake to write, never a budget to raise.

The night runs `npm run test:mutation`: Stryker on the domain and application layers of every context, the texts of
its refusals left out and its static mutants ignored, then each context held to the `mutation` floor
of the config, the ignored mutants shown beside the score. A survivor is a rule no test states: read it
as a business decision, then state it in a test named after it, or leave the mutant alive and say
why; never narrow the measure (`test/mutation-governed`). A rule written as a declaration, a
transition table or a constant at the top of a file, is never mutated: the test that states it is
its only proof. The text of a refusal leaves the score when it is handed to the error class where
the rule is checked (`InvalidSlot.forRule('ends after it starts')`); a text a helper returns before
the factory is called is measured and survives: throw where the rule is checked. On a pull request
the `mutation-changed` job lists the survivors of the files you changed (`ddd-ts-kit mutation
--changed <base>`, `--survivors` for all of them): read them before asking for a review, each a rule
to state or a survivor to leave alive and say so.

A law a value object holds for every value is stated once, as a property with `fast-check`, added
with the first one (`npm i -D fast-check`):
`fc.assert(fc.property(anyRange(), anyRange(), (one, other) => one.overlaps(other) === other.overlaps(one)))`,
the title stating the law (`overlaps another range in both directions or in none, for any two ranges`),
the arbitrary a small helper of the spec built on the factories of the model, so that every generated
value is one the model accepts. A property is for an invariant, a symmetry, a round trip or an
idempotence of the model; a use case is stated by its scenarios with named values. Every value object
spec the generator writes ends with the planned rule that asks for one;
`npx ddd-ts-kit generate property <context> <ValueObject>` starts it, with the arbitrary, a first law
and fast-check added when it is missing: replace the arbitrary by the real components first.

The titles are read back as a document: `npm run docs:generate` writes `docs/behaviour/<context>.md`
from them, one heading per use case (its handler, policy, route, end-to-end and acceptance specs), then
the model and the reactions, the titles the kit generated listed apart, the row a title cites before
the rule and the rows cited indexed at the end; the pre-commit hook regenerates it when a spec, a source or the config is staged,
and `docs --check` holds it current, so a title is a sentence the business reads, and the page is
committed with the spec.

Finish with `npm test -- <context>`, `npm run lint` (the shape of the tests), `npm run test:coverage`
before the slice is closed, and
`npx ddd-ts-kit check --rule test/no-mocks --rule test/builder-required --rule test/spec-required --rule test/helper-placed --rule test/acceptance-black-box`.
