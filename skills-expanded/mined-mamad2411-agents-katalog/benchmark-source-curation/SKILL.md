---
name: benchmark-source-curation
description: Use when BenchmarkDotNet guidance must be grounded in authoritative, current sources and converted into reusable, agent-usable benchmark guidance.
---

# BenchmarkDotNet Source Curation

## Specialization

Use this skill to curate BenchmarkDotNet and Perfolizer references for performance experiment design, diagnoser policy, and benchmark-governance decisions.

This skill governs benchmark evidence inputs only. It does not write benchmark implementations or tune production code.

## Objective

Produce a BenchmarkDotNet evidence baseline with explicit decisions for diagnosers, statistical interpretation, CI thresholding, and release-comparable benchmark reporting.

## Trigger Conditions

- BenchmarkDotNet attribute or diagnoser guidance is being created, reviewed, or corrected.
- A benchmark gate/checklist needs source-backed defaults for jobs, exporters, and environment controls.
- A BenchmarkDotNet or Perfolizer update may change interpretation rules or benchmark outputs.
- CI benchmark thresholds or baseline-comparison policies require source-backed calibration.

## Scope Boundaries

In scope:

- Source selection, authority checks, and freshness checks.
- Mapping source content into actionable guidance deltas.
- Rejected-source recording with explicit reason codes.
- Version-aware content curation for BenchmarkDotNet API changes.

Out of scope:

- Direct implementation of benchmark code.
- Statistical modeling beyond source-cited guidance.
- Non-benchmarking performance content curation.

## Inputs

- Target BenchmarkDotNet topics and expected output artifacts.
- Evaluation date in ISO format (`YYYY-MM-DD`).
- Freshness threshold in days (default: 30).
- Existing source inventory if available.

## Required Outputs

- Updated source catalog with authority, freshness, relevance, and actionability fields.
- Benchmark topic-to-source coverage matrix.
- Rejected-source table with deterministic reason codes.
- Prioritized benchmark-guidance deltas grouped by: experiment design, diagnostics, statistics, and CI enforcement.
- Version-impact note describing any BenchmarkDotNet or Perfolizer behavior changes relevant to existing benchmark skills.

## Authoritative Source Registry

| Source | Authority | Domain | URL |
|---|---|---|---|
| BenchmarkDotNet Official Docs | Primary | All BDN attributes, diagnosers, jobs, exporters | https://benchmarkdotnet.org/articles/overview.html |
| BenchmarkDotNet GitHub | Primary | Release notes, API changes, issue patterns | https://github.com/dotnet/BenchmarkDotNet |
| Microsoft Learn – BDN Tutorial | First-party | Setup, MemoryDiagnoser, CI basics | https://learn.microsoft.com/en-us/dotnet/core/testing/benchmarkdotnet |
| .NET Performance Blog | First-party | Real-world benchmark patterns from .NET team | https://devblogs.microsoft.com/dotnet/category/performance/ |
| Adam Sitnik's Blog | Co-creator | Diagnosers, hardware counters, pitfall avoidance | https://adamsitnik.com/ |
| Andrey Akinshin's Blog | Co-maintainer | Statistical interpretation, effect size, distributions | https://aakinshin.net/ |
| Perfolizer Docs | Co-maintainer | Distribution analysis, effect size, outlier detection | https://github.com/AndreyAkinshin/perfolizer |
| dotnet/performance – CI Workflow | First-party | CI threshold enforcement, benchmark suite structure | https://github.com/dotnet/performance/blob/main/docs/benchmarking-workflow-dotnet-runtime.md |
| dotnet/performance Repo | First-party | Reference benchmark implementations at scale | https://github.com/dotnet/performance |

## Source Decision Rules

- `accept`: authoritative source, freshness within threshold, and directly actionable.
- `accept-with-watch`: authoritative and relevant but partial, stale, or pending update.
- `reject`: not authoritative, too stale, redundant, or non-actionable.

## Rejected Source Reasons

- `R1`: Not authoritative for BenchmarkDotNet behavior.
- `R2`: Older than freshness threshold without durable applicability.
- `R3`: Redundant with no new actionable guidance.
- `R4`: Opinion-heavy with low implementation specificity.
- `R5`: Outside BenchmarkDotNet scope.

## Topic-to-Source Coverage Map

| Topic | Primary Source | Secondary Source |
|---|---|---|
| Attribute API (`[Benchmark]`, `[Params]`, `[GlobalSetup]`) | BenchmarkDotNet Docs | BenchmarkDotNet GitHub |
| Memory diagnoser and allocation tracking | BenchmarkDotNet Docs | Adam Sitnik's Blog |
| Hardware counters and ETW diagnosers | Adam Sitnik's Blog | BenchmarkDotNet Docs |
| Statistical interpretation (mean, error, stddev) | Andrey Akinshin's Blog | Perfolizer Docs |
| Effect size and distribution comparison | Andrey Akinshin's Blog | Perfolizer Docs |
| Outlier detection and removal rationale | Perfolizer Docs | BenchmarkDotNet Docs |
| CI threshold enforcement | dotnet/performance CI Workflow | BenchmarkDotNet GitHub |
| Benchmark suite structure at scale | dotnet/performance Repo | .NET Performance Blog |
| Setup, minimal config, and MS Learn onboarding | Microsoft Learn – BDN Tutorial | BenchmarkDotNet Docs |
| Real-world .NET team patterns | .NET Performance Blog | dotnet/performance Repo |

## Deterministic Workflow

1. Enumerate target BenchmarkDotNet topics that must be covered.
2. Collect candidate sources from the authoritative source registry.
3. Score each source for authority, freshness, relevance, and actionability.
4. Reject weak sources and record reason codes.
5. Build a topic-to-source coverage matrix to expose gaps.
6. Produce prioritized deltas that downstream skills can consume.
7. Publish closure status, unresolved benchmark-source gaps, and version-impact notes.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Authoritative source baseline | Authoritative Source Registry |
| Topic-to-source traceability | Topic-to-Source Coverage Map |
| Source quality decisions | Source Decision Rules + Rejected Source Reasons |
| Downstream guidance deltas | Deterministic Workflow steps 5–7 |
