---
name: r-lib-cli
license: CC-BY-4.0
description: >-
  Write R code that reports to users with cli: errors, warnings, and messages
  via cli_abort()/cli_warn()/cli_inform() (with call = caller_env() in
  helpers), inline markup such as {.arg}/{.val}, pluralization with {?s} and
  qty(), progress bars, semantic output, themes, and snapshot tests of cli
  output. Also for replacing stop()/warning()/message() and debugging cli errors.
compatibility: >-
  Requires R and the cli package; cli_abort(), cli_warn(), and cli_inform()
  also need rlang. Examples verified with cli 3.6.6, rlang 1.3.0, and
  testthat 3.3.2 (third edition) on 2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# CLI for R Packages

cli formats console output with glue-style `{}` interpolation, inline markup
(`{.cls value}`), pluralization (`{?}`), and semantic conditions. This file
holds the rules that most often break real code. The catalogues are in
`references/`. Verify against https://cli.r-lib.org when output format or an
API detail matters.

## Choose a reference

| Read | When you need |
|---|---|
| [references/inline-markup.rst](references/inline-markup.rst) | An inline class beyond the common ones below, vector collapsing and truncation, custom collapse separators, or advanced pluralization |
| [references/conditions.rst](references/conditions.rst) | Error design, condition classes, rlang integration, warning frequency, base R migration (`stop()`, `warning()`, `message()`, `sprintf()`, `paste()`), or anti-patterns |
| [references/progress.rst](references/progress.rst) | Progress bars beyond a simple loop: custom formats, progress variables, nested or parallel progress, Shiny, C-level progress |
| [references/themes.rst](references/themes.rst) | Themes, selectors, containers (`cli_div()`, `cli_par()`), palettes, or accessibility |
| [references/ansi-operations.rst](references/ansi-operations.rst) | `ansi_*()` string functions, hyperlinks, colour and symbol detection, `test_that_cli()`, performance, or debugging |

## Common calls

- Conditions: `cli_abort()`, `cli_warn()`, `cli_inform()` with a named
  character vector of bullets.
- Inline classes: `{.arg x}`, `{.cls data.frame}`, `{.code expr}`,
  `{.field name}`, `{.file path}`, `{.fn pkg::fun}`, `{.pkg name}`,
  `{.val {x}}`, `{.var name}`, `{.obj_type_friendly {x}}`, `{.emph}`,
  `{.strong}`.
- Semantic output: `cli_h1()`/`cli_h2()`/`cli_h3()`, `cli_text()`,
  `cli_alert_success()`/`_danger()`/`_warning()`/`_info()`, `cli_ul()`/`cli_ol()`/`cli_dl()`
  with `cli_li()` and `cli_end()`, `cli_code()`, `cli_verbatim()` (no
  interpolation).
- Progress: `cli_progress_step("Loading data")` for sequential steps;
  `cli_progress_bar("Processing", total = n)` plus `cli_progress_update()` in
  the loop. A bar closes automatically when the function that created it
  exits.

Bullet names: `"x"` problem, `"!"` warning, `"i"` information, `"v"` success,
`"*"` bullet, `">"` arrow, `" "` indented continuation.

## Rule 1: interpolate data; never paste it into the format string

The format string is evaluated as glue. A value inserted with `{x}` is not
evaluated again, but text pasted into the format string is. Pasted user
input that contains braces raises "Could not evaluate cli `{}` expression".

```r
tmpl <- "{name}.csv"
cli_abort(paste0("Invalid template: ", tmpl))   # WRONG: evaluates `name`
cli_abort("Invalid template: {.val {tmpl}}")     # Right: Invalid template: "{name}.csv"
```

Double braces print literal braces:

```r
cli_text("Use {{variable}} syntax in glue")
#> Use {variable} syntax in glue
```

## Rule 2: every `{?}` needs a quantity in the same string

- The quantity is the nearest interpolated value **before** the `{?}`. If
  none comes before it, cli uses the next one after it.
- A **numeric** value is used as the count and must be length 1. Any other
  value (character vector, list) counts by its length. A length-2 numeric
  vector (for example the result of `which()`) fails with
  `length(object) == 1 is not TRUE`.
- Each element of a `cli_abort()`/`cli_warn()`/`cli_inform()` vector is a
  separate string. A bullet with `{?s}` and no quantity fails with "Cannot
  pluralize without a quantity".
- `qty(n)` sets the quantity without printing it. `no(n)` prints "no" for
  zero. Three alternatives are zero/one/many: `{?no/the/the}`.
- In package code, helpers used inside the string are found in the calling
  environment: import `qty` and `no` (`@importFrom cli qty no`) or write
  `cli::qty()`.

```r
nfile <- 0
cli_text("Found {no(nfile)} file{?s}")                     #> Found no files
cli_text("Found {nfile} file{?s}: {?no/the/the} file{?s}")  #> Found 0 files: no files

nupd <- 3; ntotal <- 10
cli_text("{nupd}/{ntotal} {qty(nupd)} file{?s} {?needs/need} updates")
#> 3/10 files need updates

bad <- which(c(1, -1, -2) <= 0)                             # c(2L, 3L)
cli_text("Element{?s} {bad} {?is/are} not positive.")       # WRONG: numeric length 2
cli_text("{qty(length(bad))}Element{?s} {bad} {?is/are} not positive.")  # WRONG too
cli_text("Element{?s} {as.character(bad)} {?is/are} not positive.")
#> Elements 2 and 3 are not positive.
```

`qty()` does not rescue a numeric vector interpolated later in the string:
that value becomes the quantity for the next `{?}` and fails the same way
(`{.val {bad}}` too). Convert the displayed value with `as.character()`.

## Rule 3: attribute errors to the user's call

By default the error names the function that called `cli_abort()`. An input
checker called from user-facing functions should report the caller instead.
Take `call = caller_env()` (and `arg = caller_arg(x)` for the argument
name), pass `call` to `cli_abort()`, and pass it on through nested helpers.
Use `call = NULL` to show no call.

```r
check_positive <- function(x, arg = rlang::caller_arg(x),
                           call = rlang::caller_env()) {
  bad <- which(x <= 0)
  if (length(bad) > 0) {
    cli::cli_abort(c(
      "{.arg {arg}} must be positive.",
      "x" = "Element{?s} {as.character(bad)} {?is/are} not positive."
    ), call = call)
  }
  invisible(x)
}

fit <- function(weights) {
  check_positive(weights)
  # ...
}
```

## Rule 4: test condition output with snapshots

Use `expect_snapshot(error = TRUE)` and cover both the singular and the
plural wording. Snapshots record ASCII bullets without colour.

```r
test_that("fit() reports non-positive weights", {
  expect_snapshot(error = TRUE, {
    fit(c(1, -1))
    fit(c(-1, -2))
  })
})
```

testthat 3.3.2 writes this to `tests/testthat/_snaps/<file>.md`:

```
    Code
      fit(c(1, -1))
    Condition
      Error in `fit()`:
      ! `weights` must be positive.
      x Element 2 is not positive.
    Code
      fit(c(-1, -2))
    Condition
      Error in `fit()`:
      ! `weights` must be positive.
      x Elements 1 and 2 are not positive.
```

The snapshot shows `fit()`, not `check_positive()`, and the user's argument
name `weights`. For more condition tests (classes, warning frequency, mocking),
read [references/conditions.rst](references/conditions.rst).

## Migrating from base R

Replace `stop()`, `warning()`, and `message()` with `cli_abort()`,
`cli_warn()`, and `cli_inform()`. Turn `paste()`/`sprintf()` concatenation
into interpolation (Rule 1), add pluralization (Rule 2) and `call`
(Rule 3), then update snapshots (Rule 4). For side-by-side conversions, read
"Migration Guide" in [references/conditions.rst](references/conditions.rst).

```r
# Before
stop("x must be numeric")
# After
cli_abort(c(
  "{.arg x} must be numeric.",
  "x" = "You supplied {.obj_type_friendly {x}}.",
  "i" = "Use {.fn as.numeric} to convert."
))
```

## Related packages

- **rlang**: condition objects, `caller_env()`, `caller_arg()`.
- **glue**: the `{}` syntax that cli builds on.
- **testthat**: snapshot tests for cli output.
