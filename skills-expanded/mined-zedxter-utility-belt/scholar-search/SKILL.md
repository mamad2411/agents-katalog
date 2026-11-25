---
name: scholar-search
description: Use whenever an answer should name real scholarly papers instead of recalling them from memory - the user asks for papers, studies, research or prior work on a topic, a literature review or related-work section, recent preprints, the most cited or key papers on a topic, whether a free or open-access PDF of a paper exists, or BibTeX for a DOI or arXiv id ("найди статьи про", "что почитать по теме", "свежие препринты"). Searches arXiv, Crossref, Europe PMC, PubMed and bioRxiv/medRxiv without an API key (OpenAlex and Semantic Scholar with the user's keys) - title, authors, year, venue, DOI, arXiv id or PMID, abstract, citation count and open-access link, merged across sources, filtered by date and sorted by relevance, date or citations; full records for given identifiers; marks papers already in the user's Zotero. Not for checking or verifying an existing reference list or .bib file (use cite-check), general web or news search, or reading a paper's full text.
license: MIT
compatibility: Python 3.12+ (standard library only; uv optional); macOS, Linux, Windows. Needs network access to export.arxiv.org, api.crossref.org, www.ebi.ac.uk, eutils.ncbi.nlm.nih.gov and doi.org; api.unpaywall.org with an email; api.openalex.org and api.semanticscholar.org only with their keys; localhost:23119 for --zotero. arXiv is called at most once every 3 s from this machine.
metadata:
  author: zedxter
  version: "1.0.0"
  source: https://github.com/zedxter/utility-belt
---

# Scholar Search

Finds real papers through the scholarly databases themselves, not web pages
about them. Every result comes from a source record with an identifier
(DOI, arXiv id or PMID), so nothing here is invented. That only holds if you
cite these results and nothing from memory.

- **Search** a topic across sources. Each work appears once, with all its
  identifiers, its largest known citation count, and the best abstract.
- **Look up** given DOIs, arXiv ids or PMIDs: the full record and an
  open-access link.
- **BibTeX** for given identifiers, straight from the DOI registries.

## When to use

- "Find papers / studies / research on X", "what should I read about X",
  "prior work" or "related work for my paper" → search.
- "Recent preprints on X", "what's new since 2024" → `--sort date` or
  `--since`.
- "The most cited papers on X" → `--sort citations` (see workflow step 5).
- "Is there a free PDF of this paper?" → `doi ID --email ...`; with only a
  title, search it first.
- "BibTeX for these DOIs" → `bibtex`.

Not for:
- checking a reference list or whether a cited paper is real → `cite-check`;
- general web pages, news or docs → `web-search`;
- a paper's full text → open its `oa_url` with `web-extract`.

## Quick start

The script is `scripts/scholar.py` relative to this skill. It uses only the
standard library, so both `uv run` and plain `python` work.

```bash
uv run scripts/scholar.py "retrieval augmented generation" --source arxiv,crossref --since 2024
uv run scripts/scholar.py "base editing sickle cell" --source europepmc,biorxiv --sort date -n 20
uv run scripts/scholar.py '"graph neural networks"' --source arxiv,crossref -f markdown
uv run scripts/scholar.py "microplastics human blood"                           # four free sources
uv run scripts/scholar.py doi 10.1038/nature14539 arXiv:1706.03762 PMID:26017442
uv run scripts/scholar.py bibtex 10.1038/nature14539 1706.03762 > refs.bib
```

Table output (abstracts trimmed with `--snippet`; preprints are marked; result 1 left out here):

```
# retrieval augmented generation hallucination · 3 results · sorted by relevance · 2024-01-01 to now
# from arxiv 3, europepmc 3, pubmed 3, crossref 20

2. Evaluating Evidence Sensitivity and Robustness of Hallucination Detectors in Retrieval- Augmented Generation
   Ramana Kulanthaivelu · 2026-10-26 · In Review · preprint · cited 0
   doi:10.21203/rs.3.rs-11400108/v1
   https://doi.org/10.21203/rs.3.rs-11400108/v1
   Retrieval-Augmented Generation (RAG) improves the accessibility of external knowledge for large language…

3. FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation
   Mohammad Aghajani Asl, Majid Asgari-Bidhendi, Behrooz Minaei-Bidgoli · 2025-10-25 · arXiv
   arXiv:2510.22344
   https://arxiv.org/abs/2510.22344
   open access: https://arxiv.org/pdf/2510.22344
   While Retrieval-Augmented Generation (RAG) mitigates hallucination and knowledge staleness in Large Language…
```

## Choosing sources

`--source` takes a comma-separated list. The default is
`arxiv,europepmc,pubmed,crossref`; `all` adds bioRxiv and any source whose
key is set. Pick by field, because a source outside its field adds noise:

| Field | Sources |
|---|---|
| Computer science, physics, maths, quantitative fields | `arxiv,crossref` |
| Biology, medicine, health | `europepmc,pubmed,biorxiv` |
| Everything else (social sciences, humanities, economics, engineering) | `crossref`; add `openalex` if the user has a key |
| Unsure, or across fields | the default |

| Source | Covers | Has citations | Open-access links |
|---|---|---|---|
| `arxiv` | arXiv preprints | no | always (the PDF) |
| `crossref` | every DOI-registered work, all fields | yes | with `--email` (Unpaywall) |
| `europepmc` | PubMed, PubMed Central, preprints, Agricola | yes | yes |
| `pubmed` | PubMed (MEDLINE) | no | via PubMed Central |
| `biorxiv` | bioRxiv and medRxiv preprints (through Europe PMC; bioRxiv's own API has no search) | yes | yes |
| `openalex` | all fields (needs `OPENALEX_API_KEY`) | yes | yes |
| `semanticscholar` | all fields, with one-line TL;DRs (needs `S2_API_KEY`) | yes | yes |

## Query syntax

Plain words work everywhere. Each source matches them differently:
- arXiv and Europe PMC need every word. Europe PMC searches titles and
  abstracts.
- PubMed expands words to MeSH terms.
- Crossref ranks works by how many of the words they contain.

Quote a phrase to keep it together: `'"large language models" evaluation'`.
A source's own syntax passes through unchanged:
- arXiv: `ti:transformer AND cat:cs.CL`
- Europe PMC: `AUTH:"Doudna J" AND TITLE:crispr`
- PubMed: `crispr[ti] AND review[pt]`

These fields break the other sources, so use them only with that one
`--source`.

## Options

| Command | What it does |
|---|---|
| `QUERY...` (or `search QUERY...`) | Search. Write `search` first when the query itself starts with "search", "doi" or "bibtex". |
| `doi ID...` | Full records for DOIs, arXiv ids (`arXiv:1706.03762`, `hep-th/9901001`) and PMIDs (`PMID:26017442`). URLs of doi.org, arxiv.org and PubMed work too. |
| `bibtex ID...` | BibTeX from the DOI registry (Crossref, or DataCite for arXiv). Citation keys look like `lecun2015deep`. |

| Flag | Default | Meaning |
|---|---|---|
| `--source LIST` | `arxiv,europepmc,pubmed,crossref` | See above. |
| `--since`, `--until DATE` | — | `YYYY`, `YYYY-MM` or `YYYY-MM-DD`. Each source filters, and results are filtered again locally. |
| `--sort` | `relevance` | `relevance`, `date` (newest first) or `citations` (most cited first). |
| `-n N` | 10 | Results, 1–100. |
| `--oa-only` | off | Only results with a known open-access link. |
| `--email ADDR` | `SCHOLAR_EMAIL` | Unpaywall open-access links and Crossref's polite pool. It is sent to every source in the User-Agent. |
| `--zotero` | off | Marks results already in the user's Zotero library. |
| `-f` | `table` | `table`, `json`, `markdown` (a numbered list with links), or `bibtex` (search only). |
| `--snippet N` | 240 | Abstract characters in the table; 0 hides abstracts. |
| `-o FILE`, `--timeout S`, `-q` | —, 30, off | Write to FILE; network timeout; hide `note:` lines. |

## JSON output

```json
{"query": "...", "sort": "relevance", "since": "2024-01-01", "until": null,
 "sources": {"arxiv": 6, "europepmc": 6, "pubmed": "failed: ...", "crossref": 12},
 "count": 6,
 "results": [{"title": "...", "authors": ["Yann LeCun", "..."], "year": 2015, "date": "2015-05-27",
   "venue": "Nature", "type": "journal-article", "doi": "10.1038/nature14539", "arxiv": null,
   "pmid": "26017442", "pmcid": null, "url": "https://doi.org/10.1038/nature14539",
   "oa_url": "https://hal.science/hal-04206682", "citations": 78891, "abstract": "...", "tldr": null,
   "sources": ["crossref", "europepmc", "pubmed"], "alt_dois": [], "in_zotero": null}]}
```

- `sources` at the top level counts the hits kept from each source before
  merging, or says why that source failed.
- `url` is the DOI link when there is one. Otherwise it is the arXiv or
  PubMed page.
- `oa_url` is a free copy: the arXiv PDF, PubMed Central, Europe PMC, or
  Unpaywall's best location. It is `null` when none is known.
- `citations` is the largest count among the sources. It is `null` when only
  arXiv or PubMed found the work.
- `alt_dois` holds the work's other DOIs, for example the preprint's DOI next
  to the journal's.
- `in_zotero` is `true` or `false` with `--zotero`, and `null` without it or
  when Zotero cannot be reached.
- `tldr` is filled only by Semantic Scholar.
- `doi` returns `{"results": [...], "not_found": [...], "failed": {id: reason}}`.

## Workflow for the agent

1. **Choose sources by field** (see the table) and put the core words of the
   request in the query. Use `-n 10`–`20`. Run two or three narrow queries
   rather than one broad one.
2. **Read the abstracts before recommending a paper.** A title match is not
   relevance. Drop results that are off topic, and say so if few remain.
3. **Cite only what the script returned**, with its DOI, arXiv id or PMID.
   Never add a paper from memory. If the user names one, look it up with
   `doi`; if they only know the title, use `cite-check`.
4. **Say what kind each result is.** Preprints (arXiv, bioRxiv, medRxiv) are
   not peer reviewed. A result that is also published has `doi`, `arxiv` and
   the journal's venue.
5. **"Most cited"**: `--sort citations` ranks the matches, not the whole
   field, by Crossref and Europe PMC counts.
   - It works well for biomedicine.
   - For computer science it is unreliable: arXiv papers have no counts, and
     landmark papers can be missing. Say so, and suggest an OpenAlex key.
6. **Free PDFs**: pass `--email` with the user's real address, from the user
   or `SCHOLAR_EMAIL`. Never invent one; without it, leave `--email` out.
   Give the `oa_url`, and never point the user to piracy sites.
7. **For a literature list**, finish with `-f markdown` or `-f bibtex`. Before
   it goes into a paper, run it through `cite-check`.
8. **Queries go to every source chosen.** Do not search with personal or
   confidential details.
9. **On exit 4, stop and tell the user.** Do not loop: requests are already
   spaced.

## Exit codes

One `error:` line on stderr with a hint after `—`. When some sources fail
and others answer, a search still exits 0, with a `note:` line per failed
source and the failure under `sources` in JSON. With `doi` and `bibtex`, ids
that could be looked up are printed even when another id failed; the exit
code is then that failure's.

| Exit | Meaning | What to do |
|------|---------|------------|
| 0 | Results. | — |
| 1 | No results, or (`doi`, `bibtex`) an identifier was not found; the found ones are still printed. | Broaden the query, drop `--since`/`--oa-only`, try other sources; check the identifier. |
| 2 | Bad input: empty query, unknown source, a keyed source without its key, bad date, `-n` out of range, bad email, unwritable `-o` (the output then goes to stdout). | Fix the argument. |
| 4 | Rate-limited (HTTP 429): every source of a search failed and one of them for this reason, or an id could not be looked up. | Wait a few minutes; do not loop. |
| 6 | Network error, source down (5xx) or refusing (401/403, or a wrong key): every source of a search failed, or an id could not be looked up. | Retry later, or use other sources. |
| 7 | A source answered something unreadable (it rejected the query syntax, or its API changed), or an unexpected failure. | Use plain words, or leave that source out. |
| 130 | Interrupted. | — |

## Keys (optional)

- **OpenAlex** (`OPENALEX_API_KEY`, free at openalex.org): all fields,
  native citation sort. Without a key it shares a tiny daily budget per
  network, so it is used only with one.
- **Semantic Scholar** (`S2_API_KEY`, free on request): TL;DRs and citation
  counts. Without a key it answers 429 almost every time.

Keys are read from the environment and sent only to their own API, never
following a redirect. Name the source in `--source`, or use `--source all`.

## Zotero

`--zotero` asks the Zotero 7 desktop app on this computer whether each result
is already in the library. It matches by DOI, including DOIs in the Extra
field, or by exact title. The app must be running, with **Settings → Advanced
→ "Allow other applications on this computer to communicate with Zotero"**
turned on. If it is off or closed, a `note:` says so and the search still
works. The check is read-only, and nothing leaves the machine.

## Limitations

- **Metadata and abstracts only.** For full text, open the `oa_url`.
  Crossref has abstracts for only some publishers.
- **Ranking is each source's own.** Results are interleaved by rank; ties go
  to works found by several sources. Crossref's relevance is the
  weakest: it surfaces niche works for broad queries. For
  `--sort date|citations` the script keeps only Crossref results that contain
  every query word.
- **Citation counts differ by source** (Crossref, Europe PMC, OpenAlex,
  Semantic Scholar count different citing sets); the largest is shown. The
  free sources cover biomedicine far better than other fields.
  - Free sources have no counts for arXiv-only papers, so in
    `--sort citations` those come last.
  - Classic CS papers published only on arXiv or in proceedings without DOIs
    can be missing from a citation ranking. An OpenAlex key helps with most of
    this.
- **Open-access links** without `--email` come only from arXiv, PubMed
  Central and Europe PMC.
- **Dates** are the earliest publication date a source gives, so print issues
  dated in the future can sort first with `--sort date`.
- **bioRxiv and medRxiv** appear a few days after posting, when Europe PMC
  indexes them.

## Chaining

- `scholar-search` → `cite-check` before references go into a paper.
- `oa_url` → `web-extract` (or `wayback` if the link is dead) to read the
  paper.
- `-f markdown` → `human-writing` for a literature review that cites only
  these papers.
- `-f bibtex` → the user's `.bib`; `--zotero` avoids adding duplicates.
