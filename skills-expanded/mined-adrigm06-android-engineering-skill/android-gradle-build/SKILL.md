---
name: android-gradle-build
description: Android build engineering skill for Gradle architecture, convention plugins, dependency management, and build performance. Use whenever users ask to optimize build time, modular build setup, or dependency strategy.
---

# Purpose

Improve Android build reliability, determinism, and throughput through measurable Gradle architecture decisions and rollback-safe migrations.

## Scope and authority

This skill is the lead authority for:

- build logic structure (convention plugins, build-logic topology)
- dependency and version governance
- build performance interventions and CI cache strategy
- migration sequencing for build system changes

This skill must defer when applicable:

- architecture ownership boundaries to `android-architecture`
- runtime performance constraints to `android-performance`
- production rollout gates to `android-release-engineering`

## When to use

- build time optimization and CI throughput issues
- multi-module Gradle structure changes
- convention plugin/build-logic migration decisions
- annotation processing strategy (KSP vs kapt) planning
- dependency governance and reproducibility hardening

## Required inputs

Collect minimum evidence first:

- baseline metrics (configuration time, clean/incremental build times)
- CI topology (agents, cache behavior, matrix strategy)
- module graph shape and dependency hotspots
- plugin/version management approach
- delivery pressure and acceptable migration risk

If baseline metrics are missing, propose measurement-first phase before structural changes.

## Decision engine workflow

1. Baseline current build and CI behavior.
2. Classify dominant bottleneck domain (configuration, task execution, dependency graph, cache reliability).
3. Select intervention branch with expected impact and cost.
4. Validate against architecture and release constraints.
5. Define phased rollout with stop/rollback gates.
6. Specify verification metrics and regression monitors.

## Branching decision tree

### Branch A: bottleneck classification

- `Configuration-heavy`:
  - consolidate duplicated Gradle logic
  - migrate reusable setup to convention plugins
- `Execution-heavy`:
  - optimize hot tasks and annotation processing strategy
  - reduce unnecessary task invalidation
- `Dependency graph-heavy`:
  - reduce `api` leakage and classpath bloat
  - tighten dependency exposure boundaries
- `Cache instability-heavy`:
  - fix root-cause cache misses before scaling cache infra
  - enforce deterministic inputs and normalized build environments

### Branch B: build logic architecture

- small module count + low duplication:
  - lightweight centralization may be enough
- medium/high module count + repeated scripts:
  - adopt convention plugins with explicit ownership

### Branch C: annotation processing strategy

- choose `KSP` where ecosystem support and ROI are proven
- keep `kapt` where migration risk is high or ecosystem support is incomplete
- mixed mode is acceptable temporarily with migration criteria

### Branch D: CI strategy

- prioritize reproducibility and deterministic cache keys before aggressive parallelization
- if release cadence is tight, gate risky build changes behind opt-in CI paths first

## Quantitative gates

Use measurable gates and label each `pass | at-risk | fail`:

- configuration-time regression budget gate
- clean-build-time regression budget gate
- incremental-build-time regression budget gate
- cache-effectiveness gate (hit-rate and determinism trend)

If baseline build metrics are missing, run measurement-first and postpone irreversible build-graph changes.

## Conflict handling and composition

When used with other skills:

- With `android-architecture`:
  - reject build-driven module splits that violate ownership logic
- With `android-release-engineering`:
  - release stability overrides aggressive build tuning near launch windows
- With `android-testing`:
  - preserve test reliability while optimizing build pipeline
- With `android-performance`:
  - avoid build optimizations that hide runtime regressions by weakening validation paths

## Real-world tradeoff guidance

Accept justified non-ideal choices when explicit:

- temporary duplicated scripts may remain during phased plugin migration
- partial cache adoption is acceptable if deterministic misses are still being stabilized
- delaying deep dependency cleanup may be valid under strict deadlines if guardrails are defined

Do not represent temporary debt as steady-state architecture.

## Anti-pattern detection

- repeated Gradle snippets with no central ownership
- pervasive `api` dependencies increasing classpath and recompilation scope
- unpinned plugin/dependency versions
- caching strategy treated as infra-only instead of input-determinism problem
- optimization proposals without baseline and post-change evidence

## Uncertainty protocol

Always report confidence:

- `High` (>= 0.80)
- `Medium` (0.60-0.79)
- `Low` (< 0.60)

For medium/low confidence:

- state assumptions and missing metrics
- provide at least one lower-risk alternative
- request the minimum additional measurements needed
- escalate to `android-release-engineering` for near-release risk conflicts

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-gradle-build`.

## Output contract

Follow global order from `../../AGENTS.md`:

1. `Context and constraints`
2. `Decision and rationale`
3. `Alternatives considered`
4. `Tradeoffs`
5. `Risks and mitigations`
6. `Confidence and unknowns`
7. `Cross-skill impacts`
8. `Next implementation steps`

Include build-specific artifacts:

- `Current build pain points`
- `Proposed build layout`
- `Dependency/version strategy`
- `Performance interventions`
- `CI/cache strategy`
- `Migration plan with rollback gates`

## Related resources

- `references/build-optimization-checklist.md`
- `references/quantitative-gates.md`
