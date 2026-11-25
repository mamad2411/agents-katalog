---
name: hep-rumor-mill
description: >
  Analyze the HEP-theory postdoc rumor mill (the public Google Sheet at
  sites.google.com/site/postdocrumor) to see who got offers at which institutions, then pull
  each offer-holder's publication record from InspireHEP (and OpenAlex + Semantic Scholar for
  interdisciplinary people) to study what kind of profile lands where. Use when the user wants
  to study the HEP-theory / cosmology / hep-ph job market from the rumor mill: institute-by-
  institute cohort profiles (citations, papers, venues, subfield, PhD-age, named fellowships),
  benchmark their own InspireHEP profile against the accepted cohort, or generate a Korean
  job-market strategy report. Triggers on: rumor mill, postdoc rumor, HEP rumor mill, hep-th
  job market, theory postdoc offers, who got offers, offer holders, 루머밀, 포닥 루머,
  잡마켓 분석, 오퍼 받은 사람, 합격자 실적 분석, 포닥 전략, InspireHEP 프로필 분석.
---

# HEP Rumor Mill Skill

Conversational interface over the `prm` CLI. It pulls the HEP-theory postdoc rumor mill (a
public Google Sheet) for a year, resolves each offer-holder's InspireHEP profile, and analyzes
their publication records so the user can study the job market and benchmark their own profile.

Two first-class uses:

- **Institute intelligence**: for an institution, what do the people it gave offers to look
  like (citations, papers, venues, subfield mix, PhD-age, named fellowships)?
- **Self benchmarking**: place the user's own InspireHEP profile on the accepted cohort and
  surface gaps, overall and per target institute.

Data is layered across three public, no-auth sources, keyed off the InspireHEP author id that
the rumor sheet links for each person:

- **InspireHEP**: primary record (HEP papers, journals, citations, PhD year, advisors, ORCID).
- **OpenAlex**: cross-disciplinary augmentation for **everyone** with an ORCID, so ML / stats /
  CS venues (ICML, NeurIPS, journals) that InspireHEP misses are caught.
- **ORCID public API**: the author's own self-claimed work list, used to rescue people whose
  OpenAlex-by-ORCID cluster is contaminated by author-conflation (see below). Author-curated, so
  no conflation; citations are backfilled per DOI via OpenAlex.
- **Semantic Scholar**: name-based fallback (and h-index cross-check) when a person has no ORCID.

## Read this before reporting: the data is self-reported and incomplete

The rumor mill is filled in by volunteers. Offers that were never reported are simply absent,
per-institute counts are usually single digits, and the same person appears multiple times
(one row per institution, and `Offered` then `Accepted`/`Declined`). Treat the output as a
**qualitative signal, not a statistic**, and always state N and how many were resolved. The
analysis is **descriptive**: it describes what kind of profile landed where; it never predicts
whether a given profile will or will not get an offer. See `references/analysis.md`.

## Quick Reference

| Intent | Command | Reference |
|--------|---------|-----------|
| Pull a year's rumor sheet | `prm fetch --year YEAR [--sheet-id ID]` | `references/sheets.md` |
| Resolve offer-holders' records | `prm enrich [--year Y] [--status Accepted] [--limit N] [--no-cross-disc]` | `references/schema.md` |
| Show one person's record | `prm profile {recid \| --name NAME}` | `references/metrics.md` |
| Institute cohort profile | `prm institute "NAME" [--status Accepted] [--year Y]` | `references/metrics.md` |
| Benchmark your own profile | `prm analyze --me RECID [--institutes "A,B,C"] [--year Y] [--refresh]` | `references/analysis.md` |
| Emit Korean report skeleton | `prm report --year Y [--me RECID] [--out PATH]` | `references/analysis.md` |

Every command takes `--json` for machine-readable output. Run via `uv run prm ...` from the
skill directory. The local store lives at `~/.local/share/hep-rumor-mill/rumor.db`
(override with `PRM_DATA_DIR`).

## Typical workflow

1. `prm fetch --year 2026`: download the sheet, tag each institution's country/region, store
   entries. Reports total rows, unique people, institutions, and the `Offered/Accepted/Declined`
   breakdown.
2. `prm enrich --year 2026 --status Accepted`: resolve each accepted person across sources and
   compute metrics. Network-heavy and polite; it is resumable (`--limit N` caps a run, re-run to
   continue) and reports failures and any unresolved people. Start with `--status Accepted` since
   that is the cohort you usually benchmark against.
3. Explore: `prm institute "Perimeter Institute" --status Accepted`, `prm profile 1804701`,
   `prm analyze --me {your recid} --institutes "Perimeter Institute,CERN,DESY"`.
4. `prm report --year 2026 --me {your recid}`: emit a Korean markdown skeleton with the
   data-backed tables filled and clearly-marked blanks for the qualitative judgment, which you
   complete by reading the offer-holders' actual papers (see `references/analysis.md`).

## Data-quality flags surfaced by the tool

These are computed automatically; surface them when you report, do not hide them.

- **`n_large_collab`**: InspireHEP papers with > 50 authors. Big experimental / collaboration
  papers inflate a person's paper and citation counts; a high value means the headline numbers
  do not reflect lead-author output. Pair it with `n_first_author`.
- **OpenAlex author-conflation**: OpenAlex sometimes merges several same-named people (and a
  shared ORCID) into one author entity, pulling in unrelated disciplines (crystallography,
  neuroscience, economics). `enrich` drops clearly distant-field works, and when contamination
  is heavy it discards the whole OpenAlex cluster and rescues the real list from the ORCID public
  API instead (author-claimed, conflation-free), saying so in the run notes.
- **`interdisciplinary`**: set when the author's InspireHEP `arxiv_categories` include a
  non-physics category (cs, eess, stat, q-bio, econ, q-fin), or when a material share
  (>= 15%, >= 2 papers) of the record is in adjacent fields (CS / ML / stats / data science) or
  ML venues. Mathematics and mathematical physics are excluded on purpose (normal for formal
  hep-th). Physics-family fields, including OpenAlex's coarse "Physics and Astronomy", never
  trigger it on their own.
- **Citation undercount for arXiv-only preprints**: a work that exists only as an arXiv preprint
  (no DOI, not in InspireHEP) has its citations backfilled by a Semantic Scholar title match,
  which is a conservative floor (lower than Google Scholar); works Semantic Scholar does not
  index stay at 0. So citation totals for interdisciplinary candidates with many ML preprints
  still read low. Lean on the paper list and venues, not the citation total, for these people.
  Without an `S2_API_KEY` the in-pipeline backfill is best-effort (Semantic Scholar rate-limits
  hard); set the key for reliable backfill.

## Notes

- The rumor sheet is a public Google Sheet exported as CSV; no login. Year-to-sheet-id mapping
  lives in `prm/sheet.py` and `references/sheets.md`. Only 2026 ships known; add older years by
  extracting the embedded sheet id from each `postdocrumor/{year}-rumors` page.
- Journal prestige tiers (Tier A / B / C / preprint) are an editable opinion seeded with hep-th/ph
  convention. They live in `prm/metrics.py` and are documented in `references/metrics.md`.
- Be considerate with the APIs: `enrich` paces InspireHEP requests and OpenAlex paging. Semantic
  Scholar rate-limits hard and is used for the no-ORCID author fallback and for arXiv-only
  citation backfill; set `S2_API_KEY` (the same env var `reference-search` uses) to raise the
  limit and make the backfill reliable. Without it the pipeline still works, backfill is just
  best-effort.
- `prm analyze --me` uses the cached enriched record when one exists; pass `--refresh` to force a
  fresh re-enrich (otherwise a manual citation correction is preserved across runs).
