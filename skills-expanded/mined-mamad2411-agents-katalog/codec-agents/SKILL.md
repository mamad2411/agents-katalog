# Repository Guidelines

## Project Structure & Module Organization
Source lives under `src/` with `main.tsx` bootstrapping the React tree and `App.tsx` wiring routes. Shared building blocks sit in `src/components`, routed views in `src/pages`, helpers in `src/utils`, and static media in `src/assets`. Integration-style tests live under `src/test`. Public-facing assets (favicon, robots, static data) belong in `public/`, and production artifacts are emitted to `dist/` via the Vite pipeline. TypeScript and tooling configuration is centralized in the root (`tsconfig*.json`, `vite.config.ts`, `biome.jsonc`).

## Build, Test, and Development Commands
- `npm ci` installs the exact dependency graph locked in `package-lock.json`.
- `npm run dev` launches the Vite dev server with hot module reload at [http://localhost:5173](http://localhost:5173).
- `npm run build` performs a TypeScript project build (`tsc -b`) followed by `vite build` to produce `dist/` assets.
- `npm run preview` serves the build output locally for smoke testing.
- `npm run qa` runs Biome in CI mode; `npm run qa-fix` applies formatting/lint fixes.
- `npm run test` executes the Vitest suite (jsdom environment) and should pass before pushing.

## Coding Style & Naming Conventions
The codebase is TypeScript-first with ES modules and React 19 functional components. Maintain 2-space indentation, prefer arrow components, and keep files JSX/TSX-only when they render UI. Follow the existing naming patterns: PascalCase for components, camelCase for utilities, and kebab-case for asset files. Tailwind 4 utility classes drive styling; avoid ad-hoc CSS unless it belongs in `src/index.css`. Run Biome (`npm run qa`) before submit to ensure formatting, lint, and static checks stay consistent.

## Testing Guidelines
Vitest plus Testing Library covers unit and interaction tests. Co-locate spec files under `src/test` or beside the implementation as `*.test.ts(x)` when it improves readability. Write descriptive `describe` blocks and prefer explicit user-centric assertions (`screen.getByRole`). Aim for coverage on new logic and guards; add regression tests for every bug fix. Use `npm run test -- --runInBand` when debugging flaky tests locally.

## Commit & Pull Request Guidelines
Commits use imperative, concise subjects (e.g., `fix new biome complaints`) and reference PR numbers when merged. Keep commits scoped to one concern. Pull requests must describe the motivation, outline testing that was performed (`npm run qa`, `npm run test`), and link any tracked issues. Include before/after screenshots for UI-facing updates and mention any config or dependency shifts. Request at least one reviewer before merging.
