---
name: android-code-review
description: Structured Android code review skill with severity-based findings across architecture, correctness, maintainability, performance, and security. Use this for PR reviews and technical debt assessments.
---

# Purpose

Run disciplined Android code reviews that prioritize issues by incident risk and provide implementation-ready fixes.

## Scope and authority

This skill is synthesis authority across domains.
It consolidates architecture, security, performance, testing, and release concerns into a prioritized outcome.

## When not to use

- when the primary task is deep root-cause investigation (`android-debugging`)
- when the primary goal is new architecture design selection (`android-architecture`)

## When to use

- pull request reviews
- technical debt audits
- release-candidate quality checks

## Decision engine workflow

1. Establish change intent and blast radius.
2. Check non-negotiable constraints first.
3. Evaluate architecture, correctness, maintainability, performance, and security implications.
4. Rank findings by severity and operational impact.
5. Propose fix order and verification strategy.

## Branching decision tree

### Branch A: change risk profile

- `high blast radius` (cross-module, auth, payment, startup, release-critical):
  - perform deep multi-domain review with stricter evidence requirements
- `medium blast radius`:
  - prioritize correctness, maintainability, and boundary consistency
- `low blast radius`:
  - focus on local quality and regression prevention

### Branch B: release proximity

- `near release`:
  - prioritize regressions and production-risk findings first
- `normal window`:
  - include strategic maintainability improvements with staged follow-up

### Branch C: change category

- `security-sensitive`:
  - require stronger evidence and verification for exploitability/reachability concerns
- `performance-sensitive`:
  - require measurement-backed findings for hotspot regressions
- `boundary-sensitive`:
  - prioritize dependency direction and ownership violations

### Branch D: evidence availability

- `full diff/artifacts available`:
  - run normal severity-based review flow
- `partial artifacts only`:
  - scope findings to verified surfaces, mark unknowns explicitly
- `no diff/artifacts provided`:
  - do not approve/reject code quality conclusively
  - return a provisional risk review with required evidence checklist
  - provide a low-risk fallback path (narrow merge scope or hold)

## Quantitative gates

Use measurable evidence gates for high-impact findings:

- evidence sufficiency gate:
  - `pass` when finding has concrete code evidence and reproducible risk path
  - `at-risk` when evidence is partial but plausible
  - `fail` when claim is mostly speculative
- verification readiness gate:
  - `pass` when recommended fix includes clear verification steps
  - `at-risk` when verification is incomplete
  - `fail` when no verification plan exists

## Uncertainty protocol

Always include confidence on non-trivial findings.
For medium/low confidence findings, include the minimum evidence needed to confirm/refute.

Confidence bands:

- `High` (>= 0.80)
- `Medium` (0.60-0.79)
- `Low` (< 0.60)

If confidence is medium/low:

- list assumptions explicitly
- request minimum additional evidence that can re-rank severity
- provide at least one fallback recommendation with lower regression risk
- escalate to specialized skill when domain certainty is insufficient

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

Then include review-specific artifacts:

- `Findings by severity`
- `Evidence`
- `Risk impact`
- `Recommended fix`
- `Follow-up checks`

### No-diff fallback template (required when artifacts are missing)

When PR diff or runtime artifacts are missing, add:

- `Review status`: `Provisional - insufficient evidence`
- `Blocking unknowns`: exact missing artifacts (diff, module list, benchmarks, security config deltas)
- `Provisional findings`: only evidence-backed risks, each marked `confirmed` or `hypothesis`
- `Minimum evidence to finalize`: smallest artifact set needed for final severity ranking
- `Fallback path`: low-risk option (scope split, hold merge, or merge non-runtime subset only)

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-code-review`.

## Anti-pattern detection

- hidden coupling or boundary violations
- missing tests on behavior-critical changes
- performance-sensitive changes with no measurements
- security-impacting changes with weak controls

## Related resources

- `references/review-severity-evidence.md`
- `templates/review-report.md`
