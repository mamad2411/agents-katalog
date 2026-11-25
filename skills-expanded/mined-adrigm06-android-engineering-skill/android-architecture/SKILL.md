---
name: android-architecture
description: Architecture strategy for Android apps at real production scale. Use this whenever the user asks about app structure, modularization, MVVM/MVI/UDF choices, migration from legacy code, dependency boundaries, or architecture review decisions.
---

# Purpose

Design and evolve Android architecture with enforceable boundaries, explicit ownership, and migration-safe sequencing under real delivery constraints.

## Scope and authority

This skill is the lead authority for:

- module boundaries and dependency direction
- layering and ownership topology
- architecture style selection (MVVM/MVI/UDF/Clean depth)
- migration design from legacy structures

This skill is not the final authority for:

- critical security exposure (`android-security` override)
- release go/no-go (`android-release-engineering` override)
- runtime SLA constraints (`android-performance` runtime override)

## When to use

Use this skill when the user is:

- starting architecture for a new Android app or major feature set
- refactoring package/module structure
- deciding architecture style fit for current team and product complexity
- resolving dependency boundary violations
- requesting migration paths from legacy codebases
- asking for ADR-ready architecture decisions

## Required inputs

Collect the minimum set that changes the decision:

- team topology and ownership model
- app/domain complexity and release cadence
- current architecture pain points and dependency graph symptoms
- build/CI constraints and delivery deadlines
- regulatory/security constraints
- migration risk tolerance and rollback requirements

If key inputs are missing, proceed with explicit assumptions and lower confidence.

## Decision engine workflow

1. Frame constraints and decision domain.
2. Classify architecture maturity (seed, scaling, multi-team, legacy-heavy).
3. Select architecture style branch and module topology branch.
4. Validate against global dependency constraints.
5. Run cross-skill checks (security/performance/build/testing/release).
6. Resolve conflicts using authority model from `../../AGENTS.md`.
7. Return target-state design + phased migration plan + rollback points.

## Branching decision tree

### Branch A: architecture maturity

- `Seed team` (1-4 engineers, fast iteration):
  - Prefer modular monolith + package-by-feature.
  - Delay deep multi-module split unless ownership/build pain is concrete.
- `Scaling team` (5-12 engineers, multiple ownership zones):
  - Introduce selective feature/core modules by ownership and change rate.
  - Add API boundaries where coordination overhead is rising.
- `Multi-team` (12+ engineers, parallel delivery):
  - Use explicit feature modules + strong domain/core contracts.
  - Enforce strict dependency visibility and review gates.
- `Legacy-heavy` (high coupling, fragile releases):
  - Use strangler migration slices.
  - Prioritize boundary stabilization before style purity.

### Branch B: state/architecture style fit

- `MVVM`: default for mostly CRUD/form/list flows with moderate complexity.
- `MVI/UDF`: choose for event-heavy flows and high state-transition complexity.
- `Deeper Clean boundaries`: choose only when cross-feature domain policy and long-term ownership justify added indirection.

### Branch C: migration strategy

- `Low tolerance for risk`: incremental adapters + compatibility seams.
- `Moderate tolerance`: parallel module extraction with feature-by-feature cutover.
- `High tolerance with strong tests`: accelerated boundary rewrite with staged guardrails.

## Conflict handling and composition

When activated with other skills:

- With `android-performance`:
  - Keep architectural boundaries unless measured runtime/regression evidence requires exception.
  - If exception is needed, time-box it and define path back to target architecture.
- With `android-compose`:
  - Compose state patterns must fit architecture ownership boundaries.
  - Reject UI-local shortcuts that leak domain/data responsibilities.
- With `android-gradle-build`:
  - Module proposals must be build-graph-feasible; avoid theoretical splits that harm CI throughput.
- With `android-security`:
  - Security-critical controls override structural preference.
- With `android-testing`:
  - If migration confidence is weak, increase verification scope before high-risk structural changes.

## Real-world tradeoff guidance

Allow context-justified non-ideal decisions when clearly labeled:

- "Temporary shared module" may be acceptable under deadline if ownership exit criteria is defined.
- "Hybrid architecture" may be acceptable during migration if dependency direction remains enforceable.
- "Deferred module split" may be acceptable when build pain is low and team size is stable.

Do not present temporary compromises as final architecture.

## Anti-pattern detection

Flag and explain:

- god modules with mixed UI/domain/data responsibilities
- fake clean layers with pass-through use cases
- feature-to-feature dependency shortcuts
- domain contaminated by framework or transport concerns
- over-modularization with no ownership or build ROI

## Uncertainty protocol

Always report confidence for non-trivial decisions:

- `High` (>= 0.80): constraints and evidence are strong.
- `Medium` (0.60-0.79): assumptions or tradeoff ambiguity exists.
- `Low` (< 0.60): key data missing or conflicts unresolved.

If confidence is medium/low:

- list assumptions that could flip the decision
- provide at least one viable alternative path
- identify minimum missing data needed to finalize
- escalate to supporting skills where uncertainty is cross-domain

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-architecture`.

## Output contract

Use the global section order from `../../AGENTS.md` and adapt content for architecture tasks:

1. `Context and constraints`
2. `Decision and rationale`
3. `Alternatives considered`
4. `Tradeoffs`
5. `Risks and mitigations`
6. `Confidence and unknowns`
7. `Cross-skill impacts`
8. `Next implementation steps`

Also include:

- `Proposed module tree`
- `Dependency rules (allowed/forbidden)`
- `Migration path with rollback-safe phases`
- `ADR draft`

## Related resources

- `references/architecture-selection.md`
- `references/module-boundaries.md`
- `templates/architecture-proposal.md`
- `templates/adr.md`
- `examples/anti-patterns.md`
