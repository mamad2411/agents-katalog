---
name: project-tests-ci
description: "Add a hermetic testthat suite and GitHub Actions CI to an R + renv project that is not an R package -- an analysis, pipeline or simulation project. Tests the functions in R/ with closed-form cases and no real data, proves each test can fail and the suite needs nothing outside the repository, and ships a CI template whose non-obvious choices (setup-renv caching, stock system libraries, R_PROFILE_USER) are already made. Use when setting up, extending, or fixing tests or CI for such a project."
when_to_use: "Adding tests or CI to an R project without a DESCRIPTION; tests pass locally but fail in CI; a CI run is slow, cold, or never ran; configuring setup-r or setup-renv; a test reads or writes real data; turning a recorded gotcha into a regression test."
argument-hint: "[project path]"
paths:
  - "**/.github/workflows/**"
  - "**/tests/testthat/**"
---

# Testing and CI for an R project that is not a package

For an R *package*, use `r-lib:testing-r-packages` and `r-lib:r-package-development`.
This skill is for a project with no `DESCRIPTION`, where nothing drives the suite
for you.

- **Test the functions the project calls, not the scripts that call them.**
- **Tests run in a clone with no data, no outputs and no built state** -- that is
  what CI has.
- **The CI details are not obvious** and several widely-copied choices are wrong: an
  extra cache step, a spatial PPA, `R_PROFILE_USER: /dev/null` on a step that needs
  renv, and the default `setup-renv` cache setting, which discards a failed cold build.

A pipeline framework adds its own checks on top of this; for a `{targets}` project,
`targets-testing-ci` in `r-targets` lists them.

## Before starting

**Find out, without asking:**

- Does `R/` hold standalone scripts? Sourcing `R/` wholesale executes every file. Check
  with `top_level_side_effects()` from `assets/test-project-sources.R`. If the project
  sources a named list instead, the tests must source that same list.
- Every setting that changes what the project does when it loads: environment
  variables, options, switches in the local config file.
- The R version in `renv.lock`.
- Which branch work is integrated on, and whether any GitHub dependency repo is private
  (`gh repo view <owner>/<repo> --json visibility`).

**Collect these decisions and ask them together, in one prompt:**

- whether CI is wanted at all, given cold builds can take hours of runner minutes on a
  private repository;
- whether a private dependency justifies a PAT secret;
- where heavy steps run -- a shared control node is the wrong place for test suites;
  use a compute node, or a memory-capped scope (`hpc-cluster-runs`);
- whether refreshing the lockfile against current CRAN is on the table.

## Step 1 -- a hermetic test suite

Read `references/test-suite.md`. In brief:

1. `tests/testthat/test-*.R`, helpers in `helper-*.R`, run through `assets/run-tests.R`
   (edition 3 needs **both** `TESTTHAT_EDITION=3` and `NOT_CRAN=true`).
2. Record testthat in `renv.lock` with `renv::install("testthat", lock = TRUE)`; diff the
   lockfile before and after. Never `renv::snapshot()`.
3. Tests never touch real data: redirect locations with a directory argument or
   `withr::local_dir(withr::local_tempdir())`.
4. `skip_if_not()` for assertions that need built artefacts.
5. Closed-form test cases; turn recorded gotchas into regression tests.
6. For each test file, break the rule it guards and confirm it fails.
7. Add `assets/test-project-sources.R`: no top-level side effects in `R/`, sourcing
   order does not matter, no stray `browser()`.

## Step 2 -- prove it is hermetic

A `git clone --shared` with the renv library symlinked in, run with the lockfile's R and
`R_ENVIRON_USER=/dev/null`, checking for **writes** (including to gitignored data paths),
not just failures. Details in `references/test-suite.md`. One such run found three failures
in a suite that was green locally.

## Step 3 -- the CI workflow

Start from `assets/check.yaml` and `assets/ci-sysreqs.R`; read
`references/github-actions.md` before changing either. The choices most often got wrong:

- `setup-r` with `r-version: renv`; `setup-renv@v2` with **`bypass-cache: never`**, and no
  `actions/cache` step.
- System libraries from the stock distribution, derived from `renv.lock` -- **no PPA**.
- `R_PROFILE_USER: /dev/null` only on steps that must not start renv, with explicit `repos`.
- A private dependency needs a PAT; `GITHUB_TOKEN` reads only this repository.
- A guard that the tests left the checkout -- and gitignored data paths -- untouched.
- Current action versions, checked rather than copied. The template pins actions by major
  tag; once it is in the project, pin them to SHAs and let Dependabot maintain them.

Estimate source builds first: `Rscript assets/cold-cache-estimate.R renv.lock noble`.

## Step 4 -- the first run

1. Trigger the workflow with `workflow_dispatch` on the working branch. **Until it has run,
   any timing is a guess** -- in one project the quoted times belonged to another job.
2. Record the real cold-cache time; set `timeout-minutes` from it with margin.
3. Read the restore log for "The dependency tree was repaired", and the template's
   `renv::status()` warning: if they appear, CI is testing versions the lockfile does not
   record. Say so in the project docs.
4. Seed the cache with a run on the default branch; PR caches are not visible to it.

## Checklist

- [ ] `tests/testthat/` with helpers; `scripts/run-tests.R` sources what the project sources
- [ ] testthat in `renv.lock`; `TESTTHAT_EDITION=3` and `NOT_CRAN=true`
- [ ] No test reads or writes real data; artefact-dependent checks skip
- [ ] Each test file shown to fail when its rule is broken
- [ ] Hermetic `--shared` clone run: no failures, no writes
- [ ] Workflow: syntax job; tests job with stock sysreqs and `bypass-cache: never`
- [ ] Dependency visibility checked; PAT only if a dependency is private
- [ ] First run triggered, cold time recorded, restore log read

## Bundled files

| File | Use |
| --- | --- |
| `assets/run-tests.R` | the suite runner |
| `assets/test-project-sources.R` | side-effect, sourcing-order and `browser()` tests |
| `assets/check.yaml` | the workflow |
| `assets/ci-sysreqs.R` | system libraries from `renv.lock` via pak |
| `assets/cold-cache-estimate.R` | how many packages build from source |
| `references/test-suite.md` | the suite, hermetic proof, load-time traps |
| `references/github-actions.md` | action internals, caching, system libraries, renv surprises |
