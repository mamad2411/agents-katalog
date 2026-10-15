---
name: justfile
description: >-
  Create, edit, migrate, check, and inspect just/justfile runners. Use when
  changing justfiles, migrating Makefile/npm scripts to just, linting house-style
  justfiles, or discovering via just --list/--show/--dump. NOT for shell scripts
  (shell-scripter), shell conventions (shell-conventions), CI YAML
  (devops-engineer), Make mtime builds, Compose, or mise.
argument-hint: "[create|edit|migrate|check|discover] [target|description]"
license: MIT
user-invocable: true
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Justfile

Author and maintain Just task runners. House style matches this repo's root
`justfile`: `minimum-version` ≥ 1.55.0, `default-list`, `require()`,
`[default]` / `[doc]` / `[group]` / `[arg]`, prefer `[script]` for multi-line
bodies. Distill casey/Just principles; never paste third-party skill prose or
embed the casey README.

Load reference files on demand from the index below — do not load all at once.
Frontmatter is for discovery; references carry deep procedure.

## Permission posture

`write-scoped` — may write justfiles; read-only `just` inspect by default; ask
before destructive recipes, deleting a Makefile, or running side-effecting
recipes.

## Dispatch

| $ARGUMENTS | Mode |
| --- | --- |
| *(empty)* / `help` | Empty-args gallery |
| `create [description]` | Create |
| `edit [path\|recipe]` | Edit |
| `migrate [source]` | Migrate |
| `check [path]` | Check |
| `discover [query]` | Discover |
| Natural language about justfiles | Auto-detect |

### Auto-detection heuristic

1. Existing `justfile` / `Justfile` + modify/fix/rename → **edit**
2. "migrate" / Makefile / `package.json` scripts → just → **migrate**
3. "lint" / "check" / "fmt" / house-style audit → **check**
4. "list" / "show" / "what recipes" / dump → **discover**
5. New justfile or "add recipe" without existing file → **create**
6. Pure shell / CI YAML / Make build semantics / mise / Compose → refuse (see negatives)

### Empty args

When `$ARGUMENTS` is empty, show the mode gallery, posture line, critical rules
summary, and reference index. Do not invent a mutating default.

## Canonical vocabulary

Use these exactly (canonical terms):

| Term | Meaning |
| --- | --- |
| `write-scoped` | May write justfiles; ask before destructive runs/deletes |
| house style | This repo's justfile conventions (`default-list`, `[doc]`, `[script]`, …) |
| discover | Read-only inspect via `just --list` / `--show` / `--dump` |
| migrate | Map Makefile/npm task scripts into Just recipes |
| `[script]` | Multi-line script recipe attribute (never combine with recipe-level `@`) |
| opt-in gate | Create-mode confirmations before overwrite or side effects |

## Critical rules

1. **Version-first** — run `just --version` before using mid-2026 attributes; prefer ≥1.55.0.
2. **Quiet vs script** — never put `@` on a `[script]` recipe; use `@` only for line quieting.
3. **Prefer `[script]`** for multi-line shell; avoid fragile escaped multi-line recipes.
4. **No blind `--fmt`** — inspect with `--dump` / `--check` first; apply `--fmt` only with intent.
5. **Dry-run / inspect before side effects** — discover with `--list`/`--show` before running recipes that write, delete, or network.
6. **check.py-before-complete** — after skill or justfile edits in this repo skill, run `uv run python scripts/check.py` from `skills/justfile/` before declaring done.
7. **No secrets in justfiles** — use env / dotenv / user-owned secrets; never hardcode tokens.
8. **Ask before deleting Makefile** or other source runners during migrate.

## Operator contract

### `create`

1. Confirm target path; refuse overwrite without explicit approval.
2. Load [references/create.md](references/create.md) (includes opt-in gate).
3. Scaffold house-style settings + `[default]` list recipe + grouped docs.
4. Prefer `require("tool")` for hard deps; document optional tools.

### `edit`

1. Read the target justfile; run discover inspect if recipes unclear.
2. Load [references/edit.md](references/edit.md).
3. Preserve house settings; migrate Make-flavored `##` comment docs to `[doc]`.

### `migrate`

1. Inventory Makefile / npm scripts; map to recipes (see [references/migrate.md](references/migrate.md)).
2. Keep sources until user approves deletion.
3. Convert Make `##` help to Just `[doc]` / `default-list` — never keep Make comment-docs as the Just help system.

### `check`

1. Load [references/check.md](references/check.md).
2. `just --version`, then `--list` / `--dump` / `--check` as needed.
3. Report house-style gaps; do not auto-`--fmt` unless asked.

### `discover`

1. Load [references/discover.md](references/discover.md).
2. Prefer read-only: `--list`, `--show`, `--dump` (`--dump-format=json`), `--groups`.
3. Link casey manual for deep semantics: https://just.systems/man/en/

## When NOT to use

- Shell script generation → `shell-scripter`
- Shell convention-only edits → `shell-conventions`
- CI/CD workflow YAML → `devops-engineer`
- Make file-timestamp / pattern-rule builds (not task recipes)
- Docker Compose authorship
- Toolchain version management as the product → mise tooling

See [references/when-not-just.md](references/when-not-just.md).

## Reference index

| File | Use when |
| --- | --- |
| [references/discover.md](references/discover.md) | Inspect recipes with just CLI |
| [references/create.md](references/create.md) | New justfile + opt-in gate |
| [references/edit.md](references/edit.md) | Change existing recipes/settings |
| [references/migrate.md](references/migrate.md) | Makefile / npm → just |
| [references/check.md](references/check.md) | Lint / fmt-check / house-style audit |
| [references/when-not-just.md](references/when-not-just.md) | Scope refusals and redirects |
| [references/pitfalls.md](references/pitfalls.md) | Common Just footguns |
| [references/patterns.md](references/patterns.md) | House-style recipe patterns |

## Validation Contract

Run from this skill directory before declaring changes complete:

```bash
uv run python scripts/check.py
uv run python skills/skill-creator/scripts/audit.py skills/justfile/
uv run python skills/skill-creator/scripts/package.py skills/justfile --dry-run
```

`scripts/check.py` chains `validate_skill.py`, `validate_evals.py`, package
dry-run, and audit. Completion criteria:

1. `uv run python scripts/check.py` exits 0.
2. Audit grade **A** (≥90).
3. Package `--dry-run` reports portable with no errors.
4. No portable-CLI violations remain under this skill directory.

## Example Blocks

When `$ARGUMENTS` is empty, show:

- `/justfile`
- `/justfile help`
- `/justfile create <description>`
- `/justfile edit <path|recipe>`
- `/justfile migrate <Makefile|package.json>`
- `/justfile check [path]`
- `/justfile discover [query]`

State the `write-scoped` boundary (justfile writes OK; ask before destructive
recipe runs or Makefile deletion) and the validation command:

```bash
uv run python skills/justfile/scripts/check.py
```
