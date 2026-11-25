---
name: precommit-standards
description: "Use when adopting pre-commit in a repo, auditing or editing a .pre-commit-config.yaml, or when a hook keeps rewriting generated files. The shipped baseline, hook install types, stage budgets, always-on hooks, excludes, pinning and a drift audit."
license: MIT
---

# Pre-commit standards

## The baseline template

This plugin ships the baseline at `${CLAUDE_PLUGIN_ROOT}/templates/.pre-commit-config.yaml`. Read
it before adopting or auditing a config: a repo enables the sections its file types need and
comments out the rest with a one-line reason. Without the template (for example on the web), work
from the rules below, or ask the user to paste the template or their config.

## Install every hook type the config uses

```yaml
default_install_hook_types: [pre-commit, commit-msg, pre-push]
```

Without this line `pre-commit install` writes only the `pre-commit` shim, so every hook with
`stages: [pre-push]` or `stages: [commit-msg]` is configured and never runs. Existing clones pick
up a changed list only after rerunning `pre-commit install` (add `--install-hooks` to build the hook
environments up front). Confirm by listing `.git/hooks/`: it holds a shim for each declared type.

## Stage each hook by its cost

| Stage | What belongs there | Budget |
| --- | --- | --- |
| `pre-commit` | Formatters, linters, secret scans, file hygiene | About 5s total |
| `commit-msg` | Commit message format | Instant |
| `pre-push` | Test suites, typecheck, whole-repo scans | Tens of seconds |
| `manual` | Checks needing credentials or network, run in CI | n/a |

A slow commit stage is what drives people to `--no-verify`, and a config everyone bypasses enforces
nothing. A test suite belongs at push time.

## The always-on set

Every repo runs these, whatever else it enables:

- a conventional-commit check at `commit-msg` (format owned by `commit-standards`)
- `detect-private-key`, `check-merge-conflict`, `end-of-file-fixer`, `trailing-whitespace`
- two secret scanners (the template uses gitleaks plus trivy). Their rulesets disagree at the
  edges, and one has been observed missing a live cloud key the other caught, so keep both.

## Excludes

- Keep repo-wide exclusions as one verbose-mode regex at the top of the file: dependency
  directories, caches, build output, lockfiles, minified assets, tool scratch directories.
- Give every tracked generated tree (rendered diagrams, snapshots) an exclude on the hygiene hooks;
  otherwise `end-of-file-fixer` rewrites them on every `--all-files` run.
- The top-level `exclude` filters the filenames pre-commit passes. A hook with
  `pass_filenames: false` receives no filenames and scans the tree itself, so it needs its own
  ignore settings (for example `--skip-dirs`).
- Keep a hook's own trigger file in scope: excluding a lockfile from the hook that regenerates it
  disables that hook.

## Pinning

Give every `repo:` an explicit `rev:` tag or SHA so the same commit behaves the same on every
machine. Bump pins deliberately with `pre-commit autoupdate` in a commit of its own, then run
`pre-commit run --all-files` and fix what the new versions report. Where a hook breaks under a newer
runtime, pin its `language_version` and say why in a comment.

## Local hooks

A `repo: local` hook not in the baseline is either a promotion candidate (broadly useful: propose
adding it to the template) or an intentional exception (repo-specific: leave it and say so).

Write local hooks to fail loudly and correctly:

- Resolve the tool at run time and print what is missing, rather than exiting 127.
- Keep the tool-absent case in its own `if`/`else` branch. `cmd && run || echo "not installed"`
  turns a real finding (non-zero exit from `run`) into a pass.
- Scope test runners to the main tree, so a repo with worktrees under it does not collect every
  worktree's copy of the suite.

<example>
```yaml
- id: unit-tests
  name: unit tests (pre-push)
  entry: >
    sh -c 'root=$(git rev-parse --show-toplevel);
    if [ -x "$root/.venv/bin/pytest" ]; then py="$root/.venv/bin/pytest";
    elif command -v pytest >/dev/null 2>&1; then py=pytest;
    else echo "pytest not found: create the venv, then rerun"; exit 1; fi;
    "$py" tests/ -m "not integration and not e2e" -q'
  language: system
  pass_filenames: false
  stages: [pre-push]
```
</example>

## Auditing a repo for drift

1. Read the repo's `.pre-commit-config.yaml` and the template.
2. Check these categories, most impactful first:
   1. an always-on hook is missing, or `default_install_hook_types` omits a stage the config uses
   2. a section the repo needs is off (`.tf` files but no IaC section; `.py` files but no Python
      section; a `package.json` test script but no Node section)
   3. a tracked generated tree has no exclude (skip this when the repo tracks none)
   4. a pin is on a branch, or behind the template
   5. a `repo: local` hook not in the baseline
3. Report the drift as a table (`category | finding | proposed change | behaviour change: yes/no`)
   before editing. Ask before any behaviour change (enabling a section, bumping a rev); batch the
   rest (excludes, aligning a rev to the template) into one approval.

## Verify

```bash
pre-commit validate-config .pre-commit-config.yaml
pre-commit run --all-files
git diff --stat
```

Done means the config validates, every hook passes, and the run changed no file beyond your own
edits. A failing hook gets
its input fixed, per `zero-tolerance-testing`. If `pre-commit` is not installed, say so and list
these commands for the user to run.
