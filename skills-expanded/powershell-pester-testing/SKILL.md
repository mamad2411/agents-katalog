---
name: powershell-pester-testing
description: Help with Pester test work in PowerShell repositories, including detecting Pester v4/v5/v6 usage, matching an existing test style, writing focused tests for functions, scripts, and modules, handling Discovery vs Run phase issues, using Mock and Should -Invoke carefully, isolating file system or registry tests with TestDrive/TestRegistry, running Invoke-Pester locally or in CI, producing coverage or test reports, and iterating from failures without broad unrelated rewrites.
---

# Pester

Use this skill for PowerShell test work with Pester. Prefer the target repository's existing test conventions over any generic example here.

## Workflow

1. Inspect before editing.
   - Find existing tests with `*.Tests.ps1`.
   - Check `RequiredModules`, module manifests, build scripts, `psake`, `Invoke-Build`, `build.ps1`, CI workflows, and dependency setup for a pinned Pester version.
   - Identify whether tests are unit, integration, smoke, acceptance, or mixed.
   - Match existing file placement, naming, tags, assertion style, setup helpers, and command wrappers.
   - Do not migrate Pester v4 tests to v5/v6 style unless asked or required by the task.

2. Choose the smallest useful test.
   - Test observable behavior rather than private implementation details.
   - Add coverage near the requested change first.
   - Keep fixtures and setup close to the tests that need them unless the repo already has shared helpers.
   - Add regression tests for fixed bugs before or alongside the fix.

3. Respect Pester's execution model.
   - Use `Describe` for the unit or behavior under test.
   - Use `Context` only when it clarifies distinct conditions.
   - Use `BeforeAll` for expensive or shared setup.
   - Use `BeforeEach` for per-test state.
   - Use `AfterEach` and `AfterAll` for cleanup that must run even when a test fails.
   - Use `It` names that describe expected behavior.
   - In Pester v5+, put executable test setup inside `It`, `BeforeAll`, `BeforeEach`, `AfterEach`, `AfterAll`, or `BeforeDiscovery`.
   - Use `BeforeDiscovery` when dynamically generating tests or test cases.

4. Mock boundaries, not the design.
   - Mock external boundaries such as file system access, network calls, time, command invocation, native executables, cloud services, or slow dependencies.
   - Avoid mocking the function under test or duplicating its implementation in the mock.
   - Prefer asserting outputs, state changes, and important command calls over every internal step.
   - Use `-ParameterFilter` when the same command has different expected behavior for different inputs.
   - Use `Should -Invoke` in Pester v5+; preserve `Assert-MockCalled` only when maintaining older style.
   - For module internals, prefer testing exported commands. Use `-ModuleName` or `InModuleScope` only when private behavior is intentionally under test.

5. Isolate side effects.
   - Use `TestDrive:` for temporary files and directories.
   - Use `TestRegistry:` only for Windows registry tests and only when the target environment supports it.
   - Save and restore environment variables, preferences, current location, and module state that a test changes.
   - Avoid tests that depend on execution order.

6. Run tests and iterate from failures.
   - Use the repository's existing test command when one exists.
   - Otherwise run `Invoke-Pester` with the narrowest relevant path, tag, or name filter first.
   - Read failure messages before changing code.
   - Fix either the test or implementation based on the behavior the project should have.
   - Broaden to the full relevant suite before finishing.

## Version Discovery

```powershell
Get-Module Pester -ListAvailable | Sort-Object Version -Descending
Get-Module Pester
Get-Command Invoke-Pester -Module Pester -ErrorAction SilentlyContinue
```

When exact syntax matters, prefer the repository's pinned version and official Pester docs for that version.

## Common Commands

Run all tests:

```powershell
Invoke-Pester
```

Run a specific test file:

```powershell
Invoke-Pester -Path ./tests/MyCommand.Tests.ps1
```

Run detailed output:

```powershell
Invoke-Pester -Path ./tests/MyCommand.Tests.ps1 -Output Detailed
```

Run by tag or full name:

```powershell
Invoke-Pester -TagFilter Unit -ExcludeTagFilter Slow
Invoke-Pester -FullNameFilter '*Get-Widget*returns*'
```

Generate CI-friendly results with Pester configuration:

```powershell
$config = New-PesterConfiguration
$config.Run.Path = './tests'
$config.Run.Exit = $true
$config.Output.Verbosity = 'Detailed'
$config.TestResult.Enabled = $true
$config.TestResult.OutputFormat = 'JUnitXml'
$config.TestResult.OutputPath = 'test-results.xml'
Invoke-Pester -Configuration $config
```

Enable coverage when the project expects it:

```powershell
$config = New-PesterConfiguration
$config.Run.Path = './tests'
$config.CodeCoverage.Enabled = $true
$config.CodeCoverage.Path = './src'
$config.CodeCoverage.OutputFormat = 'JaCoCo'
$config.CodeCoverage.OutputPath = 'coverage.xml'
Invoke-Pester -Configuration $config
```

## Examples

Use bundled examples only as starting points:

- `examples/simple-function.Tests.ps1`: testing a pure function.
- `examples/module-command.Tests.ps1`: testing an exported module command.
- `examples/mocking.Tests.ps1`: mocking a boundary command.
- `examples/testdrive.Tests.ps1`: isolating file system behavior.
- `examples/ci-configuration.ps1`: creating a Pester configuration object for CI.

## Anti-Patterns

- Executing setup code at the top level of a Pester v5+ test file when it belongs in `BeforeAll` or `BeforeDiscovery`.
- Rewriting the project's entire test layout while adding one focused test.
- Mocking the command being tested.
- Overspecifying every internal call instead of checking behavior.
- Sharing mutable state between tests without resetting it.
- Using global environment, registry, or file system state when `TestDrive:`, `TestRegistry:`, or explicit cleanup would isolate the test.
- Depending on aliases, interactive prompts, machine-specific paths, or external services in unit tests.
