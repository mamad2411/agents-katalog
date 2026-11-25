---
name: r-publish
description: >-
  Orchestrate the full R package publication pipeline: CRAN (and
  R-universe) for distribution, JOSS for a peer-reviewed DOI, optionally a
  JSS methods paper. Use for "publish my R package". For a Python package
  use pypi-publish; for a standalone LaTeX paper (no DESCRIPTION) use the
  papermill plugin instead.
argument-hint: "[package path]"
---

# R Package Publication Pipeline

Orchestrate CRAN submission, then a JOSS paper, then optionally a JSS methods paper. This skill coordinates `/pub-pipeline:cran-audit`, `/pub-pipeline:joss-audit`, and `/pub-pipeline:joss-draft` into one workflow. Package root: `$ARGUMENTS` if given, else the current directory. If it has no `DESCRIPTION` with a `Package:` field, say so: point to `/pub-pipeline:pypi-publish` for a `pyproject.toml` project, or the papermill plugin for a `.tex` paper.

## Strategy

1. **CRAN**: distribution, discoverability, `install.packages()`.
2. **JOSS**: quick DOI, peer-reviewed citation, Crossref/Google Scholar indexing.
3. **JSS** (optional): high-prestige methods paper, Web of Science indexed.

Each stage builds on the previous: CRAN gives legitimacy, JOSS a citable DOI, JSS academic weight for the methodology.

## Workflow

### Phase 1: Assess Current State

**Load user config** (Read tool): read `.claude/pub-pipeline.local.md` if it exists. Extract author metadata, `r.domain`, `r.audience`, `r.competitors`, `r.targets`, `r.universe`, `r.dependency_chain`, and `related_work`. Companion papers and preprints in `related_work` shape the JOSS paper (cite them) and the overall strategy. If the file is missing, offer to create it from `${CLAUDE_PLUGIN_ROOT}/docs/user-config-template.md`.

1. Read `DESCRIPTION` for package metadata (Read tool).
2. Check git history (Bash tool).
3. Look for existing `paper.md`, `CITATION.cff` (Glob tool).
4. CRAN status: fetch `https://cran.r-project.org/package={name}` (WebFetch tool).
5. R-universe status (Bash tool, structured JSON; `{user}` is `r.universe`, skip if unset): `curl -s https://{user}.r-universe.dev/api/packages/{name}` returns `Version`, `_registered`, and `_status` (build result); a 404 means the package is not in that universe.
6. JOSS status: search joss.theoj.org (WebSearch tool).

**Dependency chain** (Bash tool): for each non-base, non-recommended package in `Imports`, `Depends`, and `LinkingTo`:
```bash
Rscript -e 'ap <- available.packages(); cat("PKG_NAME" %in% rownames(ap))'
```
A dependency missing from CRAN is a hard blocker for `R CMD check --as-cran`. Present the submission order (dependencies first), cross-check `r.dependency_chain`, and offer to switch to the dependency package.

**CI status**: if `.github/workflows/` exists (Glob tool), run `gh run list --limit 3 --json conclusion,name,headBranch` (Bash tool). Failing CI undermines both CRAN confidence and JOSS reviewer trust.

Classify the package:

| State | Next Step |
|-------|-----------|
| Dependencies not on CRAN | Start with the dependency package |
| On R-universe only, not on CRAN | CRAN audit; R-universe already gives installable binaries, so JOSS can proceed in parallel |
| Not on CRAN, no paper.md | Start with CRAN audit |
| On CRAN, no paper.md | Start with JOSS audit |
| On CRAN, has paper.md | Review paper, prepare JOSS submission |
| On CRAN, published in JOSS | Consider JSS (if substantive methodology) |

Bioinformatics packages (genomics, proteomics) usually belong on Bioconductor instead of CRAN, which has its own submission process.

Present the assessment and confirm the plan before proceeding.

### Phase 2: CRAN Readiness

Run `/pub-pipeline:cran-audit`. If the package is not ready: present the gap report, fix automatable issues, guide manual fixes, re-audit. Skip to Phase 3 if already on CRAN.

**Submission steps** (when ready):
1. `usethis::use_version("minor")` to bump the version (commit pending changes first; it prompts otherwise).
2. `devtools::check(args = "--as-cran")` for the final check.
3. Other platforms: `devtools::check_win_devel()` (win-builder) and `rhub::rhub_check()` (R-hub v2; one-time `rhub::rhub_setup()`; `rhub::rc_submit()` for non-GitHub repos).
4. **Submit (user runs this)**: `devtools::submit_cran()` asks interactive confirmation questions that the Bash tool cannot answer. Hand it to the user to type in the prompt:
   ```
   ! Rscript -e 'devtools::submit_cran()'
   ```
   or to run in an interactive R session. Then they confirm via the emailed link.
5. After acceptance: `usethis::use_github_release()`, then `usethis::use_dev_version()`.

**If CRAN rejects**: read the email carefully, fix every identified issue (not a subset), re-run `devtools::check(args = "--as-cran")`, note the fixes in `cran-comments.md`, and resubmit. Do not resubmit more than once a week unless CRAN asks.

### Phase 3: JOSS Readiness

Run `/pub-pipeline:joss-audit`. Common gaps: under 6 months of public history, no `CONTRIBUTING.md`, no `paper.md`. If there is no paper, go to Phase 4.

### Phase 4: Draft JOSS Paper

Run `/pub-pipeline:joss-draft`. Then present the draft, iterate on feedback, re-run `/pub-pipeline:joss-audit` for a full checklist review, and commit the paper to the repository.

### Phase 5: JOSS Submission

1. **Pre-submission**: package installable (ideally on CRAN), `paper.md` and `paper.bib` committed, audit passes, ORCID for all authors.
2. **Submit** at https://joss.theoj.org/papers/new with the repository URL; wait for the pre-review issue.
3. **During review** (typically 4-12 weeks): respond promptly, make requested changes, re-run the audit.
4. **Post-acceptance**: tag a release; archive it on Zenodo (enable the Zenodo GitHub integration for the repository, publish a GitHub release with `gh release create`, copy the deposit DOI); post the version and archive DOI in the review issue. JOSS then assigns the paper DOI via Crossref.

### Phase 6: JSS Consideration (Optional)

**Appropriate when** the package implements novel statistical methodology with substantive mathematical content, the paper would be 20-50 pages of methods plus software description, and the audience is academic statisticians.

**Not appropriate when** the package is primarily a software tool (JOSS covers it), the mathematics is textbook material, or the paper would just be a longer JOSS paper.

If appropriate: JSS uses the `rticles::jss_article` format, is indexed in Web of Science, and reviews take 6-18 months. The `papermill:writer` agent can draft long-form academic papers.

## Decision Helpers

| Criterion | Minimum for CRAN | Minimum for JOSS |
|-----------|-----------------|-----------------|
| License | OSI-approved | OSI-approved |
| Tests | Pass R CMD check | Automated test suite |
| Docs | Man pages for exports | README, examples, API docs |
| History | Any | 6+ months public, sustained |
| Users | Not required | Research impact evidence |
| Paper | Not required | 750-1750 word paper.md |

| Stage | Duration |
|-------|----------|
| CRAN prep and audit | 1-3 days |
| CRAN review | 1-7 days (usually 1-2) |
| JOSS prep and paper | 1-2 days |
| JOSS review | 4-12 weeks |
| JSS prep and paper | 2-4 weeks |
| JSS review | 6-18 months |

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/docs/cran-reference.md`**: CRAN Repository Policy, submission workflow, common rejections
- **`${CLAUDE_PLUGIN_ROOT}/docs/joss-reference.md`**: JOSS requirements, reviewer checklist, paper format

## Important Notes

- Never submit to JOSS before the package is installable (ideally on CRAN).
- CRAN and JOSS are complementary: CRAN for distribution, JOSS for citation.
- The user controls the pace: present options, don't push.
