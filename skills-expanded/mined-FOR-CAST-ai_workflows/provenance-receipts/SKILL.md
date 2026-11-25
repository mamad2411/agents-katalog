---
name: provenance-receipts
description: Recording where data came from and what produced a result, using FOR-CAST/workflowtools -- input manifests, generated data-source bibliographies, reproducibility receipts with session, package-commit and geospatial library versions, comparing hosts with session_diff(), the honest-scaffold rule for unverifiable fields, and which artefacts get a DOI.
when_to_use: Adding a new external data source; building or updating an input manifest; writing a provenance appendix or INFO.md; being asked how a result was produced, which version of a dataset or package was used, or why two hosts give different results; deciding whether code needs a DOI.
paths:
  - "**/*manifest*.json"
  - "**/INFO.md"
  - "**/CITATION.cff"
  - "**/.zenodo.json"
  - "**/reports/**"
---

# Provenance

Three layers, each cheap on its own. **`FOR-CAST/workflowtools` implements all
three.** Call its functions rather than hand-rolling a manifest or receipt, and when
something is missing, extend the package (see `r-package-dev:package-change-workflow`)
so every project gets the fix.

## 1. An input manifest

One committed JSON record per external input, written through the package so it is
validated against `input_manifest_schema()`:

```r
workflowtools::register_input(
  workflowtools::input_manifest_record(
    id = "landcover_2020",
    name = "Land cover 2020",
    source = list(type = "http_download", url = "https://example.org/datasets/landcover-2020.gpkg"),
    local_path = "data/landcover-2020.gpkg",
    extra = list(
      `_todo_version` = "confirm release designation with the data steward",
      `_todo_citation` = "no verified BibTeX entry yet -- do not invent one"
    )
  )
) ## appends to data/input_manifest.json
```

**The honest-scaffold rule:** populate only what is verifiable from the code or the
file itself. Leave `version_or_vintage`, `license` and `citation` out until they are
verified, and say why under `extra` as `_todo_*`. Never a plausible guess. See
`citation-integrity` -- the manifest is explicitly in scope for that rule.

If the project's `.gitignore` denies `*.json` wholesale, the manifest needs an
explicit `!` allowlist entry or it silently will not be committed.

## 2. A generated data-source bibliography

```r
workflowtools::sync_manifest_to_bibtex(
  manifest = "data/input_manifest.json",
  out = "citations/data-sources.bib",         # generated: never hand-edit
  references_bib = "citations/references.bib" # curated literature: read, never written
)
```

An unverified manifest field must not become a confident bib entry. From workflowtools
0.0.20 a year comes only from `version_or_vintage`; earlier versions filled a missing
year with the retrieval year or the current year, so regenerate after upgrading. Then
check the output with the `--file` check in `r-project-core:citation-integrity` --
the citation hook never sees a file that R wrote.

## 3. A reproducibility receipt

**In a report**, one chunk:

```r
workflowtools::reproducibility_receipt()                                # inline, collapsible
workflowtools::reproducibility_receipt(writeTo = "outputs/run-01/INFO.md") # refuses to overwrite
```

It renders `info_project()`: git branch and remote, the HEAD commit, submodule SHAs,
GEOS/GDAL/PROJ as sf sees them, `sessioninfo::session_info()`, and a timestamp. Before
workflowtools 0.0.20 the HEAD field held git's exit status (`0`) instead of the
commit -- check old receipts before relying on them.

**For an appendix table**, `prov_build_identity()`, `prov_repository_state()`,
`prov_toolchain()` and `prov_r_packages()` each return a `data.frame` for
`knitr::kable()`.

**What the package does not record yet** -- add it in the project, or better, to the
package:

| Missing | How |
| --- | --- |
| the commit each package was built from | `session_info()$packages$source` gives `Github (owner/repo@sha)`; `prov_r_packages()` gives versions only. An r-universe install shows its repository, not a SHA |
| terra's own GDAL/GEOS/PROJ | `terra::libVersion("all")` -- sf and terra can link different builds, and both change results invisibly to renv |
| the lockfile actually used | `tools::md5sum("renv.lock")` |
| a container | the image digest, not the tag |

**Not the machine name.** A receipt says what ran, not where. Machine names and IPs
are infrastructure identity: they belong in gitignored config, and never in a
committed receipt or a rendered report. They are also weak evidence -- the R version,
the lockfile hash and the toolchain are what let someone reproduce a result, and a
name tells them none of it. `session_info()` leaves the hostname out by default;
leave it out.

**Comparing machines.** When two of them disagree, save each `session_info()` and
diff them rather than eyeballing two printouts. Label the files by role, and keep
them out of version control:

```r
dir.create("_scratch/receipts", recursive = TRUE, showWarnings = FALSE)
saveRDS(sessioninfo::session_info(), "_scratch/receipts/session-worker.rds")
sessioninfo::session_diff(readRDS("_scratch/receipts/session-control.rds"),
                          readRDS("_scratch/receipts/session-worker.rds"))
```

A receipt describes the run that produced it, so regenerate it on every run rather
than caching it.

## What gets a DOI

| Artefact | Identifier | When |
| --- | --- | --- |
| a co-developed package | Zenodo DOI minted from a GitHub release | a release the user chooses to archive |
| the analysis code behind a paper | Zenodo DOI from a GitHub release, or a manual Zenodo upload | at submission |
| a pipeline run | none -- the reproducibility receipt | every run |
| an input dataset | the publisher's DOI, in the manifest's `citation` | when it is fetched |

How Zenodo's GitHub integration behaves:

- A DOI is minted when a GitHub **release** is published -- not for a tag or a merge.
  The repository must be switched on in Zenodo's GitHub settings; an organisation's
  repositories appear only after the organisation grants Zenodo access. Private
  repositories are not supported.
- Each release gets a **version DOI**; the record also has a **concept DOI** that always
  resolves to the latest version. Cite the version DOI in papers and receipts (it names
  the exact code); use the concept DOI for a badge or in `CITATION.cff`.
- Metadata comes from `CITATION.cff`, unless `.zenodo.json` exists, in which case only
  `.zenodo.json` is used.
- A DOI can be reserved before publication only through a manual upload, not through
  the GitHub integration. Use that, or a manual upload generally, when the repository is
  private or the code lives partly in submodules -- open the archived zip and check what
  it actually contains.
- Zenodo software deposits are also archived by Software Heritage (a SWHID).

Creating a release publishes. It needs the user's approval, and a DOI is never written
anywhere until Zenodo has minted it -- see `citation-integrity`.

## Record the environment's known-bad configurations

A short, dated "Platform" section saying which OS or toolchain versions are known
not to work, and why, saves the next person a day. One project records a specific
distribution release whose libc change breaks a pinned dependency, and pins CI to
the previous release for that reason.

## Note what is deliberately not reproduced

CI that deliberately does *not* restore the full environment should say so:

> the spatial stack (GDAL/GEOS/PROJ) makes CI slow and brittle relative to its
> value

A cheap check that parses every tracked `.R` file, validates the lockfile JSON and
validates `CITATION.cff` (`cffconvert --validate`; the syntax job in
`r-project-core:project-tests-ci`) catches most real breakage without a 40-minute
build.
