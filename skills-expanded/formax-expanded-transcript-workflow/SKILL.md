---
name: formax-expanded-transcript-workflow
description: Use when implementing/debugging Ctrl+O Expanded Transcript (second view) and thinking persistence in the REPL.
---

# formax-expanded-transcript-workflow

## Goal

Use this skill when changing `Ctrl+O` expanded transcript behavior, thinking persistence, or compact / expanded projection boundaries in the REPL.

## Read First

- `docs/contracts/transcript-surface-contract.md`
- `docs/contracts/semantics-contract.md`
- `docs/runbooks/repl-surface-debugging.md` when the change can affect clear / remount behavior

These docs are canonical. If stable expanded-transcript behavior changes, update them before or with code.

If the change touches clear / remount ownership directly, also use `formax-surface-reset-workflow`.

## Code Map

- Key handling: `packages/core/src/screens/repl/hotkeys.ts`
- View wiring + footer: `packages/core/src/screens/REPL.tsx`
- Compact projection: `packages/core/src/screens/repl/compactProjection.ts`
- Transcript rendering: `packages/core/src/screens/repl/transcript.tsx`
- Thinking persistence: `packages/core/src/features/repl/controller/streaming/streaming.ts`
- Expanded Transcript panels: `packages/core/src/screens/repl/panels.tsx`
- Compact command lifecycle: `packages/core/src/features/repl/controller/send/send.ts`
- Surface reset owner: `packages/core/src/screens/repl/useSurfaceTransitionManager.ts`

## High-Signal Patterns

- No fake thinking:
  - `thinking_delta` is the only source of truth
  - never synthesize thinking rows from timers or summaries
- Avoid `Static` hacks for toggles:
  - `Static` is append-only; if content must disappear, use reset / remount ownership instead of trying to "unrender" it
- One footer:
  - prefer a single global footer; avoid per-panel footer duplication
- Compact ordering contract:
  - keep `banner -> summary (expanded only) -> > /compact ... -> compact subline`
- UI vs LLM orthogonality:
  - transcript slicing and `ui.kind` remain independent from prompt-history packing and reminder injection

## Minimal Workflow

1. Lock the semantic source first: `thinking_delta` persistence and transcript projection rules before renderer polish.
2. Keep default transcript low-noise and Expanded Transcript read-only.
3. Preserve compact / expanded ordering before adjusting footer or panel layout.
4. If clear / remount logic changes, route through the shared surface reset path instead of local `Static` workarounds.
5. Run the regression set below before review.

## Minimum Regression

- `bun run test -- packages/core/src/screens/repl/compactProjection.test.ts packages/core/src/screens/repl/expandedTranscript.test.tsx packages/core/src/screens/repl/hotkeys.test.tsx`
- `bun run test -- packages/core/src/screens/repl/surfaceSmoke.test.tsx`
- `bun run test:surface-screen-model`
- `bun run type-check`

## Guardrails

- Do not introduce synthetic thinking or show thinking when the model did not emit `thinking_delta`.
- Do not let `Ctrl+O` steal input while prompt mode or overlays are active.
- Do not move header / messages outside `Static` to “fix” duplication; solve ownership and remount boundaries instead.
- Expanded Transcript stays read-only; do not quietly turn it into an interactive input surface.
