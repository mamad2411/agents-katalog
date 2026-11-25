# Repository Guidelines

## Project Structure & Module Organization
- `src/` TypeScript source for the CLI.
  - `commands/` oclif commands (entry: `create-roads`).
  - `lib/` helpers (templates, validation, file ops, package manager, scaffolder).
  - `bin/` runtime shim used by the compiled CLI.
  - `index.ts` exports `run` for oclif.
- `templates/` app blueprints: `default` (SSR) and `spa` (SPA). These files are copied into new projects.
- `tests/` sample scaffolded project(s) for smoke testing; not a unit-test harness.
- `dist/` build output (generated). Do not edit.
- Root configs: `package.json`, `eslint.config.js`, `tsconfig.json`.

## Build, Test, and Development Commands
- `npm run build` — compile TypeScript to `dist/`.
- `npm run dev` — TypeScript watch mode.
- `npm run lint` / `npm run lint:fix` — lint and auto‑fix per repo rules.
- `npm test` — builds and prints test hints.
- `npm run test:default` — scaffold Default template into `test-project` (no install).
- `npm run test:spa` — scaffold SPA template into `test-project-spa` (no install).
- Example run after build: `node dist/bin/run.js my-app --template spa --skip-install`.

## Coding Style & Naming Conventions
- Language: TypeScript (ESM), Node >= 18.
- Indentation: tabs; Quotes: single; Semicolons: required; EOL: unix; Max line length: 125.
- Filenames: kebab-case for modules (e.g., `project-scaffolder.ts`); classes PascalCase; functions camelCase.
- Run `npm run lint:fix` before opening a PR.

## Testing Guidelines
- Primary validation is smoke testing via `npm run test:default` and `npm run test:spa`.
- `@oclif/test` is available but not wired; if you add unit tests, place them under `tests/` and update `package.json` scripts accordingly.
- Keep tests deterministic: prefer `--skip-install` to avoid network.

## Commit & Pull Request Guidelines
- Commits: short, imperative subject (e.g., "scaffold spa template options"). Conventional Commits are welcome.
- PRs: include a clear description, CLI examples of new/changed flags, and link related issues. Update `README.md` and template files when behavior changes.
- Required: build passes (`npm run build`) and lint passes (`npm run lint`). Do not commit `dist/` or generated test projects.

## Security & Configuration Tips
- Avoid editing `dist/` and files under `templates/` unless you are intentionally changing scaffolded output (mirror changes across `default` and `spa` when relevant).
- Do not introduce network calls into the CLI without user confirmation.
