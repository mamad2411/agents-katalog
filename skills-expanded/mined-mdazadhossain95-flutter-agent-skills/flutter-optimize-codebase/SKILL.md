---
name: flutter-optimize-codebase
description: Optimizes a Flutter codebase for performance, maintainability, architecture quality, and release readiness using a prioritized, evidence-driven improvement plan.
license: MIT
metadata:
  version: 0.1.0
  owner: mdazadhossain95
---
# Optimize Flutter Codebase

## Purpose
Use this skill to audit and improve an existing Flutter codebase with practical, high-impact optimizations.

## Activation
Activate when user asks to optimize, improve, harden, refactor, or speed up a Flutter app or a specific module.

## Input Collection
Capture minimum context first:
- Scope: whole app, feature folder, or specific files.
- Target: performance, architecture, code quality, app size, stability, testability, or all.
- Optimization mode: quick, standard, deep.
- Risk tolerance: low-risk only or allow medium refactors.

If scope is missing, default to project-level scan.

## Optimization Modes
- Quick mode: fast audit + top 5 improvements.
- Standard mode: prioritized plan + key code changes.
- Deep mode: broader refactor roadmap with staged implementation plan.

## Optimization Workflow
Follow this order:

1) Baseline and hotspots
- Map project structure and critical execution paths.
- Identify hotspots in startup path, navigation, rendering-heavy screens,
  network/data pipeline, and state updates.

2) Architecture and boundaries
- Check separation of presentation, logic, and data layers.
- Detect coupling, duplicated logic, and module boundary leaks.
- Recommend consolidation where appropriate.

3) State management efficiency
- Identify excessive rebuild patterns and state over-scoping.
- Ensure state ownership is close to consumers where possible.
- Recommend selector/listener granularity improvements.

4) Rendering and UI performance
- Look for expensive build methods and unnecessary widget rebuilds.
- Prefer const constructors where safe.
- Suggest list virtualization patterns and image handling improvements.

5) Network, caching, and persistence
- Evaluate API call strategy, retry behavior, and error handling.
- Recommend caching and offline-first patterns where relevant.
- Validate model parsing path and background processing suitability.

6) Reliability and error handling
- Identify weak async error handling and null-safety risks.
- Ensure domain-level error mapping and user-safe fallbacks.

7) App size and release readiness
- Recommend app-size analysis and dependency pruning.
- Flag large assets, redundant packages, and avoidable transitive bloat.

8) Testing and maintainability
- Detect missing tests in critical modules.
- Recommend minimum unit/widget/integration coverage targets by risk.

## Output Format
Return in this structure:

1. Optimization Scope and Mode
2. Findings (ordered by impact)
3. Recommended Changes (ordered by effort and risk)
4. Quick Wins (can do now)
5. Medium Refactors (next)
6. Validation Checklist (how to verify improvements)
7. Optional Next Iteration Plan

## Behavior Rules
- Prioritize evidence-backed findings from actual code.
- Avoid vague suggestions not tied to observed patterns.
- For each recommendation, include expected impact and risk level.
- Prefer incremental changes before large rewrites.
- Keep business behavior unchanged unless user explicitly asks otherwise.

## Risk Labels
Use these labels for each recommendation:
- Low: safe local changes, minimal regression risk.
- Medium: structural changes with moderate validation required.
- High: broad refactors requiring staged rollout and tests.

## Validation Checklist
Before final response, ensure:
- Findings are prioritized by impact.
- Each recommendation has risk label and expected result.
- Suggested changes are scoped to user-selected area.
- A practical verify plan is included (tests, profiling, runtime checks).

## Completion Template
Use this response layout:
1. Scope: <project/module/files>
2. Mode: <quick/standard/deep>
3. Top Findings: <3-7 items>
4. Recommended Changes: <prioritized list with risk>
5. Verification Steps: <commands/checks>
6. Next Iteration: <optional follow-up optimization track>
