---
name: initinator-manager
description: Guides agents maintaining the initinator AI-assets manager. Use when working with initinator, AI-assets, Cursor or Spec Kit project initialization, roles, rules, skills, extensions, presets, CLI commands list/search/apply/status/validate, dry-run behavior, conflict handling, bug fixes, improvements, tests, or commits for this manager.
---

# Initinator Manager

## Purpose

Use this skill when the user asks to operate, debug, improve, test, document, or
commit changes for `initinator`: a local Python CLI that selects AI-assets from a
local library and installs them into Cursor and Spec Kit projects.

The agent should be proactive: when it finds a clear bug, contract mismatch,
missing test, confusing behavior, or low-risk improvement, it should explain the
issue and propose a concrete fix. If the user has asked for implementation, the
agent may apply the fix, update tests/docs, and verify the result.

## Repository Context

- Runtime: Python 3.13.
- Packaging: `pyproject.toml`, console script `initinator = "initinator.cli.main:main"`.
- CLI entry point: `src/initinator/cli/main.py`.
- Core layers:
  - `src/initinator/domain/`: models, search, selection plan.
  - `src/initinator/services/`: library, presets, Cursor integration, Spec Kit integration, readiness report.
  - `src/initinator/adapters/`: filesystem safety, YAML registry, JSON manifest.
  - `tests/unit/`, `tests/integration/`, `tests/contract/`.
- Design artifacts:
  - `README.md`
  - `specs/001-ai-project-initializer/spec.md`
  - `specs/001-ai-project-initializer/plan.md`
  - `specs/001-ai-project-initializer/tasks.md`
  - `specs/001-ai-project-initializer/contracts/cli-contract.md`
  - `specs/001-ai-project-initializer/quickstart.md`

## Core Workflow

1. Read the relevant context before changing behavior:
   - For user-facing CLI behavior, read `README.md` and `contracts/cli-contract.md`.
   - For scope or product intent, read `spec.md`, `plan.md`, and `tasks.md`.
   - For implementation, inspect the narrow module and matching tests first.
2. Classify the request:
   - CLI parsing or exit code: start in `src/initinator/cli/main.py`.
   - Selection, conflicts, or target paths: start in `src/initinator/domain/selection_plan.py`.
   - Library indexing or metadata: start in `LibraryManager` and YAML adapter.
   - Cursor or Spec Kit file writes: start in the corresponding integration manager.
   - Status/readiness output: start in `ReadinessReporter`.
3. Prefer test-first changes for bugs and contract behavior.
4. Keep changes small and aligned with the existing layer boundaries.
5. After implementation, run the narrowest useful tests, then broaden if the risk warrants it.

## Commands

Common development commands:

```bash
uv sync --dev
uv run initinator list --library ~/ai-assets --type role
uv run initinator search python --library ~/ai-assets --type skill --json
uv run initinator --library ~/ai-assets --dry-run
uv run initinator apply python-ddd --select speckit-russian-preset --library ~/ai-assets --yes
uv run initinator status
```

Test commands:

```bash
uv run pytest tests/unit
uv run pytest tests/integration
uv run pytest tests/contract
uv run pytest tests/unit tests/integration tests/contract
```

Use targeted test files while iterating, then run the relevant suite before
finishing.

## Proactive Fixes And Improvements

Propose or implement an improvement when one of these is true:

- The implementation contradicts `contracts/cli-contract.md`.
- `--dry-run` can write files or produce misleading output.
- Conflict handling can overwrite files without explicit `--replace`.
- `--skip` or `--replace` semantics are ambiguous or untested.
- A command returns the wrong exit code for `blocked`, `failed`, or invalid library cases.
- JSON output shape drifts from the contract.
- A user-facing change is missing README or quickstart coverage.
- A bug fix lacks a regression test.

When suggesting an improvement, include the observed issue, why it matters, and
the smallest concrete change that would fix it.

## Guardrails

- Preserve offline-first behavior. Do not add remote catalog, package updates, or uninstall behavior unless the user explicitly asks.
- Never make existing project file overwrites implicit. Existing file replacement must remain explicit through `--replace PATH`.
- Preserve project-root path safety and avoid shell-specific assumptions in domain logic.
- Keep `argparse` as the CLI approach unless the user asks for a framework migration.
- Do not introduce broad abstractions for one local behavior change.
- If public CLI behavior changes, update contract tests and user-facing docs.
- Keep human-readable Spec Kit artifacts in Russian for this repository.

## Commit Workflow

Make commits only when the user explicitly asks.

Before committing:

1. Run `git status` to see modified and untracked files.
2. Run `git diff` for the files that may be committed.
3. Run `git log` to match the repository's commit message style.
4. Stage only relevant files. Do not include unrelated local changes.
5. Do not commit secrets, local credentials, `.env` files, or unrelated generated output.

Commit message guidance:

- Use a short, imperative summary.
- Focus on the purpose of the change.
- Keep the message consistent with recent repository commits.

After committing, run `git status` and report the commit hash plus any remaining
uncommitted changes.
