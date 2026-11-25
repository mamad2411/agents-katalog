---
name: formax-web-css-convergence-workflow
description: Use when changing web CSS/UI styling so requirements, state ownership, and acceptance checks are locked before edits to prevent rework churn.
---

# formax-web-css-convergence-workflow

## Goal
- Prevent repeated CSS rework by locking requirements before any style edits.
- Convert ambiguous visual requests into a concrete edit contract with explicit acceptance checks.
- Keep behavior stable while converging structure, naming, and styling.

Use this skill when the task involves:
- component styling or layout adjustments
- cross-file CSS + TSX class changes
- interaction visual states (hover/active/focus/selected)
- repeated back-and-forth UI tuning that needs convergence

## Intake Contract (Run Before Editing)
- Require this 8-line input contract (fill missing items by explicit assumptions, not guesswork):
1. Target model in one sentence (final visual geometry).
2. Non-goals / do-not-touch list.
3. State model (if any) and single source of truth.
4. Ownership boundary (main process vs renderer).
5. Acceptance criteria (what must be true, what must never appear).
6. Runtime matrix (command, platform, light/dark).
7. Iteration policy (single-axis change per pass).
8. Rollback point (which commit/file set is safe fallback).

## Where to change what
- Core styling surfaces:
  - `packages/web-reference-react/src/styles.css`
  - `packages/web-reference-react/src/css/theme.css`
- Core UI wiring:
  - `packages/web-reference-react/src/app/ui/AppShell.tsx`
  - `packages/web-reference-react/src/components/LeftRail.tsx`
  - `packages/web-reference-react/src/components/left-rail/SidebarItem.tsx`
- Browser bridge typing surface (when needed):
  - `packages/web-reference-react/src/vite-env.d.ts`
- Desktop main/preload ownership (only for stateful window-level visuals):
  - `packages/desktop-electron/src/main.ts`
  - `packages/desktop-electron/src/preload.ts`
  - `packages/desktop-electron/src/windowAppearanceState.ts`
- Scenario-specific construct (read only if task touches transparency):
  - `docs/contracts/web/window-transparency-construct.md`

## Patterns
1. Freeze-Then-Edit Pattern
- Restate final model first.
- Freeze non-goals (do not touch drag region, menu entries, unrelated text/copy).
- Only then open code.

2. Single-Axis Convergence Pattern
- Pass A: geometry/layers only.
- Pass B: color/opacity tokens only.
- Pass C: interaction/focus/hover only.
- Never mix all three in one pass.

3. State Ownership Lock Pattern
- If the task has window/app state coupling:
  - renderer does not invent business states
  - canonical state lives in the owner layer
  - pending UI must converge to canonical state

4. Evidence-Driven Pattern
- Use deterministic checks instead of eye-balling:
  - explicit before/after acceptance list
  - “must-not-see” artifact list
  - screenshot evidence when visual regressions are likely

## Tests to update
- Required baseline for CSS changes in web-reference:
  - `bun run test -- src/App.test.tsx` (in `packages/web-reference-react`)
- Required for desktop bridge/state shape changes:
  - `npm --prefix packages/desktop-electron run build:main`
- Required only for transparency scenario:
  - `bun run test:e2e -- e2e/window-transparency.evidence.spec.js --project=chromium` (in `packages/web-reference-react`)
- Required before commit in this repo:
  - `codex review --uncommitted -c model="gpt-5.4" -c model_reasoning_effort="medium" -c service_tier="fast"`

## Guardrails
- Do not change unrelated UI behavior while “just tuning CSS”.
- Do not rely on one environment result; verify against the declared runtime matrix.
- If acceptance criteria are unclear, ask for clarification before directional edits.
- Avoid speculative visual “patch layers” that do not belong to the target model.
- If user requests `cleanup-pass`/`返工收敛`, reduce churn only:
  - remove redundancy
  - unify naming/state shape
  - preserve behavior
