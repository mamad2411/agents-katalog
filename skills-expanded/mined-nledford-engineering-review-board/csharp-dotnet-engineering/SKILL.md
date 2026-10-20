---
name: csharp-dotnet-engineering
description: C# and .NET engineering guidance. Use when adding, changing, reviewing, testing, packaging, restoring, building, publishing, or refactoring C# source, SDK-style .csproj projects, Directory.Build.props/targets, global.json, .sln/.slnx solutions, MSBuild, NuGet PackageReference, ASP.NET Core, Blazor, EF Core, or .NET test projects. Do not use for database-native schema/query design, general WebAssembly host/guest/runtime decisions, checked-in CI/release-provider configuration, Docker/OCI/Compose configuration, or a public API contract; use the owning SQL, WebAssembly, CI/release, container, or API skill instead.
---

# C# and .NET Engineering

Use this skill for project-neutral C# implementation and the .NET SDK, MSBuild,
NuGet, ASP.NET Core, EF Core, and testing mechanics that its target repository
actually uses. Inspect the repository before selecting an SDK, project SDK,
test platform, framework, package source, command, or template.

## Current Official Evidence Baseline

This is a dated research baseline, not a target-repository support declaration.
All sources below are official Microsoft product documentation or policy and
were retrieved **2026-08-01 UTC**. A source's documentation page is authoritative
only for the scope shown; the target repository's pins and its supported target
environment decide applicability. Do not treat an undocumented combination as
supported.

| Area and citation | Source authority | Exact version, revision, and status recorded | Uncertainty and required target evidence |
| --- | --- | --- | --- |
| [.NET and .NET Core Support Policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core) | Microsoft .NET official support policy | As retrieved: **.NET 10.0.10**, LTS, Active, support ends 2028-11-14; **.NET 9.0.18**, STS, Maintenance, support ends 2026-11-10; **.NET 8.0.29**, LTS, Maintenance, support ends 2026-11-10. LTS receives three years of support; STS receives two; supported installations must stay current on patches. | Patch and lifecycle data are a point-in-time policy snapshot. Confirm the current policy and the repository TFM/runtime deployment before claiming support. |
| [What's new in C# 14](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14) and [configure language version](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/configure-language-version) | Microsoft Learn C# language documentation | C# **14** is documented as the latest released C# version and supported on **.NET 10**. The language-version article applies to **.NET 5 and later**; `preview` selects the compiler's available preview, while `latest` is machine-dependent and warned against for reliable builds. | The C# feature page does not publish a separate language support lifecycle or source revision. Treat C# 14 as released, not a license to use it on another TFM; inspect `TargetFramework`, SDK/compiler, and `LangVersion`. Public-preview pages/features remain preview unless their exact page says otherwise. |
| [.NET CLI overview](https://learn.microsoft.com/en-us/dotnet/core/tools/) and [global.json overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) | Microsoft Learn .NET CLI documentation | CLI overview applies to **.NET Core 3.1 SDK and later**. Without `global.json`, the CLI selects the latest installed SDK; `global.json` requires a full SDK version and its `allowPrerelease` behavior is explicit. The cited current example uses **10.0.100** with `latestFeature`; that is an example, not a default. | No exact SDK is implied. Resolve `global.json`, ancestor-directory lookup, CI setup, installed SDK evidence, and `rollForward` before choosing a command or claiming a feature exists. Preview SDK use is unresolved unless `allowPrerelease`, the exact SDK, and repository policy permit it. |
| [MSBuild overview](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild?view=vs-2022) | Microsoft Learn MSBuild documentation, Visual Studio 2022 view | Applies to the **Visual Studio 2022** documentation view; VS 2022 uses 64-bit MSBuild. For .NET Core and .NET 5+, `dotnet build` is documented as the SDK-provided MSBuild wrapper. | MSBuild/Visual Studio build-engine versions are not interchangeable merely because project XML parses. Inspect SDK pin, Visual Studio requirement, imports, custom targets, and target OS; no preview status is asserted by this overview. |
| [.NET project SDK overview](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview) | Microsoft Learn .NET SDK documentation | Current SDK-style project guidance documents `Microsoft.NET.Sdk`, `.Web`, `.Razor`, `.BlazorWebAssembly`, `.Worker`, and other project SDK identifiers. A project SDK supplies MSBuild targets/tasks; non-base SDKs build on the .NET SDK. | The page does not establish a universal SDK/package revision or support matrix. Derive `Sdk`, `TargetFramework(s)`, imports, workload, and custom build behavior from the project and lock/pin evidence. |
| [`dotnet sln`](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-sln) | Microsoft Learn .NET CLI command reference | Applies to **.NET 6 SDK and later**. `dotnet new sln` creates `.slnx` in .NET 10; it creates `.sln` in .NET 9 and earlier. `.slnf` support in `list` was added in SDK **9.0.3xx**. These are released command semantics, not preview claims. | Solution-file format and command availability are version-sensitive. Preserve the existing solution format and verify the repository SDK before creating, migrating, or scripting `.slnx` behavior. |
| [What is NuGet?](https://learn.microsoft.com/en-us/nuget/what-is-nuget) and [PackageReference in project files](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files) | Microsoft Learn NuGet documentation | `PackageReference` is the default for .NET/.NET Standard projects; its cited support begins with **NuGet 4.0+, Visual Studio 2017, and .NET Core 2.0**. Package versions and transitive dependencies resolve at restore; `NuGet.Config` sources still apply. | These are package-management semantics, not approval of any package, source, version, or floating version. Inspect `NuGet.Config`, lock/central-package-management files, restore policy, source mapping, and target compatibility. Package prerelease status comes from the exact package version, not this documentation. |
| [What's new in ASP.NET Core in .NET 10](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-10.0?view=aspnetcore-10.0) | Microsoft Learn ASP.NET Core release notes | **ASP.NET Core in .NET 10** release notes; its lifecycle follows the .NET 10 LTS policy recorded above. It documents released .NET 10 framework behavior, including Blazor changes. | Framework feature availability is TFM- and hosting-model-sensitive. Inspect the project SDK, TFM, packages, hosting/runtime model, and target server/browser; do not apply a .NET 10 feature to .NET 8/9 without exact evidence. |
| [What's new in EF Core 10](https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-10.0/whatsnew) and [EF Core overview](https://learn.microsoft.com/en-us/ef/core/) | Microsoft Learn EF Core documentation | **EF Core 10.0 (EF10)** was released November 2025, is **LTS**, supported until **2028-11-10**, and requires the **.NET 10 SDK** to build and **.NET 10 runtime** to run; it does not run on earlier .NET or .NET Framework. | Provider, database-server, migration, and query behavior are not generalized by EF's version support. Inspect the provider/package versions and use the matching SQL skill for database-native behavior. |
| [Testing in .NET](https://learn.microsoft.com/en-us/dotnet/core/testing/) | Microsoft Learn .NET testing documentation | Current conceptual testing documentation: unit tests exclude infrastructure; integration tests exercise component integration and may include infrastructure. It distinguishes VSTest from Microsoft.Testing.Platform and lists MSTest, NUnit, TUnit, and xUnit.net as frameworks. The page declares no single product revision or preview/stable state. | Test platform/framework support is unresolved until the repository's test SDK, adapter/framework versions, runner command, and CI are inspected. Do not assume a framework migration or that `dotnet test` alone proves a target matrix. |
| [ASP.NET Core Blazor](https://learn.microsoft.com/en-us/aspnet/core/blazor/?view=aspnetcore-10.0) and [host and deploy Blazor WebAssembly](https://learn.microsoft.com/en-us/aspnet/core/blazor/host-and-deploy/webassembly?view=aspnetcore-10.0) | Microsoft Learn ASP.NET Core/Blazor documentation | Requested **ASP.NET Core 10.0** view for C#/Razor component and Blazor WebAssembly mechanics. Blazor components are C# classes commonly expressed in `.razor` files; the WebAssembly hosting document describes browser download/execution. | Retrieval returned a stale-version warning despite the requested `aspnetcore-10.0` view, so this row is **unresolved for support/lifecycle claims**. Confirm the rendered version selector and exact target/browser documentation before relying on it. General Wasm artifact, host/guest, ABI, runtime, capability, package, and deployment decisions belong to `webassembly-engineering`. |

The table intentionally records uncertainty rather than fabricating a document
revision when a Microsoft Learn page exposes no immutable revision. Re-retrieve
the exact official page for a later decision, especially after an SDK/framework
release or when the target uses a preview feed, SDK, workload, package, or
framework.

No SDK, workload, template, tool, package, restore, build, or test was installed
or executed to establish this baseline.

## Scope and Routing

Use this skill for C# source, compiler/language settings, .NET project and
solution layout, SDK/MSBuild mechanics, NuGet workflow, ASP.NET Core/Blazor
implementation, EF Core adapter mechanics, and .NET test implementation.

- Use [`api-design`](../api-design/SKILL.md) when an HTTP, RPC, SDK, CLI,
  event, serialization, versioning, or error contract is being designed or
  changed; keep C# handlers and types here.
- Use [`sql-engineering`](../sql-engineering/SKILL.md) plus the matching engine
  skill for database-native schema, query, transaction, index, privilege, RLS,
  migration, or plan behavior. This skill owns EF Core/C# adapter mechanics, not
  database semantics.
- Use [`webassembly-engineering`](../webassembly-engineering/SKILL.md) for a
  general Wasm artifact, WASI/WIT, Component Model, host/guest ABI, runtime,
  capability, packaging, or deployment decision. Keep C#, Razor, Blazor, SDK,
  and test mechanics here; do not duplicate the Wasm host/runtime owner.
- Use [`ci-release-engineering`](../ci-release-engineering/SKILL.md) for
   checked-in hosted workflow/release behavior and
   [`container-engineering`](../container-engineering/SKILL.md) for Docker/OCI or
   Compose behavior. This skill owns the C# commands those workflows invoke.
- Use [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md),
  [`security-review`](../security-review/SKILL.md), and
  [`security-review-evidence`](../security-review-evidence/SKILL.md) before
  executing an input that can restore, load, generate, compile, or run
  third-party code. The required pre-execution gate is defined below; this skill
  owns only the .NET mechanics after the gate is satisfied.
- Use [`parallelism-engineering`](../parallelism-engineering/SKILL.md) when
  CPU-bound partitioning, worker bounds, reductions, cancellation across workers,
  or oversubscription is the design problem. Keep ordinary C# `async` I/O,
  `Task` lifetime, and framework mechanics here.
- Use [`observability-engineering`](../observability-engineering/SKILL.md) for
  telemetry semantics, correlation, metrics, traces, dashboards, alerts, or SLOs;
  keep .NET logging and instrumentation implementation mechanics here.
- Use [`mcp-server-engineering`](../mcp-server-engineering/SKILL.md) for MCP
  protocol, transport, tool/resource/prompt, and capability-contract work. Keep
  the C# SDK, hosting, and test implementation mechanics here.
- Use [`playwright-e2e`](../playwright-e2e/SKILL.md) for checked-in browser E2E
   test design, [`css-scss-styling`](../css-scss-styling/SKILL.md) for stylesheet
   decisions, [`test-driven-development`](../test-driven-development/SKILL.md)
   for implementation-driving regression tests,
   [`testing-strategy`](../testing-strategy/SKILL.md) for a test-suite audit or
   plan, and [`documentation-engineering`](../documentation-engineering/SKILL.md)
   for reader-facing docs after behavior is settled.

## MCP SDK Composition

For MCP implementation, load
[`mcp-server-engineering`](../mcp-server-engineering/SKILL.md) and its dated
[SDK selection record](../mcp-server-engineering/references/sdk-selection.md).
The selection record is the canonical source for the selected C# lane's
retrieval-time authority, package/version, tier, core-revision, transport, and
conformance caveats. It is not a target-repository pin or local test result.

## MCP .NET Mechanics

Use this section only after loading
[`mcp-server-engineering`](../mcp-server-engineering/SKILL.md) and its dated
[SDK selection record](../mcp-server-engineering/references/sdk-selection.md).
Those sources own the selected MCP revision, capability contract, and transport
rules; this section owns only .NET package and implementation mechanics.

- **Discover and resolve packages:** inspect `Directory.Packages.props`, every
  `PackageReference`, `packages.lock.json`, `NuGet.Config`, target frameworks,
  and CI restore policy. Select the resolved `ModelContextProtocol` SDK surface
  and any hosting/ASP.NET Core companion package from the target's compatible
  package graph and the resolved-version API docs. Keep related SDK packages in
  the versions the repository resolves; do not infer compatibility from the
  dated record or add a package solely to try an example.
- **Compose server and client wiring at the edge:** register the SDK server,
  handlers, dependencies, and serializers through the target's existing generic
  host, DI container, or ASP.NET Core composition root. Keep tool/resource/prompt
  application operations as ordinary typed services; let a thin SDK adapter map
  requests and results. For clients, construct the SDK client with the selected
  transport in a scoped factory/service rather than exposing transport/session
  objects through domain APIs.
- **Integrate the selected transport idiomatically:** bind a local adapter to
  the application's console/process lifetime, or a remote adapter to the
  repository's ASP.NET Core pipeline and endpoint configuration. Do not recreate
  protocol framing, discovery, or transport policy in handlers; obtain those
  behaviors from the parent skill and selected SDK. Thread request-abort and
  host-stopping cancellation tokens through owned work.
- **Use types as the schema boundary:** model SDK inputs and structured outputs
  as explicit C# records/classes with nullable and serialization policy made
  visible. Use the resolved SDK's supported schema derivation/generation path,
  then test representative valid and invalid payloads plus structured-output
  serialization. C# type checking or a generated schema alone does not validate
  untrusted runtime input.
- **Make ownership and shutdown explicit:** make each SDK client, server
  connection, stream, and transport adapter have one owner. Use the target's
  host lifetime, `CancellationToken`, `IAsyncDisposable`, and `await using`
  conventions; await cleanup in the composition layer and do not dispose
  container-owned services from handlers. Verify the selected SDK's close and
  disposal APIs instead of assuming a host stop closes every resource.
- **Test at .NET boundaries:** use the repository's configured test platform and
  framework. Unit-test typed handlers with fakes at application boundaries;
  integration-test the resolved SDK adapter, schema conversion, cancellation,
  and cleanup with an SDK-supported local/in-memory fixture when available.
  Exercise a real selected transport only in an authorized repository test lane;
  the parent MCP skill defines the protocol scenarios that fixture must cover.

## Repository-First Workflow

1. Inspect `global.json`; `*.sln`, `*.slnx`, and solution filters; every project
   and its `Sdk`/imports; `Directory.Build.props`, `Directory.Build.targets`,
   `Directory.Packages.props`, and other imported props/targets; `NuGet.Config`,
   package lock/central-package files, and local tool manifest; `.editorconfig`,
   analyzer/global-config files, `*.runsettings`, source generators, CI, README/
   AGENTS guidance, and test projects. Record the selected SDK and
   `rollForward`; TFM(s), runtime identifier(s), `LangVersion`, nullable policy,
   warning/analyzer/format policy; project SDK and build graph; package sources
   and central/locked package policy; test platform/framework; and existing
   format, restore, build, test, pack, and publish commands.
2. Classify the change: C# behavior, build/project graph, dependency, public
   contract, ASP.NET Core endpoint/pipeline, Razor/Blazor component, EF adapter,
   database behavior, test, or deployment. Load only the companion skills whose
   boundary the evidence reaches.
3. Derive commands from target evidence. Prefer its documented recipe, checked-in
   scripts, CI command, and pinned SDK. If none exists, select only a CLI command
   available in the resolved SDK and state the assumption. Never turn the baseline
   examples or a newest SDK into a repository mandate.
4. Complete the pre-execution provenance gate before a command can restore,
   load, generate, compile, or execute external inputs. Then specify behavior
   and edge cases before editing. Use
   [`test-driven-development`](../test-driven-development/SKILL.md) for focused
   behavior/regression work and
   [`behavior-driven-development`](../behavior-driven-development/SKILL.md) for
   user-visible workflows.
5. Keep domain policy independent of ASP.NET Core, EF Core, transport, persistence,
   and UI details unless the project intentionally makes the code an adapter. Load
   the appropriate architecture skill when that boundary is the design problem.
6. After the gate, run the narrowest repository-approved format, restore, build,
   test, migration, pack, publish, or target-environment check first, then the
   broader applicable lane. Report commands not run and the version-sensitive
   reason; do not claim a framework, browser, database, or CI matrix from a local
   result.

## Executable Input and Provenance Gate

Treat the following as executable supply-chain inputs, even when their extension
or purpose suggests configuration rather than code:

- an SDK selected by `global.json`, project SDK, MSBuild import, custom
  `.props`/`.targets`, task assembly, build hook, package restore hook, or
  repository template;
- every NuGet package, feed, package source mapping, lock/restore graph, and
  package-provided build target/task;
- analyzer, compiler extension, source generator, test adapter, template,
  workload, `dotnet` tool, local tool manifest entry, and generator output whose
  source is not already trusted; and
- any invocation of `dotnet restore`, `build`, `test`, `format`, `pack`,
  `publish`, `new`, `workload`, `tool`, a custom `dotnet` command, or direct
  MSBuild that can cause one of those inputs to be restored, loaded, generated,
  compiled, or executed.

Before executing any such surface, load
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md),
[`security-review`](../security-review/SKILL.md), and
[`security-review-evidence`](../security-review-evidence/SKILL.md). Establish
the applicable package/tool/template/workload/import identity, version or digest,
publisher and registry/feed, lock/source mapping, transitive and build-time
effects, and repository approval policy. Perform the security review and retain
only sanitized evidence. A lockfile, cache, signature, or previous successful
build is evidence to assess, not permission to execute. If provenance or policy
is unresolved, do not run the command; report the blocked input and missing
evidence instead. Static inspection that does not load or execute these inputs is
not a substitute for the gate, but may establish what needs review.

## Version and Project Rules

- Treat the TFM, SDK selection, runtime/deployment target, and package graph as a
  compatibility set. A compiler accepting syntax does not prove the target
  runtime, reference assemblies, framework libraries, provider, browser, or host
  supports it.
- Let the target framework select the normal C# language version. Do not set
  `LangVersion` to `latest`; use `preview` only when the target explicitly needs
  a preview and its SDK, CI, deployment, and support policy allow it. Record that
  preview status in the change and test it with the exact selected SDK.
- Do not silently create, remove, or change `global.json`, `rollForward`, solution
  format, project SDK, workload, TFM, runtime identifier, source generator, or
  build import. These alter build selection or graph behavior.
- Preserve SDK-style/MSBuild structure and existing property/item/target policy.
   Avoid overriding imported defaults or using broad `Directory.Build.*` changes
   for a local concern without proving their affected project set.
- Use the repository's existing NuGet source, central version, lock, restore, and
  package-reference conventions. A package change is both a compatibility and
  supply-chain change; do not hand-edit generated restore assets or lock data.
- Preserve the repository's solution extension. In particular, do not infer that
   `.slnx` automation is valid on .NET 9 or earlier from .NET 10 documentation.
- Treat nullable annotations, warning levels, analyzers, editor configuration,
  and formatter settings as part of the compilation contract. Follow the
  repository's configured diagnostic policy rather than suppressing warnings or
  introducing an analyzer/formatter as a local preference.
- Select restore/build/test/format/pack/publish mechanics from checked-in scripts,
  CI, and the resolved SDK. Do not assume a command's default configuration,
  solution selection, runtime identifier, test runner, package output, or
  reproducibility option; record each explicitly when it matters.

## C# and Framework Implementation Checks

- Make nullability, ownership/disposal, cancellation, async completion, exception
   mapping, culture/time handling, and serialization behavior explicit at public
   and external boundaries. Do not use nullable suppression or broad exception
   catches to hide an unmodeled state.
- Make the owner of every `IDisposable`, `IAsyncDisposable`, stream, response,
  cancellation registration, timer, and scope clear. The code that creates or
  explicitly takes ownership performs the matching cleanup; do not dispose an
  injected/shared dependency. Use `await using` when asynchronous disposal is
  required and preserve cancellation and exceptions rather than fire-and-forget
  work across a request, scope, or process boundary.
- Model expected failures with types, result/error paths, and boundary-specific
  exception translation. Preserve diagnostic context without exposing internal or
  sensitive details; use security review for a trust-boundary error surface.
- Keep services, handlers, controllers, Razor components, `DbContext`, entities,
   and provider APIs at their intended adapter/framework boundary. Avoid leaking
   them into domain contracts without an explicit architecture decision.
- For ASP.NET Core, derive middleware order, DI lifetime, configuration binding,
   authentication/authorization, endpoint behavior, environment handling, and
   server hosting/deployment from the target application and framework version.
   Validate options at the boundary, avoid singleton capture of scoped services,
   and keep middleware/request scopes and cancellation flow intentional. Use
  [`security-review`](../security-review/SKILL.md) and
  [`security-review-evidence`](../security-review-evidence/SKILL.md) for auth,
  sessions, cookies, CORS/CSRF/CSP, secrets, file paths/uploads, redirects,
  command execution, or another trust boundary.
- For EF Core, select provider APIs and migrations using the exact EF/runtime and
   database versions. Treat `DbContext` as a short-lived unit-of-work; choose
   tracking, projections, loading, transaction, concurrency, and query execution
   deliberately. Test queries and migrations against a representative provider;
   an in-memory substitute is not evidence of relational/database behavior. Route
   migration SQL, schema, index, transaction, privilege, RLS, and query-plan
   decisions to the matching SQL owner.
- For Blazor, keep Razor/C# component, rendering, DI, JS-interop, and test
  mechanics here. Treat browser support, download delivery, capabilities, Wasm
  runtime/ABI, and packaging as separate evidence questions under
  `webassembly-engineering`.

## Dependencies, Testing, and Validation

- Match tests to the configured platform and framework; the test framework and
  test platform are distinct decisions. Cover pure C# behavior narrowly, use
  integration tests for framework/database/filesystem/network wiring, and use
  target-environment tests for browser, provider, and deployment claims.
- Prefer behavior-focused tests at the smallest useful boundary. Make fixtures and
  builders express domain intent; avoid tests coupled to private implementation,
  broad mocks that restate framework behavior, order-dependent shared state, or
  an in-memory EF substitute standing in for provider behavior. Use a test double
  only at a genuine boundary and assert externally meaningful outcomes.
- Keep tests deterministic: control clocks, randomness, environment, ports,
  temporary paths, global static state, parallel execution, and external services.
  Use [`random-data-identifiers`](../random-data-identifiers/SKILL.md) for an ID,
  token, nonce, random fixture, or seeded test-data decision.
- Treat a passed local command as evidence only for its resolved SDK, TFM,
  platform, packages, configuration, and test selection. Report those limits and
  all skipped lanes.

## Anti-Patterns

- Hard-coding the current baseline's .NET 10/C# 14 commands, project SDKs, or
  framework features without target-repository evidence.
- Calling a preview SDK, package, compiler feature, template, or workload stable
   because a nearby released framework is LTS.
- Assuming `dotnet build`, an IDE build, and a custom MSBuild invocation resolve
  the same SDK, imports, properties, or solution context.
- Treating a successful EF Core in-memory test as proof of provider SQL, migration,
  transaction, collation, concurrency, or performance behavior.
- Treating Blazor WebAssembly implementation as proof of a general Wasm host,
  runtime, capability, ABI, browser, or packaging claim.
- Installing an SDK, workload, template, tool, or package merely to discover a
   command. Inspect repository pins and current official documentation first.
- Running restore, build, test, format, pack, publish, template, workload, tool,
  analyzer, generator, or imported MSBuild work before the executable-input
  provenance gate has completed.
- Hiding ownership, nullability, cancellation, or failure behavior with
  null-forgiving operators, unbounded background tasks, broad exception catches,
  service-location, or a long-lived/shared `DbContext`.

## Successful Use

Report the changed C#/project/framework surface; selected SDK, TFM, language and
framework/package versions; preview/LTS/STS or unresolved-support status; commands
and test results; dependency/source or security-review status where applicable;
and any unverified target, provider, browser, or CI compatibility.

## TypeScript Zod Interoperability

For a real TypeScript/backend JSON crossing, load [`zod-engineering`](../zod-engineering/SKILL.md). .NET independently validates/maps wire DTOs and safe errors; test shared malformed/null/unknown/number/date fixtures.
