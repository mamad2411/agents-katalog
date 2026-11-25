---
name: package-conventions
description: Per-package overrides and local conventions that the r-lib package-development skills cannot know -- which packages forbid air format, which are still testthat edition 2, how to detect the naming convention, roxygen version pinning, regenerated documentation committed with the code that changed it, the single NEWS.md development heading that release retitling depends on, test-file pairing, and generating CITATION.cff. Use alongside r-lib:r-package-development, not instead of it.
when_to_use: Working in an R package in this ecosystem, once you already know the general devtools workflow -- specifically before running air format, devtools::document(), adding a NEWS.md entry, or writing new tests or names in an unfamiliar package.
paths:
  - "**/DESCRIPTION"
  - "**/NAMESPACE"
  - "**/NEWS.md"
  - "**/R/*.R"
  - "**/tests/**"
---

# Package conventions: the local deltas

**Use `r-lib:r-package-development` for the workflow itself** (load_all / document /
test / check), `r-lib:testing-r-packages` for testthat, `r-lib:cran-extrachecks`
before a CRAN submission, and `r-lib:lifecycle` for deprecations. Those skills are
installed and this one does not repeat them.

What follows is only what those skills cannot know: the things that differ
**per package** in this ecosystem, where guessing wrong causes a large, noisy diff
or a broken test suite.

## Check these four things before you touch a package

```sh
grep -E '^(Package|Version|Language)|RoxygenNote|Config/(roxygen2|testthat)' DESCRIPTION
cat .lintr 2>/dev/null
ls air.toml 2>/dev/null
grep '^export' NAMESPACE | head -20
```

**1. Is `air format` allowed here?**
Most packages format with air at 100 cols / 2-space, and their `air.toml` files are
byte-identical. At least one mature package **explicitly forbids it**: its HEAD is
not air-clean, so `air format .` reformats hundreds of untouched lines and buries
the real change. Record the answer in `.claude/r-project-policy.json` as
`"noAirFormat": true` and the guard in `r-project-core` will enforce it.
Where air *is* allowed, still prefer `air format <changed-file>` over
`air format .` unless the tree is already clean.

**2. Which testthat edition?**
`Config/testthat/edition: 3` in most. At least one mature package has **no such
field and is still edition 2**, with hundreds of `expect_equivalent()` and
`expect_is()` calls. Write expectations for the edition in use, and do not
"modernise" edition-2 tests as a side effect of an unrelated change.

**3. Which naming convention?**
Both are in active use and both are correct in their own repo:

| Convention | Typical of |
| --- | --- |
| `snake_case`, often with a package prefix | newer, tidyverse-facing packages |
| `camelCase` | the PredictiveEcology lineage; sometimes enforced by `object_name_linter("camelCase")` in `.lintr` |

One package deliberately mixes three conventions because it wraps an external
tool's vocabulary. Take a majority vote over `NAMESPACE` exports; never impose a
convention across a boundary.

**4. Does the installed roxygen2 match what the package pins?**

```sh
grep -E 'RoxygenNote|Config/roxygen2' DESCRIPTION
Rscript -e 'packageVersion("roxygen2")'
```

If they disagree, `devtools::document()` rewrites the **entire** `NAMESPACE` --
one version change replaced `RoxygenNote` with `Config/roxygen2/version` and
emitted one multi-line `importFrom()` per package. Say so rather than committing
the churn. (Watch for packages carrying *both* fields, with the old one stale.)

## Regenerated documentation goes in the same commit as the code

Run `devtools::document()` before committing, and stage the regenerated `man/` and
`NAMESPACE` with the code change that caused them. A commit whose roxygen and `.Rd`
files disagree is a broken intermediate state. Roughly twenty standalone catch-up
commits across these repos (`redoc`, `rebuild documentation`, `with prev`) exist
because the documentation was left behind. A `Stop` hook in this plugin warns when
roxygen lines changed in `R/` but `man/` and `NAMESPACE` are unmodified.

A documentation commit of its own is right only when the code did not cause it:

- a change that is documentation only;
- churn from a tooling update, such as a roxygen2 version change (8.0.0 -> 8.1.0)
  that rewrites every `.Rd` file. Commit that alone, naming the roxygen2 version
  that produced it, so the churn does not bury a real change.

## `NEWS.md`: one development heading, never one per bump

Development notes accumulate under a **single** heading:

```
# <pkg> (development version)

## New features
## Enhancements
## Bug fixes
```

Keep bumping the `Version` in `DESCRIPTION` on every change -- that part is right --
but never add a heading per bump (`# <pkg> 1.2.0.9027`). File the bullet in the
matching subsection of the development section instead, adding the subsection if it
is missing.

At release, `usethis::use_version()` retitles exactly **one** heading:
`# <pkg> (development version)` becomes `# <pkg> 1.2.1`. A numbered development
heading survives that retitle untouched and is left sitting *above* the release
heading, so the shipped `NEWS.md` advertises versions that were never released and
their bullets fall outside the section for the version that actually shipped.

Before adding an entry, look at what is already there:

```sh
head -20 NEWS.md
grep -nE '^#+ .*[0-9]+\.[0-9]+\.[0-9]+\.9[0-9]+' NEWS.md   # dev headings that should not exist
```

If the second command prints anything, the file already carries the mistake. Do not
copy it -- that is exactly how it spreads, one session at a time. Fold those
headings back in: move each bullet into the matching subsection of the development
section and delete the heading. Do that **on one branch only**, and say so, because
it rewrites lines near the top of a file that every open pull request also touches,
so it conflicts with everything in flight.

If the top of the file is a released version with no development heading, add one
above it.

## Test-file pairing, and the drift that breaks it

`R/{name}.R` pairs with `tests/testthat/test-{name}.R`. The rule is stated in most
of these packages and violated in practice almost entirely through hyphen /
underscore drift -- `R/ext_social_climate_fire.R` covered by
`test-ext_social-climate-fire.R`, and so on for nine files in one package.

When adding a source file, create the matching test file with the **identical
stem**. When you cannot find a test for a file, search both separator spellings
before concluding there is none.

Where a package documents a parallelism setting for its suite, honour it -- some
must run with `TESTTHAT_PARALLEL=false`.

## `.Rbuildignore` needs `^\.claude$`

`R CMD check ... NOTE: Found the following hidden files and directories: .claude`
occurs 28 times in the session record. A `PostToolUse` hook in this plugin appends
the entry automatically whenever a `.claude/` directory appears beside a
`DESCRIPTION`.

## `CITATION.cff`

GitHub's "Cite this repository" button and Zenodo both read `CITATION.cff` at the
repository root. Generate it from `DESCRIPTION` at each version bump rather than
editing it by hand:

```r
cffr::cff_write(dependencies = FALSE)
```

`dependencies = FALSE` keeps a `references:` block listing every dependency out of the
file. Then, before committing:

- **Check `doi:`.** cffr 1.4.2 writes a CRAN DOI for any package it finds in a
  configured repository, including one that is only on r-universe or GitHub. Run the
  `--file` check from `r-project-core:citation-integrity` on the file; remove a DOI
  that does not resolve.
- ORCIDs appear only for authors whose `Authors@R` entry carries
  `comment = c(ORCID = "...")`.
- Add `^CITATION\.cff$` to `.Rbuildignore`, or `R CMD check` notes a non-standard
  top-level file.

Do not use `cffr::cff_gha_update()`: the workflow it installs commits and pushes on its
own.

## Branches, CI, and installing into a project

The sequence -- check branch and freshness, work on `development`, test, push,
wait for clean CI, merge to `main`, install into the project from remote `main` --
is its own skill: `package-change-workflow`. Follow it for any change to a package
a project depends on.

Do not commit or push unless asked. Stage named paths; never `git add -A` --
another session may share the worktree.
