---
name: nuget-package-scaffold
audience: team
description: >
  NuGet package creation with CI/CD pipeline setup and test harness. Use when
  creating new NuGet packages, configuring package metadata, or setting up publish
  workflows. Do NOT use when the library is internal-only and not intended for
  NuGet publication; Do NOT use when the target is an application project.
---

# NuGet Package Scaffold

> "The best libraries are those that disappear into the code that uses them."
> -- Krzysztof Cwalina, Framework Design Guidelines

## Core Philosophy

This skill scaffolds production-ready NuGet packages with proper metadata, testing, CI/CD pipelines, and publish workflows. Every package must meet a quality bar before it reaches any feed.

**Non-negotiable constraints:**

1. **No publish without tests** -- a package without a passing test suite is not a package, it is a liability
2. **Semantic versioning is law** -- every version bump must communicate intent: breaking, feature, or fix
3. **Metadata is not optional** -- description, license, authors, repository URL, and README are required before first publish
4. **Multi-target when possible** -- support the broadest reasonable set of target frameworks for your consumers
5. **Deterministic builds** -- the same source must produce the same binary, every time

The full domain principles, knowledge-base lookup protocol, AI discipline rules, anti-patterns, and error-recovery procedures live in `references/conventions.md`.

## Workflow

Six-step pipeline: **Scaffold → Configure → Test → Pack → Publish** (with iterate back if needed).

### Step 1: Scaffold

Create the solution structure:

```
PackageName/
├── src/
│   └── PackageName/
│       ├── PackageName.csproj
│       └── Class1.cs
├── tests/
│   └── PackageName.Tests/
│       ├── PackageName.Tests.csproj
│       └── Class1Tests.cs
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── publish.yml
├── PackageName.sln
├── Directory.Build.props
├── README.md
├── LICENSE
└── .editorconfig
```

### Step 2: Configure .csproj Metadata

Required metadata properties checklist:

- [ ] `PackageId` -- unique identifier on the feed
- [ ] `Version` -- SemVer-compliant version string
- [ ] `Authors` -- comma-separated author names
- [ ] `Description` -- concise summary of what the package does
- [ ] `PackageLicenseExpression` -- SPDX license identifier (e.g., MIT, Apache-2.0)
- [ ] `PackageProjectUrl` -- link to the project repository
- [ ] `RepositoryUrl` -- source repository URL
- [ ] `RepositoryType` -- typically `git`
- [ ] `PackageReadmeFile` -- path to the README to embed in the package
- [ ] `PackageTags` -- space-separated discovery tags
- [ ] `TargetFrameworks` -- semicolon-separated TFMs

Multi-target decision: `TargetFrameworks: netstandard2.0;net10.0` when pre-.NET 10 consumers need support; `TargetFrameworks: net10.0` otherwise. Full property reference: `references/csproj-metadata.md`.

### Step 3: Test

```bash
dotnet test --configuration Release
```

Verify all unit tests pass on every target framework, public API surface is tested, edge cases and error paths are covered.

### Step 4: Pack and Verify

```bash
dotnet pack --configuration Release --output ./artifacts
dotnet nuget verify ./artifacts/PackageName.1.0.0.nupkg
unzip -l ./artifacts/PackageName.1.0.0.nupkg
```

### Step 5: Publish

```bash
# To nuget.org
dotnet nuget push ./artifacts/PackageName.1.0.0.nupkg \
  --api-key $NUGET_API_KEY \
  --source https://api.nuget.org/v3/index.json

# To a private feed
dotnet nuget push ./artifacts/PackageName.1.0.0.nupkg \
  --api-key $FEED_API_KEY \
  --source https://pkgs.dev.azure.com/org/project/_packaging/feed/nuget/v3/index.json
```

AI discipline rules (never publish without tests, validate metadata, multi-target verification, API-surface review), the anti-pattern catalog, and step-by-step error recovery all live in `references/conventions.md`.

## State Block

```
<nuget-scaffold-state>
step: [scaffold | configure | test | pack | publish]
package_name: [name]
target_frameworks: [frameworks]
version: [version]
publish_target: [nuget.org | private feed | local]
last_action: [what was done]
next_action: [what's next]
blockers: [issues]
</nuget-scaffold-state>
```

## Output Template

| Template | Required Content |
|----------|-----------------|
| Project Scaffold | Created files table (path → purpose), initial state block |
| .csproj Configuration | Configured properties list (PackageId, Version, Authors, etc.), Build settings (Deterministic, Source Link, Nullable), state block |
| CI/CD Pipeline Setup | Pipeline stages table (Stage / Trigger / Actions: Build=Push/PR, Pack=Tag push, Publish=Tag+approval), state block |

Full templates: `references/cicd-templates.md`.

**Reference files:**

- [.csproj Metadata Reference](references/csproj-metadata.md) -- Complete property reference for package metadata
- [CI/CD Pipeline Templates](references/cicd-templates.md) -- GitHub Actions and Azure DevOps pipeline templates
- [Conventions, Discipline & Recovery](references/conventions.md) -- Domain principles, KB lookups, discipline rules, anti-patterns, error recovery

## Integration with Other Skills

- **`dotnet-vertical-slice`** -- use to structure the internal architecture, then use this skill to wrap it as a distributable NuGet package
- **TDD** (`tdd-loop` skill, `tdd-agent` agent) -- develop the package internals using TDD workflows before progressing to the Pack step; the test project created by this scaffold integrates directly with TDD phase management
- **`mcp-server-scaffold`** (in the `edge-ai-robotics-automation-toolkit` supplement) -- when building an MCP server that ships as a dotnet tool NuGet package, use this skill for the packaging and `mcp-server-scaffold` for the server implementation
