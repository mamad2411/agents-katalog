---
name: targets-debugging
description: Debug and inspect a {targets} pipeline -- the tar_outdated/tar_visnetwork/tar_workspace ladder, running in-process for browser(), reading errors from tar_meta rather than the console, forcing a rebuild, and the symptom-to-cause catalogue for targets, crew and callr failures.
when_to_use: A target failed, a run behaved oddly, results look stale or suspiciously fast, asked to inspect a pipeline's state, or debugging inside a target with browser().
argument-hint: "[optional: target name or symptom]"
---

# Debugging a targets pipeline

## Inspect first, do not re-run

```r
targets::tar_validate()                              # graph is well-formed
targets::tar_manifest()                              # what targets exist
targets::tar_visnetwork(); targets::tar_glimpse()    # the DAG
targets::tar_outdated()                              # what WILL rebuild
targets::tar_progress()                              # what happened
targets::tar_meta(fields = c("seconds", "bytes"))    # cost
targets::tar_meta(fields = "error", complete_only = TRUE)   # the real errors
targets::tar_read(<target>); targets::tar_load(c(a, b))
```

**Read errors from `tar_meta`, not from the console.** Under `error = "continue"`
or `error = "trim"` failed branches are silently skipped and the console looks
clean. This has shipped wrong results more than once.

## Interactive debugging

`workspace_on_error = TRUE` (set it in every project) makes this work:

```r
targets::tar_workspace(<failing_target>)   # loads that target's deps into globals
```

To get a real `browser()`, take callr and crew out of the loop:

```r
Sys.setenv(PROJ_CREW = "false")        # the project's own no-crew toggle
targets::tar_load_globals()
targets::tar_make(callr_function = NULL)
```

Two projects make `callr_function = NULL` the *documented default* invocation:

- `## NOTE: callr/sf interaction causes multithread deadlock`
- for long runs: *"the outer callr wrapper crashes under the optimiser + 90-container load"*

## Forcing a rebuild

```r
targets::tar_invalidate(<one_bare_name>)   # ONE at a time -- the vector form
                                           # aborts on a missing name and silently
                                           # leaves the cache intact
targets::tar_prune()                       # drop targets no longer in the pipeline
targets::tar_destroy()                     # nuclear; acts on the ACTIVE project only
```

`tar_make(names = )` matches **parent** targets and re-walks the whole
cross-expansion; it does not accept a dynamic-branch hash. To rebuild specific
branches, invalidate the branch hashes then make the parent.

`tar_make(shortcut = TRUE)` skips upstream checks -- *"Verify the stored upstream is
the one you mean."*

## Symptom to cause

| Symptom | Cause |
| --- | --- |
| run finished far too fast; numbers identical to the decimal | silent staleness -- see `targets-staleness` |
| clean console, wrong results | `error = "continue"`; check `tar_meta(fields = "error")` |
| `NULL value passed as symbol address`, in the *consumer* not the producer | a terra/sf external pointer stored by a plain `tar_target`; use `tar_terra_*` or `format = "file"` |
| store lock held after you killed the run | `tar_make()` wraps the pipeline in a `callr` child that does **not** die with the screen; see `targets-cluster-runs` |
| `crashed N consecutive times` | raise `crashes_max` on the controller (a race under high worker counts) |
| worker cannot find a function that exists locally | the worker library differs; check node sync and that the package is in `tar_option_set(packages = )` |
| a setting "did not take" on a worker | it was set in `_local.R`; workers do not source it -- see `targets-project-setup` |
| target rebuilds every run, apparently without cause | a non-reproducible file write (GDAL timestamps), or an intentional `cue = tar_cue(mode = "always")` on a provenance target |

## Stopping a run

The stop order that actually ends a run, and clears the store lock, is in
`targets-cluster-runs`: ending a `screen` does not stop `tar_make()`, because its
`callr` child survives.

## Fixing what you find

Name the defect's `file:line` before changing anything, and fix it where it lives. A
guard added to a target's command to route around a bug in a helper or a package
leaves the bug for the next target that calls it -- see `root-cause-fixes` in
`r-project-core`.
