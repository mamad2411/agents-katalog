---
name: bibtex-gen
description: >
  Generate BibTeX entries for academic references from arXiv IDs, DOIs, titles,
  URLs, batch lists, or reference-search JSON. Route HEP papers to InspireHEP,
  non-HEP papers to Google Scholar when available, and CrossRef DOI BibTeX as a
  fallback; preserve source-native keys and print or append to a .bib file. Use
  when the user asks for bibtex, citation entries, bibliography filling,
  arXiv/DOI/title-to-BibTeX, InspireHEP BibTeX, publisher BibTeX, or converting
  discovered references into a .bib file.
---

# bibtex-gen — BibTeX Generator (InspireHEP / Google Scholar / CrossRef)

Generate bibtex entries by routing each query to the most authoritative
source. The skill is **read-only** for the user's existing `.bib` files
unless they pass `--output`, in which case new entries are appended (never
overwritten or de-duplicated — that is the user's call).

## Routing logic

Each input is classified as HEP or non-HEP, then routed:

| Class      | Primary source            | Fallback                   |
|------------|---------------------------|----------------------------|
| HEP        | InspireHEP (`format=bibtex`) | non-HEP path if InspireHEP returns nothing |
| non-HEP    | Google Scholar via `scholarly` | CrossRef DOI bibtex transform |

**Classification rule**: a query is HEP iff InspireHEP returns at least one
match for it. arXiv IDs additionally check the arXiv API for `hep-*` /
`nucl-*` categories as a strong pre-signal. The user can override with
`--hep` or `--no-hep`.

This intentionally aligns with the user's preference:

- HEP citations follow **InspireHEP** style (`Author:YYYYabc` keys, journal
  abbreviations, eprint fields, collaboration tagging).
- Non-HEP citations follow **Google Scholar** style first; if Scholar is
  unavailable or returns nothing, fall back to the **publisher's bibtex**
  via CrossRef's DOI→bibtex transform.

## Inputs accepted

The orchestrator auto-detects the input type:

- **arXiv ID** — `2301.00001`, `arxiv:2301.00001`, `hep-ex/0511032`
- **DOI** — `10.1103/PhysRevD.98.030001`, `doi:10.1...`, `https://doi.org/10.1...`
- **Title** — anything else is treated as a title / free-text query
- **URL** — DOI URLs are parsed; arXiv URLs are normalized to arXiv IDs

Batch mode reads one query per line from a file (`#` comments and blank
lines ignored).

For an OpenAlex-driven discovery → citation pipeline, the orchestrator
also accepts `--from-search refs.json`, where `refs.json` is the JSON
output of the `reference-search` skill (`openalex_search.py --format
json`). Each result's DOI is extracted (title fallback if no DOI) and
routed through the normal HEP / Scholar / CrossRef pipeline — so you can
run "find me 10 papers on X" and turn that into a `.bib` in one extra
command. See `references/examples.md` for the full pipeline recipe.

## Bibtex key style

Each source returns its own key style; **the skill preserves them verbatim**:

- InspireHEP: `Smith:2024abc`
- Google Scholar: `smith2024title`
- CrossRef: DOI-suffix style (e.g. `Smith_2024`)

Do not silently rewrite keys. If the user asks for a unified style, surface
it as an explicit follow-up step, not a side effect.

## Workflow

1. **Confirm the input set**. If the user gave a Korean / English list of
   references, treat each line as one query. If they gave a single phrase,
   treat it as one query.
2. **Decide routing override**. If the user said "HEP", "high energy", "장
   인용", "물리 논문" etc., pass `--hep`. If they said "ML 논문", "biology
   paper", etc., pass `--no-hep`. Otherwise let auto-classification run.
3. **Run the orchestrator**:
   ```bash
   uv run bibtex-gen/scripts/bibtex_gen.py "<query>" [--hep | --no-hep] \
     [--output refs.bib]
   ```
   For batch mode:
   ```bash
   uv run bibtex-gen/scripts/bibtex_gen.py --batch refs.txt --output refs.bib
   ```
4. **Surface the bibtex**. Stream to stdout by default. If `--output` is set,
   confirm append count to the user.
5. **Report failures**. Any query that produced no bibtex from any source is
   listed explicitly. Do not invent a bibtex entry — ask the user to refine
   the query or supply a DOI.

## What this skill does NOT do

- It does not deduplicate entries in the target `.bib` file. Run a separate
  pass if needed.
- It does not normalize keys across sources. If the user wants
  `FirstAuthorYear` everywhere, ask before doing it.
- It does not fabricate missing fields. If a source returns sparse bibtex
  (no DOI, no journal), surface it as-is.
- It does not handle paywalled publisher endpoints directly. CrossRef
  bibtex is the publisher proxy and is sufficient for most journals.

## Dependencies

The orchestrator carries **PEP 723 inline script metadata** declaring
`scholarly` as a dependency. When run with `uv run`, uv reads that header
and provisions an ephemeral environment that includes `scholarly` — the
user does not need to `uv add` or `pip install` anything ahead of time.

If the orchestrator is run with a bare `python3` (no `uv`), `scholarly`
may be missing; in that case the Google Scholar path is skipped with a
one-line stderr note and non-HEP queries fall through to CrossRef. HEP
queries continue to work unchanged via the stdlib-only InspireHEP path.

## Source notes (quick reference)

| Source     | Endpoint                                                                | Auth   | Stdlib only? |
|------------|-------------------------------------------------------------------------|--------|--------------|
| InspireHEP | `https://inspirehep.net/api/literature?q={query}&format=bibtex`         | none   | yes          |
| arXiv      | `http://export.arxiv.org/api/query?id_list={id}` (for HEP category)     | none   | yes          |
| CrossRef   | `https://api.crossref.org/works/{DOI}/transform/application/x-bibtex`   | none   | yes          |
| Scholar    | `scholarly.search_pubs(q)` → `scholarly.bibtex(pub)`                    | none   | requires `scholarly` |

Full source-by-source semantics in `references/sources.md`. HEP
classification heuristics in `references/hep_classification.md`.

## Resources

- `scripts/bibtex_gen.py` — orchestrator; runnable as `uv run scripts/bibtex_gen.py "<query>"`.
- `references/sources.md` — per-source API details, response shape, and gotchas.
- `references/hep_classification.md` — when a query is classified HEP vs non-HEP and how to override.
- `references/examples.md` — copy-pasteable CLI invocations (single, batch, HEP override, file append, `reference-search` integration).

## Companion skills

- `reference-search` — OpenAlex-based literature discovery. Use it upstream of this skill when the user has a topic / claim / section in mind but no specific paper picked out. Save its output with `--format json`, then run `bibtex-gen --from-search <file>.json` to materialize a `.bib`.

After creating or updating this skill, suggest starting a new session so
the new skill is discoverable from session start.
