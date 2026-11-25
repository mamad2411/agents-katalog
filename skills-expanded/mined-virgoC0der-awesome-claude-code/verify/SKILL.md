---
name: verify
description: Run the project's full verification suite (format, lint, typecheck, tests, architecture) using commands declared in .harness/project.md
---

Run the project's verification suite, using the commands declared in `.harness/project.md`. This skill is project-agnostic — it does not assume any specific language or tooling.

## Step 1: Load the project config

```bash
ls .harness/project.md 2>/dev/null
```

If the file exists, read it and use the **Commands** section verbatim.

If it does not exist:
- Detect the project type from manifest files (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, etc.).
- Fall back to conventional defaults (e.g. `pnpm test`, `go test ./...`, `cargo test`, `poetry run pytest`).
- Tell the user that `.harness/project.md` is missing and recommend creating one (the `harness` skill can bootstrap it).

## Step 2: Run each check

Execute, in this order, and report each:

| # | Check | Command (from project config) |
|---|---|---|
| 1 | Format | `format_check` |
| 2 | Imports / lint | `lint` |
| 3 | Type check | `typecheck` (skip if not defined) |
| 4 | Tests | `test` |
| 5 | Architecture compliance | rules from project config (see below) |

For the architecture check:
- If `Architectural Rules.layer_order` is declared, get the changed files (`git diff --name-only`) and confirm none import from a higher layer to a lower one. Use `Grep` over each changed file's imports.
- If `Architectural Rules.placement_rules` is declared, confirm new files satisfy each rule.
- If no rules are declared, run the universal check: no new circular imports.

## Step 3: Report

Output a single summary table:

| Check | Status | Details |
|---|---|---|
| Format | PASS / FAIL | <command output excerpt or "ok"> |
| Lint | PASS / FAIL | … |
| Typecheck | PASS / FAIL / SKIP | … |
| Tests | PASS / FAIL / SKIP | <X passed, Y failed, Z skipped> |
| Architecture | PASS / FAIL / N/A | <rule violated, if any> |

For any failure, list the specific files / lines and the suggested fix.

Treat **SKIP** as legitimate when a category isn't configured (e.g. no typecheck command declared). Don't claim PASS when something was skipped — be explicit.
