---
name: setup-pre-commit-data
description: Set up pre-commit hooks for a data repo, covering SQL formatting and linting (SQLFluff), YAML linting, dbt metadata checks (dbt-checkpoint), and a destructive-SQL tripwire. Use when user wants to add pre-commit hooks, lint or format SQL at commit time, enforce model descriptions or tests before commit, or block destructive SQL from being committed.
---

# Setup Pre-Commit Hooks

Commit-time gates are static and warehouse-free. Anything that needs a warehouse connection (data tests, builds, compilation against live schemas) belongs in CI, not the hook.

## What This Sets Up

- **pre-commit** framework wired into `.git/hooks/pre-commit`
- **SQLFluff** fix + lint on SQL files
- **yamllint** on YAML configs
- **dbt-checkpoint** metadata gates (descriptions, declared tests, `ref()`/`source()` discipline), dbt repos only
- **Destructive-SQL tripwire**: a local hook that fails the commit on `DROP` / `TRUNCATE` / bare `DELETE`

## Steps

### 1. Detect the toolchain

Check for `dbt_project.yml` (a dbt repo, so include the dbt-checkpoint block in step 3). Check Python dependency management: `uv.lock` (uv), `poetry.lock` (poetry), `requirements*.txt` (pip). Use whichever is present. Default to plain `pip` if unclear.

### 2. Install pre-commit

Add `pre-commit` to dev dependencies with the detected tool. Confirm `pre-commit --version` runs.

### 3. Create `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-added-large-files
      - id: no-commit-to-branch

  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 4.2.2
    hooks:
      - id: sqlfluff-fix
      - id: sqlfluff-lint

  - repo: https://github.com/adrienverge/yamllint
    rev: v1.38.0
    hooks:
      - id: yamllint

  # dbt repos only. These hooks read target/manifest.json: dbt-parse must run first.
  - repo: https://github.com/dbt-checkpoint/dbt-checkpoint
    rev: v2.0.10
    hooks:
      - id: dbt-parse
      - id: check-model-has-description
      - id: check-model-has-tests
        args: ["--test-cnt", "1", "--"]
      - id: check-script-has-no-table-name
      - id: check-script-ref-and-source

  # Destructive-SQL tripwire: no stock linter has this rule.
  - repo: local
    hooks:
      - id: no-destructive-sql
        name: Block DROP/TRUNCATE in SQL
        language: pygrep
        entry: '(?i)\b(DROP\s+(TABLE|SCHEMA)|TRUNCATE\s+TABLE)\b'
        types: [sql]
      - id: no-bare-delete
        name: Block DELETE without WHERE (line-based, best-effort)
        language: pygrep
        entry: '(?i)\bDELETE\s+FROM\s+\S+\s*;?\s*$'
        types: [sql]
```

**Adapt**: Drop the dbt-checkpoint repo if there is no `dbt_project.yml` and tell the user. Drop `no-commit-to-branch` if the repo commits to main directly. Every `rev` must be an immutable tag or SHA, never a branch. The revs above were current mid-2026; resolve each repo's latest release tag at install time. The tripwire's `types: [sql]` matches only files the identify library tags as SQL, and `.sqlx` (Dataform) gets an empty tag set, so in Dataform repos override both tripwire hooks with `files: '\.(sql|sqlx)$'` and `types: [text]` (pre-commit sniffs unknown extensions as text at runtime).

### 4. Create `.sqlfluff` (if missing)

```ini
[sqlfluff]
templater = jinja
dialect = ansi
```

Set `dialect` to the warehouse dialect (`bigquery`, `snowflake`, and 28 supported in total as of 4.2.2). Keep `templater = jinja` in the hook even in dbt repos: the dbt templater needs the warehouse adapter installed and may need database access at compile, so official guidance is jinja for hooks and IDE, dbt templater for CI. The templater can only be set in this root config.

### 5. Create `.yamllint` (if missing)

```yaml
extends: default
```

Only create if no yamllint config exists. Add rule overrides only when the defaults are unworkable.

### 6. Install the hook

```bash
pre-commit install
```

This writes `.git/hooks/pre-commit`. Completion: that file exists.

### 7. Verify

- [ ] `.pre-commit-config.yaml` exists; every `rev` is a tag or SHA, not a branch
- [ ] `pre-commit run --all-files` completes (first run builds tool environments, slow once and cached after)
- [ ] Tripwire test: stage a scratch `.sql` file containing `DROP TABLE t;` and the commit must fail (the tripwire hooks only scan files pre-commit classifies as SQL, so a `.txt` scratch file proves nothing); then delete the file
- [ ] dbt repos: `dbt-parse` appears before every `check-*` hook in the config

### 8. Commit

Stage all changed/created files and commit with message: `Add pre-commit hooks (pre-commit + sqlfluff + dbt-checkpoint)`

This will run through the new pre-commit hooks: a good smoke test that everything works.

## Notes

- Data tests never run in the hook: they execute against the warehouse. Pre-merge code checks and in-flow data audits are separate test planes; the hook owns only the first.
- dbt-checkpoint hooks read `target/manifest.json`. A stale manifest is a false pass, which is why `dbt-parse` leads the block.
- SQLFluff ≥3.0: `fix` applies without prompting (`--force` is deprecated because its behavior became the default; `--check` restores the prompt) and skips files with parse errors.
- dbt-checkpoint was formerly `pre-commit-dbt`: old tutorials point at the dead repo name and a different hook set.
- Prefer a pure formatter? sqlfmt is Black-style, formats jinja without compiling, and pairs with SQLFluff-as-linter, the dbt-recommended split.
