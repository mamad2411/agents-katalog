---
name: code-quality
description: "Run evidence-based code-quality, non-Go diagnosis, and merge-readiness passes. Use when users request thermonuclear review, ruthless test strategy, TDD, zero tech debt, architecture deepening, or a merge gate."
---

# Code Quality

Choose one evidence-driven mode for improving a code change, test suite, or diagnosed failure.

## Route

| Mode | Select when | Read |
| --- | --- | --- |
| `implement-small` | The user requests the smallest coherent behavior change | `references/implement-small.md` |
| `review-sprawl` | The user requests a sprawl audit or explicitly names a harsh or thermonuclear review | `references/review-sprawl.md` |
| `refactor` | The user requests behavior-preserving refactoring | `references/refactor.md` |
| `clean-slate` | The user explicitly says clean-slate, zero tech debt, or hard cut before compatibility deletion | `references/clean-slate.md` |
| `tdd` | The user says TDD, red-green-refactor, or test-first | `references/tdd.md` |
| `test-strategy` | The user asks to audit, prune, de-flake, choose tests, or migrate test-only ShoeHorn assertions | `references/test-strategy.md` |
| `regression` | A resolved bug needs a deterministic regression test | `references/regression.md` |
| `quality-gate` | The user requests merge readiness, a Definition of Done, or a second evidence-backed review | `references/quality-gate.md` |
| `architecture` | The user requests deepening, seam analysis, or architecture cleanup | `references/architecture.md` |
| `diagnose` | The user explicitly asks to diagnose a non-Go hard failure or performance regression | `references/diagnose.md` |

Select exactly one mode by default. Read only its reference. Combine modes only when the user asks for a pass sequence or when a selected reference explicitly requires the next mode.

## Do not use when

For a Go performance regression or Go verification claim, `go-lang` owns the first pass. This suite owns non-Go source-code diagnosis; Kubernetes or infrastructure-as-code desired/live failures belong to `infra-bundles`.

## Shared workflow

1. Inspect the requested scope, current code, existing tests, and repository conventions before proposing a change or conclusion.
2. Use the selected reference for mode-specific work; resolve version-sensitive tooling from installed state, live help, then current primary documentation.
3. Support conclusions with current evidence: a path and line, a failing or passing check, a reproduction signal, or a confirmed caller.
4. Preserve public behavior unless the selected mode and user request explicitly define an intended end-state change.

## Hard rules

- Prefer a coherent local shape over a broad speculative rewrite.
- Add files, dependencies, abstractions, seams, and mocks only when they reduce total complexity or isolate a real system boundary.
- Test observable behavior through the right public surface; do not lock tests to internal choreography by default.
- Do not patch a quality-gate finding unless the user requested a fix loop.
- State uncertainty and the missing evidence instead of guessing about tool, API, or repository behavior.

## Stop conditions

- Ask for direction when two modes would materially change the result and the request does not identify a winner.
- Stop a diagnosis before fixing when no trustworthy feedback loop or reproduction signal can be built; report what access or artifact is needed.

## Output

Return the selected mode, evidence, the smallest justified action or decision, verification performed, and unresolved risk or follow-up.
