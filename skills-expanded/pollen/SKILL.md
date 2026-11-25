---
name: pollen
description: How to install, upgrade and use pollen to deploy and pin Agent Skills (pollen.yaml → .claude/skills and .agents/skills). Trigger when installing or upgrading pollen itself (macOS, Linux, WSL, Windows), creating or editing a pollen.yaml, seeing what skills a source provides before adding it (pollen show), adding a skills source to a project or to the user-level config, updating or pinning skill versions (pollen update, outdated, autoupdate --freeze, validate --pinned), or fixing a pollen error (directory pollen did not install, target managed by another config, branch revision warning).
---

# pollen

pollen makes skills directories match a `pollen.yaml`: it installs what is
declared, refreshes what changed and removes what was dropped. It only touches
directories it installed itself, recorded in `.pollen.json` in each target.

## Install and upgrade pollen

The same command installs and upgrades; it replaces the binary in place, so
`PATH` is set once.

| System | Command |
|--------|---------|
| macOS, Linux, WSL with Homebrew | `brew install groupbees/tap/pollen` · `brew upgrade groupbees/tap/pollen` |
| Linux, WSL, macOS without Homebrew | [`scripts/install.sh`](scripts/install.sh) `[vX.Y.Z] [dir]` → `~/.local/bin` |
| Windows (PowerShell) | [`scripts/install.ps1`](scripts/install.ps1) `[-Version vX.Y.Z] [-InstallDir dir]` |
| Any, with Python ≥ 3.11 | `uv tool install pollen-skills` · `uv tool upgrade pollen-skills` (or pipx) |

Where a policy blocks unsigned executables (`pollen.exe` refused on a managed
Windows machine), install the Python package and run `python -m pollen`.

Both scripts take the latest release by default and check the archive against
the release's `SHA256SUMS`; `install.sh` defers to brew when brew installed
pollen. Run them from this skill's directory (e.g.
`~/.claude/skills/pollen/scripts/install.sh`). Behind a corporate proxy, set
`https_proxy` first. Private sources need an SSH key on the machine that the
git host accepts; public ones work over HTTPS as is.

## Where the config lives

| Scope | Config | Command | Targets |
|-------|--------|---------|---------|
| Project | `pollen.yaml` at the project root, committed | `pollen update` | `.claude/skills/` + `.agents/skills/` — gitignore both |
| Machine | `~/.config/pollen/pollen.yaml` (`$XDG_CONFIG_HOME`) | `pollen update -g` | `~/.claude/skills/` + `~/.agents/skills/` |

One config per target directory: an update removes whatever its config does
not declare, so pollen refuses a directory another config manages. Add sources
to that config; `--force` only to hand the directory over on purpose.

## pollen.yaml

```yaml
repos:
  - repo: git@github.com:org/skills.git      # SSH for private repos
    revision: 4e1e8e25a2f32d8311cd52c5d9a703bad990e525  # v0.2.0
    paths:
      - path: skills/docker                  # immediate children
      - path: skills
        recurse: true                        # the whole tree
        exclude: ^terraform/                 # regex on the path under `path`
  - repo: local                              # paths next to this file
    paths:
      - path: .skills
```

Skills deploy flat under their folder name, so names must be unique across
sources. Before adding a source, `pollen show <repo>` lists its skills — the
`path` to put under `paths:`, each description — and prints the
`revision: <sha>  # vX.Y.Z` line to paste.

## Pin a commit, not a branch — and no lockfile

- Pin the **commit of a release**, tag in a comment: `revision: <sha>  # vX.Y.Z`.
  A branch moves on every push and pollen warns about it; a tag can be moved;
  a commit cannot.
- That pinned `pollen.yaml` is the lock. pollen resolves no version ranges and
  skills have no transitive dependencies, so a lockfile would only repeat it.
  Do not add one.
- Write the tag, then let `pollen autoupdate --freeze` turn it into its commit.

## Commands

```bash
pollen update [--dry-run]           # deploy; -g for the machine-wide config
pollen list                         # what is deployed, from which commit
pollen outdated                     # newer release per source
pollen autoupdate [--freeze]        # bump every source (rewrites revision: lines only)
pollen validate [--config-only] [--pinned]   # check config and skills; --pinned requires commits
pollen show <repo> [--revision R] [--path P] [--format json]   # what a source provides; writes nothing
```

`pollen validate --config-only --pinned` is offline: run it in CI or in the
`pollen-validate` pre-commit hook (`args: [--pinned]`).

## Errors

| Message | Fix |
|---------|-----|
| `… already exists and pollen did not install it` | A hand-written or legacy copy: move it aside, or `--force` to take it over |
| `… is managed by another config, …` | Declare the source in that config; `--force` hands the directory over |
| `` `main` is a branch `` (warning) | Pin a tag, then `pollen autoupdate --freeze` |
| `two sources provide …` | Rename one skill, or `exclude` it in one source |

## Don't

- Edit an installed copy: change the source, then `pollen update`.
- Commit `.claude/skills/` or `.agents/skills/` in a project using pollen.
- Point two configs at the same target directory.
