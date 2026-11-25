---
name: r-lib-testing
license: CC-BY-4.0
description: >-
  Write, organize, and debug testthat (3rd edition) tests for R packages:
  test_that()/describe(), expectations, snapshot tests, fixtures and
  test_path(), helper vs setup files, mocking with local_mocked_bindings(),
  withr cleanup, skips, and which testthat version a feature needs. Use for
  tests/testthat/ work or failing R package tests.
compatibility: >-
  Requires R, testthat >= 3.0.0 (third edition), and withr. Newer
  expectations need the versions marked beside them. Examples verified with
  testthat 3.3.2, withr 3.0.3, devtools 2.5.2, and pkgload 1.5.3 on
  2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Testing R Packages with testthat

This file holds the decisions that most often go wrong: which files run when,
which testthat version a feature needs, and how to keep tests self-contained.
Check the installed version with `packageVersion("testthat")` and the testthat
NEWS (https://testthat.r-lib.org/news/) before using a feature marked with a
version; if the package's `Suggests: testthat (>= x.y.z)` is lower, raise it
or avoid the feature.

## Choose a reference

| Read | When you need |
|---|---|
| [references/snapshots.rst](references/snapshots.rst) | Snapshot workflow, `transform`, variants, snapshot files, or CI behaviour |
| [references/fixtures.rst](references/fixtures.rst) | Constructor and `local_*()` fixtures, static files, helper and setup files in depth, temporary files, database fixtures |
| [references/mocking.rst](references/mocking.rst) | `local_mocked_bindings()`/`with_mocked_bindings()` details, S3/S4/R6 mocking, databases, APIs, files, random numbers, webfakes/httptest2 |
| [references/bdd.rst](references/bdd.rst) | `describe()`/`it()` specifications, nesting, pending specs, or mixing BDD with `test_that()` |
| [references/advanced.rst](references/advanced.rst) | Skips (including `skip_unless_r()`), flaky tests, secrets, custom expectations, CRAN constraints, parallel tests |

## Setup

```r
usethis::use_testthat(3)   # tests/testthat/, tests/testthat.R, Config/testthat/edition: 3
usethis::use_test("foofy") # tests/testthat/test-foofy.R, paired with R/foofy.R
```

## Which files run when

| File in `tests/testthat/` | `devtools::load_all()` | Test runners: `devtools::test()`, `test_file()`, `test_dir()`, `R CMD check` |
|---|---|---|
| `helper-*.R` | sourced | sourced |
| `setup-*.R` | **not** sourced | sourced |
| `test-*.R` | not sourced | run |
| `fixtures/` (convention) | not sourced | read with `test_path("fixtures", ...)` |

- Put reusable test code (constructors, custom expectations, skip helpers) in
  `helper-*.R` so it is also available interactively after `load_all()`.
- Put global test-only side effects (options, connections, caches) in
  `setup-*.R`. Register cleanup with `withr::defer(..., teardown_env())` or
  `.local_envir = teardown_env()`.
- Verified with testthat 3.3.2: after `load_all()` a helper object exists and a
  setup side effect does not; `devtools::test()` and `test_dir()` see both.

## Test structure

```r
test_that("str_trunc() truncates from the right", {
  expect_equal(str_trunc("This string is moderately long", 20), "This string is mo...")
})
```

Descriptions state behaviour, not implementation. `describe()`/`it()` is an
alternative syntax; `it()` with no body is a pending (skipped) spec. Since
testthat 3.3.0, `test_that()`, `describe()`, and `it()` nest arbitrarily.

## Expectations and version conditions

```r
# Equality
expect_equal(10, 10 + 1e-7)              # numeric tolerance
expect_identical(10L, 10L)               # exact
expect_equal(x, y, ignore_attr = TRUE)   # replaces expect_equivalent()

# Conditions
expect_error(f(), class = "mypkg_error") # prefer class over message regex
expect_no_error(f()); expect_warning(g()); expect_no_message(h())

# Types and structure
expect_type(obj, "list"); expect_s3_class(model, "lm"); expect_length(x, 10)

# Sets (testthat >= 3.1.9)
expect_contains(fruits, "apple")
expect_in("apple", fruits)

# testthat >= 3.3.0
expect_all_equal(x, 1)                   # every element equals the value
expect_all_true(x > 0); expect_all_false(x < 0)
expect_disjoint(set1, set2)
expect_r6_class(obj, "MyR6Class")
expect_shape(m, dim = c(10, 5))          # name the argument: nrow =, ncol =, or dim =
```

`expect_shape(m, c(10, 5))` fails with "`...` must be empty" because the shape
must be passed by name.

| Feature | Needs testthat |
|---|---|
| Third edition, `expect_snapshot()`, `local_edition()` | 3.0.0 |
| `expect_contains()`, `expect_in()` | 3.1.9 |
| `local_mocked_bindings()`/`with_mocked_bindings()` (experimental in 3.1.7) | 3.2.0 |
| `expect_all_*()`, `expect_disjoint()`, `expect_r6_class()`, `expect_shape()`, `skip_unless_r()`, `test_file(desc =)` with `it()`, arbitrary nesting | 3.3.0 |
| `devtools::test(shuffle = TRUE)`, `devtools::test(reporter = "slow")` | 3.3.0 |
| New snapshots fail on CI instead of being written | 3.3.0 |

## Self-contained tests

Each test creates its own inputs and undoes its own side effects. Repeat setup
code rather than sharing top-level objects between tests; a test that relies on
an object created outside `test_that()` breaks when run alone or shuffled.

```r
test_that("my_function() respects options", {
  withr::local_options(my_option = "test_value")
  withr::local_envvar(MY_VAR = "test")
  path <- withr::local_tempfile(lines = c("a", "b", "c"))

  expect_equal(my_function(path)$setting, "test_value")
})  # everything above is restored or deleted here
```

Write only to temporary paths (`withr::local_tempfile()`,
`withr::local_tempdir()`), never into the package directory. Read fixtures with
`test_path("fixtures", "data.rds")`, which works from `devtools::test()`,
`R CMD check`, and interactive runs; a bare relative path does not.

A reusable fixture that cleans up after the calling test takes an environment:

```r
local_temp_csv <- function(data, env = parent.frame()) {
  path <- withr::local_tempfile(fileext = ".csv", .local_envir = env)
  write.csv(data, path, row.names = FALSE)
  path
}
```

## Snapshots

Use snapshots for output that is hard to assert programmatically, especially
user-facing errors, warnings, and messages. Snapshot the error, not a regex of
it:

```r
test_that("validate_input() explains a NULL input", {
  expect_snapshot(validate_input(NULL), error = TRUE)
})
```

Snapshots live in `tests/testthat/_snaps/`. Review changes with
`testthat::snapshot_review("file")` and accept with
`testthat::snapshot_accept("file")`; never accept automatically in CI.

## Mocking

Replace a dependency for the duration of one test. The mocked binding must
exist in the package namespace (or be named with `.package`).

```r
test_that("my_function() handles the API response", {
  local_mocked_bindings(
    external_api = function(...) list(status = "success", data = "mocked")
  )
  expect_equal(my_function_that_calls_api()$status, "success")
})
```

`with_mock()` and `local_mock()` were deprecated in testthat 3.0.0 and are
defunct since 3.3.0; replace them with `local_mocked_bindings()`.

## Modernizing older tests

- `context()` → delete (the file name is the context)
- `expect_equivalent()` → `expect_equal(ignore_attr = TRUE)`
- `with_mock()` → `local_mocked_bindings()`
- `expect_is()` → `expect_type()`, `expect_s3_class()`, or `expect_s4_class()`
- `setup()`/`teardown()` → `setup-*.R` files or `withr::defer()`

## Running tests

```r
devtools::test()                                  # whole suite
devtools::test(filter = "foofy")                  # test-foofy.R
testthat::test_file("tests/testthat/test-foofy.R")
devtools::check()                                 # includes tests, as CRAN runs them
```
