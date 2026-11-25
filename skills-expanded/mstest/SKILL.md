---
name: mstest
description: "Write, run, or repair .NET tests that use MSTest. Use when a repo uses `MSTest.Sdk`, `MSTest`, `[TestClass]`, `[TestMethod]`, `DataRow`, or Microsoft.Testing.Platform-based MSTest execution. USE FOR: the repo uses MSTest; you need to add, run, debug, or repair MSTest tests; the repo is moving between VSTest and Microsoft.Testing.Platform. DO NOT USE FOR: xUnit projects; TUnit projects. INVOKES: inspect the repository context, edit targeted files, and run relevant build, test, lint, or validation commands when changes are made."
---

# MSTest

## Diagnostic Output Budget

Keep native test progress and ANSI visible; use the detected runner's supported flags (`--progress on --ansi on` for MTP/TUnit), not MTP switches on VSTest. Keep console logs at `Warning` or higher and one concise final summary. Do not replay progress redraws, successful-test output, or Information/Debug/Trace logs into model context. On failure/crash, show only the failing test/resource, root error, and relevant stack frames; deduplicate and cap each diagnostic response at 80 lines / 8 KiB. Never dump entire console/host/browser logs, HTML, TRX, or crash artifacts. Keep necessary artifacts size-bounded outside context, link them, and inspect exact bounded excerpts. Preserve the runner exit code through capture/filtering; disclose truncation. Silence alone does not establish a hang.

## Trigger On

- the repo uses MSTest
- you need to add, run, debug, or repair MSTest tests
- the repo is moving between VSTest and Microsoft.Testing.Platform

## Value

- produce a concrete project delta: code, docs, config, tests, CI, or review artifact
- reduce ambiguity through explicit planning, verification, and final validation skills
- leave reusable project context so future tasks are faster and safer

## Do Not Use For

- xUnit projects
- TUnit projects
- generic test strategy with no MSTest-specific mechanics

## Inputs

- the nearest `AGENTS.md`
- the test project file and package references
- the active MSTest runner model

## Quick Start

1. Read the nearest `AGENTS.md` and confirm scope and constraints.
2. Run this skill's `Workflow` through the `Ralph Loop` until outcomes are acceptable.
3. Return the `Required Result Format` with concrete artifacts and verification evidence.

## Workflow

1. Detect the MSTest project style first:
   - `MSTest.Sdk` project SDK
   - `MSTest` meta-package
   - legacy package set with explicit `Microsoft.NET.Test.Sdk`
2. Read the repo's real `test` command from `AGENTS.md`. If the repo has no explicit command yet, start with `dotnet test PROJECT_OR_SOLUTION`.
3. Keep the runner model consistent:
   - `MSTest.Sdk` defaults to the MSTest runner on Microsoft.Testing.Platform
   - VSTest is opt-in with `UseVSTest=true` or legacy package choices
   - do not pass VSTest-only switches or assume legacy `.runsettings` behavior on Microsoft.Testing.Platform jobs
4. Prefer `[DataRow]` or `DynamicData` for stable data-driven coverage. Keep test lifecycle hooks minimal and deterministic.
5. Keep MSTest analyzers enabled and fix findings instead of muting them casually.
6. Align coverage/reporting packages with the active runner.

## Bootstrap When Missing

If MSTest is requested but not configured:

1. Detect current framework first:
   - `rg -n "MSTest\\.Sdk|PackageReference Include=\"MSTest\"|xunit|TUnit|UseVSTest|TestingPlatformDotnetTestSupport" -g '*.csproj' .`
2. If the repo currently uses `xUnit` or `TUnit`, do not auto-migrate. Return `status: not_applicable` unless migration is explicitly requested.
3. For explicit MSTest adoption, add package(s) to target test project:
   - `dotnet add TEST_PROJECT.csproj package MSTest`
4. Document runner model (`MSTest.Sdk` default MTP vs `UseVSTest`) in `AGENTS.md`.
5. Run `dotnet test TEST_PROJECT.csproj` and return `status: configured` or `status: improved`.


## Deliver

- MSTest tests that match the repo's runner model
- commands that work in local and CI runs
- explicit guidance for VSTest versus Microsoft.Testing.Platform usage

## Validate

- the runner model is documented and consistent
- test commands match that runner
- data-driven tests stay deterministic
- analyzer, coverage, and reporting packages align with the chosen runner

## Ralph Loop

Use the Ralph Loop for every task, including docs, architecture, testing, and tooling work.

1. Plan first (mandatory):
   - analyze current state
   - define target outcome, constraints, and risks
   - write a detailed execution plan
   - list final validation skills to run at the end, with order and reason
2. Execute one planned step and produce a concrete delta.
3. Review the result and capture findings with actionable next fixes.
4. Apply fixes in small batches and rerun the relevant checks or review steps.
5. Update the plan after each iteration.
6. Repeat until outcomes are acceptable or only explicit exceptions remain.
7. If a dependency is missing, bootstrap it or return `status: not_applicable` with explicit reason and fallback path.

### Required Result Format

- `status`: `complete` | `clean` | `improved` | `configured` | `not_applicable` | `blocked`
- `plan`: concise plan and current iteration step
- `actions_taken`: concrete changes made
- `validation_skills`: final skills run, or skipped with reasons
- `verification`: commands, checks, or review evidence summary
- `remaining`: top unresolved items or `none`

For setup-only requests with no execution, return `status: configured` and exact next commands.

## Load References

- [references/mstest.md](references/mstest.md)
- [references/patterns.md](references/patterns.md)
- [references/anti-patterns.md](references/anti-patterns.md)

## Example Requests

- "Fix our MSTest runner setup."
- "Add an MSTest regression test."
- "Move this MSTest project to Microsoft.Testing.Platform safely."
