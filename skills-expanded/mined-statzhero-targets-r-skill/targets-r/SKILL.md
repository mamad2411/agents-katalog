---
name: targets-r
description: Modern patterns for reproducible analysis pipelines with the targets R package. Use this skill when writing `_targets.R`, defining targets, debugging pipeline failures, running individual targets safely, configuring storage, or integrating Quarto/R Markdown. Covers `tar_target()`, the tarchetypes factories, dynamic and static branching, error handling, cycle debugging, cloud and CAS repositories.
license: CC-BY-4.0
metadata:
  author: Ulrich Atz
  r_version: ">= 4.1.0"
  targets_version: ">= 1.12.0"
  tarchetypes_version: ">= 0.14.1"
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, mcp__r-btw__*
---

# Building Pipelines with targets

A target is a pipeline step that runs R code and caches its result. `tar_make()` hashes each target's code, arguments, and upstream dependencies, then skips anything still up to date.

## Reference files

Consult the appropriate reference file for detailed patterns and examples:

| Topic | Reference file | When to consult |
|-------|----------------|-----------------|
| **Targets** | [targets.md](references/targets.md) | `tar_target()`, formats, file tracking, tarchetypes factories |
| **Branching** | [branching.md](references/branching.md) | Dynamic `map()`/`cross()`, static `tar_map()`, `tar_combine()` |
| **Debugging** | [debugging.md](references/debugging.md) | `tar_workspace()`, `tar_igraph()`, browser(), cycles |
| **Performance** | [performance.md](references/performance.md) | Memory, batching, parallel via crew, cloud + CAS |
| **Literate** | [literate.md](references/literate.md) | Quarto, R Markdown, Typst/LaTeX compilation |

For requests that span multiple topics (e.g. "set up a parallel pipeline that renders a Quarto report"), read several files.

## Core principles

1. **Functions live in `R/`, targets live in `_targets.R`.** Source with `tar_source()`.
2. **Targets return one saveable value and avoid side effects** (unless `format = "file"`).
3. **Track every input file.** Use `tar_file_read()` rather than reading a literal path inside a target.
4. **Prefer tarchetypes factories** (`tar_qs()`, `tar_file()`, `tar_parquet()`) to passing `format = "..."` manually.
5. **Read the NEWS before relying on any behavior** — `targets` ships breaking-ish default changes roughly every minor release.

## Quick reference

### Minimum viable pipeline

```r
library(targets)
library(tarchetypes)

tar_source()
tar_option_set(packages = "tidyverse", format = "qs")

list(
  tar_file_read(raw, "data/raw.csv", read = readr::read_csv(!!.x)),
  tar_target(clean, clean_data(raw)),
  tar_target(model, fit_model(clean)),
  tar_quarto(report, "report.qmd")
)
```

### Directory layout

```
project/
├── _targets.R          # Pipeline (required)
├── _targets.yaml       # Optional config, multi-project support
├── R/                  # Functions sourced by tar_source()
│   ├── clean.R
│   ├── model.R
│   └── report.R
├── data/               # Input data
├── report.qmd          # Literate document
└── _targets/           # Auto-generated store (gitignore _targets/objects/)
    ├── meta/meta       # Metadata; commit this if you want teammates to share skip state
    └── objects/        # Target outputs
```

### Essential commands

| Command | Purpose |
|---------|---------|
| `tar_make()` | Run the pipeline |
| `tar_outdated()` | What will run next? |
| `tar_read(x)` / `tar_load(x)` | Return / attach a target |
| `tar_manifest()` | List targets + commands |
| `tar_visnetwork()` | Interactive dependency graph |
| `tar_igraph()` | Graph object for `igraph::find_cycle()` |
| `tar_validate()` | Check pipeline validity |
| `tar_prune()` | Delete stored targets no longer in pipeline |

### Running targets safely

Preview before running anything:

```r
tar_manifest()          # list every target and its command
tar_outdated()          # what would rerun
```

Scope `tar_make()` to specific targets instead of rebuilding everything:

```r
tar_make(names = c("clean_data", "model"))
tar_make(names = starts_with("plot_"))        # tidyselect helpers work
tar_make(names = "report", shortcut = TRUE)   # rebuild report only, skip upstream
```

`shortcut = TRUE` rebuilds only the named targets even if upstream is invalidated. Handy for rerunning a downstream report without recomputing expensive ancestors.

**One `tar_make()` per store.** Two concurrent runs on the same `_targets` store are not supported; targets locks the store via `_targets/meta/process` and errors. After a crashed run, a stale lock can cause a false positive — clear it with `tar_unblock_process()`.

### Regenerate outputs without recomputing

When only a *presentation* function changed (a table formatter, a plot theme, report wording) while the upstream data is identical, you do not need to rerun the expensive ancestors that a naive `tar_make()` would invalidate.

Preferred, provenance-consistent path. If the rendering is its own target, rebuild just it and skip the invalidated upstream:

```r
tar_make(names = "tables", shortcut = TRUE)
```

Escape hatch. When the rendering is a side effect buried inside an expensive target (say a function that both fits models and writes `.typ` files), pull the cached value and re-render by hand against the updated function:

```r
desc <- tar_read(desc_stats)                  # cached value, no recompute
save_table(desc$year_table, "tbl-year.typ")   # updated formatter writes the file
```

`tar_read_raw("desc_stats")` takes the name as a string, which is easier to loop over in a script. Use this only when the inputs are provably unchanged. It writes outside targets' bookkeeping, so the store still reports the target outdated; reconcile with a normal `tar_make()` when convenient, since it reproduces byte-identical output. Never fake freshness with `tar_invalidate()` or by touching files.

The durable fix is structural: split the "fit" and the "format" into separate targets so `shortcut = TRUE` always works and the escape hatch is unnecessary.

Scope invalidation and deletion the same way:

```r
tar_invalidate(names = "model")                 # force rerun, keep stored value
tar_delete(names = c("model", "fit"))           # drop stored value
tar_prune()                                     # drop only stale targets no longer in pipeline
```

Never pass `everything()` to `tar_invalidate()` or `tar_delete()` reflexively. Use a name vector.

Protect expensive targets with a cue that only invalidates on demand:

```r
tar_target(
  slow_model,
  fit_slow(data),
  cue = tar_cue(mode = "never")   # runs only when manually invalidated
)
```

Avoid `tar_destroy()` when a scoped command will do:

| Goal | Command |
|------|---------|
| Drop one target's stored value | `tar_delete(names = x)` |
| Drop stale targets no longer in pipeline | `tar_prune()` |
| Clear error metadata | `tar_destroy(destroy = "meta_errors")` |
| Clear workspaces | `tar_destroy(destroy = "workspaces")` |
| Clear progress | `tar_destroy(destroy = "meta_progress")` |

`tar_destroy()` prompts interactively by default. Do not pass `ask = FALSE` casually.

### Error strategies

| `error =` | Behavior |
|-----------|----------|
| `"stop"` (default) | Abort the whole pipeline |
| `"continue"` | Keep going; mark failed targets as errored |
| `"null"` | Return `NULL` from failed target, keep going |
| `"abridge"` | Let running targets finish; start no new ones |
| `"trim"` | Let running targets finish; start new ones only on healthy parts of the graph |

### Memory options (targets >= 1.11)

| `memory =` | Behavior |
|------------|----------|
| `"auto"` (default) | Transient, except persistent for non-dynamic targets that feed a `pattern` |
| `"transient"` | Unload after each target completes |
| `"persistent"` | Keep in memory to end of pipeline |

## Best practices

1. **Name targets as nouns** (`clean_data`), **functions as verbs** (`clean_data()`). The collision is fine because one is a value and the other is a callable.
2. **Pass data as function arguments**, never via globals. `targets` hashes function bodies, not the calling environment.
3. **Wrap closures.** `purrr::safely()`, `Vectorize()`, and `Rcpp::cppFunction()` hide code from static analysis; wrap them in named R functions so changes get tracked.
4. **Batch tiny work.** A hundred branches of 100 items beats 10,000 targets.
5. **Keep the store small.** Use `butcher::butcher()` or `lean = TRUE` (fixest) to slim model objects before returning.
6. **Compile external docs last.** Put Typst/LaTeX targets at the tail with `cue = tar_cue(mode = "always")`. Ordering is guaranteed and the skip logic rarely pays off for fast compiles.
7. **Verify before running.** `tar_validate()` + `tar_outdated()` catches most mistakes before you spend CPU time.

## Anti-patterns

| Avoid | Do instead |
|-------|------------|
| Global variables inside a target command | Pass data as function arguments |
| Side effects in regular targets | Use `format = "file"` for outputs |
| `tar_target(..., format = "file")` | `tar_file()` or `tar_file_read()` |
| `tar_target(..., format = "qs")` | `tar_qs()` |
| `tar_target(..., format = "file_fast")` | `tar_file()` (the `"file_fast"` format is deprecated) |
| Setting `memory = "transient"` reflexively | Trust `memory = "auto"` unless profiling says otherwise |
| Setting `priority` | Gone since targets 1.10.1, silently ignored |
| Millions of tiny targets | Batch: 100 branches of 100 items, not 10,000 branches |
| Separate file-tracking target + reading target | `tar_file_read()` (one call) |
| Storing full model objects | `butcher::butcher()`, `lean = TRUE` (fixest), or return only the slice you need |
| `devtools::load_all()` for a local package | `install.packages()` + `imports = "pkg"` |
| Reading a literal file path inside a target | Track the file with `tar_file()` so changes invalidate downstream targets |
| Closures inside `tar_target()` commands | Define named functions in `R/` so targets can hash them |

## Example

```r
library(targets)
library(tarchetypes)

tar_source()
tar_option_set(
  packages = "tidyverse",
  format = "qs",
  controller = crew::crew_controller_local(workers = 4)
)

list(
  tar_file_read(
    raw_data,
    "data/penguins.csv",
    read = readr::read_csv(!!.x, show_col_types = FALSE)
  ),
  tar_target(clean_data, clean_penguins(raw_data)),
  tar_target(species, unique(clean_data$species)),
  tar_target(
    species_model,
    fit_species_model(clean_data, species),
    pattern = map(species),
    iteration = "list"
  ),
  tar_target(
    coefs,
    purrr::map_dfr(species_model, broom::tidy, .id = "species")
  ),
  tar_quarto(report, "report.qmd")
)
```
