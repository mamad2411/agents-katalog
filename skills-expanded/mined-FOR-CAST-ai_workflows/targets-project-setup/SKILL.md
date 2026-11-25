---
name: targets-project-setup
description: Structure a FOR-CAST {targets} pipeline -- multi-project _targets.yaml and TAR_PROJECT, the targets_* list module pattern required by tarborist, tar_source() vs explicit source(), load order and the definition-time vs run-time contract for _local.R and _hosts.R, tar_option_set choices, env-var stage gates, targets that write tracked files or render reports, and the deliberate tripwires (cue="never", pinned run fleets) that must never be tidied away.
when_to_use: Creating or restructuring a _targets.R; adding a new R/targets_*.R module or target group; setting up a second targets project; choosing tar_option_set values; editing _local.R or _hosts.R in a targets project; a value from _local.R is missing inside a running target; rendering a Quarto report from the pipeline; reviewing a pipeline's architecture.
paths:
  - "**/_targets.R"
  - "**/_targets*.R"
  - "**/_targets.yaml"
  - "**/R/targets_*.R"
  - "**/_local.R"
---

# Structuring a targets pipeline

## The module pattern (required, not stylistic)

Each `R/targets_*.R` defines **a top-level `targets_* <- list(...)` object**, assembled in
`_targets.R`. Do not wrap target lists in a `get_targets_*()` function:

> the tarborist IDE extension uses static AST analysis and cannot resolve function
> calls, so it requires literal `list()` assignments to discover targets.

And in `_targets.R`: *"Use `list()` (not `c()`) so tarborist recognises the pipeline container."*

The sanctioned exception is a group that must read an option set in `_local.R`,
which is sourced *after* `tar_source()`. Document the reason at the wrapper.

Register every custom target factory the project uses so tarborist can see its
targets, in `.vscode/settings.json` -- the geotargets factories (`targets-spatial`),
and any factory a domain package provides:

```json
{ "tarborist.additionalSingleTargetFactories":
  ["tar_terra_rast", "tar_terra_vect", "<pkg>::tar_<factory>"] }
```

## `tar_source()` is not always safe

**Check what is in `R/` before adding `tar_source()`.** One project deliberately
`source()`s six *specific* files:

> Gated "extended analyses" ... These define functions only; `R/` also holds
> standalone scripts, so source the specific files rather than `tar_source()`-ing
> the whole dir.

`R/` there also contains `remove_old_sim_files.R`, which **deletes files**, plus
`upload.R` and `update_FMA_boundaries.R`. Replacing those `source()` calls with
`tar_source()` executes all of them at pipeline-definition time. This is the
sharpest single guardrail in that repo.

Related: in a multi-project layout the root `R/` may hold manual-maintenance
helpers that are deliberately
**not** sourced by either pipeline; each project sources only its own
`tar_source("<proj>/R")`.

## Load order in `_targets.R`

```r
source("_local.R")                       # definition-time knobs
if (file.exists("_hosts.R")) source("_hosts.R")   # BEFORE tar_option_set()
# ... controllers ...
tar_option_set(...)
tar_source("<proj>/R")
```

`_hosts.R` must be sourced before `tar_option_set()` *"so the `crew.ssh.*` options
drive the controller construction below. `_local.R`, sourced later, would be too
late."*

Guard cluster config with `file.exists("_hosts.R")`, never a hostname match --
that keeps the guard hostname-free and survives the cluster being renamed.

## Definition time and run time

`_local.R` and `_hosts.R` are read by the controlling session, at pipeline
**definition** time. Crew workers never source them. Three consequences:

1. **A `Sys.setenv()` or `options()` call in `_local.R` never reaches a worker.** Put
   anything a worker must see in `.Rprofile` -- see `project-config-layout` in
   `r-project-core`.
2. **A value read from `_local.R` is baked in at definition time.** Anything that
   depends on it must be `deployment = "main"`, and changing it does not invalidate
   targets on its own -- see `targets-staleness`.
3. **`_local.R` values do not exist inside a running target.** As one project's docs
   put it: *"Do not assume `local$...` exists inside a running target."*

## Multi-project layouts

`_targets.yaml` with **no default project** is a deliberate safety pattern:

```r
Sys.setenv(TAR_PROJECT = "prep-fit")   # or "predict"; a bare tar_make() will NOT build
targets::tar_make()
```

Each project gets its own `_targets.R`, `_local.R`, `R/`, and store. `tar_destroy()`
and `tar_prune()` act on the **active** project only.

Projects hand off by `format = "file"`, never by cross-store `tar_read(store = )` --
see `targets-staleness`.

## `tar_option_set()` choices, as actually made

| Option | When to set it |
| --- | --- |
| `workspace_on_error = TRUE` | always -- it is what makes `tar_workspace(<target>)` debugging possible |
| `memory = "transient"`, `storage`/`retrieval = "worker"` | large spatial pipelines, to keep objects off the main process |
| `format = "file"` per target | any heavy or spatial output; see the `r-geospatial` plugin |
| `error = "trim"` | when unrelated targets should keep building |
| `error = "continue"` | **temporary only.** Failed branches are silently skipped. If you set it, write a dated revert condition in a comment, and always check `tar_meta(fields = "error")` afterwards |
| `trust_timestamps = TRUE` | only for multi-GB archives where hashing is prohibitive |
| `format = "qs"` | fine, but the backend changed: targets 1.9.0 switched it from `qs` to `qs2`, and `qs` was archived from CRAN on 2026-01-17. A lockfile still pinning `qs` will not restore from CRAN |
| `seed` | set it; unseeded RNG is audit item 6 in `targets-staleness` |

## Stage gating by environment variable

Expensive optional stages are appended only when an env var is set, so a plain
`tar_make()` can never pick up a 40-hour experiment:

```r
if (isTRUE(as.logical(Sys.getenv("PROJ_DATAPREP", "false")))) {
  targets_all <- c(targets_all, targets_dataprep)
}
```

Name them `<PROJ>_<STAGE>` so they are greppable and obviously project-scoped.
These are read at **definition** time -- set them before `tar_make()`, not inside it.

Some gates must be **off** for a valid run -- one reuse-cached-aggregates gate skips
a ~2 h recompute and is documented *"MUST be FALSE for a fresh run"*. When you see a
gate, find out which way it has to point before running.

## Deliberate tripwires -- do not tidy these away

Three separate patterns exist purely to stop an accidental expensive run. All are
removal-gated by human review:

```r
cue = tar_cue(mode = "never")   ## FROZEN 2026-07-10 ... REMOVE before the production run phase
                                ## (it freezes ALL branches, not just the baselines)
```
```r
run_scenarios = c("baseline", "fire")   ## pin the run fleet so no tar_make can
                                        ## launch production
```
```r
## Deliberately NOT a variant of main_<sa>: the spec is COPIED, not shared, so editing it can
## never invalidate main_<sa> (a 22 h rebuild); gated behind an env var.
```

If a comment says a duplication or a freeze is deliberate, believe it. "Refactoring"
these is how a 22-hour rebuild or a production launch happens by accident.

## Targets that write files or render reports

- **`deployment = "main"` for any target that writes a git-tracked path** -- a rendered
  PDF, a README, a generated `.bib`, an input manifest. A worker would otherwise write
  it inside that worker's checkout and block the next node sync (`targets-cluster-runs`).
- A function backing a `format = "file"` target returns the path it wrote.
- **Take a rendered report's path from the render, never reconstruct it.** Quarto in
  project mode mirrors the input directory under `output-dir`; `tar_quarto()` records
  the real path. See `quarto-reports` in `r-reporting`.
- **Crew workers do not inherit the shell `PATH`.** Resolve the Quarto binary (or any
  external tool) explicitly before a worker renders.
- **Two concurrent renders of one template in one directory clobber each other's
  intermediates.** Render from a branch-unique copy when branching over scenarios.
- A provenance target -- a reproducibility receipt, a session record -- is set to
  `cue = tar_cue(mode = "always")`. Seeing it rebuild on every run is expected.

## Comments are the spec

These projects encode their institutional memory as dated `##` post-mortems
inline in `_targets.R`, `.Rprofile`, `_local.R`, and `.gitignore`. A refactor that
drops them is a regression, not a cleanup. Preserve them; add to them.

## Naming

| Suffix | Meaning |
| --- | --- |
| `_v` | terra `SpatVector` |
| `_png` | figure file target |
| `_files`, `_manifest` | file-path / fingerprint companion target |
| `qmd_*`, `*_pub` | Quarto render target, and the target that publishes its PDF |
| `*_year`, `rep_index` | dynamic branch dimensions |
| `prod_*` | production per-scenario branches |
| `<stage>_<studyArea>` | static per-study-area branching |
