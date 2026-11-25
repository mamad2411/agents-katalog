---
license: CC-BY-4.0
description: >-
  Prepare an R package for CRAN submission or resubmission, or answer CRAN
  reviewer feedback, by checking what `devtools::check()` does not: Title and
  Description wording, `\value`/`@return` and examples, `\dontrun{}`, URLs and
  file URIs, `cph` roles, LICENSE year, and method references. Distinguishes
  check NOTEs from reviewer requests.
compatibility: >-
  Requires R; checks use `R CMD check --as-cran` (or devtools), urlchecker,
  and usethis. Claims verified on 2026-09-29 against CRAN Repository Policy
  revision 6875, the CRAN submission checklist, Writing R Extensions for
  R 4.5.3, and `R CMD check --as-cran` runs on R 4.5.3.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# CRAN Extra Checks

Find the problems a CRAN reviewer will raise that a default local check does
not. CRAN's rules change: when a verdict matters, recheck the
[CRAN Repository Policy](https://cran.r-project.org/web/packages/policies.html)
and the [submission checklist](https://cran.r-project.org/web/packages/submission_checklist.html).
If they are unreachable, say which items rest on this file's 2026-09-29
verification.

For the detailed rules with examples (Title, Description, documentation,
URLs, and administrative items), the standard reviewer wording, and the tool
list, read [references/cran-details.rst](references/cran-details.rst).

## Scope and authorization

- **Review request** ("check", "review", "is it ready"): read the package and
  report findings with the fix for each. Do not edit files.
- **Fix request** ("fix", "prepare", "update"): edit the files within the
  requested scope without asking again. Report anything outside that scope
  as a finding instead of editing it.
- Never submit to CRAN (`devtools::submit_cran()`, `devtools::release()`, the
  web form) or email the CRAN team. The maintainer does that.
- Running local checks (`R CMD check`, `urlchecker::url_check()`) is part of
  a review. The URL checks need network access; if it is unavailable, say the
  URL items were not verified.

## Which tool catches what

Label every finding with its source, so the user knows what blocks
submission:

- **check**: `R CMD check --as-cran` reports it. CRAN expects no WARNINGs and
  no significant NOTEs.
- **reviewer**: the check passes, but CRAN reviewers routinely ask for it by
  email and the package is returned until it is fixed.
- **convention**: a practice of an organisation or this skill; not a CRAN
  rule.

`devtools::check()` runs with `remote = FALSE`, which sets
`_R_CHECK_CRAN_INCOMING_=false`, so its default run **skips** the incoming
checks that report Title and Description problems. Use
`devtools::check(remote = TRUE)` or
`R CMD check --as-cran pkg_x.y.z.tar.gz`. CRAN also checks file URIs in
`README.md` (`_R_CHECK_CRAN_INCOMING_CHECK_FILE_URIS_=true`), which a local
`--as-cran` run on R 4.5.3 does not do unless you set that variable.

## Checklist

| Item | Source | Passes when |
|---|---|---|
| Title case | check | `tools::toTitleCase()` leaves the Title unchanged |
| Title does not start with or equal the package name | check | "The Title field starts with the package name" is absent |
| Title has no "A Toolkit for", "Tools for", "for R", "in R" | reviewer | Every CRAN package is for R; say what it does |
| Title ≤ 65 characters, one line, no final period | reviewer / WRE | Listings may truncate at 65 characters |
| Description does not start with "This package", the package name, or the title | check | NOTE "should not start with the package name, 'This package' or similar" is absent |
| Description is several complete sentences in one paragraph | WRE / reviewer | Explains what the package does and why; no one-liners |
| Software, package, and API names in single quotes; functions as `foo()` without quotes | checklist | `'dplyr'`, `'OpenSSL'`, `case_when()` |
| Acronyms expanded on first use | reviewer | "Extended Speech Assessment Methods Phonetic Alphabet (X-SAMPA)" |
| References as `Author (year) <doi:...>`, URLs as `<https:...>` | checklist | No space after `doi:` or `https:` |
| Every exported function's Rd has `\value` (`@return`/`@returns`), also for `@keywords internal` topics | reviewer | Side-effect functions say so, e.g. "No return value, called for side effects" |
| Exported functions with a useful result have runnable `@examples` | reviewer | Examples run in a few seconds each (policy) |
| No commented-out code in examples | reviewer | Use toy data that runs instead |
| `\dontrun{}` only when the code truly cannot run (missing software, credentials) | reviewer | Slow examples use `\donttest{}`; examples that must error use `try()`; conditional ones use `@examplesIf` or `if (...)` |
| Unexported functions have no examples | reviewer | Use `@noRd`, drop the examples, or export the function; reviewers have asked to "omit these examples or export these functions" |
| Examples and tests use at most 2 cores | policy | Examples set, e.g., `daemons(2)` or `mc.cores = 2` |
| URLs resolve without redirect, including `http://` → `https://` | check (remote) | `urlchecker::url_check()` is clean except aspirational CRAN URLs |
| No file URIs to files excluded from the build | check (CRAN incoming) | README links only to files that ship, or to full URLs |
| Copyright holders are clear | policy; `cph` is a reviewer request | `Authors@R` gives `cph` to whoever holds copyright; reviewers often ask for `cph` even for a sole author |
| LICENSE year is current for the submission (MIT-style `YEAR:` files) | reviewer | Reviewers have asked "Should the year in the LICENSE file be updated?" |
| `NEWS.md` and `cran-comments.md` exist | convention | `usethis::use_news_md()`, `usethis::use_cran_comments()` |
| Method references | reviewer | Add `<doi:...>` references to Description, or reply that there are none (optionally note it in `cran-comments.md`) |

## Repository context

- If `README.Rmd` exists, edit it, never `README.md`, then run
  `devtools::build_readme()`.
- Before the first release, CRAN URLs for the package itself (for example
  `https://CRAN.R-project.org/package=pkgname` and CRAN badges) do not resolve
  yet. Leave them and explain them in `cran-comments.md` if the check flags
  them.
- README install instructions should work after acceptance:
  `install.packages("pkgname")`.
- Organisation rules are conventions. For example, Posit-maintained packages
  add `person("Posit Software, PBC", role = c("cph", "fnd"), comment = c(ROR = "03wc8by49"))`;
  apply such a rule only when the package belongs to that organisation.

## Example: a first submission review

For a package whose DESCRIPTION reads

```
Title: tidyclean: a toolkit for cleaning data frames in R
Description: This package provides functions for cleaning data frames using dplyr.
URL: http://github.com/example/tidyclean
```

`R CMD check --as-cran` (R 4.5.3, remote checks on) reports the Title starting
with the package name, the Title case, the Description start, and the `http`
URL that redirects to `https`. It does **not** report the missing `\value` on
an exported function, a commented-out example, "toolkit ... in R", the
one-sentence Description, the unquoted `dplyr`, or the missing `cph` role.
Report those as reviewer items. A fix could read:

```
Title: Clean and Tidy Data Frames
Description: Removes empty rows, standardises column names, and fixes
    common encoding problems in data frames. Works with base data frames and
    with 'dplyr' tibbles. Designed for preparing messy spreadsheet exports
    for analysis.
URL: https://github.com/example/tidyclean
```

## Report format

Group findings by file (DESCRIPTION, `R/` and `man/`, README, other). For each
one give the source label (check, reviewer, convention), the evidence (file
and line or check output), and the fix. End with what was not verified, such
as URL checks without network access.
