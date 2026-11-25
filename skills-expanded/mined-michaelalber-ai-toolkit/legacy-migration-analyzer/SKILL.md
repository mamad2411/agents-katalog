---
name: legacy-migration-analyzer
audience: team
description: >
  Analyze .NET Framework to .NET 10 migration paths. Use when assessing legacy codebases for
  modernization, identifying breaking changes, and planning incremental migration strategies.
  Also
---

# Legacy Migration Analyzer

> "The best migrations are the ones you don't notice. Incremental, tested, and invisible to the end user."
> -- Immo Landwerth, .NET Platform Compatibility Lead

## Core Philosophy

This skill analyzes legacy .NET Framework codebases and produces actionable migration plans to .NET 10. It does NOT perform the migration itself — it assesses, quantifies risk, and creates a phased plan that humans and other skills execute.

**Non-negotiable constraints:**
1. **Assess before acting** — Scan the codebase, catalog dependencies, and score risk before recommending any approach.
2. **Incremental migration over big-bang rewrites** — The strangler fig pattern and project-by-project migration succeed. Full rewrites fail.
3. **Preserve business logic unchanged** — Migration changes infrastructure, not behavior.
4. **Dependencies are the real blockers** — Third-party NuGet packages, COM interop, and Windows-specific APIs are where migrations stall. Identify these first.
5. **Every recommendation must cite evidence** — Reference specific files, namespaces, NuGet packages, or API calls. Vague guidance is not actionable.

The full 10-row domain principle table, AI discipline rules, and the anti-pattern catalog live in
`references/migration-decision-matrix.md`.

## Workflow

Analysis proceeds through four phases: **SCAN** (codebase inventory) → **ASSESS** (risk scoring) → **PLAN** (migration roadmap) → **VALIDATE** (feasibility confirmation). Do not skip phases or reorder them.

**Approach selection:** Hard blockers (WCF duplex, COM-heavy, undocumented protocols) that can be isolated → strangler fig; that cannot be isolated → hybrid (keep blocked components on .NET Framework behind API gateway). Single monolith under 50K LOC → in-place upgrade. All NuGet dependencies compatible → project-by-project in-place. Incompatible packages with replacements → replace packages first, then upgrade. No clean path → strangler fig for affected projects.

### Phase 1: SCAN — Codebase Inventory

1. Run `upgrade-assistant analyze <SolutionPath> --target-tfm net10.0`
2. Catalog all projects (class libraries, ASP.NET MVC/Web API, WCF, Windows Services, Console, WinForms/WPF)
3. Enumerate all NuGet package references and versions
4. Identify `System.Web` namespace usages, COM interop, and P/Invoke declarations
5. Catalog all `web.config`/`app.config` sections with custom configuration
6. Catalog authentication mechanisms, IIS-specific features, and Windows-specific APIs
7. Map project-to-project references and dependency graph

Analysis commands, upgrade tooling, complexity classification, and the SDK-style `.csproj` target
are in `references/breaking-changes-catalog.md` (.NET Framework Upgrade Specifics).

### Phase 2: ASSESS — Risk Scoring

1. Cross-reference each NuGet package against [Breaking Changes Catalog](references/breaking-changes-catalog.md) and [Breaking Changes 4.x to 10](references/breaking-changes-4x-to-10.md)
2. Score each project using the [Migration Decision Matrix](references/migration-decision-matrix.md)
3. Consult [Package Replacement Map](references/package-replacement-map.md) for NuGet migration paths
4. Consult [API Replacement Patterns](references/api-replacement-patterns.md) for code-level migration patterns
5. For web projects, consult [ASP.NET to Blazor Patterns](references/aspnet-to-blazor-patterns.md)
6. Classify each breaking change: Blocker, High, Medium, Low
7. Calculate effort estimates per project and aggregate into overall risk score

### Phase 3: PLAN — Migration Roadmap

Order projects by dependency graph (leaf nodes first). Group into 2-4 week phases. Assign risk levels and rollback strategies. Define validation criteria per phase.

Standard phase order: Phase 0 (prerequisites: characterization tests, NuGet updates, extract interfaces) → Phase 1 (class libraries with no framework dependencies; multi-target if needed: `net48;net10.0`) → Phase 2 (data access layer; coordinate with `ef-migration-manager`) → Phase 3 (business logic layer) → Phase 4 (presentation/API layer; ASP.NET Core, gRPC) → Phase 5 (infrastructure; Worker Services, Kestrel, CI/CD).

### Phase 4: VALIDATE — Feasibility Confirmation

1. Walk the plan with the development team; verify effort estimates against capacity
2. Confirm all hard blockers have mitigation strategies
3. Validate rollback is possible at each phase boundary
4. Confirm deployment constraints are respected
5. Get stakeholder sign-off on timeline and risk acceptance

When the Upgrade Assistant, a NuGet package, WCF, or `System.Web` blocks progress, follow the
recovery procedures in `references/api-replacement-patterns.md` (Error Recovery).

**Load on demand — `references/breaking-changes-catalog.md`:** Knowledge Base Lookups (run them at the start of SCAN and ASSESS; every risk finding cites its source).

## State Block

```
<migration-analysis-state>
step: [SCAN | ASSESS | PLAN | VALIDATE]
source_framework: [e.g., ".NET Framework 4.8"]
target_framework: [e.g., ".NET 10"]
breaking_changes_found: [count]
risk_level: [low | medium | high | critical]
last_action: [what was just done]
next_action: [what should happen next]
blockers: [any issues]
</migration-analysis-state>
```

A worked example of a populated state block is in `references/migration-decision-matrix.md`.

## Output Template

The Migration Inventory Report template (metrics, package compatibility, breaking changes by
category, hard blockers, risk score) is in `references/migration-decision-matrix.md`
(Output Report Template).

**Reference files:**

- [Breaking Changes: .NET Framework 4.x to .NET 10](references/breaking-changes-4x-to-10.md)
- [Package Replacement Map](references/package-replacement-map.md)
- [API Replacement Patterns](references/api-replacement-patterns.md) — code-level patterns + Error Recovery
- [ASP.NET to Blazor Patterns](references/aspnet-to-blazor-patterns.md)
- [Migration Decision Matrix](references/migration-decision-matrix.md) — scoring + domain principles, discipline rules, anti-patterns, output template
- [Breaking Changes Catalog](references/breaking-changes-catalog.md) — catalog + .NET Framework upgrade commands/tools/complexity

## Integration with Other Skills

- **`ef-migration-manager`** — When the analysis identifies EF6 usage, coordinate for the EF6→EF Core migration. The database schema migration is often the riskiest part and should be planned and tested independently.
- **`dotnet-vertical-slice`** — When the plan calls for decomposing a monolithic application, use this skill to structure new .NET 10 projects as vertical slices. Especially relevant in strangler fig migrations.
- **`nuget-package-scaffold`** — When shared libraries need to be extracted or multi-targeted (`net48;net10.0`) during the transition period.
