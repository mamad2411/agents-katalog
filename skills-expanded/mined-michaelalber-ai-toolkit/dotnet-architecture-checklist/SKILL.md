---
name: dotnet-architecture-checklist
audience: team
description: >
  Grades an existing .NET solution against the style it actually uses — controller-based
  layered/N-tier Web API OR vertical-slice CQRS (FreeMediator/Mapster)/Blazor — detecting
  framework, hosting model, and style FIRST (a layered API is not penalized for not being
  vertical-slice), then checking architectural coherence, controller/handler discipline, EF Core
  lifetimes, framework health, and config/secrets hygiene with file:line evidence. Use to review
  or grade a .NET solution. Not for Socratic critique (architecture-review), security audits
  (dotnet-security-review), or new test-first code (tdd-loop).
---

# .NET / Blazor Architecture Checklist

> "A checklist cannot fly a plane, but a pilot cannot fly safely without one."
> — Atul Gawande

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` architecture checklists — same values, language-specific checks.

**Non-Negotiable Constraints:**
1. **Detect before judging** — no checklist item is applied until the version, framework, and structure are known
2. **Evidence or it is not a finding** — every finding cites `file:line` and the offending pattern
3. **Version-correct advice only** — never recommend an API the detected version does not have
4. **The grade is counted, not felt** — the A–F grade comes from the tally of findings

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Evidence over opinion** | Every finding cites `file:line` and the offending pattern. "Handlers are coupled" is not a finding; "`OrderHandler.cs:12` inherits `BaseCrudHandler<T>`" is. |
| 2 | **Feature cohesion** | Organized by business capability (feature folders), not technical layer. Cross-feature imports are a violation. |
| 3 | **Dependencies point inward** | Domain logic does not depend on infrastructure; entities do not leak across API boundaries (anti-corruption layers). |
| 4 | **Explicit error handling** | Failures handled at the right layer (pipeline behaviors); no silent swallowing; errors carry diagnostic context. |
| 5 | **Config & secrets hygiene** | No hardcoded secrets; configuration via `IOptions<T>`; no secrets in WASM bundles. |
| 6 | **Tests gate change** | Untested code is a finding; high-risk handlers without tests are prioritized. |

## Workflow

Shared skeleton: `DETECT → SCAN → REPORT → RECOMMEND`.

```
DETECT     Target framework (grep <TargetFramework> in all .csproj; global.json/Directory.Build.props),
           hosting model (Program.cs render modes: Server/WASM/Auto; or controller Web API), and —
           CRITICAL — the ARCHITECTURE STYLE: layered/N-tier controllers vs. vertical-slice CQRS vs.
           mixed (see references/layered-ntier.md for the style-detection grep). Then CQRS library
           (FreeMediator vs MediatR), Mapster, and Telerik usage. The detected style selects which
           checklist branch is authoritative. If the framework or style is unclear, ask — never assume
           .NET 10 or vertical-slice.

SCAN       Run the checklist branch for the DETECTED style — the Vertical-Slice/CQRS branch (table below)
           OR the Layered/N-tier Controller branch (references/layered-ntier.md) — section by section,
           cross-referencing references/red-flags.md. Gather evidence with grep and dotnet build/analyzers.
           Every violation becomes a finding with file:line and a severity (critical/high/medium/low).

REPORT     Emit the graded report (Output Template). Grade = function of counted findings.

RECOMMEND  Prioritize: critical → quick wins → modernization. Version-gate every recommendation; provide
           upgrade paths for EOL frameworks (references/framework-detection.md).
```

**Load on demand — `references/operating-guide.md`:** .NET Checklist, AI Discipline Rules. Deeper detail: `references/cqrs-patterns.md`, `references/review-checklist.md`.

## State Block

```
<arch-checklist-state>
language: dotnet
mode: DETECT | SCAN | REPORT | RECOMMEND | COMPLETE
architecture_style: layered-controllers | vertical-slice-cqrs | mixed
detected: [target_framework | hosting_model | cqrs_lib | mapster:y/n | telerik:y/n | tests:y/n]
issues_found: [critical:N high:N medium:N low:N]
last_action: [what was just done]
next_action: [what should happen next]
</arch-checklist-state>
```

## Output Template

Shared across all four architecture checklists.

```markdown
## Architecture Checklist: [solution] (.NET)
**Framework**: [version] | **Style**: [Layered-Controllers/Vertical-Slice-CQRS/Mixed] | **Hosting**: [Server/WASM/Auto/Web API] | **CQRS**: [FreeMediator/MediatR/None] | **Tests**: [yes/no]

| Section | Pass | Fail | Warn |
|---------|------|------|------|
| Coherence / Controllers-Handlers / Pipeline / EF / Framework / Config / Telerik | … | … | … |

### Grade: [A–F]
Grading: **A** 0 crit/0 high/≤3 med · **B** 0 crit/≤2 high · **C** 0 crit, gaps in one area ·
**D** 1+ crit · **F** fundamental problems (EOL framework, singleton DbContext, missing auth; *vertical-slice:*
base-handler hierarchy; *layered:* business logic + EF queries in controllers). Grade against the detected
style — a coherent layered controller API with clean boundaries is an A.

| Severity | Location | Finding | Recommendation |
|----------|----------|---------|----------------|
| CRITICAL | file:line | [pattern] | [version-gated fix] |

**Quick wins**: [low-effort, high-impact] · **Modernization**: [larger items with effort estimate]
```

## Integration with Other Skills

- **`architecture-review`** — When the grade is D/F, escalate to the Socratic critic: this checklist finds _what_ is wrong; `architecture-review` builds _why_.
- **`dotnet-security-review`** — Companion for the security dimension (OWASP, Telerik, deserialization).
- **`dotnet-vertical-slice`** — Correct-pattern reference when a vertical-slice/CQRS project flags structural violations.
- **`dotnet-controller-api-scaffolder`** — Correct-pattern reference when a layered controller API flags structural violations (fat controllers, entity leakage, inconsistent conventions).
- **`ef-migration-manager`** — For EF Core lifetime/migration findings.
- **`legacy-migration-analyzer`** — When EOL/.NET Framework is detected, for a phased upgrade plan.
- **`tdd-loop`** — Methodology for adding tests the checklist flags as missing.
- **`python` / `php` / `rust`-architecture-checklist** — Sibling skills sharing this exact Core Values + workflow + output.
