---
name: formax-semantics-parity-workflow
description: Use when implementing or modifying behavior that must stay consistent across TUI and Web (mode/input/tool/replay/order). Require canonical semantics first, then TUI/Web adapters, then renderer-specific UI.
---

# formax-semantics-parity-workflow

## Goal

Use this skill when changing behavior that must stay consistent across TUI, app-server, and Web: mode, input lifecycle, tool sequencing, replay, or ordering.

## Read First

- `docs/contracts/semantics-contract.md`
- `docs/contracts/app-server-interaction-contract.md`
- `docs/frontend/app-server-ui-spec.md`
- `docs/contracts/interactive-input-contract.md` when input lifecycle changes

These docs are canonical. If stable cross-surface behavior changes, update them before or with code.

## Code Map

### 1) Semantic single source of truth
- `packages/core/src/features/semantics/*`
  - `canonicalEvents.ts`
  - `transcriptProjection.ts`
  - `modeSemantics.ts`
  - `replModeTransition.ts`
  - `turnInputBuilder.ts`
  - `inputStateMachine.ts`

### 2) App-server contract emit / restore
- `packages/core/src/app-server/turnRunner.ts`
- `packages/core/src/app-server/server.ts`
- `packages/core/src/app-server/threadStore.ts`
- `packages/core/src/app-server/store/sessionEventReader.ts`
- `packages/core/src/app-server/turn/inputStore.ts`

### 3) TUI adapter (renderer can differ, semantics cannot)
- `packages/core/src/features/repl/controller/send/send.ts`
- `packages/core/src/features/repl/controller/streaming/streaming.ts`
- `packages/core/src/features/repl/useReplController.ts`

### 4) Web adapter (renderer can differ, semantics cannot)
- `packages/web-reference-react/src/eventAdapters.ts`
- `packages/web-reference-react/src/App.tsx`
- `packages/web-reference-react/src/store.ts`
- `packages/web-reference-react/src/turnEventCursor.ts`

### 5) Canonical docs to keep in sync
- `docs/contracts/semantics-contract.md`
- `docs/contracts/app-server-interaction-contract.md`
- `docs/frontend/app-server-ui-spec.md`
- `docs/contracts/interactive-input-contract.md` when input lifecycle changes

## High-Signal Patterns

- Semantic-first implementation order:
  1. define contract / event shape / state transition
  2. update shared semantics
  3. update app-server emit / replay state
  4. update TUI and Web adapters
  5. update renderer-only UI last
- Ordering discipline:
  - `replaySeq` is the primary ordering key
  - `traceId/seq` are diagnostics and turn-local hints, not global order
  - on replay gap, rebuild from semantic baseline; do not keep stitching stale tails
- Tool semantics discipline:
  - keep `toolUseId -> toolName` sticky behavior in semantics / adapter path
  - never depend on UI copy to infer tool state
- Mode/input discipline:
  - mode is a semantic transition, not just a visual toggle
  - input lifecycle remains a finite-state machine, not ad-hoc UI flags

## Minimal Workflow

1. Define the event / state transition in canonical docs and the shared semantics layer first.
2. Update app-server emit / replay state so the semantics remain recoverable.
3. Update TUI and Web adapters to consume the shared semantics; update renderer-only UI last.
4. If `packages/core/src/features/repl/**` semantic-flow files move, run the REPL semantic gate before review.
5. Run the minimum regression set below, then review via `AGENTS.md`.

## Minimum Regression

- `bun run type-check`
- `bun run test -- packages/core/src/features/semantics`
- `bun run test -- packages/core/src/features/semantics/__tests__/projectionParity.test.ts`
- `bun run test -- packages/core/src/app-server/turnRunner.test.ts packages/core/src/app-server/server.test.ts packages/core/src/app-server/turn/inputStore.test.ts`
- `npm --prefix packages/web-reference-react run type-check`
- `npm --prefix packages/web-reference-react run test -- src/App.test.tsx src/store.test.ts src/turnEventCursor.test.ts src/toolEventNormalizer.test.ts`
- `bun run test:repl-semantic-gate` when `packages/core/src/features/repl/**` semantic-flow files change

For fixture selection and parity assertions, use `references/fixtures-checklist.md`.

## Guardrails

- Do not patch one renderer in isolation when the bug belongs to shared semantics.
- Do not add a second semantic state machine inside TUI or Web.
- Do not use UI text or copy as semantic-state input.
- Do not introduce new ordering rules outside the shared semantics layer.
- Do not call a parity change done until app-server, TUI, and Web consume the same semantic rule.
