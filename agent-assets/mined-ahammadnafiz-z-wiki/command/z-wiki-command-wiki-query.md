---
description: Answer a question using only the compiled wiki; file the full answer and print a polished summary in the terminal.
argument-hint: "<question>"
when_to_use: Use when the user asks a question the wiki could plausibly answer from its compiled sources. Grep-first retrieval, then reads candidate pages, answers with wikilink citations, files the full answer under wiki/outputs/, then prints a scannable summary. Never invents facts — if coverage is insufficient, says so and lists missing sources. Also triggered by phrases like "query the wiki", "what does the wiki say about", "ask the vault".
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Wiki Query

Read `CLAUDE.md` for conventions. Follow the QUERY operation exactly as specified there.

## The question
$ARGUMENTS

## Retrieval strategy (grep-first, do NOT load `wiki/index.md`)

At any vault size, this is the designed sequence. Do **not** skip to
reading `wiki/index.md` — at 2000 sources it's 40K tokens of
context tax per query.

1. **Grep.** Run
   `python3 scripts/wiki_search.py "<question>"` (derive a terse
   keyword form of the question). Returns up to 10 ranked paths.
   - If ≥3 hits with score ≥1.0: treat as the candidate set.
   - If <3 hits or all scores <1.0: step 2.
2. **Tag shards.** If the question has an obvious topical angle,
   read `wiki/indexes/by-tag/<tag>.md` if present. Pull every page
   listed there into the candidate set.
3. **Type catalogs.** Read `wiki/<type>/_index.md` for the type the
   question most plausibly lives under (sources for factual lookups,
   concepts for definitional, entities for "who/what is X").
4. **Fallback: top-level index.** Only read `wiki/index.md` when 1–3
   all came up empty. At that point you are almost certainly going
   to print "No coverage."

If after all four steps the candidate set is empty, go to the "No
coverage" failure mode below.

## Reading and answering

- Read every candidate page (max ~10; drop the rest).
- Cite every non-obvious claim with a `[[wikilink]]` to a source
  summary or concept page. Bare assertions not traceable to a cited
  page are not allowed.
- If citation would require a page that does not exist in the
  candidate set, do not invent the link — surface the gap in
  "What I would add" and stop citing.
- Save the full answer to `wiki/outputs/{question-slug}.md` using
  `templates/output.md`.
- Set `last_seen: <today>` on the new output page AND on every page
  actually cited (not every page read — only cited).

## After filing

- Run `python3 scripts/build_meta.py --embed-if-enabled` — refreshes the sidecar (and embeddings if /wiki-enable-semantic was run) so
  the new output appears in the backlink graph.
- Run `python3 scripts/shard_index.py` — updates outputs `_index.md`.
- Append to `wiki/log.md`: `## [YYYY-MM-DD HH:MM] query | <slug>`.
- **Print the terminal block below.**

## Terminal output format

Exact shape, markdown (Claude Code renders it):

```markdown
---

### 🔍 `<the original question>`

**Short answer**
<2–4 sentences. Matches or summarises the short-answer section of the filed output. Plain prose — no bullets, no headers, no code blocks.>

**Sources cited** (<N>)
- `[[wikilink-1]]` — one-line purpose of this citation
- `[[wikilink-2]]` — one-line purpose
- ... (typically 3–10)

**Gaps** (<N>)
- What's missing to strengthen this answer — one line each
- (Omit the whole "Gaps" section if the filed output has no "What I would add" items)

**Filed**
📄 `wiki/outputs/<slug>.md`

---
```

Length target: ≤ 25 lines of terminal output.

## No-coverage failure mode

If retrieval steps 1–4 all return empty, or every candidate page is
tangential, do **not** file anything. Print:

```markdown
---

### 🔍 `<the original question>`

**No coverage.** The wiki has no source that speaks to this. To answer it, you would need to ingest one of:

- <concrete suggestion for a source type / URL / paper>
- <second suggestion>

Run `/wiki-add <url-or-path>` to add a source, or drop one into `raw/` manually and run `/wiki-ingest`.

---
```

No output file, no index update, no log entry. Zero writes.

## Reporting

The terminal block IS the report. No separate structured summary.
