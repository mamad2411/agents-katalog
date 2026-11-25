---
name: read-research-paper
description: Renders ANY research paper (URL / arXiv ID / DOI / PDF / pasted text) into a visually engaging multi-format reading experience — with mind maps, method flowcharts, key-finding infographics, comparison tables, related-work timelines, and a plain-English layer alongside the technical content. Activates on slash commands (`/read-research-paper`, `/read-paper`, `/explain-paper`, `/visualize-paper`) and natural-language requests like "read this research paper [URL]", "explain this paper [URL]", "make this paper visual [URL]". Caches every fetched paper locally so re-asks are instant. Ships with a bundled corpus of canonical papers for offline fallback. Hands off to `research-paper` for citation reuse and to `get-research-paper` for related-work expansion. Runtime-neutral.
license: MIT
version: 1.2.0
---

# Read Research Paper

Where the other two skills do this:

| Skill | What it does |
|---|---|
| `get-research-paper` | **FINDS** real papers on a topic |
| `research-paper`     | **WRITES** new papers |
| **`read-research-paper`** (this) | **READS** ONE paper and makes it engaging |

Give it a URL, arXiv ID, DOI, or pasted text. It produces a visual,
multi-layer rendering: technical depth + plain English + mind maps +
method flowcharts + key-finding infographics + comparison tables +
related-work timelines.

This file is the **entry point**. Heavier guidance lives in topic
folders and is loaded on demand.

---

## 1. When to activate

### Slash commands

| Command                      | What it does                              |
| ---------------------------- | ----------------------------------------- |
| `/read-research-paper <input>` | Full visual rendering (default)         |
| `/read-paper <input>`         | Alias                                     |
| `/explain-paper <input>`      | Same, with extra plain-English layer      |
| `/visualize-paper <input>`    | Same, emphasizing visuals over prose      |
| `/tldr-paper <input>`         | One-page infographic summary only         |

`<input>` can be:
- A URL: `https://arxiv.org/abs/2403.01234`, `https://doi.org/...`,
  `https://example.com/paper.pdf`, journal landing page, etc.
- An arXiv ID: `2403.01234` or `cs.LG/0701002`
- A DOI: `10.1145/3589334`
- Pasted text: the paper's abstract or full body
- **A local file** in any supported format (see below).

### Supported file formats

The skill reads **any of these** as input:

| Format    | Extensions             | Library used                | Always available?       |
| --------- | ---------------------- | --------------------------- | ----------------------- |
| Markdown   | `.md`, `.markdown`     | stdlib                      | yes                      |
| Plain text | `.txt`                 | stdlib                      | yes                      |
| LaTeX      | `.tex`, `.latex`       | stdlib + regex de-LaTeX      | yes                      |
| JSON       | `.json`                 | stdlib                      | yes                      |
| HTML       | `.html`, `.htm`         | beautifulsoup4 (or regex)   | yes (regex fallback)     |
| CSV / TSV  | `.csv`, `.tsv`          | pandas (or stdlib)          | yes (basic via stdlib)   |
| RTF        | `.rtf`                  | striprtf (or regex)         | yes (regex fallback)     |
| **PDF**     | `.pdf`                  | pdfplumber / pypdf          | install one              |
| **DOCX**    | `.docx`                 | python-docx                 | install                  |
| **PPTX**    | `.pptx`                 | python-pptx                 | install                  |
| **XLSX**    | `.xlsx`, `.xls`         | pandas + openpyxl            | install                  |
| **EPUB**    | `.epub`                 | ebooklib                    | install                  |
| **Images**  | `.png`, `.jpg`, `.tiff`, `.bmp` | pytesseract + PIL    | install (OCR)            |

One-line install for everything:

```bash
pip install pdfplumber python-docx python-pptx pandas openpyxl \
            beautifulsoup4 striprtf ebooklib pytesseract Pillow
```

(Plus install Tesseract OCR system-wide for images.)

The reader is `toolchains/read_any_file.py`. Self-test:

```bash
python toolchains/read_any_file.py --self-test
python toolchains/read_any_file.py --list-formats
```

Full reference: `sources/file-formats.md`.

### Common options

| Option              | Default     | Effect                                      |
| ------------------- | ----------- | ------------------------------------------- |
| `--depth`            | `standard`  | quick / standard / deep                       |
| `--audience`         | `mixed`     | academic / technical / general / mixed         |
| `--visuals`          | `auto`      | auto / max / minimal / none                    |
| `--include-figures`  | `true`      | Try to extract / re-create paper's own figures |
| `--cache`            | `true`      | Use local cache (auto-fill on re-asks)         |
| `--language`         | `en`        | Plain-English language                          |
| `--out`              | `./<paper-slug>/` | Working directory                          |
| `--with-related`     | `false`     | Trigger `get-research-paper` for related work   |
| `--with-handoff`     | `false`     | Emit bibliography.yaml for `research-paper`     |

### Natural-language patterns

- "read this research paper <URL>"
- "explain this paper <URL>"
- "make this paper visual <URL>"
- "I want to understand this paper <URL>"
- "summarize this paper <URL>"
- "tldr this paper <URL>"
- "what does this paper say <URL>"

### Negative activation

Do NOT activate for:
- Requests to **find** papers on a topic (route to `get-research-paper`).
- Requests to **write** a new paper (route to `research-paper`).
- Pasted prose without a paper-shaped input ("here's an article…").
- Casual questions about a topic that don't reference a specific paper.

---

## 2. Output contract

Every run produces:

1. **`paper-visual.md`** — the headline deliverable. Multi-layer:
   - One-page **infographic** at the top (mind map + key numbers).
   - **TL;DR** in 5–8 sentences.
   - **Plain-English summary** in 5–10 sentences.
   - **Section-by-section walk-through** with each section preceded
     by a 1-paragraph plain-English version, then the technical
     content with extracted / generated visuals.
   - **Method flowchart** (Mermaid).
   - **Key findings infographic** (charts with the paper's
     headline numbers).
   - **Comparison table** to baselines (when present).
   - **Related work timeline** (when references are available).
   - **"Why this matters" footer**.
2. **`paper-data.json`** — structured extracted metadata: title,
   authors, year, abstract, sections, figures, tables, key numbers,
   references. Schema in `schemas/visual-paper.json`.
3. **`figures/`** — generated charts / diagrams / mind maps as
   PNG + SVG + Mermaid sources.
4. **`cache/<paper-id>.json`** — cached for re-use.
5. **`Known-gaps.md`** — anything that couldn't be fetched / parsed.

If `--with-handoff` is set, also produces `bibliography.yaml`
ready for the `research-paper` skill.

If `--with-related` is set, the orchestrator dispatches
`get-research-paper` on the paper's key topics to seed a related-work
section.

---

## 3. Operating principles

0. **Anchor to TODAY's date.** When the input is a topic-style query
   (rather than a specific URL/DOI/path), determine today's actual
   date first (via `date -u +%Y-%m-%d`, runtime context, or asking
   the user). For a specific paper input, the freshness check
   compares the paper's publication date to today and flags
   stale findings. Full protocol: `instructions/freshness.md`.
1. **Don't bluff.** If a URL doesn't resolve or a PDF can't be
   parsed, say so. Mark `[FETCH FAILED — fallback to cache | model
   knowledge | corpus]` and surface in `Known-gaps.md`.
2. **Cache everything.** Every successfully fetched paper is written
   to `~/.agents/skills/read-research-paper/cache/`. Re-asks are
   instant.
3. **Ship the corpus.** A small bundled corpus of canonical papers
   (`corpus/anchor-papers.yaml`) is searched first when the input is
   a topic-style query rather than a specific paper.
4. **Visual-by-default.** Generate at minimum: 1 mind map + 1 method
   flowchart + 1 key-findings figure + 1 comparison table.
5. **Dual register.** Every section has BOTH plain-English and
   technical content. Never strip the technical depth — augment with
   simpler language alongside.
6. **Honest interpretation.** Don't oversell findings. Match the
   paper's own certainty. If the paper hedges, the visual paper
   hedges.

---

## 4. Top-level workflow

```
intake → fetch → parse → extract-figures-and-data →
plan-visuals → render → assemble → cache → output
```

Each phase has a dedicated playbook. Master pipeline:
**`workflows/ingestion.md`**.

---

## 5. Source detection

The skill auto-detects input type:

| Input pattern                                   | Path                                       |
| ----------------------------------------------- | ------------------------------------------ |
| `arxiv.org/abs/...`                              | arXiv API                                   |
| `\d{4}\.\d{4,5}` (bare arXiv ID)                 | arXiv API                                   |
| `doi.org/...` or `10\..../...`                   | Crossref → URL → fetch                       |
| `*.pdf` (URL or local path)                      | PDF extraction                              |
| Journal landing page URL                         | URL scrape + Crossref enrichment            |
| Pasted text (no URL)                             | Treat as paper body; build structure heuristically |

See `workflows/ingestion.md §1`.

---

## 6. Three-tier fallback

```
1. Local cache (~/.agents/skills/read-research-paper/cache/)
   ├── Hit  → return immediately (instant)
   └── Miss → next tier

2. Live fetch (arXiv API / Crossref / WebFetch / PDF parser)
   ├── Success → render + cache
   └── Fail    → next tier

3. Bundled corpus (corpus/anchor-papers.yaml)
   ├── Hit  → return + flag as "from bundled corpus"
   └── Miss → next tier

4. Model knowledge
   ├── Confident → render + flag every fact [UNVERIFIED — offline]
   └── Not confident → fail honestly with a Known-gaps entry
```

Every tier transition is logged in `Known-gaps.md` so the user knows
where the rendered paper came from.

---

## 7. Visual rendering plan

For every paper, the skill produces:

| Visual                   | Source                               | Renderer                       |
| ------------------------ | ------------------------------------ | ------------------------------ |
| **Mind map**              | Paper structure (sections + key ideas) | Mermaid `mindmap`              |
| **Method flowchart**      | Method section                        | Mermaid `flowchart`             |
| **Key-findings infographic** | Headline numbers from results        | matplotlib if available, else Markdown table |
| **Comparison table**       | Paper's own benchmark table             | Markdown table                  |
| **Related-work timeline**   | References + their years                | Mermaid `gantt`-style timeline  |
| **Author network**          | Authors + affiliations                  | Mermaid `flowchart` (small)      |
| **Concept map**             | Paper's terminology                     | Mermaid `mindmap`               |
| **Figure re-captions**      | Original figures (when extractable)     | Pass-through with new captions   |

Decision logic: `workflows/visualization.md`.

---

## 8. Cache architecture

The cache lives at:

```
~/.agents/skills/read-research-paper/cache/
├── manifest.json              # index of all cached papers
├── arxiv/
│   ├── 2403.01234.json
│   └── 2005.11401.json
├── doi/
│   ├── 10.1145_3589334.json
│   └── ...
├── url/
│   └── <sha256-hash>.json
└── topics/
    └── <topic-slug>.json      # topic → list of cached paper IDs
```

When the user asks about a topic (not a specific paper), the cache's
`topics/` index is searched first, before any live fetch.

Cache schema: `workflows/caching.md`.

---

## 9. Bundled corpus

Ships in `corpus/`:

- `anchor-papers.yaml` — ~30 canonical, high-impact papers across
  major topics (transformers, RAG, RLHF, contrastive learning, RCT
  methodology, PRISMA, etc.).
- `topics-index.yaml` — maps topic keywords to the anchor papers.

When the user asks for a paper that's in the corpus, the skill uses
the corpus version (always available, even offline). Users can extend
the corpus by adding files to `corpus/user/`.

---

## 10. Failure handling

- **URL doesn't resolve** → try arXiv ID extraction, then DOI lookup,
  then surface in `Known-gaps.md`.
- **PDF unparseable** → fall back to abstract-only rendering with a
  warning.
- **Model couldn't extract figures** → generate Mermaid alternatives.
- **No headline numbers in results** → use qualitative findings.
- **Web tools unavailable** → cache + corpus + model-knowledge in
  that order.

Full matrix: `workflows/ingestion.md §10`.

---

## 11. Where to look next

- **Plan an ingestion** → `workflows/ingestion.md`
- **Pick visuals** → `workflows/visualization.md`
- **Cache protocol** → `workflows/caching.md`
- **Plain-English layer** → `prompts/plain-english.md`
- **Mind-map generation** → `prompts/generate-mindmap.md`
- **Output format** → `templates/visual-paper.md`
- **Bundled corpus** → `corpus/`
- **Fetch tools** → `toolchains/fetch_paper.py`,
  `toolchains/extract_pdf.py`

This skill complements but does not require the other two:
- `get-research-paper` → **find** papers
- `research-paper` → **write** papers
- `read-research-paper` → **read** papers (this one)
