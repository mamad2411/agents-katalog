---
name: project-config-layout
description: Where a research project's settings belong -- .Rprofile for anything every R process must see, a local config file for the controlling session, a gitignored hosts file for machine identity -- and why a setting in a file that worker processes never read is a silent no-op there. Also one source of truth per setting, secrets and service-account keys, and the renv dependency shims.
when_to_use: Editing .Rprofile, _local.R, _hosts.R or _hosts.R.example; adding a Sys.setenv() or options() call to a project; debugging a setting that "did not take" in a worker or a callr subprocess; adding a tracked .json file; setting up a service-account key or other credential, or a Drive login for pipeline runs; renv dropping a package the project still needs.
paths:
  - "**/.Rprofile"
  - "**/_local.R"
  - "**/_hosts.R"
  - "**/_hosts.R.example"
  - "**/*.Renviron"
  - "**/.renvignore"
  - "**/_dependencies.R"
---

# Where does this setting go?

One project states this rule four separate times inside `.Rprofile` alone, which is
a reliable signal that it kept being got wrong:

> Set here (`.Rprofile`, **NOT** `_local.R`, which [the workers] do not source) so
> every R process inherits it.

## Three files, three audiences

| File | Tracked? | Read by | Put here |
| --- | --- | --- | --- |
| `.Rprofile` | yes | **every** R process started in the project, including parallel workers and `callr` subprocesses | env vars (`Sys.setenv`), cache paths, GDAL/PROJ config -- anything a worker must see |
| `_local.R` | usually yes | the session that drives the run, when it sources it | run toggles, study-area choice, replicate counts, CRS/resolution |
| `_hosts.R` | **no** -- gitignored, `.example` shipped | the controlling session on the control node | cluster identity: node names, worker counts, SSH details |

The consequence that bites: **a `Sys.setenv()` or `options()` call in a file only the
driving session sources never reaches a worker.** It looks set where you tested it and
is simply absent on the worker. Move it to `.Rprofile`.

Do **not** attach packages in `.Rprofile`. It breaks a fresh clone and CI, where the
packages are not installed yet.

## One source of truth per setting

From a project's `_local.R`: *"Do NOT also set these in `.Rprofile` or pass an
equivalent argument to the [function that consumes them] -- that would create a
second source."*

If a value appears in two places, one of them will drift. Pick the layer that the
consumer actually reads and delete the other.

The deliberate exception is a setting whose *absence* is silent and expensive, set
in `.Rprofile` for workers **and** repeated in the driver script for interactive use,
with a comment at both sites saying exactly why. Duplicate only with that
justification written down.

## Infrastructure identity stays out of the repo

In one incident, cluster node names leaked from the gitignored `_hosts.R` into
comments across the project config, the Quarto config, an ops script, and an
archived config.

> Infrastructure identity does not belong in the repo. Comments now refer to
> roles ("the control node", "a compute node") instead of machines.

One leak was also functional -- a hostname-match guard. It was replaced with
`file.exists("_hosts.R")` *"so the guard is both hostname-free and robust to the
cluster being renamed or moved."* Prefer capability tests over identity tests.

## `.renvignore` and `_dependencies.R`

- `.renvignore` scopes renv's dependency scan (to `R/`, `scripts/`, root `*.R`),
  excluding archived trees and rendered output.
- `_dependencies.R` is an `if (FALSE) { library(...) }` block that pins indirect
  dependencies renv would otherwise drop: *"renv follows only
  Imports/Depends/LinkingTo, so nothing pulls it in on our behalf any more"* once
  an upstream package demotes a dependency to Suggests.

## Secrets

`*.Renviron`, `.httr-oauth*`, service-account `*.json`, and `_hosts.R` are
gitignored. A good pattern denies **all** `.json` and allowlists the few tracked ones
by exact path, never as a pattern like `!*.json`:

```gitignore
*.json
!renv/settings.json
!.vscode/settings.json
!_input_manifest.json
## key names come after the ! entries, so none of those can re-include a stray copy
drive-sa*.json
```

Consequence to remember: **a new tracked `.json` needs an explicit `!` allowlist
entry**, or it silently will not be committed.

A service-account key does not belong in the repository at all, even gitignored. It
lives in `~/.config/<project>/` (folder 700, file 600) on every machine that runs the
pipeline, and a gitignored `<Project>.Renviron` holds its path. A `Read()` deny rule
in `.claude/settings.json` keeps it out of the transcript, and a pre-commit hook
([assets/dispatch](assets/dispatch), installed by [assets/install.sh](assets/install.sh))
keeps it out of git. The `.Rprofile` must also stop a failed service-account login
from falling back to someone's cached personal Google token.
The whole pattern: [references/credentials.md](references/credentials.md).
