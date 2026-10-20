# Copilot instructions for cocogen

## Mission
Build `cocogen`: an `npx`-runnable generator that reads TypeSpec (`.tsp`) and scaffolds runnable Microsoft Copilot connector projects.

## Hard constraints
- **All generator code must be written in TypeScript.**
- Prefer Node.js libraries and patterns.
- Keep the codebase small, composable, and testable.

## Runtime & packaging
- Target **Node 22 LTS**.
- Use **npm**.
- Use **ESM**.

## CLI requirements
- CLI must be **colorful** and friendly:
  - Use color for success/warn/error states.
  - Respect `NO_COLOR=1`.
  - Errors must be actionable (what failed + how to fix).
- Prefer a clean command structure consistent with docs/architecture.md.

## CLI libraries
- Use `commander` for command parsing.
- Spinners are OK (prefer `ora`), but must degrade cleanly in non-TTY/CI and when `NO_COLOR=1`.

## Output requirements
- Generated project(s) must be runnable.
- CSV ingestion must be implemented behind a swappable datasource interface.
- People connectors (preview) support must follow docs/architecture.md rules.
- **Generated files should come from EJS templates** under `src/init/templates/**` and be rendered via `renderTemplate` (avoid large inline string assembly for emitted files).

## Coding style
- Prefer explicit names over cleverness.
- Avoid one-letter identifiers except in tiny lambdas.
- Avoid adding comments unless necessary; prefer readable code.
- Prefer functional-ish composition for parsing/validation, but keep ergonomics.

## Dependencies
- Prefer small dependencies; avoid heavy frameworks.
- OK to use:
  - `picocolors` or `chalk` for color
  - `commander` for CLI parsing
  - `@inquirer/prompts` for prompts
  - `ora` for spinners
  - `zod` for validation (if helpful)
  - `vitest` for tests

## Documentation
- Update docs/architecture.md when behavior changes.
- If you add new CLI flags/commands, document them.
- Maintain CHANGELOG.md for consumer-facing changes (features, fixes, changes, breaking changes).
- Do not log release notes in AGENT-TASKS.md.

## Agent task tracking
- Maintain **AGENT-TASKS.md** as a continuously updated task log (add/complete/reshuffle as work progresses).

## Source control
- Use standardized commit messages (prefer **Conventional Commits**: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`).
- Commit when a feature is done (coherent + runnable), not mid-refactor.
- When relevant, include smart keywords like `fixes #123` to link work to issues.
