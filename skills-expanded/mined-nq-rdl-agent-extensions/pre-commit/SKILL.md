---
name: pre-commit
license: CC-BY-4.0
description: >-
  pre-commit framework (`.pre-commit-config.yaml`): add or update hooks, pin
  and refresh hook revisions, install it with the project's own tooling (pixi,
  uv, pipx or pip) and run it in CI. Use when the repository has
  `.pre-commit-config.yaml`, including Node or Go projects, or the user asks for
  pre-commit. For `.husky/` or `lefthook.yml` use the husky or lefthook skill.
compatibility: >-
  pre-commit 4.x (tested 4.6.2); commands tested with pixi 0.78.0 and uv
  0.12.17 on 2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# pre-commit

## Confirm the hook manager first

Inspect the repository. `.pre-commit-config.yaml` means pre-commit, whatever
else the project contains; a `package.json` beside it is common. `.husky/` or
`lefthook.yml` without it means another tool (`gh:husky`, `gh:lefthook`). When
nothing is configured and no tool is named, say so and let the user choose.

## Install with the project's tooling

Match how the project already manages tools; do not introduce pixi or uv:

| Project signal | Add pre-commit | Run it |
|---|---|---|
| `pixi.toml` or `[tool.pixi]` | `pixi add pre-commit` (pixi has no `--dev` flag) | `pixi run pre-commit …` |
| pixi, lint-only environment | `pixi add --feature lint pre-commit` then `pixi workspace environment add lint --feature lint` | `pixi run -e lint pre-commit …` |
| `uv.lock` | `uv add --dev pre-commit` | `uv run pre-commit …` |
| anything else | `pipx install pre-commit` (or `pip install pre-commit`) | `pre-commit …` |

Then install the Git hook once per clone: `pre-commit install`. Other stages
need their hook type: `pre-commit install --hook-type commit-msg` (or set
`default_install_hook_types` in the config). The installed hook calls the
environment it was installed from, so reinstall after recreating that
environment.

## Configure with pinned revisions

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.9
    hooks:
      - id: ruff-check     # `ruff` is the legacy alias
        args: [--fix]
      - id: ruff-format
```

- `rev` is a tag or commit SHA, never a branch. The revisions above were the
  latest releases on 2026-09-29; do not copy a revision from memory. Refresh with
  `pre-commit autoupdate` (`--freeze` pins SHAs) and review the diff.
- A hook that imports project packages (pylint, mypy) runs in its own
  environment: list them in `additional_dependencies`.
- `repo: local` runs a project script without a hook repository:

```yaml
  - repo: local
    hooks:
      - id: check-scripts
        name: check scripts
        entry: ./scripts/check.sh
        language: script
        types: [shell]
```

## Run and handle failures

- `pre-commit run --all-files` after setup or a config change;
  `pre-commit run <id> --all-files` for one hook.
- A hook that rewrites files fails the commit. Review the change, `git add` the
  files and commit again.
- Skip one hook with `SKIP=<id>[,<id>] git commit …`; skip all with
  `git commit --no-verify`.
- In CI, run `pre-commit run --all-files --show-diff-on-failure` explicitly
  rather than relying on Git hooks, and cache `~/.cache/pre-commit` keyed on the
  config file. With pixi, install the environment with
  `prefix-dev/setup-pixi` (v0.10.2 on 2026-09-29) and run the same command
  through `pixi run`.
