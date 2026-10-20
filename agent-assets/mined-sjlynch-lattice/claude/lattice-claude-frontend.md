# frontend

Vite + React + TypeScript frontend package. `src/` is the source of truth;
`src/CLAUDE.md` holds the rules for all UI code; `src/MAP.md` (read on demand)
says which file owns what.

## Notes

- `README.md` is a brief package note for humans.
- Runtime UI is under `src/`; feature subdirectories often carry their own
  `CLAUDE.md` files with local conventions.
- Styling is hand-written CSS under `src/styles/` and aggregated from
  `src/index.css`; do not introduce MUI/styled-components.

## Scripts

- `npm run dev` — Vite dev server; the user owns this process.
- `npm run build` — TypeScript build plus Vite bundle.
- `npm test` — node:test via `tsx` over `src/__tests__/*.test.ts`, through the
  compact reporter `../scripts/testReporter.mjs` (failures + one summary line).
- `npm run test:file -- <file>` — one or more test files.

## Validation

- Type-check: `npm run typecheck` (`tsc -b`, which includes the tests via
  `tsconfig.test.json`) from `frontend/`, or the root `npm run typecheck`.
- Tests: `npm test` from `frontend/`.
