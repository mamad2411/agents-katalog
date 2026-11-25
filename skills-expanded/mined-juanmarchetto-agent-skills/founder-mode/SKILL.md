---
name: founder-mode
description: "End-to-end product builder with founder mindset. Orchestrates 9 phases: idea evaluation → architecture → TDD → implementation → E2E → verification → analysis → GTM. Produces a launched product with README, pitch, tweet thread, and Product Hunt draft. Use when: build product, founder mode, full lifecycle, idea to launch, end to end, build from scratch, MVP, product builder, launch kit, vibe coding with quality."
license: MIT
metadata:
  version: 1.0.0
  category: toolchain
  tags: [product-builder, orchestration, tdd, e2e, gtm, multi-phase, founder]
---

# Founder Mode — End-to-End Product Builder

From idea to launched product. Not just code — a product.

## How It Works

```
/founder-mode "Build a CLI that converts markdown to slides"
        │
        ▼
  Phase 0: Bootstrap ─── config.json + state.json + mode detection
        │
        ▼
  Phase 1: Idea Evaluation ─── /architect dispatches 6 evaluators
        │
        ▼
  ══ GATE 1 ══ Go/No-Go decision ─── [continue|reject|iterate|edit]
        │
        ▼
  Phase 2: Architecture ─── system design, components, tech stack
        │
        ▼
  Phase 3: TDD Planning ─── decompose into test-first chunks
        │
        ▼
  Phase 4: Implementation ─── chunk-with-summary TDD loop
        │
        ▼
  ══ GATE 2 ══ Implementation review ─── [continue|iterate|stop|edit]
        │
        ▼
  Phase 5: E2E Testing ─── strategy by project type
        │
        ▼
  Phase 6: Verification ─── false positives + spec-to-test gap + arch drift
        │
        ▼
  ══ GATE 3 ══ Verification review ─── [continue|iterate|stop|edit]
        │
        ▼
  Phase 7: Post-Run Analysis ─── lessons + recommendations
        │
        ▼
  Phase 8: GTM Draft ─── README + pitch + tweets + PH + CHANGELOG
        │
        ▼
  DONE ─── all artifacts in .founder/
```

## Phases

| Phase | What It Does | Agent |
|-------|-------------|-------|
| 0 - Bootstrap | Config generation, mode detection, codebase scan (existing projects), lesson loading | `bootstrapper.md` |
| 1 - Evaluation | Dispatches 6 parallel evaluators via `/architect`, extracts acceptance criteria | `evaluator.md` |
| 2 - Architecture | Generates system design (new) or reverse-engineers from codebase (existing) | `architect-gen.md` |
| 3 - TDD Planning | Decomposes architecture into ordered test-first chunks | `planner.md` |
| 4 - Implementation | TDD per chunk with cross-chunk summaries, supports re-entry for fixes | `implementer.md` |
| 5 - E2E Testing | Generates and runs E2E tests matched to acceptance criteria | `e2e-runner.md` |
| 6 - Verification | False-positive detection, spec-to-test gap analysis, architecture drift check | `verifier.md` |
| 7 - Analysis | Post-run pattern analysis, lesson extraction, recommendations | `analyzer.md` |
| 8 - GTM Draft | README, pitch, tweet thread, Product Hunt listing, CHANGELOG | `gtm-drafter.md` |

## Human Gates

Three checkpoints where you make Go/No-Go decisions:

- **Gate 1 (Post-Eval):** Review the idea score. Continue, reject, or iterate with refined framing.
- **Gate 2 (Post-Implementation):** Review test results and known issues. Continue or iterate to fix.
- **Gate 3 (Post-Verification):** Review verification verdict. Continue to GTM or iterate to fix issues.

Each gate supports: `[continue]`, `[iterate]`, `[stop]`, `[edit]`

Iteration starts with a cap of 3 (configurable). When reached, you're prompted to extend or move on.

## Config

Generated at `.founder/config.json` during bootstrap. Key settings:

- `mode`: `"new"` or `"existing"` (auto-detected)
- `maxIterations`: iteration cap (default 3, extendable at gates)
- `gates`: per-gate behavior — `"pause"`, `"auto"`, or `"skip"`
- `phases`: enable/disable individual phases
- `tdd`: strictness and coverage threshold
- `gtm`: enable/disable individual GTM artifacts

Edit the config before saying `go` to customize the pipeline.

## Modes

- **New Idea:** Full pipeline from Phase 0 to Phase 8.
- **Existing Project:** Pass a path (`/founder-mode ./my-project`). Skips eval, reverse-engineers architecture, plans around existing tests, extends code, respects existing test framework.

## Dependencies

- **Required:** `architect` skill (for Phase 1 evaluation)
- **Optional:** `learn-by-mistake` (error memory), `post-run-analysis` (enhanced Phase 7)

## Usage

```
/founder-mode "Build a task management API with natural language input"
/founder-mode "./my-existing-project"
/founder-mode resume
```

## Crash Recovery

State is persisted to `.founder/state.json` after every phase and gate decision. If your session crashes, run `/founder-mode resume` to pick up exactly where you left off — including mid-gate crashes.
