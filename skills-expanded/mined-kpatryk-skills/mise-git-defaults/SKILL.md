---
name: mise-git-defaults
description: >
  Add shared git defaults via a mise enter hook in the current repository's
  mise config. Use when the user mentions mise hooks, mise enter hook, git
  defaults via mise, blame.ignoreRevsFile, diff.algorithm histogram,
  merge.conflictstyle zdiff3, rerere, fetch.prune, or standardizing git config
  across clones in a repo using mise.
license: MIT
---

# mise-git-defaults

Configure team git defaults via an idempotent `[hooks]` enter block in the
current repository's mise config. All inspection, file patching, and
verification are handled by the Python scripts in `scripts/`.

**Requires:** git (≥2.37 recommended), python3 (≥3.11), mise (≥2026.6.6 or
`experimental = true`), POSIX sh.

Run scripts by their absolute path under this skill's directory (the `scripts/`
folder next to this `SKILL.md`), e.g.
`python3 <skill-dir>/scripts/inventory.py --json`, with CWD set to the target
repository. Do not use a relative `scripts/...` path from the repo root — the
skill may be installed globally while it operates on the local repo.

## Rules

- **Shared file at repo root** — targets the first existing file at repo root
  among `mise.toml`, `.mise.toml`, `.config/mise.toml`, `.mise/config.toml`, or
  `mise/config.toml`. Only target personal/local configs (`mise.local.toml` / `.mise.local.toml`)
  via `--local` when explicitly requested.
- **Git work tree only** — abort if outside a git work tree.
- **Merge, never overwrite** — preserve existing `[hooks]`, enter commands,
  and any manual `--local` git overrides; bump `mise.gitDefaultsVersion` only
  when missing keys are added so the hook skips re-running on repeat entries.
- **Local scope only** — every git setting is written with `--local`.
- **Clean tree required** — before any changes, `git status --porcelain` must show
  no working-tree or staged changes. Otherwise abort with a concise message to
  review, stash, or commit existing changes before re-running the skill.
- **Commit only if changed and green** — create a single commit with message
  `chore(mise): add shared git defaults via enter hook` only when Patch reports
  a change (new/updated target file or newly created `.git-blame-ignore-revs`)
  and Verify passes. A Verify failure after Patch means the patch broke
  something (or exposed invalid pre-existing config) — commit nothing, report
  the failure, and fix instead. Stage the touched files with `git add -f`
  (force, since a shared target may be gitignored); otherwise commit nothing.

## Workflow

### 1. Inventory (read-only)

First verify a clean tree: `git status --porcelain` must be empty — abort
otherwise per Rules. Then run `<skill-dir>/scripts/inventory.py --json` (pass `--minimal`, `--local`, or `--file`
if applicable). Confirm git work tree, check mise / git versions, inspect
existing config files and `.git-blame-ignore-revs`, and capture the initial
local git config snapshot for final reporting. Warn if mise is older than
2026.6.6 without `experimental = true`, or if a shared target file is
gitignored.

### 2. Patch

Run `<skill-dir>/scripts/patch_mise.py --json` (with `--minimal` for the first four entries
up through `rerere.enabled`, `--local` for personal config,
`--skip-ignore-revs` to skip creating `.git-blame-ignore-revs`, `--file` to
override target, or `--dry-run` to preview). Unless `--local` or
`--skip-ignore-revs` is set, the script also creates `.git-blame-ignore-revs`
with a comment header if missing.

### 3. Verify

Run `<skill-dir>/scripts/verify.py --json` (matching `--minimal`, `--local`, or `--file`).
It validates TOML and POSIX `sh -n` syntax, runs `mise trust` and
`mise config ls` if mise is installed, executes the hook once in the repo root
(since `mise trust` does not execute enter hooks), and confirms all expected
keys are present in local git config. Pass `--no-exec` for a dry check that
skips executing the hook (no `git config` writes).

### 4. Commit and report

If Patch reported no change or Verify failed, commit nothing. Otherwise
force-stage only the target file and `.git-blame-ignore-revs` if the skill
created it (`git add -f`, since a shared target may be gitignored), and
create a single commit with the message from Rules. Then summarize the target file, whether `.git-blame-ignore-revs` was
created, which keys were newly added vs. already present, and any warnings.
