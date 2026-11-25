---
name: targets-staleness
description: Detect and prevent silent {targets} staleness -- targets that stay "up to date" while their real inputs changed, because options, package internals, path strings and option-bearing symbols are not tracked dependencies. Every recorded instance produced a silently wrong run, never an error. Use when editing a pipeline, changing an option, or when results look suspiciously unchanged.
when_to_use: Editing _targets.R or any R/targets_*.R; changing a getOption()/option value that a pipeline reads; a run finished suspiciously fast; validation numbers are identical to a previous run; asked why a target did not rebuild, or to audit a pipeline for staleness.
paths:
  - "**/_targets.R"
  - "**/_targets*.R"
  - "**/R/targets_*.R"
  - "**/_local.R"
---

# Silent staleness: the #1 trap in this corpus

At least **eight separate incidents** in one project alone. Every one produced a
*silently wrong run*, not an error. The commit that fixed the eighth says so
outright:

> Same trap already fixed for `rep_index` ... and `scenario_definitions` ...;
> `study_areas` was missed.

and the file itself carries: *"the same class of silent staleness has already cost
this project days."*

## Why it happens

`targets` hashes the **command expression** and the objects it can see. It does
**not** see:

| Not tracked | Consequence |
| --- | --- |
| `getOption("x")` inside a command | option changes, target stays current |
| a symbol bound to an option value (`nodes = .cal_nodes`) | *"targets hashes the command EXPRESSION -- it sees the symbol `.cal_nodes`, never the `c(hostA = 40, hostB = 40)` behind it"* |
| functions defined **inside packages** | *"targets hashes the functions in the project's `R/` globals but NOT the ones inside packages"* |
| a path **string** (`dirname(x)`) | *"a PATH STRING, identical every time ... the spin-up silently reused a snapshot built from superseded initial communities"* |
| `Sys.getenv()` read at definition time | toggling the env var does not invalidate |

The worst recorded case:

> switching to a different study area left the pipeline silently running the old one ...
> a scoped calibration run finished in 3 minutes having skipped the calibration
> entirely

## Audit checklist

When you touch a pipeline, scan for each of these:

1. **`getOption(` or `Sys.getenv(` inside a `command =`, or in any function the
   command reaches.** Either lift the value into an upstream target, or set
   `cue = tar_cue(mode = "always")` **and** `deployment = "main"` on the target that
   reads it -- workers never source the definition-time config file, so the option is
   not even set there. The validator in `targets-testing-ci` checks this for every
   target; in one project it found six real stale-configuration bugs.
2. **A command referencing a symbol whose value came from `_local.R`.** Same fix:
   make the value itself a target so its content is hashed.
3. **A dependency on a path string where a `format = "file"` target exists.**
   Depend on the file target, not on `dirname()` of it.
4. **A package function doing real work.** Package function bodies are **not hashed**
   unless the project opts in with `tar_option_set(imports = c("pkg"))`.
   `tar_option_set(packages = )` is unrelated -- it only controls what workers attach.
   So upgrading a package invalidates nothing, which is a hazard rather than a relief:
   already-built targets keep the old version's results, anything rebuilt later uses the
   new one, and nothing records the boundary. Decide deliberately per co-developed
   package -- `imports =`, or a `<pkg>_version` target every consumer depends on -- and
   verify with one cheap representative target: rebuild it and diff the numbers.
5. **A non-reproducible file write under `format = "file"`.** GDAL stamps
   `gpkg_contents.last_change`, so an identical write re-hashes and *cascades*
   downstream rebuilds. Fix: pin `OGR_CURRENT_DATE`.
6. **Unseeded RNG anywhere reachable from a target**, including inside dependency
   packages and `callr`/crew subprocesses (see below).

## The opposite trap: `targets` hashes source text, not behaviour

A change that provably cannot alter results still invalidates every target that reaches
it, because `targets` hashes the deparsed function source. Measured: replacing a
deprecated call with its drop-in replacement -- identical return value -- inside two path
helpers took a store from **0 to 108 of 112 targets outdated**, including every
multi-hour target.

- Comment-only edits are safe; the deparsed source drops comments.
- Cosmetic edits to widely-reached helpers are not: formatting, renames, a new default
  argument added for testability. Batch them with a change that already forces a rebuild.
- Before editing a helper, check its reach: `targets::tar_outdated()` after a trial edit,
  then revert if the cost is not worth it.

## Always verify invalidation after a change

Do not trust the run summary. After editing a pipeline:

```r
targets::tar_validate()                 # the graph still builds
targets::tar_outdated()                 # the targets you EXPECT are listed
targets::tar_visnetwork()               # visual check of what is stale
```

If a target you changed does **not** appear in `tar_outdated()`, that is the bug --
not a convenience.

## How the silent cases were actually caught

The detection heuristics are worth internalising, because the pipeline reports a
clean run in every case:

- **File mtimes, not the summary.** *"it is invisible: the pipeline
  reports a clean run. Caught by checking file mtimes rather than trusting the
  summary."*
- **Numbers identical to the decimal.** *"The NTEMS validation then returned
  numbers identical to the decimal, which is what exposed it."* If a validation
  statistic is bit-identical across a change that should have moved it, suspect
  staleness before celebrating.
- **A run that finished far too fast.**

## The stable-path trap (found twice, independently)

**A target that returns a stable path string does not invalidate its consumers
when the contents behind that path change.** `targets` skips a downstream target
whose dependency *values* are unchanged, even though the upstream re-ran --
verified against targets 1.12.0.

From the fix commit:

> The `*_dataset` targets returned a stable root path, so consumers reading the
> Arrow datasets off disk were skipped whenever replicate content changed ...
> `cumulative_burn_map` had the same hole via its `list.files()` scan.

**The remedy, and the idiom to reuse:** a `*_manifest` target carrying
path/size/mtime fingerprints, which consumers map over.

```r
tar_target(scen_manifest, {
  f <- fs::dir_ls(scen_dataset, recurse = TRUE, type = "file")
  data.frame(path = f, size = fs::file_size(f), mtime = fs::file_info(f)$modification_time)
})
```

A changed replicate then invalidates only its own scenario.

## Other invalidation rules that bite once each

- **`tar_make(names = )` matches parents, not dynamic branches.** It re-walks the
  whole cross-expansion. To rebuild specific branches, `tar_invalidate()` the
  branch hashes first, then `tar_make()` the parent.
- **`tar_invalidate()` fails silently on a vector.** `tar_invalidate(any_of(c(...)))`
  aborts if any name is missing from `tar_meta()` and **leaves the cache intact**.
  Invalidate one bare name at a time.
- **`format = "file"` with `trust_timestamps = TRUE` checks mtime + size, not
  content.** Touching such a file re-triggers downstream even when nothing changed.
- **Cross-store reads are forbidden.** Projects hand off by file, never by
  `tar_read(store = )`: *"A cross-store read is invisible to targets -- the reading
  project cannot tell that the value it read has since been rebuilt."* Reading a
  `format = "file"` target puts the file's hash in the consumer's graph instead.
- **Split a project by measurement, not taste.** One project's `comparison` split
  was made when that chain had *"ten inbound dependencies and zero outbound. Check
  that both ways before splitting anything else out -- a two-way boundary would
  not be safe."*
- **`deployment = "main"` is mandatory for any target that writes a git-tracked
  path** (`README.md`, `INFO.md`, `reports/pdf/*`, `citations/*.bib`,
  `_input_manifest.json`). Otherwise a worker writes it inside that worker's
  checkout, dirties the tree, and blocks the next `git merge --ff-only` sync.
- **`error = "continue"` silently skips branches whose upstream failed.** After any
  big run under it: `tar_meta(fields = "error", complete_only = TRUE)`. Do not
  trust a clean-looking console.

## Everything passed to a target factory is baked into the command hash

A factory that `bquote()`s its arguments in at definition time makes every argument
part of the command, so a cosmetic edit to an argument block invalidates the target.
One project records a stage whose rebuild takes 22 hours being invalidated again and
again by worker-count and memory-fraction toggles in its factory arguments. Before
editing any argument block of a cached stage, check what it costs to rebuild.
Runtime resource knobs (worker counts, memory fractions) should not live in a hashed
command at all.

## Confirming a change did what it should

Compare the rebuilt outputs with the previous ones per cell or on medians, against an
independent reference, with package versions held fixed across both runs --
`verification-method` in `r-code-review`. A validation number that stays
bit-identical across a change that should have moved it is the staleness signal
above.

## Related

- Spatial objects across the store: `targets-spatial` (external pointers do not
  survive serialisation).
- Definition-time settings and why workers never see them: `targets-project-setup`.
