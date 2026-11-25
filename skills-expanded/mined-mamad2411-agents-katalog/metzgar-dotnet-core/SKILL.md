---
name: metzgar-dotnet-core
description: "Knowledge base from \".NET Core in Action\" by Dustin Metzgar. Use when applying Metzgar's frameworks for .NET Core / .NET Standard, the dotnet CLI, MSBuild/.csproj, xUnit, ADO.NET/Dapper/EF Core, dependency injection, ASP.NET Core microservices, debugging (SOS), performance profiling (PerfView), i18n/localization, multi-targeting (TFM/RID), and NuGet packaging — studying the book or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# .NET Core in Action
**Author**: Dustin Metzgar (foreword by Scott Hanselman) | **Pages**: ~289 | **Chapters**: 12 + 4 appendices | **Publisher**: Manning, 2018 | **Generated**: 2026-07-03

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `dependency injection`, `multi-targeting`, `EF Core`, `SOS`, `localization`… I find and read the relevant chapter.
- **With a chapter** — ask for `ch06`; I load that file.
- **Browse** — ask "what chapters do you have?" for the index.

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering.

> ⚠️ Book is 2018 / .NET Core 1.x–2.0 era. Concepts (TFM/RID, DI, ADO.NET, EF Core, MSBuild) still hold, but APIs, tooling defaults (`csproj` PackageReference is now standard), and platform support have moved on. For current syntax, verify against today's .NET docs.

---

## Core Frameworks & Mental Models

**.NET Standard Library** — the API contract every .NET implementation honors. Code a library to `netstandard` once and it's binary-shareable across .NET Core, Framework, and Xamarin. *Rule*: libraries target `netstandard` (lowest version with your APIs); apps target `netcoreapp*`. Think of it as the USB spec of .NET.

**Framework (TFM) vs Runtime (RID)** — the book's central multi-platform distinction. A **TFM** (`netstandard2.0`, `net461`) selects the *API surface you compile against*; a **RID** (`win-x64`, `linux-x64`) selects the *OS/arch you run on*. Branch API availability with `#if <TFM>` (compile-time); branch OS behavior with `RuntimeInformation.IsOSPlatform` (runtime). RIDs are hierarchical — fall back to a broader parent if a specific one fails.

**dotnet CLI + xcopy deployment** — the CLI is the lowest-common-denominator surface (works in any editor / Docker / headless Linux). `dotnet new/build/run/test/publish/pack`. Deployment = copy a folder; `publish -r <RID> --self-contained` bundles the runtime so no machine-wide install is needed.

**MSBuild `.csproj`** — build is data: `PropertyGroup` (properties), `ItemGroup` (inputs/`PackageReference`), `Target` (ordered tasks). Multi-target with `<TargetFrameworks>` + `Condition="'$(TargetFramework)'=='net461'"` per-TFM options.

**xUnit testing** — `[Fact]` for one case; promote to `[Theory]` + `[InlineData]` when you can't prove all cases. Share setup: constructor (per test), `Dispose` (cleanup), `IClassFixture` (per class), `ICollectionFixture` (across classes). Filter with `Traits`.

**Data access spectrum** — pick by control vs boilerplate: **ADO.NET** (hand-write SQL, max control, always *parameterize* — never concatenate) → **Dapper** micro-ORM (mapping, you own the SQL) → **EF Core** full ORM (`DbContext`/`DbSet`, LINQ, migrations, code-first schema).

**Dependency Injection** — register in `IServiceCollection`, inject via constructor. Lifetimes: `Transient` (per resolve), `Scoped` (per request), `Singleton` (per app). *Rule*: shortest correct lifetime; never inject a shorter-lived service into a longer-lived one (captive dependency).

**ASP.NET Core microservice** — `Startup` class wires services + pipeline; `Kestrel` is the cross-platform server. I/O-bound work is `async`/`await` returning `Task<IActionResult>`; reuse one `HttpClient`; **never** block async with `.Result`/`.Wait()`. Externalize secrets/endpoints via `IConfiguration`.

**Measure before optimizing** — track microbenchmarks with xUnit.Performance `[Benchmark]`; capture traces with PerfView (CPU/GC/exceptions) or `perfcollect` on Linux; fix the *measured* hot path; re-measure. Profile in Release on representative data.

**Layered diagnostics** — start in the IDE debugger (VS Code `launch.json`, VS, VS for Mac); escalate to **SOS (Son of Strike)** under WinDBG/CDB (Windows) or LLDB (Linux/mac) against a self-contained app to inspect heap/stacks/exceptions.

**World-ready by default** — i18n is a *process*: swap `Console` for `Microsoft.Extensions.Logging`; extract strings to resources behind `IStringLocalizer`; persist/interchange in **invariant culture**; run a localizability review; test an RTL language. i18n ≠ globalization ≠ localization.

**Ship it** — publish a library with `.csproj` package metadata + `dotnet pack` + `dotnet nuget push`. Strong-name/delay-signing gives assembly *identity*, not tamper security.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-why-dotnet-core.md) | Why .NET Core? | .NET Standard Library, xcopy deploy, containers vs VMs |
| [ch02](chapters/ch02-first-applications.md) | Building your first apps | dotnet CLI, Kestrel, Startup, publish/Docker |
| [ch03](chapters/ch03-build-system-msbuild.md) | How to build with .NET Core | MSBuild, PropertyGroup/Target/ItemGroup, TFMs |
| [ch04](chapters/ch04-unit-testing-xunit.md) | Unit testing with xUnit | [Fact]/[Theory], fixtures, Traits |
| [ch05](chapters/ch05-relational-databases.md) | Relational databases | SQLite, ADO.NET, parameterized queries, transactions |
| [ch06](chapters/ch06-orms-dapper-efcore.md) | ORMs | Dapper, EF Core, dependency injection |
| [ch07](chapters/ch07-microservice-aspnet.md) | Creating a microservice | ASP.NET Core, HttpClient, async, Azure Blob |
| [ch08](chapters/ch08-debugging.md) | Debugging | VS Code/VS debuggers, SOS, WinDBG/LLDB |
| [ch09](chapters/ch09-performance-profiling.md) | Performance and profiling | xUnit.Performance, PerfView, perfcollect |
| [ch10](chapters/ch10-world-ready-i18n.md) | World-ready applications | Extensions.Logging, IStringLocalizer, EventSource |
| [ch11](chapters/ch11-multiple-frameworks-runtimes.md) | Multiple frameworks & runtimes | Portability Analyzer, multi-target, RID, #if |
| [ch12](chapters/ch12-preparing-for-release.md) | Preparing for release | NuGet pack, feeds, strong-name/delay-sign |

Appendices (in cheatsheet): A TFMs & RIDs · B xUnit CLI options · C .NET Standard contents by version · D NuGet cache locations.

## Topic Index

- **ADO.NET / DataReader** → ch05
- **async / await** → ch07
- **Azure Blob Storage** → ch07
- **CLI (dotnet)** → ch02, ch03
- **Containers / Docker** → ch01, ch02
- **CSV parser sample** → ch03
- **Dapper** → ch06
- **Debugging (IDE)** → ch08
- **Dependency injection / lifetimes** → ch06
- **Deployment / publish** → ch01, ch02, ch11
- **Entity Framework Core** → ch06
- **EventSource / EventListener** → ch10, ch11
- **[Fact] / [Theory] / fixtures** → ch04
- **Globalization / invariant culture** → ch10
- **HttpClient** → ch07
- **Kestrel / Startup** → ch02, ch07
- **Localization / IStringLocalizer** → ch10
- **Logging (Extensions.Logging)** → ch10
- **MSBuild / .csproj** → ch03, ch11, ch12
- **.NET Standard** → ch01, ch11, App C
- **NuGet packaging / feeds** → ch06, ch11, ch12
- **PerfView / profiling** → ch09
- **Portability Analyzer** → ch01, ch11
- **RID (runtime identifier)** → ch11, App A
- **Self-contained app** → ch02, ch08
- **Signing / strong names** → ch12
- **SOS / WinDBG / LLDB** → ch08
- **SQLite** → ch05
- **TFM / multi-targeting** → ch03, ch11, App A
- **Transactions** → ch05
- **Unit testing** → ch04, ch09
- **xUnit.Performance** → ch09

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions + chapter refs
- [patterns.md](patterns.md) — reusable techniques (targeting, DI, data access, async, profiling, packaging)
- [cheatsheet.md](cheatsheet.md) — decision rules + appendix tables (TFM/RID, DI lifetimes, ORM trade-offs, SOS/xUnit CLI, .NET Standard versions, NuGet cache)

---

## Scope & Limits

Covers the book's content (.NET Core 1.x–2.0 era, 2018). Concepts are durable; verify exact APIs/tooling against current .NET docs. For hands-on work in a specific codebase, combine with project tools. Related skills: `brownfield-dotnet` (reviving legacy .NET), `khorikov-unit-testing` / `art-of-unit-testing` (testing depth).
