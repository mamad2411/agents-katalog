---
name: nullables-test
description: "Write illustrative tests for code that follows the Nullables pattern. Verifies the class under test is ready (all HARDWIRED_INFRA replaced by INJECTED_INFRA, every dependency has .createNull), then writes narrow, sociable, state-based tests using .createNull(). Tests should illustrate the system's concepts and architecture, not just achieve coverage. Use after applying the nullables-refactor skill, or when writing tests for code that already uses DUAL_FACTORY."
---

# Nullables Test

Write tests for code that follows the Nullables pattern. Tests should illustrate how the system works — grounding the codebase's own concepts through concrete examples.

## Vocabulary

This skill uses terms from `references/vocabulary.md`. Key terms: HARDWIRED_INFRA, INJECTED_INFRA, DUAL_FACTORY, NULLABLE, CONFIGURABLE_RESPONSE, OUTPUT_TRACKING, INFRASTRUCTURE_WRAPPER, NULLABLE_CLASS, CREATE_BOUNDARY_RULE, VALUE_OBJECT.

## Philosophy

Tests are not just for coverage — they are **illustrations of the system**. A developer reading the tests should learn:

- What the class does and why it exists
- What its key behaviors are, expressed in the system's own vocabulary
- What OUTSIDE_WORLD interactions it has (visible through CONFIGURABLE_RESPONSE and OUTPUT_TRACKING)
- How it handles important edge cases

Write the minimum number of tests that ground these concepts. Don't exhaustively test every path — focus on tests that teach a reader about the system. The system being tested has its own domain, its own vocabulary, its own architecture. The tests should reflect that.

## Precondition: Is This Class Ready To Test?

Before writing tests, verify the class under test is testable. Walk this checklist:

### 1. No HARDWIRED_INFRA remaining

Scan the class for any OUTSIDE_WORLD calls used directly (imported and called inline). If found, the class is not ready — the `nullables-refactor` skill should be applied first.

### 2. Class has DUAL_FACTORY

The class must have `.create()` and `.createNull()`. If not, it's not ready.

### 3. All INJECTED_INFRA has `.createNull()`

For each dependency injected through the constructor:

- Does it have `.createNull()`?
- Does `.createNull()` accept CONFIGURABLE_RESPONSE parameters?
- If not → that dependency needs to be made nullable first.

This may require **recursive refactoring**: follow the dependency graph down to the leaves (INFRASTRUCTURE_WRAPPERs). Every node in the chain must have `.createNull()` for the top-level `.createNull()` to produce a fully nulled instance.

The chain:
```
ClassUnderTest.createNull()
  → calls DependencyA.createNull()
    → calls InfraWrapperX.createNull()  ← leaf, has EMBEDDED_STUB
  → calls DependencyB.createNull()
    → calls InfraWrapperY.createNull()  ← leaf, has EMBEDDED_STUB
```

If any link in this chain is missing `.createNull()`, flag it. Tell the human which dependency needs work and suggest using `nullables-refactor` on it.

### 4. `.createNull()` actually nulls everything

Create an instance via `.createNull()` with no arguments. It should:
- Execute without errors
- Not make any real OUTSIDE_WORLD calls
- Return sensible defaults

If `.createNull()` throws or makes real I/O calls, the EMBEDDED_STUBs or CONFIGURABLE_RESPONSE defaults are incomplete.

## Writing Tests

### How to instantiate in tests

There are two distinct cases — getting this right matters:

#### Testing `Foo` itself (Foo is the class under test)

Use `new Foo(...)` directly and pass in nulled dependencies with specific CONFIGURABLE_RESPONSE values:

```typescript
// Testing Foo — use `new` so you control each dependency's configuration
const bar = Bar.createNull({ response: specificValue });
const client = HttpClient.createNull({ status: 404 });
const foo = new Foo(bar, client);
```

This gives you fine-grained control over each dependency. You can configure exactly the scenario you want to test. `Foo.createNull()` would bundle its own defaults, which may not expose the granularity you need.

#### Foo as a dependency (testing something that uses Foo)

Use `Foo.createNull()` — its bundled defaults keep the test focused on the actual class under test:

```typescript
// Testing AppService which depends on Foo
// We don't care about Foo's internals here
const appService = new AppService(Foo.createNull());
```

`Foo.createNull()` exists to make Foo a convenient, safe dependency in other tests. It provides sensible defaults so the test reader doesn't get distracted by Foo's configuration.

### What to test

For each class, write tests that illustrate its key behaviors:

#### For INFRASTRUCTURE_WRAPPERs (leaf nodes)

- **Test `.createNull()` works**: creating a NULLABLE instance should succeed with defaults
- **Test CONFIGURABLE_RESPONSE**: configure a specific response and verify the wrapper returns it
- **Test OUTPUT_TRACKING**: if the wrapper has `trackX()`, verify it records interactions
- **Test error paths**: configure error responses via CONFIGURABLE_RESPONSE to verify error handling

These tests verify the wrapper's contract — that the EMBEDDED_STUB faithfully represents what the real system does at the behavior level.

#### For NULLABLE_CLASSes (orchestrators)

- **Test the core behavior**: what does this class *do*? Instantiate with `new` and pass nulled deps, call its methods, verify the result. The test should read like a description of the class's purpose.
- **Test with CONFIGURABLE_RESPONSE**: configure specific dependency responses to test how the class handles different inputs from the outside world
- **Test OUTPUT_TRACKING on dependencies**: verify the class makes the right calls to its dependencies (what was written, in what order) — use trackers, not mocks
- **Test edge cases that matter to the domain**: not every edge case, just the ones that illuminate how the system handles its key scenarios

#### For VALUE_OBJECTs

- Test `.create()` and `.createTestInstance()`
- Test any transformation methods
- Keep it simple — these are usually straightforward

#### For PURE code

- Test with plain inputs and outputs
- No nullable machinery needed

### Example

```typescript
describe('ReportGenerator', () => {
  // ReportGenerator is the class under test — use `new` with nulled deps
  // so we can configure each dependency's responses for the test scenario

  it('generates a report from a template and data', () => {
    const fileStore = FileStore.createNull({
      templates: { 'Sales.html': '<h1>{{title}}</h1>{{rows}}' },
    });
    const webhook = WebhookClient.createNull();
    const generator = new ReportGenerator(fileStore, webhook);

    const result = generator.generate({
      title: 'Sales',
      rows: [{ label: 'Q1', value: 100 }],
    });

    expect(result).toContain('<h1>Sales</h1>');
  });

  it('notifies the webhook after writing the report', () => {
    const fileStore = FileStore.createNull();
    const webhook = WebhookClient.createNull();
    const tracker = webhook.trackNotifications();
    const generator = new ReportGenerator(fileStore, webhook);

    generator.generate({ title: 'Sales', rows: [] });

    // State-based: what was sent, not how
    expect(tracker.data).toEqual([
      { title: 'Sales', path: './output/Sales-report.html' },
    ]);
  });
});
```

### What NOT to do

- **Don't use mocks, spies, or stubs** — use `.createNull()` with CONFIGURABLE_RESPONSE instead
- **Don't test implementation details** — test behaviors and outcomes
- **Don't write exhaustive tests** — write illustrative ones that teach a reader about the system
- **Don't use `.create()` in unit tests** — `.create()` is for narrow integration tests that verify real OUTSIDE_WORLD behavior, run separately
- **Don't add tests for things that can't fail** — if the code is PURE and trivial, a test adds noise not signal
- **Don't use `Foo.createNull()` when testing Foo itself** — use `new Foo(deps.createNull(...))` for fine-grained control

## Integration Tests (Sparingly)

For INFRASTRUCTURE_WRAPPERs only, write a small number of narrow integration tests using `.create()`:

- Verify the real wrapper talks to the real external system correctly
- Verify the EMBEDDED_STUB's behavior matches reality
- These go in a separate test directory/command (they're slow, need real services)
- Keep them few — they exist to validate the contract, not to test business logic

## Output

Present the tests with brief commentary explaining what each test illustrates about the system. Group tests by the class they're testing. If any precondition check fails, report what's blocking and what needs to happen first.
