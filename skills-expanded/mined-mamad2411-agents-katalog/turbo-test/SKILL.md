---
name: turbo-test
description:
  Run the full turbo-themes build and test pipeline. Use when asked to build,
  test, lint, or validate the turbo-themes project. Includes example projects
  by default.
---

# Turbo-Themes Test Pipeline

Run the full build and test pipeline for turbo-themes. This project has a
multi-stage pipeline where later stages depend on earlier outputs.

**Do NOT use `uv run lintro tst`** for this project — it does not cover the
full turbo-themes pipeline (examples, E2E, site build).

## Full Pipeline (default)

When `/turbo-test` is invoked with no arguments, run all stages in order:

```bash
# 1. Lint (fast fail — catches formatting/type issues early)
uv run lintro chk

# 2. Build core + packages
bun run build

# 3. Build example projects (depends on core build output)
bun run examples:build

# 4. Unit tests (~2000 tests across ~74 files, with coverage)
bun run test

# 5. Example E2E tests (~139 tests across example projects)
bun run examples:test
```

If any stage fails, stop and fix before continuing to the next stage.

## Subcommands

| Argument   | Stages                         | Use when...                  |
| ---------- | ------------------------------ | ---------------------------- |
| _(none)_   | All 5 stages                   | Full validation (default)    |
| `lint`     | Lint only                      | Quick formatting/style check |
| `build`    | Build + examples:build         | Verifying build works        |
| `unit`     | Unit tests only                | Running tests after a build  |
| `examples` | examples:build + examples:test | Validating example projects  |
| `quick`    | Lint + build + unit tests      | Fast check, skip examples    |

## Optional E2E Stages

These are NOT part of the default pipeline. Run when explicitly needed:

```bash
# Smoke tests
bun run e2e:smoke

# Visual regression tests (snapshots generated on Linux CI only)
bun run e2e:visual

# Accessibility audits
bun run e2e:a11y
```

**Note on visual regression:** Snapshots are generated on Linux CI. Local
failures on macOS are expected. Use the `maintenance-generate-snapshots.yml`
workflow to regenerate snapshots after visual changes.

## Rules

- **Lint before build** — catches issues early without waiting for compilation.
- **Build before examples:build** — examples depend on core package output.
- **Build before test** — some tests depend on build artifacts (tokens.json, CSS).
- **Always include examples** — example builds and tests are part of the standard
  pipeline, not optional extras. Do not skip them unless explicitly told to.
