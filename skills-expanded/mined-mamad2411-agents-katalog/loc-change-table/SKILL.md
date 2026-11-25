---
name: loc-change-table
description: Count line changes in one folder and all subdirectories since a given date, grouped by git repository and file category. Use when the user asks for LOC changes, line changes, churn, diff stats, changed lines, or repo-by-category tables since a date.
---

# LOC Change Table

Use this skill when the user wants a repo-by-category table of line changes under a folder since a date.

## How to run

The bundled script is the single source of truth. Run it and present its output verbatim. Do not hand-compute counts, and do not substitute ad-hoc `git log`/`git diff` one-liners — they count differently and produce inconsistent results.

1. Resolve the inputs:
   - Folder: use the user's path, or the current working directory if none is given.
   - Date: required. If the user did not give one, ask. Accept any `git`-compatible form, such as `2026-06-01`, `last Friday`, or `2 weeks ago`.
2. Run:

   ```bash
   python3 scripts/loc_change_table.py <folder> --since <date>
   ```

3. Present the Markdown table the script prints, then relay its trailing notes (hidden repos, empty-tree warnings, skipped repos). Do not drop the notes — the empty-tree warning is how a wrong date is caught.

### Flags

- `--include-uncommitted` — also count working-tree changes (only when the user asks for uncommitted work).
- `--include-binary` — count each changed binary file as 1 line.
- `--show-empty` — also list repos with zero changes (hidden by default).

## Behavior

- Counts `added + deleted` per file from `git diff --numstat`, diffing `HEAD` against the last commit before `--since`.
- If no commit predates the date, the repo is diffed against the empty tree (full history) and flagged in a note — surface that note so inflated totals are visible.
- Each nested git repository is its own row; repos with no changes are hidden; rows are sorted by total descending.
- Repos with no commits or git errors are reported under "Skipped".

## Categories

Script defaults (precedence: `generated`, `tests`, `docs`, `config`, `frontend`, `backend`, `other`):

- `frontend`: `.js/.jsx/.ts/.tsx/.svelte/.vue/.css/.scss/.sass/.less/.html`
- `backend`: `.py/.go/.rs/.java/.kt/.cs/.rb/.php`
- `tests`: paths with `test/tests/spec/specs/__tests__`, or `.test.*` / `.spec.*` files
- `config`: `.json/.yaml/.yml/.toml/.ini/.env`, Dockerfiles, Makefiles, lockfiles, CI folders
- `docs`: `.md/.mdx/.rst/.txt`, `docs/`, `README`, `CHANGELOG`
- `generated`: `generated/gen/dist/build`, coverage, snapshots, lockfiles
- `other`: anything else
