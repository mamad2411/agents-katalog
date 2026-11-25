---
name: targets-testing-ci
description: "Tests, a static pipeline validator and CI for a {targets} + renv project, on top of the general project-tests-ci skill. Ships a tested validator that catches what targets itself accepts -- commands naming another project's target or a gated-off stage, helpers missing two calls deep, pattern= over non-targets, untracked option reads -- bugs that survive for months because a function returns early on empty input. Use when setting up, extending, or fixing tests or CI for a targets pipeline."
when_to_use: "Adding tests, validation or CI to a targets project; asked whether a pipeline's commands resolve; a pipeline CI run fails while defining the pipeline; after restructuring _targets.R, adding a gated stage, or splitting a repo into several targets projects."
argument-hint: "[project path]"
paths:
  - "**/_targets*.R"
  - "**/_targets.yaml"
  - "**/.github/workflows/**"
  - "**/tests/testthat/**"
  - "**/tests/validate/**"
---

# Testing and CI for a targets project

Start from `project-tests-ci` in `r-project-core`: it has the hermetic testthat suite,
the proof that the suite needs nothing outside the repository, and the CI template.
Follow it, with the changes in `references/targets-additions.md`. This skill adds the
part only a `targets` project needs:

- **`targets` does not check that the names in a command resolve.** Add the bundled
  validator; it catches a bug class nothing else does.
- **The test runner sources what `_targets.R` sources** -- `tar_source()`, or the
  explicit list the pipeline uses when `R/` also holds standalone scripts.
- **Editing a helper to make it testable invalidates every target that reaches it.**

## Before starting

On top of the general list, find out without asking:

- The projects in `_targets.yaml`, and **every setting that changes which targets
  exist**: environment variables, options, user-dependent switches in `_local.R`,
  static-branching keys.
- Whether the pipeline uses `tar_quarto()` (CI then needs Quarto before anything
  defines the pipeline).

Add to the one batched prompt: **which variants must be validated** (default, CI graph,
all stages on, ...).

## Step 1 -- the suite

Follow `project-tests-ci` Step 1, then `references/targets-additions.md` for the test
runner, the helper-invalidation trap, and definition in a clean clone.

## Step 2 -- the validator

Read `references/validator.md`. In brief:

```bash
mkdir -p scripts tests/validate
cp "${CLAUDE_SKILL_DIR}"/scripts/validate-projects.R "${CLAUDE_SKILL_DIR}"/scripts/validate_lib.R scripts/
cp "${CLAUDE_SKILL_DIR}"/assets/validate.yml "${CLAUDE_SKILL_DIR}"/assets/unresolved_allowlist.csv tests/validate/
```

1. List every variant in `tests/validate/validate.yml`. Use a project-specific variable for
   the CI graph, not `CI=true` -- a personal `~/.Renviron` can override it.
2. Set `run_scoping_options` to the project's option prefix.
3. Run `Rscript-<version> scripts/validate-projects.R`. Triage each finding: **fix real
   defects first** -- expect some; every project this has run on had them.
4. Allowlist only genuine false positives, one reason per row. Stale rows fail the run.
5. Prove it: reintroduce a bug it should catch, confirm it fails and names it, revert.

If you change the bundled validator, run its self-test (a few seconds, negligible memory):
`Rscript-<version> "${CLAUDE_SKILL_DIR}"/selftest/run-selftest.R`.

## Step 3 -- hermetic proof and CI

Run the general hermetic proof and add the validator to it; start CI from the general
template and add the steps in `references/targets-additions.md`: Quarto before
`setup-renv` if `tar_quarto()` is used, the validator after the tests, and a guard that no
`_targets*` store was created.

## Checklist

- [ ] Everything in the `project-tests-ci` checklist
- [ ] `scripts/run-tests.R` sources what `_targets.R` sources
- [ ] Validator installed, every variant listed, findings fixed or allowlisted with reasons
- [ ] Validator shown to catch a reintroduced bug
- [ ] Hermetic run includes the validator and creates no store
- [ ] Workflow: Quarto if `tar_quarto()`; validator step; store guard

## Bundled files

| File | Use |
| --- | --- |
| `scripts/validate-projects.R`, `scripts/validate_lib.R` | the validator; copy into the project's `scripts/` |
| `selftest/` | planted-bug project and self-test for the validator itself |
| `assets/validate.yml`, `assets/unresolved_allowlist.csv` | validator configuration templates |
| `references/validator.md` | checks, variants, allowlist, limits |
| `references/targets-additions.md` | changes to the general suite, hermetic proof and CI |

## Related

- Why targets go stale without the validator noticing: `targets-staleness`.
- Where heavy steps may run: `hpc-cluster-runs` in `r-project-core`, and
  `targets-cluster-runs`.
- Changing a co-developed package the tests depend on: `package-change-workflow` in
  `r-package-dev`.
