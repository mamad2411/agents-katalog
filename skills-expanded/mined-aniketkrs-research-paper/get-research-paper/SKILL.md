---
name: get-research-paper
description: Discovers, retrieves, ranks, and summarizes real existing research papers on any topic. Searches arXiv, Google Scholar, PubMed, Semantic Scholar, and reputable open repositories; returns a curated reading list with verified DOIs, key findings, and citation-ready metadata. Activates on slash commands (`/get-research-paper`, `/find-paper`, `/fetch-paper`, `/papers-on`, `/scholar`) and natural-language requests like "get research paper on …", "find papers about …", "what are the top papers on …". Hands off cleanly to the `research-paper` skill for paper writing. Runtime-neutral — works with Claude Code, OpenCode, Cursor, Cline, Codex, Aider, Amp, and 50+ agents.
license: MIT
version: 1.1.0
---

# Get Research Paper

A research-discovery skill. Where the **`research-paper`** skill *writes*
papers, this skill **finds** them. Give it a topic, get a ranked,
de-duplicated reading list of real existing papers with verified DOIs,
key findings, and ready-to-cite metadata.

This file is the **entry point**. Heavier guidance (per-source
strategies, ranking criteria, summarization prompts) lives in topic
folders and is loaded **on demand**.

---

## 1. When to activate

### Slash commands

| Command                        | What it does                                      |
| ------------------------------ | ------------------------------------------------- |
| `/get-research-paper <topic>`   | Curated reading list (default 10 papers)         |
| `/find-paper <topic>`           | Alias for `/get-research-paper`                  |
| `/find-papers <topic>`          | Alias for `/get-research-paper`                  |
| `/fetch-paper <topic>`          | Alias for `/get-research-paper`                  |
| `/papers-on <topic>`            | Alias for `/get-research-paper`                  |
| `/scholar <topic>`              | Quick scholarly summary (5 papers, 2-line summaries) |

Common options:
- `--n <N>` — number of papers (default 10).
- `--years <range>` — e.g. `2020-2024`, `last-5`, `since-2018`.
- `--source <src>` — `arxiv`, `scholar`, `pubmed`, `semantic-scholar`, `all` (default).
- `--depth <quick|standard|deep>` — summary detail.
- `--style <harvard|apa|ieee|...>` — pre-format the bibliography.
- `--audience <academic|technical|general>` — adjust summary register.
- `--handoff` — emit a `bibliography.yaml` ready for the `research-paper` skill.

### Natural-language patterns

- "get research paper on / about / for [topic]"
- "find research papers on [topic]"
- "find papers on / about [topic]"
- "what are the top papers on [topic]"
- "show me research on [topic]"
- "fetch papers about [topic]"
- "list papers on [topic]"
- "literature on [topic]" (shorter than `/literature-review`)
- "scholar [topic]"

### Negative activation

Do NOT activate for:
- Requests to **write** a paper (route to `research-paper`).
- Requests to **review** or **critique** a draft (route to `research-paper`).
- Casual questions ("what is X?") that don't need scholarly sources.
- Pure code / API documentation lookup.

---

## 2. Output contract

Every run produces, at minimum:

1. **Reading list** — N papers with:
   - Title (full)
   - Authors (first 3 + "et al." if more)
   - Year
   - Venue / journal / preprint server
   - DOI / arXiv ID / URL
   - 2–4 sentence **summary** (problem → method → finding → significance)
   - **Relevance score** (1–5) and **quality score** (per `citation_engine` rubric)
   - **Cite key** (lowercase author_year_word) ready for use
2. **Field briefing** (optional, default ON for `--depth deep`) — a
   1-paragraph synthesis of where the field is and what the dominant
   approaches are.
3. **`bibliography.yaml`** — canonical-format file ready to drop into
   the `research-paper` skill.
4. **`Known-gaps.md` block** — every paper that couldn't be verified is
   surfaced with severity and recommended fix.

See `templates/reading-list.md`, `templates/paper-summary.md`,
`templates/briefing.md`.

---

## 3. Core principles

0. **Anchor to TODAY's date FIRST.** Before any search, determine
   today's actual date (via `date -u +%Y-%m-%d`, runtime context, or
   asking the user). **Never default to training-cutoff dates.** Year
   ranges like `--years last-3` are computed from today. Full protocol:
   `instructions/freshness.md`.
1. **Real papers only.** Never invent papers, DOIs, authors, or
   findings. Use only sources the model can verify (or honestly mark
   `[UNVERIFIED — offline]`).
2. **De-duplicate aggressively.** Same DOI / arXiv ID / first-author + year + title prefix → one entry.
3. **Rank by relevance and quality.** A bad paper that mentions the
   topic is less useful than a great paper that's two clicks adjacent.
4. **Cite-ready by default.** Every entry has cite_key + DOI + ready-to-use formatted citation.
5. **Triangulation.** For load-bearing claims, prefer ≥ 2 independent
   sources. Note when a finding rests on a single source.
6. **Honest about limits.** Without web tools, the model relies on
   training-data knowledge — flag every entry accordingly.
7. **Hand off cleanly.** Output is consumable by the `research-paper`
   skill via `--handoff` mode.

---

## 4. Top-level workflow

```
intake → search-strategy → fan-out search → rank+dedupe →
verify → summarize → assemble briefing → output (+ optional handoff)
```

Each step has a dedicated playbook. Read the file for the step you're
on; persist the artifact; move on. Master pipeline:
**`workflows/search.md`**.

---

## 5. Source coverage

| Source                | When to prefer                            | Tool                                         |
| --------------------- | ----------------------------------------- | -------------------------------------------- |
| **arXiv**             | CS, ML, AI, physics, math, quant-bio       | `toolchains/arxiv_search.py` (works offline-only via API) |
| **Google Scholar**    | Generic / cross-discipline broad surveys   | `WebSearch` with `site:scholar.google.com`    |
| **Semantic Scholar**   | API-friendly, citation graph, summaries     | `WebFetch` of api.semanticscholar.org         |
| **PubMed / PubMed Central** | Biomedical, life sciences           | `WebFetch` of eutils.ncbi.nlm.nih.gov         |
| **DBLP**               | CS authors / venues / publication lists    | `WebFetch` of dblp.org                        |
| **ACM DL**            | HCI, systems, security, networks           | `WebSearch` with `site:dl.acm.org`            |
| **IEEE Xplore**        | Engineering, signal, hardware              | `WebSearch` with `site:ieeexplore.ieee.org`   |
| **OpenReview**         | NeurIPS, ICLR, ICML reviews + papers       | `WebFetch` of openreview.net                  |
| **Crossref**           | DOI verification + metadata fill-in        | `WebFetch` of api.crossref.org                |
| **Retraction Watch**   | Retraction screening                       | `WebFetch` of retractionwatch.com / database  |

Per-source strategy details: `sources/`.

---

## 6. Ranking and quality

Each candidate paper is scored on:

- **Authority (0–4)** — venue quality (peer-review rigor, impact).
- **Methodological rigor (0–3)** — replicability, sample size, sound stats.
- **Recency / relevance (0–3)** — fresh + topical, OR foundational + canonical.
- **Total (0–10)** — used to rank.

Default reading lists keep papers scoring **≥ 5**. Higher floors raise
the bar (`--quality-floor 7`).

Full rubric: `prompts/ranking.md` (extends the
`citation_engine/source-evaluation.md` of the `research-paper` skill).

---

## 7. Handoff to `research-paper`

After producing a reading list:

```bash
/get-research-paper "graph neural networks for fraud detection" \
    --n 25 --handoff --style ieee --years 2020-2024
```

Produces:

```
gnn-fraud-detection/
├── reading-list.md            # human-readable curated list
├── bibliography.yaml          # ← canonical file for research-paper skill
├── briefing.md                # 1-paragraph synthesis
└── Known-gaps.md              # any unverifiable items
```

The user then runs the writer skill with the produced bibliography:

```bash
/research "graph neural networks for fraud detection" \
    --style ieee --bibliography ./gnn-fraud-detection/bibliography.yaml
```

The writer reads the curated bibliography directly — no re-search needed.

---

## 8. Failure handling

- **No web search available** → use model-known papers, mark every
  entry `[UNVERIFIED — offline]`, lower the recommended `--n` to 5–8,
  and surface the limitation in the briefing.
- **Search returns nothing** → broaden the query (drop adjectives,
  try synonyms), then return what was found with an honest note.
- **Conflicting metadata across sources** → prefer the published
  (peer-reviewed) version over the preprint; note the relationship.
- **Retracted paper detected** → drop from the list; flag in
  `Known-gaps.md`.
- **Out-of-scope topic** → surface a note in the briefing; deliver
  best-effort results.

---

## 9. Where to look next

- **Plan a search** → `workflows/search.md`
- **Per-source strategy** → `sources/`
- **Ranking rubric** → `prompts/ranking.md`
- **Summarization** → `prompts/summarization.md`
- **Output templates** → `templates/`
- **Hand off to writer** → `workflows/handoff-to-writer.md`
- **arXiv search tool** → `toolchains/arxiv_search.py`

This skill is intentionally smaller than the writer skill. Its job is
discovery and curation; the heavy lifting (writing, methodology,
review) lives in `research-paper`.
