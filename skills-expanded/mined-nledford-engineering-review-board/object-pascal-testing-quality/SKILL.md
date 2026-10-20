---
name: object-pascal-testing-quality
description: Object Pascal and Delphi testing and quality-lane guidance. Use when selecting, adding, running, or reviewing DUnitX, DUnit, fpcunit, TestInsight, Delphi-Mocks, Spring4D, integration tests, UI tests, or Object Pascal quality commands, and when applying TDD, BDD, or DDD to Object Pascal or Delphi projects. Do not use for ordinary Object Pascal implementation, pattern choice, or smell-only review; use object-pascal-engineering, object-pascal-design-patterns, or object-pascal-antipatterns instead.
---

# Object Pascal Testing Quality

## Use When

Use for Object Pascal test design, runner selection, quality commands, and
compatibility verification. Use
[`object-pascal-engineering`](../object-pascal-engineering/SKILL.md) for
implementation mechanics.

## Workflow

1. Inspect project files, test projects, configured frameworks, mocking
   libraries, CI, and existing tests before choosing a command.
2. Select the lowest level that proves the changed observable contract, then add
   integration or UI coverage where the boundary makes unit proof insufficient.
3. Use repository-native commands and report checks actually run.

## Runner And Tool Discovery

Treat `.dproj`/`.dpr`/`.lpi`/`.lpk` project files, `.dunitx`/test project
configuration, package references, CI, and existing test units as evidence. Do
not assume DUnitX, DUnit, fpcunit, TestInsight, Delphi-Mocks, or Spring4D is
installed because an Object Pascal project could use them. Confirm the framework
and its version from the repository.

## Test Level Selection

- **Unit:** pure policy, values, errors, state transitions, and edge cases.
- **Integration:** database, filesystem, HTTP, framework, event, serialization,
  or component boundaries.
- **Contract:** public APIs, CLI output, form/view-model behavior, and adapter
  behavior.
- **Behavior/BDD:** user-visible workflows and acceptance rules.
- **UI/E2E:** rendered VCL/FMX/LCL workflows, keyboard interaction, and
  accessibility names.
- **Property/generative:** broad invariants where generated inputs add coverage.
- **Mutation:** confidence in meaningful assertions when a mutation tool is
  configured.
- **Static analysis:** type and API consistency; it never proves runtime
  behavior.
- **Compatibility:** declared supported compilers, dialects, and platforms.

## DUnitX, DUnit, And fpcunit

Use the framework already owned by the repository.

- **DUnitX (Delphi):** fixtures are classes with `[TestFixture]`; tests are
  `[Test]` methods; lifecycle uses `[Setup]`/`[TearDown]` and
  `[SetupFixture]`/`[TearDownFixture]`; parameterized tests use
  `[TestCase('name','args')]`; `[Ignore('reason')]` and `[Category('...')]` are
  supported. Register fixtures with `TDUnitX.RegisterTestFixture`. Assertions use
  `Assert.AreEqual`, `Assert.IsTrue`, `Assert.WillRaise`, `Assert.WillRaiseAny`,
  and `Assert.HasNoException`. Run through the console runner with `--run`,
  `--include`/`--exclude`, `--suite`, `--fixture`, `--testcase`, `--format`,
  `--xml`, `--output`, `--hidebanner`, and `--exitbehavior` as configured.
- **DUnit (Delphi, legacy):** `TTestCase` descendants with `published` test
  methods and `SetUp`/`TearDown`. Preserve the repository's convention; do not
  migrate to DUnitX merely for preference.
- **fpcunit (Free Pascal/Lazarus):** `TTestCase` descendants with `published`
  test methods, `SetUp`/`TearDown`, and `TTestSuite`/`TTestRegistry` registration.
  Use `consoletestrunner` with `--format=plain|xml|latex|junit`, `--suite`,
  `--testcase`, `--progress`, `--file`, `--list`, `--all`, `--verbose`, and
  `--sparse` as configured. `OneTimeSetUp`/`OneTimeTearDown` come from a test
  decorator.

Do not claim a command exists or passed without observing it.

## TDD, BDD, And DDD Application

- **TDD:** drive behavior through Red-Green-Refactor with the repository's
  framework. Load [`test-driven-development`](../test-driven-development/SKILL.md)
  for the workflow. Keep tests at the smallest boundary that proves the contract.
- **BDD:** express acceptance criteria as Given/When/Then scenarios. Load
  [`behavior-driven-development`](../behavior-driven-development/SKILL.md) for
  discovery and [`gherkin`](../gherkin/SKILL.md) for formal `.feature` syntax.
  Formal Gherkin tooling for Object Pascal is limited; check the repository before
  assuming a runner exists, and otherwise encode scenarios as descriptively named
  tests.
- **DDD:** keep domain units free of VCL/FMX/LCL, dataset, and transport types so
  domain behavior is unit-testable. Load
  [`domain-driven-design`](../domain-driven-design/SKILL.md) for modeling and
  [`domain-modeling`](../domain-modeling/SKILL.md) for a model review.

## Integration And UI Boundaries

Use real supported services and isolated fixtures for persistence, filesystem,
and component behavior. For UI, test the view-model/presenter directly where
possible; use the repository's UI test stack for rendered behavior. Use
[`ux-accessibility-review`](../ux-accessibility-review/SKILL.md) for rendered
review and [`playwright-e2e`](../playwright-e2e/SKILL.md) only for checked-in
browser tests.

## Fixtures, Doubles, And Determinism

- Use explicit clocks, seeded randomness, isolated databases/filesystems, and
  cleanup owned by each test. Avoid shared process globals and order dependence.
- Double external boundaries by behavior, not private calls. Use Delphi-Mocks
  (`TMock<T>`, `TMockRepository`, `WillReturn`, `WillExecute`, `When`) or Spring4D
  mocking (`Mock<T>`, `Mock.Return`, `Mock.Receive`, `Mock.Verify`) when the
  repository already uses them; do not add a mocking library for a small project
  that hand-written fakes serve.
- Keep fixtures minimal and readable.

## Compatibility And Migration Tests

When support metadata promises multiple compilers, dialects, or platforms, run
compatible lanes for each claimed range. Add focused tests only for an observable
compatibility contract; do not treat a successful compile as behavioral proof.

## Command Strategy

Prefer the narrow configured command that covers the changed contract, then the
repository's required quality lane. Compilation is not behavioral proof. Run
formatters and static analyzers when configured; do not invent universal
commands. Adaptable examples only: a targeted DUnitX `--fixture`/`--testcase`
run, a DUnit test project build, or an fpcunit `--suite`/`--testcase` run; do not
assume any of these commands exists.

## Review Checklist

- Does each test defend a behavior, boundary, invariant, transition, precedence,
  or real error?
- Is the selected framework/config actually installed and repository-owned?
- Are deterministic inputs, cleanup, and external service ownership explicit?
- Is compatibility evidence proportional to declared support?

## Anti-Patterns

Avoid tests that assert private plumbing, shared global state, random timing,
ambient services, broad mocks, and compile/static-analysis success claimed as
product verification.

## Successful Use

Report discovered tools, test level chosen, commands run, covered behavior, and
unavailable service or compatibility evidence.
