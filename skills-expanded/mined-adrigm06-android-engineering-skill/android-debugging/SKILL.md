---
name: android-debugging
description: Android debugging skill for root-cause analysis using hypothesis-driven workflows, reproduction plans, instrumentation, and narrowing strategies. Use when bugs are intermittent, hard to reproduce, or cross-layer.
---

# Purpose

Diagnose Android issues with hypothesis-ranked investigation, reproducible experiments, and evidence-based root-cause closure.

## Scope and authority

This skill is root-cause authority for incident triage and narrowing workflow.

## When not to use

- when the primary question is architecture topology rather than incident diagnosis (`android-architecture`)
- when the task is release go/no-go decision without active root-cause investigation (`android-release-engineering`)

## When to use

- intermittent crashes and inconsistent behavior
- cross-layer regressions
- environment- or device-specific failures

## Decision engine workflow

1. Define symptom, scope, and impact.
2. Build reproducibility matrix.
3. Rank hypotheses by likelihood and blast radius.
4. Add targeted instrumentation.
5. Run narrowing experiments and update confidence per hypothesis.
6. Propose fix candidates and verification path.

## Branching decision tree

### Branch A: reproducibility state

- `reproducible`:
  - run controlled experiments and binary-search recent changes
- `non-reproducible`:
  - invest first in telemetry and environment narrowing before proposing fixes

### Branch B: incident severity

- `production-impacting`:
  - optimize for fast containment and rollback-safe mitigation
- `non-blocking`:
  - optimize for high-confidence root-cause isolation before code change

### Branch C: issue class

- `crash-heavy`:
  - prioritize crash signature clustering and deterministic repro around top signatures
- `ANR/jank-heavy`:
  - prioritize thread-state and timing instrumentation; escalate to `android-performance`
- `data-integrity risk`:
  - prioritize correctness containment and rollback-safe mitigations

## Quantitative gates

Use measurable debugging gates before declaring closure:

- reproducibility gate:
  - `pass` when deterministic repro or high-signal repro matrix exists
  - `at-risk` when repro is intermittent but bounded
  - `fail` when no meaningful repro path exists
- evidence convergence gate:
  - `pass` when top hypothesis has converging signals across independent instrumentation
  - `at-risk` when signals are partially convergent
  - `fail` when evidence conflicts materially
- verification gate:
  - `pass` when proposed fix eliminates symptom in controlled validation runs
  - `at-risk` when partial improvement only
  - `fail` when regression or no improvement appears

## Uncertainty protocol

Always provide confidence per primary hypothesis:

- `High` (>= 0.80)
- `Medium` (0.60-0.79)
- `Low` (< 0.60)

If confidence is medium/low:

- list assumptions explicitly
- request minimum additional evidence needed to finalize root cause
- provide at least one fallback containment option
- escalate to supporting skill by domain when cross-skill impact is material

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-debugging`.

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

Then include debugging-specific artifacts:

- `Observed symptoms`
- `Most likely root causes`
- `Reproduction strategy`
- `Instrumentation plan`
- `Narrowing experiments`
- `Fix candidates and verification`

## Anti-pattern detection

- guess-based fixes without evidence
- no reproducible baseline
- noisy logs without diagnostic hypothesis
- deep refactor before root cause confirmation

## Related resources

- `references/debugging-playbook.md`
- `templates/debug-investigation.md`
