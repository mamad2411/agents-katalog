---
name: r-style
description: House R coding style for research projects -- air formatting, `<-` and `|>` only, `##` vs `#` comments, ASCII-only code and reports, package-qualified calls in worker code, roxygen in non-package R/. Use whenever writing or editing R code or .qmd chunks, or reviewing R style.
when_to_use: Writing or editing any .R, .qmd, or .Rmd file; setting up or changing air.toml or .lintr; asked about formatting, linting, or code style in R.
paths:
  - "**/*.R"
  - "**/*.r"
  - "**/*.qmd"
  - "**/*.Rmd"
  - "**/air.toml"
---

# House R style

## Non-negotiable

| Rule | Why it is stated as absolute |
| --- | --- |
| **`<-` for assignment.** Never top-level `=`. | measured across the corpus: hundreds of `<-`, zero top-level `=` |
| **Native pipe `\|>`.** Never `%>%`. | zero `%>%` in any `R/` directory anywhere; `magrittr` was actively removed |
| **`##` starts a comment. `#` only prefixes commented-out code.** | the ratio runs ~250:1 in recently-written code |
| **ASCII only** in code and rendered reports. | an undeclared glyph is a hard `pdflatex` failure; smart quotes and non-breaking spaces are invisible in review |
| **100 columns, 2-space indent**, spaces not tabs. | every `air.toml` in the corpus agrees |
| **Zero bare `T` / `F`.** Write `TRUE` / `FALSE`. | already clean everywhere; keep it that way |

For ASCII, use `--` for a dash, `->` for an arrow, `>=` / `<=`, `x` for times. If a
*report* genuinely needs the symbol, use LaTeX math (`$\geq$`, `$\times$`,
`$\rightarrow$`) rather than the raw glyph. A `\DeclareUnicodeCharacter` block in
`_quarto.yml` is a render backstop, not permission to paste glyphs.

A `PreToolUse` hook in this plugin blocks non-ASCII writes to `.R/.qmd/.Rmd/.bib`.
Prose `.md` (CLAUDE.md, design notes) is exempt.

## Naming is per-project -- detect it, do not assume it

Both conventions are in active use and both are correct in their own repo:

- **snake_case**, often with a package prefix (`dryad_search`, `build_model_dataset`)
- **camelCase**, the PredictiveEcology house style (`createTurtles`,
  `prepClimateLayers`, `NLwith`), sometimes enforced by
  `object_name_linter("camelCase")` in `.lintr`

Some packages legitimately mix three conventions because they wrap an external
tool's vocabulary. **Read the convention off the repo before naming anything.**
A cheap detector:

```sh
grep '^export' NAMESPACE | head -40      # majority vote
```

Match the file you are editing, not a global preference.

## Formatting is delegated to air -- where it is allowed

```sh
air format .            # whole project
air format path/to.R    # one file
```

**`air format .` is not universally safe.** Some mature packages deliberately
forbid it, because their HEAD is not air-clean and a whole-project reformat buries
real changes in noise. One package's CLAUDE.md states the exception outright:
*"do not run `air format .` on this package."*

The rule that generalises:

- **A repo may opt out.** Check for an opt-out before running air. This plugin's
  `PostToolUse` hook reads `noAirFormat` from the project policy file (see
  `project-policy`) and skips formatting when it is set.
- **Where air is allowed, format only what you changed** -- `air format <file>`,
  not `air format .` -- unless the repo is already air-clean.
- **`air` has no `--exclude` flag.** Use `exclude` in `air.toml`.

`air` does not reflow comment or roxygen prose, so long comment lines are normal
and not a violation.

### Canonical `air.toml`

```toml
[format]
line-width = 100
indent-width = 2
indent-style = "space"
line-ending = "auto"
persistent-line-breaks = true
exclude = []
default-exclude = true
skip = ["globalVariables"]
```

Extend `skip` for any function whose call is a long hand-curated block that air
would re-wrap on every run:

- `globalVariables` -- packages with large `utils::globalVariables()` vectors
- `use` -- long import blocks
- any hand-aligned metadata DSL a framework uses

## Package-qualify calls in code that runs in another R process

```r
ggplot2::ggplot(d) + ggplot2::geom_sf(...)     ## yes, inside a worker
ggplot(d) + geom_sf(...)                        ## no
```

Worker processes (`callr`, `parallel`, `future`, `mirai`, a pipeline's workers) do
not reliably attach packages, and an unqualified call then fails only on the worker,
hours in. Package-qualify anything that runs in a worker or a Quarto chunk.

Do **not** attach packages in `.Rprofile`. It breaks a fresh clone and CI, where the
packages are not installed yet. Nulling the profile in CI (`R_PROFILE_USER: /dev/null`)
is not a general fix: it also stops renv activating and drops the CRAN mirror that
`setup-r` configures, so it suits only steps that never need the project library. See
`project-tests-ci`.

## roxygen in non-package `R/`

Helper functions are documented with roxygen (`#'`, `@param`, `@return`) even where
`R/` is *not* a package -- over a thousand roxygen lines in one pipeline project's
`R/`. Follow it: a helper worth keeping is a helper worth documenting.

## Comment content

Comments carry decisions and measurements, not restatements of the code. The house
pattern is to record the **falsified** option beside the setting so it is not
retried:

```r
## overrideBiomassInFires stays TRUE. Setting it FALSE was tried and made agreement
## with the independent reference worse: biomass MAE 812 -> 1104 t/ha.
```

Mark structurally-complete-but-unverified work with an explicit marker:

```r
## TODO(curate): wired against the module contract, but the reclass values are
## unconfirmed against the source data dictionary.
```

**Comments are the spec.** Dated `##` post-mortems inline in the driver scripts,
`.Rprofile`, `_local.R` and `.gitignore` are how these projects carry institutional
memory. A refactor that drops them is a regression, not a cleanup.

## The R binary

Where a project pins its R version, call the pinned binary explicitly --
`Rscript-4.6.1`, not bare `Rscript`. A bare call silently uses whatever the version
manager's default is, which is often an older R with an incomplete library. This is
the single most-violated convention in the corpus (over a thousand bare calls), so
it is worth being deliberate about. Set `rBinary` in the project policy file and
this plugin's hook will flag bare calls for you.
