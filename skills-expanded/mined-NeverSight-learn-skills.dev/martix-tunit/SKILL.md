---
name: martix-tunit
description: Standalone-first TUnit guidance for project setup, awaitable assertions, data sources, lifecycle hooks, parallel execution, extensibility, and framework migration. Use when prompts mention TUnit, await Assert.That(...), dotnet run on Microsoft.Testing.Platform, TUnit attributes ([Test], [Before], [After], [Arguments]), or migrating xUnit/NUnit/MSTest tests to TUnit.
license: Complete terms in LICENSE.txt
---

# MartiX TUnit router

- Standalone-first skill package focused on TUnit-specific decisions for
  .NET 8+, C# 12+, and modern .NET test projects running on
  `Microsoft.Testing.Platform`.
- Keep decisions grounded in the bundled rule files and TUnit reference maps.
- Use [AGENTS.md](./AGENTS.md) when the task crosses multiple workstreams or
  needs the long-form review routes, package inventory, or maintainer guidance.

## When to use this skill

- Set up or configure a TUnit test project from scratch.
- Author test classes and parameterized tests using any TUnit data source.
- Design test lifecycle using `[Before]` and `[After]` hooks and shared context.
- Configure parallel execution, test ordering, retries, or inter-test dependencies.
- Write or review assertions using `await Assert.That(...)`.
- Wire up dependency injection inside TUnit tests.
- Extend TUnit with custom attributes, hooks, or `ITestRegisteredEventReceiver`.
- Migrate an existing xUnit, NUnit, or MSTest suite to TUnit.

## Out-of-scope handoffs

- Use `martix-dotnet-csharp` for broad .NET or C# language guidance that is not
  specific to TUnit test behavior.
- Use `martix-fastendpoints` for endpoint design and API pipeline concerns that
  are not test-framework routing decisions.
- Use `martix-powershell` for script automation details unrelated to TUnit
  runner, assertions, hooks, or data-source behavior.

## Critical TUnit constraints

Surface these before applying any rule. They are the most common source of
broken setups and silent test failures:

- **Unawaited assertions silently pass.** Every `Assert.That(...)` chain must
  be `await`ed. An unawaited call compiles and runs without failing.
- **`dotnet run` is the canonical execution surface.** `dotnet test` works but
  routes through a compatibility shim; TUnit-specific flags require `--`.
- **`OutputType` must be `Exe`.** The source generator provides the `Main`
  entry point; a library project breaks discovery.
- **Never add `Microsoft.NET.Test.Sdk`.** It hooks the VSTest platform and
  breaks TUnit discovery entirely.
- **Coverlet packages are incompatible.** Use TUnit's bundled code-coverage
  support instead.
- **`TUnit.Mocks` is beta and requires C# 14.** Gate all mocking guidance on
  this constraint.

## Start with the closest workstream

1. Pick the closest workstream below.
2. Read only the linked rules needed for the current change.
3. Pull reference maps in only after the core workstream is chosen.
4. Open [AGENTS.md](./AGENTS.md) for cross-workstream review routes, package
   inventory, and maintainer guidance.

## Rule library by workstream

### Foundation and project setup

- Use for package installation, NuGet references, project file configuration,
  `OutputType=Exe` shape, `Microsoft.Testing.Platform` runner wiring, source
  generator setup, IDE configuration, CLI flags, test filters, and environment
  variables.
- Rule:
  - [TUnit foundation — installation and project shape](./rules/foundation-installation-project.md)
- Map: [TUnit foundation map](./references/foundation-map.md)

### Data-driven and parameterized tests

- Use for `[Arguments]`, `[MethodDataSource]`, `[ClassDataSource]`,
  `TestDataRow`, matrix tests, combined data sources, nested sources, generic
  attributes, and custom `IDataSourceGeneratorAttribute` implementations.
- Rules:
  - [TUnit data — inline arguments and method data sources](./rules/data-inline-method-sources.md)
  - [TUnit data — class data sources, sharing, and nested sources](./rules/data-class-property-sources.md)
  - [TUnit data — matrix tests, combined data sources, and custom generators](./rules/data-matrix-combined-generators.md)
- Map: [TUnit data map](./references/data-map.md)

### Lifecycle, hooks, and dependency injection

- Use for `[Before]` and `[After]` hooks at Test, Class, Assembly, TestSession,
  and TestDiscovery scopes, `[BeforeEvery]` and `[AfterEvery]`, hook execution
  order, `IAsyncInitializer`, `IAsyncDiscoveryInitializer`, property injection,
  and DI via `IServiceProvider` or `[ClassConstructor]`.
- Rules:
  - [TUnit lifecycle hooks](./rules/lifecycle-hooks.md)
  - [TUnit property injection and initialization](./rules/lifecycle-property-injection.md)
  - [TUnit dependency injection construction](./rules/lifecycle-di.md)
- Map: [TUnit lifecycle map](./references/lifecycle-map.md)

### Assertions

- Use for `await Assert.That(...)`, the unawaited-assertion pitfall, value and
  collection assertions, exception and async delegate assertions, `.And`/`.Or`
  chains, `Assert.Multiple`, member assertions, and custom assertion
  extensibility.
- Rules:
  - [TUnit assertion fundamentals](./rules/assertions-fundamentals.md)
  - [TUnit value, collection, and async assertions](./rules/assertions-value-collection-async.md)
  - [TUnit combining and custom assertions](./rules/assertions-combining-custom.md)
- Map: [TUnit assertions map](./references/assertions-map.md)

### Parallel execution and execution control

- Use for parallel-by-default behavior, `[ParallelLimiter<T>]`, `[NotInParallel]`,
  `[DependsOn]`, test ordering, retries, repeats, timeouts, test filters,
  `[Skip]`, `[Explicit]`, CI/CD reporting, engine modes, and AOT constraints.
- Rules:
  - [TUnit parallel execution](./rules/execution-parallelism.md)
  - [TUnit execution control](./rules/execution-control.md)
- Map: [TUnit execution map](./references/execution-map.md)

### Mocking and extensibility

- Use for `TUnit.Mocks` (beta, requires C# 14), mock setup and verification,
  argument matchers, `ITestRegisteredEventReceiver`, custom test attributes,
  data source generators, argument formatters, dynamic tests, and built-in
  extension points.
- Rules:
  - [TUnit.Mocks — source-generated mocking](./rules/mocking-tunit-mocks.md)
  - [TUnit extension points](./rules/extending-extension-points.md)
- Map: [TUnit mocking and extending map](./references/mocking-extending-map.md)

### Migration and framework comparison

- Use for behavioral differences from xUnit, NUnit, and MSTest; attribute
  equivalence; class and method lifecycle mapping; assertion API differences;
  and step-by-step migration guidance.
- Rule:
  - [TUnit migration and framework comparison](./rules/migration-comparison.md)
- Reference: [TUnit migration attribute matrix](./references/migration-attribute-matrix.md)

### Advanced scenarios

- Use for ASP.NET Core integration, .NET Aspire, Playwright, complex
  infrastructure fixtures, FsCheck, OpenTelemetry, and CI pipeline examples.
  These are linked references, not rule files.
- Reference: [TUnit cookbook index](./references/cookbook-index.md)

## Package conventions

- Every rule follows the shared section contract in
  [rules/_sections.md](./rules/_sections.md): `Purpose`, `Default guidance`,
  `Avoid`, `Review checklist`, `Related files`, and `Source anchors`.
- Use [the rule template](./templates/rule-template.md) for new rules,
  [the research pack template](./templates/research-pack-template.md) for
  scoped source inventories, and
  [the comparison matrix template](./templates/comparison-matrix-template.md)
  for external comparisons.
- Use [metadata.json](./metadata.json) as the registration-ready inventory for
  entrypoints, workstream coverage, and distribution notes.
- The taxonomy and preferred ordering live in
  [assets/taxonomy.json](./assets/taxonomy.json) and
  [assets/section-order.json](./assets/section-order.json).

## Standalone-first note

- This skill is authored as a standalone package under `skills`.
- If you document or install the package directly, use
  `npx skills add <source>` rather than `npx skill add`.
- Keep TUnit-specific guidance here. Pull broader .NET guidance from
  `martix-dotnet-csharp` only when the task clearly widens beyond TUnit.
