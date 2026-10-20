---
name: bibliography-generator
description: Generate a properly formatted reference list (Vancouver, APA, Chicago, or MLA) from the citations used in a document and integrate it into the final paper. Stage 7 of the academic-pipeline. Use to turn a drafted paper with a bibliography placeholder into a publication-ready document, or, in renumber mode, to recompute Vancouver numbering by first appearance after a finished paper has been edited ("renumber the citations", "fix the reference order", "I added a citation mid-paper").
license: Proprietary - MoxyWolf LLC
---

# Bibliography Generator — Stage 7

Take every citation the writer actually used, format the reference list correctly, and produce the finished document.

## Role in the pipeline

Seventh stage of the `academic-pipeline`. Consumes Stage 6's `draft_document.md` and `all_citations_used`; produces `<target-slug>.md` — the main deliverable, which Stage 8 (`professor`) then critiques.

## Inputs

- **`all_citations_used`** — the deduplicated list of BibTeX keys cited across the paper (from Stage 6's return, or extracted from the draft).
- **`draft_document.md`** — from the run folder's `pipeline/` subfolder, containing the `## Bibliography` placeholder.
- **The BibTeX file** — at the `bibtex_source_path` in `handoff_for_writer.json`. Read it directly for full entry data.
- **Citation style** — from `handoff_for_writer.json` (`citation_style`); default Vancouver for Academia.edu submissions.

## Process

### Step 1 — Collect unique citations

Deduplicate `all_citations_used`. If the list was not passed in, extract citation markers directly from `draft_document.md`.

**Deduplicate on the work, not only on the key.** Two BibTeX keys can point at one publication: a preprint record and an aggregator's page for the same paper, or the same arXiv identifier entered twice. Key-level dedupe passes them through and the reference list then carries one work under two numbers. Normalize each entry's DOI, or its URL when there is no DOI (lowercase, drop the scheme, `www.`, a `doi.org/` prefix and any trailing slash), and warn when two keys resolve to the same value. Keep the canonical record, drop the mirror, and say in `warnings` which key was dropped and why. A mirror worth mentioning in the text is mentioned in prose, not given its own reference number.

### Step 2 — Retrieve full entries

For each key, pull the complete BibTeX entry: author/organization, year, title, journal/booktitle/howpublished, volume, number, pages, DOI, URL. Flag any missing fields. **Never invent citation data** — use only what the `.bib` contains.

### Step 3 — Format each entry

**Vancouver (default — Academia.edu):** numbered in order of first appearance in the text.

```
1. Lastname AB, Otherlastname CD, Thirdlastname EF, et al. Title of article. Journal Name. 2024;15(3):45-52. https://doi.org/xxx
```

**APA (7th):**

```
Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), pages. https://doi.org/xxx
Organization. (Year). Title of work. https://url
```

**Chicago (Author-Date):**

```
Author, First Last, and Second Author. Year. "Title of Article." Journal Name Volume (Issue): pages. https://doi.org/xxx
```

**MLA (9th):**

```
Author, First Last, et al. "Title of Article." Journal Name, vol. X, no. Y, Year, pp. pages. DOI or URL.
```

### Step 4 — Special cases

- **No author** → use the organization or title; alphabetize (or order) accordingly.
- **Multiple authors** → APA lists up to 20 then "et al."; Chicago uses "et al." after 3; MLA uses first author + "et al." beyond two.
- **Organization authors** → BibTeX wraps these in `{...}`; use as-is, no name parsing.
- **Missing fields** → `n.d.` for no date; prefer DOI, fall back to URL; record every gap in `warnings`.

### Step 5 — Order

- **Vancouver / numbered** → order by first appearance in the text.
- **APA / MLA / Chicago Author-Date** → alphabetical by first author's last name.

### Step 6 — Integrate

Replace the `## Bibliography` placeholder in `draft_document.md` with the formatted reference list (one blank line between entries). Write the result to **`<run folder>/<target-slug>.md`** — this is the pipeline's primary deliverable, placed at the run-folder root, not in `pipeline/`.

## Return to the orchestrator

```json
{
  "status": "complete",
  "citations_formatted": 12,
  "citation_style": "Vancouver",
  "output_file": "<run folder>/<target-slug>.md",
  "warnings": ["Missing DOI for org2025key — used URL instead"]
}
```

## Renumber mode (after Stage 7, any time a finished paper is edited)

Vancouver numbers by first appearance, so a citation inserted mid-paper by hand shifts every number after it and silently breaks venue compliance. Do not renumber by hand. Run the bundled pass:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/bibliography-generator/scripts/renumber_citations.py" <target-slug>.md          # report
python3 "${CLAUDE_PLUGIN_ROOT}/skills/bibliography-generator/scripts/renumber_citations.py" <target-slug>.md --write  # apply
python3 "${CLAUDE_PLUGIN_ROOT}/skills/bibliography-generator/scripts/renumber_citations.py" <target-slug>.md --check  # exit 1 if out of order
```

What it does: reads every `[n]`, `[n,m]`, `[n–m]` marker before `## References`, computes first-appearance order, rewrites the markers, and reorders the `N. ` entries to match; ranges are re-compressed only where the new numbers are contiguous. It verifies the result is `1..N` on both sides before writing, and refuses (exit 2, nothing written) if a cited number has no entry or an entry is never cited, so it never invents or drops a reference.

How to use it when editing: add the new entry to the list with any unused number (or append it as `N+1`), cite it in the body with that number, then run the pass with `--write`. Run `--check` as the last step of any edit to a Vancouver paper and before Stage 8. Author-date styles need no renumbering; the pass is a no-op for them.

## BibTeX field mapping

```
author → Author        title → Title           journal → Publication (articles)
booktitle → Publication (proceedings)           howpublished → Publication (misc)
year → Year            volume → Volume          number → Issue
pages → Pages          doi → DOI                url → URL
```

Author parsing: split `"Last, First and Last, First"` on ` and `; treat `{Organization Name}` as a single literal author.

## Quality checklist

Every key in `all_citations_used` is included; ordering is correct for the style; formatting is consistent; DOIs/URLs render; no duplicates; author names parsed correctly; the placeholder is fully replaced.

## Notes

- Never fabricate citation data.
- Always include a URL when the DOI is missing; prefer DOI when both exist.
- Final typographic polish (hanging indents, etc.) happens at document export — `.docx`/PDF via the `academia-formatting` skill.
