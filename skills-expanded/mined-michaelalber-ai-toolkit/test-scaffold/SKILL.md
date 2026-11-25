---
name: test-scaffold
audience: team
description: Test generation conventions, naming patterns, mock strategies, and project structure for .NET test suites. Use when generating tests for C#/.NET projects with xUnit, FluentAssertions, and NSubstitute.
---

# Test Scaffold

> "The ratio of time spent reading versus writing code is well over 10 to 1. Tests should be the
> most readable code in the project."
> -- Robert C. Martin

## Core Philosophy

This skill provides the conventions, patterns, and structural guidance for generating .NET test
suites with xUnit, FluentAssertions, and NSubstitute: test naming, file organization, mock
strategy, the AAA (Arrange-Act-Assert) structure, and test project setup. Apply these conventions
consistently across every generated test. Tests are documentation of behavior — they must be the
most readable code in the project, isolated, deterministic, and independent of execution order.

**Non-Negotiable Constraints:**
1. AAA ALWAYS — every test follows Arrange-Act-Assert with explicit comment markers; never mix Act and Assert in one expression.
2. DESCRIPTIVE NAMING — every test name is `MethodName_Scenario_ExpectedResult`, a complete sentence describing what is tested.
3. ONE CONCEPT PER TEST — each test verifies one logical concept (multiple asserts allowed only when they verify aspects of that same concept).
4. NO INTERDEPENDENCE — tests never depend on order; each sets up its own state, runs in isolation, and cleans up.
5. MOCK ONLY WHAT YOU OWN — mock interfaces you control; for third-party libraries use their test helpers or wrap them in your own interface first.

## Workflow

```
IDENTIFY   The unit under test (handler, validator, service, endpoint, pipeline behavior) and the
           scenarios to cover: happy path, not-found, validation, exception, guard clause, edge,
           state change, side effect.

CHOOSE     The test type per scenario (decision table in references/test-patterns.md):
           unit + mocks · validator TestValidate() · WebApplicationFactory integration ·
           InMemory DbContext · mocked RequestHandlerDelegate for behaviors.

SCAFFOLD   Place the test file mirroring src/ structure (naming-conventions.md). Write each test
           AAA-structured, named MethodName_Scenario_ExpectedResult. Build data with builders;
           mock only external boundaries (mock-patterns.md); use InMemory DbContext, not a mocked one.

VERIFY     dotnet test passes; each test isolated and order-independent; no testing of private
           methods or framework code; DbContext disposed; no hardcoded GUIDs/dates.
```

**Exit criteria:** every identified scenario has an AAA-structured, correctly named, isolated test;
the right test type per scenario; mocks limited to external boundaries; `dotnet test` green.

## State Block

```
<test-scaffold-state>
phase: IDENTIFY | CHOOSE | SCAFFOLD | VERIFY | COMPLETE
unit_under_test: [class/member]
scenarios: [count identified]
tests_written: [count]
test_types: [unit | validator | integration | behavior | db]
build_status: pass | fail | not-run
last_action: [description]
next_action: [description]
</test-scaffold-state>
```

## Output Template

- **Project structure, .csproj, GlobalUsings, AAA example, data builders, InMemory factory,
  FluentValidation, WebApplicationFactory, when-to-use table, pitfalls** — `references/test-patterns.md`.
- **Mock/stub/fake patterns (repositories, mediator, HttpClient, DbContext)** — `references/mock-patterns.md`.
- **Test naming patterns, file organization, project structure conventions** — `references/naming-conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `tdd-loop` | The RED phase writes a failing test first; this skill supplies the conventions, naming, and structure those tests follow. |
| `tdd-agent` (agent) | Autonomous operating mode of the TDD loop that generates tests — it applies these scaffolding conventions. |
| `dotnet-vertical-slice` | Scaffolds the feature handlers/validators/endpoints this skill writes tests for; the test tree mirrors the slice structure. |
| `evaluate-tests` | Audits generated tests for TDD discipline and quality — run it after scaffolding to verify the suite. |
