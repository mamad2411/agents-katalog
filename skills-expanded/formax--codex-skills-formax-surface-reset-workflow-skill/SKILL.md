---
name: formax-surface-reset-workflow
description: Use when changing REPL clear/reset/resume/surface behavior (onClearTerminal, transcriptSeq remount, Ink Static paths, Ctrl+O/Ctrl+E transitions). Enforces single-owner reset transaction and prevents black-screen/flicker/duplicate-row regressions.
---

# Formax Surface Reset Workflow

## Goal

Use this skill when changing REPL clear/reset/resume behavior or any transcript surface transition that can remount `Static`.

## Read First

- `docs/contracts/transcript-surface-contract.md`
- `docs/runbooks/repl-surface-debugging.md`
- `docs/contracts/invariants.md` when ownership or sequencing is unclear

These docs are canonical. If stable surface behavior changes, update them before or with code.

## Code Map

- Reset helpers / queue owner:
  - `replaceTranscript`
  - `queueTranscriptSurfaceReplace`
  - `resetTranscriptSurface`
  - `queueTranscriptSurfaceReset`
  - `surfaceOpQueueRef`
- High-risk flows:
  - `packages/core/src/features/repl/controller/ui/`
  - `packages/core/src/features/repl/controller/session/`
  - `packages/core/src/features/repl/useReplController.ts`
  - `packages/core/src/screens/repl/`
  - `packages/core/src/runtime/bootstrap/runLegacyCli.tsx`
- Call sites to watch:
  - `onClearTerminal`
  - `clearTerminal`
  - `resetInkStaticOutputForStdout`
  - `transcriptSeq` remount behavior in `ReplTranscript` / `ExpandedReplTranscript`

## Trigger Conditions

Use this skill whenever the change touches any of:
- `/resume`, `/clear`, compact boundary transitions
- Ctrl+O / Ctrl+E transcript view switches
- `onClearTerminal`, `clearTerminal`, or `resetInkStaticOutputForStdout`
- `replaceTranscript`, `queueTranscriptSurfaceReplace`, `resetTranscriptSurface`, `queueTranscriptSurfaceReset`, or `surfaceOpQueueRef`
- files under `packages/core/src/features/repl/controller/ui/`, `packages/core/src/features/repl/controller/session/`, `packages/core/src/features/repl/useReplController.ts`, `packages/core/src/screens/repl/`, or `packages/core/src/runtime/bootstrap/runLegacyCli.tsx`

## Minimal Workflow

1. Identify the exact path (`/resume`, `/clear`, Ctrl+O / Ctrl+E, compact boundary, etc.).
2. Route it through `replaceTranscript` / `resetTranscriptSurface` instead of local clear / remount sequencing.
3. Treat reset as one transaction, not scattered side effects.
4. Add or extend regression tests for ordering and surface reset ownership.
5. Run the minimum regression set below and at least one real surface smoke path.

## Minimum Regression

- `bun run test -- packages/core/src/features/repl/controller/ui/surfaceReset.test.ts`
- `bun run test -- packages/core/src/features/repl/useReplController.test.tsx -t "resume|clear|compact"`
- `bun run test -- packages/core/src/screens/repl/surfaceSmoke.test.tsx`
- `bun run type-check`
- If change touches compact / expanded toggles broadly: `bun run test:surface-screen-model`

## Guardrails

- Keep one surface owner; do not add a second independent clear / remount path.
- Do not stack `replInstance.clear()` and ANSI clear in legacy paths unless ownership is explicit and serialized.
- Do not accept a Vitest-only fix without running a real surface smoke path.

## References

- `docs/pitfalls/summary.md` sections covering `/clear`, compact + Ctrl+O, and resume black-screen regressions
- `docs/pitfalls/repl-transcript-surface-handoff-pitfall.md`
- `docs/pitfalls/repl-transcript-static-rootcause.md`
