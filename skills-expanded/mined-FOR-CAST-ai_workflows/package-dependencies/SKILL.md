---
name: package-dependencies
description: "The single most frequent failure class in R package work -- a symbol used but not declared. Covers pkg:: qualification vs @importFrom, the base-adjacent packages that are the repeat offenders (stats, utils, methods), Imports vs Suggests vs Remotes, utils::globalVariables for data.table NSE, and the sanctioned way to reach a non-exported helper."
when_to_use: "Adding a call to another package's function; a check reports 'no visible global function definition', 'no visible binding for global variable', or an undeclared import; deciding between pkg:: and @importFrom; adding a dependency; using ::: on an internal helper."
paths:
  - "**/DESCRIPTION"
  - "**/NAMESPACE"
  - "**/R/*.R"
---

# Declaring what you use

This is the most frequent failure class in the corpus by a wide margin. It is
cheap to prevent and always caught late -- by `R CMD check` on CI, or by a user.

## The rule

Every symbol from another package must be **both**

1. reachable -- either `pkg::fun()` at the call site, or `@importFrom pkg fun`, and
2. declared in `DESCRIPTION` under `Imports:` (or `Depends:`).

Doing one without the other is what fails. So is using a function from a package
that is only in `Suggests:` without guarding it.

## The repeat offenders are base-adjacent

`stats`, `utils`, `methods`, `tools`, `grDevices`, `parallel`. They are attached in
an interactive session, so the code works while you write it and fails only under
`R CMD check` or in a worker.

Named in the record: `setNames` (`stats::`), `head` (`utils::`),
`packageVersion` (`utils::`), `getFromNamespace` (`utils::`), `dbDisconnect`
(`DBI::`). One of these cost **four commits and a spurious version bump** for a
single line -- a fix, a revert of the fix, a re-application of the identical diff,
and then a separate commit to add the NEWS bullet.

Before finishing, grep your diff for bare calls to those:

```sh
git diff -U0 -- R/ | grep '^+' | grep -nE '\b(setNames|head|tail|packageVersion|getFromNamespace|str|modifyList|capture\.output|installed\.packages)\('
```

## `pkg::` or `@importFrom`? Detect the package's strategy

Both are defensible and the corpus contains both:

- Some packages have **zero `@importFrom` and an empty NAMESPACE import section** --
  everything is `pkg::`-qualified.
- Others use `@importFrom` heavily (tens of tags).

Check before adding:

```sh
grep -c importFrom NAMESPACE
```

Follow whichever the package already does. In code that runs in another R process
(workers, `callr`, Quarto chunks), always `pkg::`-qualify regardless -- worker
environments do not reliably attach packages.

## `utils::globalVariables()` for NSE

`data.table` and tidyverse NSE produce `no visible binding for global variable`
NOTEs (29 occurrences in the record). Declare the symbols:

```r
utils::globalVariables(c("pixelID", "cohort_id", "B", ".N", ".SD"))
```

Keep this list in one place (commonly `R/<pkg>-package.R`), and add
`globalVariables` to `air.toml`'s `skip` list so the formatter does not re-wrap the
hand-curated vector on every run.

## Reaching a non-exported helper

`pkg:::internal()` is an `R CMD check` NOTE and a CRAN blocker. The sanctioned
pattern, from a package in this corpus:

```r
#' non-exported objects and functions from other packages
#' @importFrom utils getFromNamespace
#' @keywords internal
#' @rdname imports
assessGoogle <- utils::getFromNamespace("assessGoogle", "reproducible")
```

Collect these in one `R/imports.R`, and record the reason in `NEWS.md`. It is still
a dependency on another package's internals -- prefer asking upstream to export it.

## Imports, Suggests, Remotes

- **`Imports:`** -- used unconditionally in `R/`. Add it the moment you add the call,
  in the *same* commit; a dependency added one commit after the code is a broken
  intermediate state.
- **`Suggests:`** -- used only in tests, examples, or vignettes, or behind a guard.
  Guard every use: `if (!requireNamespace("pkg", quietly = TRUE)) skip("needs pkg")`.
  Packages here run a dedicated `nosuggests` CI job, which is exactly what catches
  an undeclared `Imports:` masquerading as a suggestion.
- **`Remotes:`** -- development versions from GitHub. The house form is
  `owner/repo@branch`, matched by a version floor in `Imports:` where the code needs
  one. **Never request the same repo at two different branches anywhere in the
  dependency graph**: the resolver treats the solve as one problem, so a single
  double-request fails the whole solve *and* reports every other package as
  conflicting, which reads like a far larger problem than it is.
- **Justify every new dependency.** Stated in several packages. A one-line reason in
  the commit body is enough; "it was convenient" is not.

## Drift happens on the remote too

A branch pin can go stale without any local change -- one pinned `@development`
branch silently fell nine commits behind `main`, leaving the pin resolving to a
version below the floor another package required. Only a periodic re-resolve
catches this. If a package suddenly fails to solve and nothing local changed,
re-resolve before debugging your own code.
