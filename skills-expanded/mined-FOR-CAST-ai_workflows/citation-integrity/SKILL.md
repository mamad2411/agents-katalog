---
name: citation-integrity
description: Never invent or guess any part of a citation, reference, DOI, dataset version, or access date. Verify against an authoritative source, or leave the field null with a _todo note and ask. Applies to bibliographies, reports, manuscripts, data manifests, README prose, code comments, and commit messages alike -- in every project, not only ones with a bib file.
when_to_use: Any time a citation, reference, DOI, URL, dataset version, access date, author list, journal name, or publication year is about to be written or quoted -- in a .bib file, a report, a manuscript, a data manifest, a CITATION.cff, a docstring, a code comment, a commit message, or chat prose. Also when asked "what is the DOI for", "cite this", or "add a reference".
paths:
  - "**/*.bib"
  - "**/*.qmd"
  - "**/*.Rmd"
  - "**/*.tex"
  - "**/CITATION.cff"
  - "**/citations/**"
  - "**/references/**"
  - "**/*manifest*.json"
  - "**/README.md"
  - "**/README.qmd"
  - "**/README.Rmd"
---

# Citations: the imperative

**This is a critical rule for every project, with or without a bibliography.** It is
stated first and in capitals in the `CLAUDE.md` files that state it at all, and it
applies equally where nothing is written down.

> NEVER invent citations or any part of one (authors, year, title, journal,
> volume, pages, publisher, DOI, URL). Do not guess or "fill in" plausible-looking
> fields. Always verify citation information against an authoritative source, and
> always verify the DOI. If you cannot verify a citation yourself, ASK THE USER
> rather than fabricating it. **It is better to omit a citation than to include an
> unverified one.** This applies to `citations/*.bib`, `data/input_manifest.json`,
> report prose, code comments, and commit messages alike.

This is the rule most likely to cause real damage if broken. A fabricated DOI in a
published report is not obviously wrong to a reader, survives review, and is not
recoverable once cited by someone else. Unlike a code bug, nothing downstream fails
loudly -- so there is no verification loop except this one.

It applies wherever a factual provenance claim is made: a `.bib` entry, a data
manifest, a `CITATION.cff`, a figure caption, a README, a code comment naming the
paper a formula came from, a commit message, and an answer in chat. "I am fairly
sure this is the right paper" is not verification.

**A mechanical backstop exists.** A `PostToolUse` hook in this plugin extracts every
DOI you write, resolves it, and reports the title it actually resolves to. A DOI
that 404s is reported as probably fabricated; a DOI that resolves to a different
paper than your entry claims is visible in the reported title. Bib entries added
with no DOI are listed so they can be marked unverified. Treat a hook complaint as
a finding, not noise: remove the citation rather than guessing again.

## Citations that R writes

The hook sees only what is written through Edit or Write. Files produced by R code
bypass it entirely:

- `citations/data-sources.bib` from `workflowtools::sync_manifest_to_bibtex()`;
- a package bibliography from `grateful::cite_packages()`;
- `CITATION.cff` from `cffr::cff_write()`.

Treat each as **generated and unverified**, and check it after every regeneration:

```sh
"${CLAUDE_SKILL_DIR}"/../../scripts/check-citations.sh --file citations/r-packages.bib CITATION.cff
```

It resolves every DOI, lists bib entries without one, and exits 1 when a DOI does not
resolve. Fix a bad field where it comes from -- the package's `DESCRIPTION` or
`inst/CITATION`, the manifest record, the generator's arguments -- and regenerate.
Never patch the generated file.

How these generators produce confident-looking wrong fields:

- **grateful** reformats what each package says about itself (`utils::citation()`).
  Without an `inst/CITATION`, R builds the entry from `DESCRIPTION`, taking the year
  from `Date/Publication`, else `Date`, else the build's `Packaged` stamp -- so a GitHub
  or r-universe install is dated by when it was built, not released, and usually has no
  DOI. It finds packages with `renv::dependencies()`, which sees only packages the
  code loads or declares in the usual places; where a project loads packages some
  other way, pass `pkgs =` explicitly.
- **cffr 1.4.2** writes `doi: 10.32614/CRAN.package.<pkg>` for a package found in *any*
  configured repository, r-universe included. A package that is not on CRAN then carries
  a DOI that does not resolve.
- **workflowtools before 0.0.20** filled a missing year in `data-sources.bib` with the
  retrieval year or the current year. Regenerate after upgrading.

## What to do instead of guessing

Write an **honest scaffold**. Populate only what you can verify from the code or
the file itself; leave everything else `null` with a `_todo`. One project's manifest describes itself as:

> Honest scaffold: only code-verifiable fields are populated ... version,
> access_date, and uncertain `citation_key` values are null with `_todo` notes, to
> be verified by a human per the Citations imperative -- NOT fabricated.

```json
{
  "layer_key": "vri_2025",
  "url": "https://catalogue.data.gov.bc.ca/dataset/vri-2025",
  "retrieved_by": "R/targets_preamble.R:fetch_vri()",
  "version": null,
  "_todo_version": "confirm release designation with the data steward",
  "citation_key": null,
  "_todo_citation": "no verified BibTeX entry yet -- do not invent one"
}
```

## A catalogue's own suggested citation can be stale

A real case: a bib entry was copied verbatim from a data catalogue page whose own
suggested-citation block was a year out of date, and the wrong release year shipped. The fix records a comment on the entry *"so it is not 'restored'
from the page"*. Copying a citation block is not verification; cross-check the
release designation against the data itself or the steward.

## Probing a URL

Use a ranged GET, never HEAD:

```r
httr2::request(url) |> httr2::req_headers(Range = "bytes=0-0") |> httr2::req_perform()
```

Some data portals answer HEAD with 404 for files that exist. A HEAD-based existence
check then reports every file as missing, which has led to a published dataset being
recorded as unavailable.

## Checklist before writing any citation

1. Do I have the actual source in front of me (fetched page, PDF, DOI resolver)?
2. Does the DOI resolve, and does it resolve to *this* work?
3. Is the year the release year of the *version actually used*, not the newest?
4. If any field is unknown: is it `null` with a `_todo`, rather than plausible?
5. Have I asked the user rather than filling a gap?

If you cannot answer 1-3 affirmatively, do not write the entry. Say what is
missing and ask.

## Where verified sources are kept

`reports/citations/` holds `references.bib` (literature, hand-curated),
`data-sources.bib` (generated from the input manifest -- do not hand-edit), and
the CSL file (`ecology-letters.csl`). A bib entry generated from the manifest
inherits the manifest's honesty: an unverified manifest field must not become a
confident bib field.
