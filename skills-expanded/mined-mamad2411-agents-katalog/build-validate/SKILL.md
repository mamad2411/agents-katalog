---
name: build-validate
description: Use when a task needs build, test, lint, type-check, static-analysis, sanitizer, or runtime validation selection and execution. Trigger for implementation, bugfix, refactor, build/tooling, API or ABI, parser, interop, packaging, concurrency, generated-code, or security-sensitive changes where Codex must decide the smallest correct validation path. Do not trigger for pure explanation, brainstorming, or review-only requests that do not require running checks.
---

# Build Validate

Choose and run the smallest correct validation path for the current change. Treat repository-native commands and repo-specific docs as the source of truth.

## Procedure

1. Inspect the repo before choosing commands.
   - Read the nearest `AGENTS.md`.
   - Read `docs/codex/build-and-test.md` when present.
   - Check canonical project files such as `README.md`, CI workflows, `pyproject.toml`, `Makefile`, `CMakeLists.txt`, `CMakePresets.json`, `meson.build`, test configs, and lint/type-check configs.
2. Classify the change.
   - Narrow local validation: touched code is isolated and the contract surface is small.
   - Full validation: change affects broad flows or multiple subsystems.
   - Escalated validation: any API, ABI, parser, interop, security-sensitive, build-system, packaging, concurrency, migration, deployment, or generated-code impact.
3. Prefer canonical repo commands over guesses.
   - If the repo defines a build, test, lint, type-check, or static-analysis path, use it.
   - Only fall back to generic language-tool commands when the repo does not define a canonical path.
4. Run checks that match the change.
   - For narrow changes, run the smallest command set that gives real evidence.
   - For escalated changes, expand validation across affected layers and interfaces.
   - Include sanitizers or focused runtime checks when the repo supports them and the change justifies them.
5. Report facts only.
   - Never say a check ran if it did not.
   - Separate passed, failed, blocked, and unverified items explicitly.

## Validation Selection Rules

- Use narrow local validation for isolated logic or leaf-module changes with stable interfaces.
- Use full validation when multiple modules, user-visible behavior, orchestration paths, or broad refactors are involved.
- Escalate beyond local checks when contracts or operational assumptions may have changed, especially at language boundaries or trust boundaries.
- If repository instructions conflict, follow the most specific applicable source of truth and state the assumption.

## Output Contract

- `Validation scope:` narrow local, full, or escalated.
- `Commands run:` exact commands actually executed.
- `Passed:` what succeeded.
- `Failed:` what failed, with the most relevant signal.
- `Not run:` checks that were expected but could not be executed, and why.
- `Remaining unverified:` behavior or risks still not covered by the run.
