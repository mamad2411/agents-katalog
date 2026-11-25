---
description: Autonomous literature explorer — from a query or topic, search papers + the credibility-scored web, read the papers full-text, and build an interlinked concept web (paper + concept pages) in a non-personal library, ending in a synthesis page. Standalone → explore_library/<query>/; invoked by /curriculum → course/<slug>/library/.
argument-hint: <research query or topic> (e.g. "how do diffusion models avoid mode collapse?", "continual learning")
allowed-tools: Read, Write(explore_library/**), Write(course/**), Glob, Bash(date:*), Bash(mkdir:*), Bash(sh .claude/src/pyrun:*), WebSearch, WebFetch
---

Starting from **$ARGUMENTS** (a research query or topic), autonomously build a
richly interlinked **concept web**: gather the relevant literature by searching papers
+ the credibility-scored web, read the papers, decompose their ideas into elementary
**concept pages**, link everything up over several passes, and finish with a
**synthesis page** that answers the original query.

If **$ARGUMENTS** is empty, ask the user for a query or topic, then continue.

## Destination — NEVER the personal base

This skill **never writes to the personal `sources/`, `papers/`, or `concepts/`.** It always
writes its whole concept web into a **non-personal `<dest>` directory**, laid out with the
**same type-subfolders as the main vault** (`<dest>/sources/`, `<dest>/papers/`,
`<dest>/concepts/`) so file stems equal their slugs and wikilink resolution works:

- **Standalone** (`/autoexplore <query>`) → **`explore_library/`** — *one accumulating
  corpus* (do **not** create a per-query subfolder; new pages join the existing
  `explore_library/{sources,papers,concepts}/`). Default snowball depth **`--hops 2`**.
  This corpus **is separately indexed** (`.index/explore_library.pkl`) so it scales and is
  queryable on its own — but it is a **distinct index from the personal base**, never merged.
- **Invoked by `/curriculum <slug>`** → **`course/<slug>/library/`** (the caller passes this
  directory and `--hops 0`). Same `{sources,papers,concepts}/` layout, but the per-course
  library is **not indexed** (resolved by filesystem instead).

Material only ever enters the personal base later, by explicit promotion (e.g. `/tutor`
graduating a mastered library file into `sources/`, or you hand-promoting from `explore_library/`).

**File naming inside `<dest>` (type-subfolders; stem == slug):**
- objective sources: `<dest>/sources/alphaxiv_<slug>.md`, `<dest>/sources/web_<slug>.md`
  (written by `/alphaxiv`, `/web`)
- paper pages: `<dest>/papers/<slug>.md`
- concept pages: `<dest>/concepts/<slug>.md`
- synthesis (standalone only): `<dest>/concepts/<query-slug>.md`

## Prerequisites

- The literature engine is the **pip-installed `prior` package** (pinned in
  `.claude/requirements.txt`) — **no `../prior` checkout needed**. It is driven through two
  thin wrappers in this repo, both of which load `.env` and need **no API key**:
  - `.claude/src/explore_lit.py` — topic → scoped corpus (LLM query variation over
    OpenAlex/arXiv/Semantic Scholar + citation snowball), writing a JSONL corpus.
  - `.claude/src/fulltext_lit.py` — render a corpus's papers to full Markdown (full-text
    cascade: arXiv / OA PDF / Unpaywall / publisher) for reading.
- **Run every Python wrapper through `sh .claude/src/pyrun …`, never a bare interpreter.**
  `pyrun` finds whatever environment actually has the deps installed (venv / uv / conda /
  system / `PKM_PYTHON`), so you must **not** pre-check for `.venv`/`.env` existence or
  reason about relative-vs-absolute paths — that check is meaningless and misleads. Just run
  the command. If (and only if) `pyrun` prints `PKM_ENV_ERROR` and exits non-zero, the deps
  genuinely aren't importable in any environment: **do not** speculate about paths — use
  `AskUserQuestion` to ask whether the right environment is activated, offering (a) activate
  it and retry, (b) point at an existing interpreter via `PKM_PYTHON=/path/to/python`, or
  (c) install deps (`pip install -r .claude/requirements.txt`). `pyrun` never installs
  anything itself. Re-run the same command once they choose.
- Paper discovery + full text require `.env` (`PRIOR_*`) and network. **Semantic Scholar
  rate-limits (HTTP 429) without a key** — the scoper logs the skip and degrades to
  OpenAlex + arXiv, so recall is slightly lower but the run still succeeds.
- Work artifacts (corpus JSONL, logs) go to a gitignored dir `<dest>/.work/`. Full-text
  renders go to **`<dest>/sources/`** (visible, alongside `alphaxiv_*` and `web_*`); they
  are named `<title-slug>.md` by `fulltext_lit.py`. The **knowledge-base output** (pages)
  follows this repo's normal page conventions.

> Heads-up: this is a heavy, long-running operation — explore + full-text rendering make
> many network/API + LLM calls and can take several minutes. Tell the user before a deep run.

## Overview (pseudocode)

`$` = external wrapper · `«LLM»` = a reasoning step you perform.

```python
def autoexplore(query, dest, hops):                           # dest + hops set by mode (above)
    topic_def  = «LLM» in/out-of-scope definition for query   # 1. frame (optional WebSearch)
    queries    = confirm_with_user([topic_def] + «LLM» related_queries(query))

    corpus = []                                               # 2. acquire (per query)
    for q in queries:
        $ explore_lit.py --topic q --hops hops --out dest/.work/<q>.jsonl
        corpus += read_jsonl(...)
    corpus = dedup_by_id(corpus)
    pull credibility-scored web → dest/sources/web_*.md                 # /web only

    for batch in chunks(corpus):                              # 3. triage — ONE combined call/batch
        for p, t in «LLM» triage(batch): p.summary, p.relevance, p.reason = t
    core, deferred = split_by_relevance(corpus, cap≈15-25)
    if «LLM» gaps_remain(core): queries += «LLM» more_queries(); goto 2

    $ fulltext_lit.py --corpus dest/.work/corpus.jsonl --out dest/sources/         # 4. read core
    for p in core: p.ideas = «LLM» read(render(p) or p.abstract)

    for p in core:                                            # 5. ingest into dest (NOT personal)
        prepend_frontmatter(dest/sources/<title-slug>.md)     #   fulltext_source YAML + ## Content
        write dest/papers/<slug>.md                           #   paper page citing the source above

    repeat 2-3 passes:                                        # 6. concept web
        for idea in core.ideas: write dest/concepts/<slug>.md #   decompose → elementary concepts
        for link in dangling(dest): write dest/concepts/<link>.md  # via retrieve_cli --resolve-dir
        add cross-links
    if standalone: write dest/concepts/<query-slug>.md        # 7. synthesis answering query

    report(...) ; review_loop(/edit)                          # no manual reindex (poller handles it)
```

## Steps

### 1. Frame the topic (+ related queries)
Turn **$ARGUMENTS** into a precise **in-/out-of-scope topic definition** (what counts as
relevant, what doesn't) — `explore_lit.py`'s `--topic` expects this, and recall depends on
it. Use `WebSearch`/`WebFetch` to orient and identify seed terms or landmark papers, then
write the definition. Also propose a handful of **related queries** — adjacent sub-topics,
competing approaches, foundational precursors. Show the framing + related queries and confirm
which to include before a deep run. Each chosen query becomes its own `explore_lit` run in Step 2.

### 2. Acquire the literature (papers + credibility-scored web)
Resolve `<dest>` and `<hops>` from the mode (see **Destination** above), then:

```bash
mkdir -p "<dest>/.work"
sh .claude/src/pyrun --need prior .claude/src/explore_lit.py --topic "<in/out-of-scope definition>" \
  --hops <hops> --out "<dest>/.work/<query-slug>.jsonl"
```
- `--hops` is snowball depth: `0` = search only (curriculum default), `1–3` = follow
  citations outward (deeper = broader but slower; standalone default `2`).
- Run once per chosen query, each to its **own** `--out` JSONL, then read + **merge** them
  (dedup by `id`) into one `<dest>/.work/corpus.jsonl`. Useful fields per record: `id`
  (`openalex:W…`/`arxiv:…`/`doi:…`), `doi`, `title`, `abstract`, `url`, `year`, `authors`,
  `is_review`, `cited_by_count`, `referenced_works`, sometimes `full_text`/`pdf_url`. Report
  corpus size + the completeness estimate (only defined for `--hops ≥ 1`).
- **Web**, in the same pass — pull canonical/reputable web grounding via `/web` (curated
  registries + credibility scoring), writing into `<dest>/sources/` (pass that as its destination):
  - `/web wiki "<topic>"` — encyclopedic grounding (almost always include one).
  - `/web search "<sub-topic> tutorial | explained | guide"` — vetted blogs/tutorials/docs.
  Track each kept web source's `kind`, `tier`, and `score`.
- If the paper pull fails (no `.env`/network), say so and continue with web + abstracts only.

### 3. Triage by summary + relevance
Before expensive full-text reads, **summarise and score** the corpus from the abstracts in
the merged JSONL:
- For each paper produce a `{summary, relevance, reason}` triple **in one combined call**,
  **batching several papers per call**. Use `is_review`, `cited_by_count`, `year` as
  secondary signals.
- Keep the **core set** (high/medium relevant; cap ~15–25); set aside the rest with a
  one-line reason each (reported in the wrap-up, not silently dropped).
- **Spot landscape gaps.** If summaries reveal sub-areas the queries missed, propose new
  related queries and loop back to Step 2. Repeat until the core set covers the query well.

### 4. Read the papers (full text)
Render full text for the whole corpus (the cascade caches, so re-runs are cheap):
```bash
sh .claude/src/pyrun --need prior .claude/src/fulltext_lit.py \
  --corpus "<dest>/.work/corpus.jsonl" --out "<dest>/sources/"
```
This writes `<dest>/sources/<title-slug>.md` per paper with retrievable full text.
Immediately after rendering, for each file **prepend the YAML frontmatter** block so it
follows `.claude/Templates/source.md` (`fulltext_source` type):

```yaml
---
type: fulltext_source
title: <paper title from corpus>
concepts_mentioned: []        # fill in during step 6 once you know the concept web
source_links:
  - <canonical URL — arXiv URL if arxiv:… id, else DOI URL, else p.url from corpus>
---

## Content

```
Write this header block at the top of the file (before the title/authors/year line that
`fulltext_lit.py` wrote). Leave `concepts_mentioned` as `[]` for now — you will back-fill it
after building the concept web in step 6. For any core paper with no retrievable full text,
fall back to its `abstract` (+ `full_text`/`pdf_url` if present) in the corpus and write a
minimal `fulltext_source` file manually.

`Read` each `<dest>/sources/<title-slug>.md` for the core papers. Capture each paper's
**core ideas, contributions, methodology, and key equations** (LaTeX) — raw material for
the pages below.

### 5. Write paper pages → `<dest>`
The full-text source files were written and structured in step 4 — no separate alphaxiv
ingestion needed. For each core paper:
- **Paper page** → `<dest>/papers/<slug>.md`: objective summary + key contributions +
  methodology, following `.claude/Templates/paper.md` and the **Page conventions** in
  `.claude/AGENTS.md`. Cite the source as a relative link to `../sources/<title-slug>.md`.
  Write this page directly — **do not delegate to `/collate`**, which has its `Write`
  permissions locked to the personal `papers/` and `concepts/` directories and cannot
  target `<dest>/papers/`.

### 6. Build the concept web — iterate (over `<dest>`)
- **Dedup first.** Before creating a concept, check it doesn't already exist:
  - in **`<dest>`** (this corpus) — see the resolver below;
  - for **standalone** runs, also `--corpus explore --retrieve "<concept>"` to reuse a
    concept a *prior* exploration already wrote into `explore_library/` (link to it, don't
    duplicate);
  - optionally `--retrieve "<concept>"` (base corpus, read-only) — if the personal base
    already covers it, note "covered in base" and do **not** write there.
- **Decompose.** Break each paper's core ideas into **elementary concepts** (smallest
  reusable units). For each, create `<dest>/concepts/<slug>.md` following
  `.claude/Templates/concept.md` + the Page conventions, grounded in and citing the relevant
  `<dest>/sources/`+`<dest>/papers/` files (relative links). Be mathematical where the
  concept is.
- **Interlink.** Under "Related concepts"/"Related work", link existing `<dest>` pages with
  relative links; for page-worthy concepts that don't exist yet, leave `[[wikilinks]]`.
- **Loop (2–3 passes).** Re-read every paper + concept page in `<dest>` and tighten the web.
  Resolve `[[wikilinks]]` against `<dest>` with the **index-free** resolver (works whether or
  not `<dest>` is indexed, and is always fresh during the build — no per-link reindex):
  ```bash
  sh .claude/src/pyrun .claude/src/retrieve_cli.py --resolve-dir "<dest>" "<wikilink>" ...   # NONE = no page yet
  ```
  Then for each pass:
  - create `<dest>/concepts/<slug>.md` pages for `[[wikilinks]]` that resolve to `NONE` and
    deserve their own page;
  - add missing cross-links between related concepts (discover them by `Glob
    "<dest>/concepts/*.md"` and reading titles / `concepts_mentioned`).
  Stop when no important concept is missing and no relevant `[[wikilink]]` is left dangling.

### 7. Synthesis page (standalone only)
When run standalone, write `explore_library/concepts/<query-slug>.md` that ties the concepts
together and **directly answers the original query** — narrating how the linked
concepts/papers bear on it, citing the `<dest>` pages, and ending with open questions / gaps.
**When invoked by `/curriculum`, skip this** — the curriculum's module docs are the synthesis.

## Wrap up
Report: `<dest>`, corpus size, papers read, the source/paper/concept pages created, the
synthesis page (if standalone), and anything deferred or left dangling (one line each).
Confirm **no** personal `sources/`/`papers/`/`concepts/` file was written. Then ask the user
to review and co-edit via `/edit <page>` until they're happy. **Do not reindex manually** —
the personal-base index never sees `<dest>`, and the standalone `explore_library/` index
(`--corpus explore`) auto-rebuilds lazily on the next query when its corpus changes (or run
`sh .claude/src/pyrun .claude/src/retrieve_cli.py --corpus explore --reindex` to pre-warm it).
