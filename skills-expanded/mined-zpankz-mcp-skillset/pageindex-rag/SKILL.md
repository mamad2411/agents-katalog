---
name: pageindex-rag
description: Use this skill whenever the user wants high-quality semantic retrieval, cross-textbook synthesis, reference verification, or authority-ranked question answering over the PageIndex corpus. Trigger on requests like "find which texts cover X", "compare sources", "retrieve semantically", "verify this claim from my textbooks", "build a reading list from the corpus", "cluster by topic", or any PageIndex question where naïve filename search would miss relevant material. This skill teaches a state-of-the-art hybrid retrieval workflow over the PageIndex catalog and live MCP extraction surface.
---


## Enforcement scripts

This skill includes programmatic enforcement of the catalog-first retrieval invariant:

- `scripts/retrieve.py` — CSV-based semantic retrieval with authority ranking
- `scripts/verify.py` — PageIndex MCP tool call plan generator
- `scripts/pipeline.py` — End-to-end: semantic query → catalog → rerank → verification plan

See `scripts/README.md` for full usage.
# PageIndex Semantic Retrieval Best Practices

Use this skill to answer corpus-grounded questions over the PageIndex library with high recall and high precision.

It is a **retrieval-and-verification** skill, not a raw indexing skill.

This skill is designed to be **standalone**. It ships with a bundled catalog snapshot under:

- `data/current/`

So it can be used remotely in Claude.ai without depending on another local skill installation.

If the user needs a fresher live crawl than the bundled snapshot, then refresh separately with:

- `pageindex-reference-index`

## What "best practice" means here

Use a hybrid workflow:

1. **catalog-first retrieval** for breadth
2. **authority-aware reranking** for trustworthiness
3. **work / section / topic clustering** for semantic coverage
4. **live PageIndex page extraction** for exact verification
5. **citation-rich synthesis** in the final answer

Do not jump straight to `get_page_content` across random PDFs.
Do not rely on filenames alone when the catalog already has `work_title`, `topic_category`, tags, and relations.

## Primary retrieval workflow

### 1. Check whether the catalog is current enough

Use the bundled snapshot in:

- `data/current/`

Inspect at least:

- `data/current/pageindex_summary.json`
- `data/current/pageindex_diff.md`
- `data/current/pageindex_enrichment.md`
- `data/current/pageindex_work_index.csv`
- `data/current/pageindex_topic_index.csv`
- `data/current/pageindex_verification_index.csv`

If the user's request depends on the newest live library state and the bundle is stale, note that limitation explicitly and, if available, refresh separately with `pageindex-reference-index`.

### 2. Generate candidates from the catalog

Prefer hybrid candidate generation:

- `topic`
- `topic_category`
- `specific_topic`
- `work_title`
- `work_section_title`
- `source_family`
- `document_type`
- `authority`
- `exam_domain`
- hierarchical tags

Remote-first use:

- `data/current/pageindex_work_index.csv`
- `data/current/pageindex_topic_index.csv`
- `data/current/pageindex_verification_index.csv`
- `data/current/pageindex_catalog.csv`

If you have an execution environment, you may also use bundled query helpers or SQL mirrors, but the skill should remain effective even without them.

### 3. Rerank by authority and coverage

Default ranking order:

1. `official` syllabi / examiner reports / guidelines
2. `textbook`
3. `journal`
4. `reference`
5. `notes` / community-style material

Then balance for breadth:

- prefer multiple `source_family` values over many hits from one work
- prefer section diversity when synthesizing a topic
- include both full-book anchors and chapter-level hits when useful

### 4. Verify with live PageIndex only after narrowing the set

Once you have the best candidate documents:

- use `get_document` to confirm readiness
- for docs >20 pages, use `get_document_structure` first
- then use `get_page_content` for tight ranges only

Always preserve exact document / page provenance in your notes.

### 5. Answer with explicit grounding

Your answer should distinguish:

- metadata-level retrieval
- live page-verified retrieval

When verified, cite:

- document name
- folder path
- page range
- why that source was chosen

## Retrieval patterns

### Pattern A — "Which texts cover X?"

1. search `topic`, `topic_category`, `specific_topic`, and FTS text
2. cluster by `source_family`
3. surface 5–10 best works
4. optionally verify the top 2–3

### Pattern B — "Compare what different sources say about X"

1. retrieve from at least 3 distinct `source_family` values
2. prioritize textbooks + official sources
3. verify representative passages live
4. synthesize agreements, disagreements, and level of specificity

### Pattern C — "Find the best source to answer X"

1. use `verification_index`
2. filter by likely `topic_category`
3. rank by `authority`, `work_title`, `work_section_title`
4. verify the best 1–3 sources live

### Pattern D — "Build a reading stack for X"

1. official syllabus / examiner reports first
2. core textbook chapters next
3. supplementary texts after
4. BJA / notes only as adjuncts

## Important heuristics

- Prefer `work_title` and `work_section_title` over bare filenames.
- Prefer `topic_category` for recall and `specific_topic` for precision.
- Use `material_kind` to separate full books from chapters, front matter, back matter, and problem sets.
- Use `source_family` to avoid overcounting multiple chapter hits from the same work.
- Use `exam_domain` to keep ANZCA / CICM filtering intentional.
- Treat `pageindex_discrepancies.md` as a warning surface, not a footnote.

## Rich semantic retrieval checklist

Before finalizing an answer, ask yourself:

- Did I retrieve from the catalog first?
- Did I include the highest-authority sources available?
- Did I avoid collapsing everything into one work?
- Did I verify exact pages when making strong claims?
- Did I cite folder path + page range?
- Did I mention uncertainty if the result is metadata-only?

## Recommended references

Read as needed:

- `references/retrieval-playbook.md`
- `references/query-recipes.md`
- `references/citation-template.md`
- `references/remote-usage.md`
- `data/current/README.md`

## Output contract

For retrieval tasks, usually return:

1. best candidate works
2. best candidate documents
3. verified page-backed evidence where available
4. a brief synthesis
5. suggested next retrieval moves if confidence is partial
