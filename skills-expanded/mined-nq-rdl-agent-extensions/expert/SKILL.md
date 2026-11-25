---
license: CC-BY-4.0
description: >-
  Idiomatic R for general scripts and analysis code: base R and tidyverse
  style, vectorization, the native pipe and \(x) lambdas (with R version
  conditions), cli-based errors, formatter choice, and performance/IO tools.
  Use for writing, reviewing, or debugging R code that is not specifically a
  package, testing, cli, lifecycle, mirai, CRAN, or Shiny task.
compatibility: >-
  Requires an R runtime. Version conditions checked against the R NEWS for
  4.1.0-4.3.0 and executed on R 4.5.3, 2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# R Expert — Idiomatic R Language Guide

This skill captures the non-inferable delta: R-version-pinned high-drift items,
this project's toolchain preferences, and where to delegate. Generic tidyverse
style (naming, spacing, assignment, basic pipes, vectorization, pre-allocation)
is assumed — follow the [tidyverse style guide](https://style.tidyverse.org/);
do not restate it here.

## High-drift items (verify against your R version)

- Native pipe `|>` over magrittr `%>%` — base R, no import. Available since
  **R 4.1**, but the `_` named-argument placeholder (`x |> f(y = _)`) needs
  **R 4.2+** (R 4.3+ to use `_` with extraction, e.g. `_$col`). Without `_`,
  the piped value can only fill the first argument.
- Lambda shorthand `\(x)` — backslash function syntax, **R 4.1+**
  (e.g. `purrr::map_dbl(x, \(d) d^2)`).
- `testthat` **3rd edition** semantics (`expect_snapshot()`, parallel tests,
  stricter `expect_*`) — opt in via `DESCRIPTION`'s `Config/testthat/edition: 3`.
  See `r-lib-testing`.

## Project toolchain preferences

- User-facing messages/errors via `cli::cli_abort()` / `cli::cli_inform()` /
  `cli::cli_warn()` (not bare `stop()` / `warning()` / `message()`). cli markup
  (`{.val}`, `{.code}`, pluralization) gives consistent, styled output.
- Formatter: follow the project's existing config — `air.toml`/`.air.toml`
  present → `air format .`; otherwise keep the project's convention (e.g.
  `styler`). Do not switch formatters unasked. Lint with `lintr`.
- Performance / IO stack: `bench` (benchmarking), `data.table` / `arrow` /
  `vroom` (large data + fast IO); for parallel or async work use mirai
  (`r:lib-mirai`).

## Delegation

Skills in this `r` plugin (Claude Code names; Codex lists the leaf after the
colon):

- Package development → `r:lib-package-dev`, with deep dives in
  `r:lib-testing` (testthat), `r:lib-cli` (user-facing messages),
  `r:lib-lifecycle` (deprecation), and `r:lib-cran-extrachecks` (CRAN).
- Parallel and async code → `r:lib-mirai`; command-line apps →
  `r:lib-cli-app`.
- Shiny apps are in the separate `shiny` plugin, when installed:
  `shiny:bslib` (layouts, components) and `shiny:bslib-theming` (theming,
  dark mode, brand.yml).
- Style-guide details (naming, spacing, pipes, vectorization): the tidyverse
  style guide — do not restate here.

## References

- [Tidyverse Style Guide](https://style.tidyverse.org/) — canonical style reference
- [Advanced R (Hadley Wickham)](https://adv-r.hadley.nz/)
- [R for Data Science (2e)](https://r4ds.hadley.nz/)
