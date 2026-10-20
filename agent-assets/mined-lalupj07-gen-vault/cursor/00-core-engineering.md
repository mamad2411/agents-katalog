---
description: Core engineering standards for every project
globs:
alwaysApply: true
---

# Core Engineering

## Know the project first
- Detect the real stack from manifests before writing code: `package.json`, lockfiles, `pubspec.yaml`, `Cargo.toml`, `go.mod`, `pyproject.toml`, framework configs, `wrangler.*`, `Dockerfile`, CI workflows.
- Note the package manager (from the lockfile), lint/format/test tooling, and existing docs (`README`, `AGENTS.md`, project `.cursor/rules`). Follow them.
- Never apply guidance for a technology the project does not use.

## Before changing code
- Read the files you touch and trace the real flow end to end. Preserve working behavior.
- Make focused changes. Do not rewrite whole files, swap frameworks, or replace working dependencies without a stated reason.
- Do not "improve" unrelated code. Note problems you find instead of fixing them silently.

## Structure
- Separate concerns: data/content, API clients, domain logic, presentation, server handlers. Follow the project's existing folder conventions.
- Split a file when it holds unrelated responsibilities or grows past roughly 300 lines. Do not split cohesive code just to make files small.
- No abstraction until there are two or three real call sites. No speculative interfaces, factories, or config layers.
- DRY real logic, not coincidental similarity.

## Code
- Meaningful names that describe intent. Small functions that do one thing.
- Use the strongest type system available. TypeScript: no `any`, no non-null `!` on external data, narrow `unknown` at trust boundaries. Dart: sound null safety. Python: type hints on public functions.
- Handle errors explicitly. Never swallow errors; never show raw errors to users.
- Await or handle every async operation. No floating promises or unobserved futures.

## Dependencies
- Reuse what is installed before adding anything. New dependency only if the platform or stdlib cannot do it in a few lines. See `03-security.mdc` for vetting.

## Configuration and environments
- Config from environment variables or the platform's secret store. Client-exposed prefixes (`VITE_`, `NEXT_PUBLIC_`, `EXPO_PUBLIC_`, Flutter `--dart-define`) are public: never put secrets there.
- Keep `.env.example` (placeholders only) updated when adding config.
- Keep dev-only allowances (localhost origins, sandbox APIs, debug flags) out of production paths. Fail closed in production.

## Production readiness
- Run the project's lint, type-check, build and tests after changes. Fix new errors you introduce.
- No leftover debug logging or commented-out code blocks.
- Never claim "100% secure", "unhackable", "military-grade", or "completely secure". State the actual controls.
