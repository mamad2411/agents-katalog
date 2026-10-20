# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pnpm dev          # start dev server
pnpm build        # tsc -b + vite build
pnpm test         # vitest run (single pass)
pnpm test:watch   # vitest (watch mode)
pnpm lint         # eslint
```

Run a single test file:
```bash
pnpm vitest run src/pipeline/replacement/DirectReplacement.test.ts
```

Always use **pnpm** — never npm.

## Architecture

The app is a fully static React + Vite + TypeScript SPA with no backend. All state lives in the browser; mappings are persisted to `localStorage` under the key `pseudonymizer_mappings_v1`.

### Three-stage pipeline (`src/pipeline/`)

Follows the Detection → Generation → Replacement model from arxiv.org/html/2502.15233v1. Each stage is an interface so implementations can be swapped independently.

- **`pipeline/types.ts`** — all pipeline interfaces (`DetectionStrategy`, `GenerationStrategy`, `ReplacementStrategy`, `IPipeline`, etc.)
- **`pipeline/Pipeline.ts`** — orchestrator; `pseudonymize()` chains all three stages, `depseudonymize()` runs only Replacement with swapped `source`/`target` pairs
- **`pipeline/replacement/DirectReplacement.ts`** — the core algorithm: sorts pairs longest-first, replaces each source with a null-byte placeholder token (prevents double-replacement), then resolves tokens to targets. Direction-agnostic — the caller decides which is source and which is target.
- Detection and generation are currently manual stubs (`ManualDetection` returns `[]`, `ManualGeneration` returns `''`); the UI drives both stages instead.

### Data model (`src/types/index.ts`)

`PiiMapping` is the central record: `{ id, realValue, pseudonym, category, caseSensitive }`. A `MappingSet` wraps an array of these with `{ version: 1, name, mappings[] }`. The version field exists for forward-compatible import/export.

### State and hooks (`src/hooks/`)

- **`useMappings`** — owns the `MappingSet`, auto-saves to localStorage on every change via `useEffect`
- **`usePipeline`** — instantiates `Pipeline` once (module-level singleton), exposes memoized `pseudonymize` and `depseudonymize` callbacks
- **`useTextSelection`** — tracks textarea selection; used by `TextPanel` to trigger the inline mapping popup

### TypeScript constraints

- `erasableSyntaxOnly: true` — constructor parameter shorthand (`private x: T`) is **not allowed**; declare properties explicitly
- `noUnusedLocals` / `noUnusedParameters` — prefix intentionally unused params with `_`
- `vite.config.ts` imports `defineConfig` from `vitest/config` (not `vite`) so the `test` config key is recognized
- vitest runs with `globals: true` — `describe`/`it`/`expect` are available without imports in test files
