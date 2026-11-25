---
name: dotnet-architecture-enforcement
description: >-
  Enforce repository-owned .NET architecture with ArchUnitNET. Use when an existing .NET test project needs
  assembly and namespace dependency rules, forbidden references, architecture review, or CI enforcement. Trigger
  for ArchUnitNET, architecture tests, namespace layering, forbidden dependencies, assembly selection, or .NET
  dependency direction questions. Keep the repository's current test/build/runtime choices.
metadata:
  version: 1.0.0
  tool: ArchUnitNET
allowed-tools: Read, Glob, Grep, Bash
---

# .NET architecture enforcement

Use ArchUnitNET from an ordinary existing test project. Do not create a special four-layer directory structure,
upgrade the runtime, or install arbitrary packages just to satisfy an architecture rule. The repository owns the
architecture vocabulary, assembly selection, and failure policy.

## Workflow

1. **Discover the existing test boundary.** Find the solution, production projects, target frameworks, test runner,
   and current package references. Pin the ArchUnitNET package version explicitly before installation or restore, and
   obtain approval before installing it. Reuse an existing test project and target its current Debug build output unless
   the repository already uses another configuration. Report missing package/project dependencies as setup errors.
2. **Separate actual from proposed architecture.** Inspect real namespaces, references, and compiled assemblies before
   writing rules. A proposed rule describes desired direction; it does not prove the current code follows it.
3. **Select assemblies deliberately.** Load only the repository's intended compiled assemblies. Assert that the
   assembly selection and each rule selector are nonempty and name the expected production assembly or namespace.
   An empty selection is a failing setup, never a passing architecture test.
4. **Write repository-owned tests.** Keep rules close to the existing test conventions. Use real allowed and
   forbidden examples: an allowed namespace dependency that should remain valid, and a forbidden dependency that
   fails when introduced. Keep the forbidden assertion active, not skipped or inverted to match current debt.
5. **Run the narrowest real gate.** Build the existing project in Debug, run its architecture test through the normal
   test runner, then run behavior tests for authorization and writes when the change touches those paths.
6. **Report limits.** Record selected assembly names, test command, target framework, ArchUnitNET version already
   resolved by the project, and any generated/reflection limitations. Report target-repository evidence generically and do
   not infer rollout success from a local run.

## Rule contract

- Rules describe repository-owned boundaries, not a universal layering recipe.
- Assembly and namespace selectors must be nonempty and explain what they selected.
- Detect missing project/package dependencies before interpreting rule failures.
- Never weaken a rule, skip a failing forbidden example, or widen a selector merely to obtain green tests.
- Architecture tests do not establish authorization correctness, persistence correctness, or runtime behavior.
  Add focused behavior tests for writes and authorization alongside the architecture test.
- Use the existing Debug build and runtime. Do not require an arbitrary SDK/runtime upgrade or global installation.

## Documented API shape

Use ArchUnitNET's documented loading and rule flow, adapting names to the package version already resolved by the
existing test project:

```csharp
var architecture = new ArchLoader()
    .LoadAssemblies(productionAssembly)
    .Build();

var webTypes = architecture.Types()
    .That().ResideInAssembly(webAssembly)
    .Should().NotDependOnAny(persistenceAssembly)
    .Because("web code must use the service boundary");

webTypes.Check(architecture);
```

Before checking the rule, verify through the compiled ArchUnitNET API that the assembly and namespace selectors are
nonempty. If the resolved version does not expose a stable selector-count API, inspect the selected objects with the
project's documented API or add a test-visible diagnostic. Treat an empty selector as setup failure. Do not invent
`Architecture.GetAssemblies()`, `ShouldNotBeEmpty()`, or `ShouldNotDependOnAny()` calls.
