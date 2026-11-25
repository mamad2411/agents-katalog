---
name: mcp-server-shipping
description: "Use when building, installing or registering a personal MCP server — adding its `[project.scripts]` entry point, installing it with `uv tool install` from a local checkout or straight from git instead of publishing to PyPI, registering it with `claude mcp add` and choosing local/project/user scope, switching between an editable dev install and a released one without re-registering, and the per-repo dev loop (`inv dev-env.setup`, `inv quality.precommit`, why automation needs `uv run inv`) for the repos that produce these servers."
---

# Shipping a personal MCP server

Workflow for repos whose entire purpose is producing an MCP server for personal, cross-project use
(not a library other code imports) — e.g. `olx-polite-mcp`, `emag-polite-mcp`, `altex-polite-mcp`,
`temu-polite-mcp`, `product-research-pipeline`. Covers going from a working repo to "loadable in any
project," and how that differs between the dev machine and everywhere else.

Shipping an **Agent Skill** is a different job with a different mechanism — see the
`skill-authoring` skill, which also covers getting an edit to an existing skill deployed.

## Per-repo dev loop

Every repo in this family takes [`repo-tasks`](https://github.com/TheodoreAD/repo-tasks) as a dev
dependency (git-as-artifact-store, no PyPI —
`uv add --dev git+https://github.com/TheodoreAD/repo-tasks`) instead of hand-rolled `tasks.py`
logic; the repo's own `tasks.py` is then just `from repo_tasks
import ns`. See that repo's own
README for the full task catalog (one invoke module per facility — `quality`, `venv`, `deps`,
`direnv`, `agents`, `docs`, ...) — the two that matter for day-to-day work here:

- `inv dev-env.setup` once after cloning — syncs `.venv` from `uv.lock` (fails loudly on a missing
  or stale lockfile rather than silently rewriting it), `direnv allow`s it, and wires Claude Code's
  Bash tool to auto-activate the same venv (a no-op if the repo has no `.envrc`).
- `inv quality.precommit` before considering a change done — fixes everything auto-fixable
  (`ruff`/`dprint`/`shfmt`), then runs the full CI-style gate (lint/format/type-check/shell-check/
  test). `pytest` runs against checked-in fixtures (saved HTML snapshots, etc.) — no live-network
  calls in tests.
- `AGENTS.md` + `CLAUDE.md` symlink + `.agents/skills`/`.claude/skills` scaffold comes from
  [`scaffoldapy`](https://github.com/TheodoreAD/scaffoldapy) automatically at generation time —
  nothing to run for it.

`invoke` is a per-project venv dependency (pulled in transitively via `repo-tasks`), never assumed
to be a machine-wide tool — unlike `power-user-linux-setup`'s own `inv`, which `bootstrap.sh`
installs as a global `uv tool` for real end users. Anything invoking `inv` from outside an
already-activated shell (a CI step, a `copier.yml` `_tasks` hook, any automation) needs
`uv run inv <task>`, not bare `inv` — nothing guarantees the latter resolves. `scaffoldapy`'s
`copier.yml` (`_tasks: [uv sync, uv run inv configure]`) and every generated repo's own
`.github/workflows/ci.yml` (`uv run inv quality.check`) both already follow this; keep new
automation consistent with it rather than assuming a global `inv`.

## One entry point, `uv tool install` for a stable PATH binary

Add a `[project.scripts]` entry point to the MCP repo's `pyproject.toml` (e.g.
`olx-polite-mcp = "olx_polite_mcp.server:main"`) before writing `server.py`, not as a retrofit. Then
install it as a real tool via `uv tool` (validated end-to-end in `olx-polite-mcp/README.md`) rather
than pointing `claude mcp add` at a `uv run`/`uvx` invocation — `uv tool install` builds an isolated
env and drops a shim on `PATH` (`~/.local/bin/` by default), so registration itself becomes a bare
binary name with no path/flags to keep in sync:

Install against the **local working tree** while actively developing (editable — picks up local
edits without reinstalling, so the repo has to stay put at that path):

```shell
uv tool install -e ~/projects/github.com-personal/olx-polite-mcp
```

Install **from GitHub** once not actively iterating (pin `@<tag>`/`@<sha>` for reproducibility, omit
for the default branch):

```shell
uv tool install git+https://github.com/TheodoreAD/olx-polite-mcp
```

Either way, registration is the same one-liner, independent of which source was installed:

```shell
claude mcp add --scope user olx-polite-mcp olx-polite-mcp
```

Switching sources is `uv tool install` again with the other source (uv replaces the existing tool) —
no `claude mcp remove`/re-`add` needed, since the registered command name never changes.
`--scope user` (not `local`/`project`) matches how skills already install globally, so the server is
available in every project on this machine, not just one. Use `--scope project` instead only for a
_consumer_ repo that wants the server offered automatically to anyone who clones it (see
`olx-polite-mcp/README.md`'s project-scope example) — a different case than personal cross-project
use.

Editable and from-GitHub installs can't be combined (editable needs a real working directory uv can
point at; a git-sourced install doesn't expose one) — for "edit locally, sourced as if from GitHub,"
`git clone` it yourself, then `uv tool install -e` that clone, which is just the editable-from-disk
case again.

Project- and user-scope servers need a one-time approval on `claude` startup before a _new_ session
launches them (`claude mcp list` shows pending ones) — an already-running session that had it
approved keeps it live.

## Distribution: skip PyPI

At this scale (personal, non-commercial), `uv tool install` resolving straight from a git remote
(see above) makes the GitHub repo itself the artifact store — no version-bump/publish/credentials
ceremony. Pin `@<tag>`/`@<sha>` once a repo has a stable point worth freezing; no ref (tracks the
default branch) is fine while iterating.

## Full rationale

[`references/rationale.md`](references/rationale.md) — why git+`uv` beat PyPI (and the
`uvx`/`uv run` draft that came first), why `--scope user`, and why one registered command covers
both install sources.
