---
name: kos-query
description: Use this skill when the user wants to ask a question, search, or retrieve information from their existing Kodex OS Layer 1 LLM Wiki. Triggers include "ask kos", "what does my wiki say about X", "find notes on Y", "search my wiki", "what's open on Z", or any retrieval-style question that should be answered from the user's own captured knowledge rather than general world knowledge. The skill searches across all six wiki directories (sources, books including the _archived/ subfolder, entities, concepts, synthesis, questions), follows wikilinks, and synthesizes an answer with citations to specific wiki pages. Refuses to fabricate when the wiki doesn't contain the answer. Do not use this skill to add new content (use kos-ingest) or to validate wiki structure (use kos-lint).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# KOS — Query

Answer questions by searching and synthesizing knowledge from the wiki.

## Before You Begin: Read the Contract

**Always read `<vault-root>/SCHEMA.md` first.** It defines the directory structure, page format, and operation rules. The user may have customized it. If anything in this skill conflicts with SCHEMA.md, **SCHEMA.md wins**.

If `SCHEMA.md` does not exist at the vault root, stop and tell the user the vault is not initialized. Suggest they run `/kos`.

---

## The Most Important Rule

**Answer ONLY from the wiki. Do not fabricate.**

If the wiki does not contain the information needed to answer the user's question, say so explicitly. Do not fall back on training data. Do not infer beyond what's in the pages. Do not paraphrase plausible-sounding answers from general knowledge.

When the wiki is silent on a topic, the correct response is something like:

> "Your wiki doesn't have information on this. The closest pages I found were [[page-1]] and [[page-2]], but neither addresses your question directly. Want me to web-search for it instead, or would you like to ingest a source on this topic first?"

This is the load-bearing rule of `/kos-query`. Violating it makes the wiki useless — the user can't tell which answers came from their own captured knowledge versus the LLM's general knowledge.

---

## Classify the Query

Before searching, identify what kind of query this is. Different types need different search strategies:

- **Factual lookup** — "What does my wiki say about X?" → search by topic, read pages on X
- **Time-scoped** — "What was I working on in March?" → filter by date in book/source frontmatter
- **Status-scoped** — "What questions are still open?" → filter `wiki/questions/` by `status: open`
- **Comparison** — "How do X and Y differ in my notes?" → read both topics, synthesize differences
- **Exploration** — "What have I been thinking about?" → broader scan, narrative answer
- **Source-tracing** — "Where did I read about X?" → return source pages with context

If the query type is ambiguous, ask the user before searching.

---

## Search Strategy

### 1. Start with the index

Read `wiki/index.md`. Scan all section headers for entries that match the query:

- `## Books` (active books)
- `## Archived Books` (completed books, by envelope number)
- `## Sources`
- `## Entities`
- `## Concepts`
- `## Synthesis`
- `## Questions (open)`

The index is the cheapest source of structured signal in the wiki. For time-scoped or "where is this book now" queries, the `## Archived Books` section is often where the answer lives.

### 2. Use qmd if available

If `qmd` is installed (`command -v qmd` returns a path), use it for retrieval — especially in wikis larger than ~100 pages where index-scanning becomes inefficient:

```bash
qmd search "query terms" --path wiki/
```

### 3. If qmd is not available, fall back to grep

Find pages mentioning the query terms, ranked by mention frequency:

```bash
grep -rli "query terms" wiki/ | xargs -I{} sh -c 'echo "$(grep -ic "query terms" {}) {}"' | sort -rn
```

Read the top 5–10 most relevant pages.

### 4. Read identified pages

Read the wiki pages identified by index, qmd, or grep. Follow `[[wikilinks]]` **one hop** to pull in directly-related context. Do not follow links transitively — that explodes quickly in a well-linked wiki.

**Search bounds:**
- Start with up to 5 directly relevant pages
- If the question isn't answered, expand to up to 10 more
- Beyond ~20 pages, stop and ask the user whether to keep searching, narrow the question, or proceed with a partial answer

### 5. Apply directory-specific strategies

Match search behavior to the query type from classification:

| Query type | Primary directories | Filter on |
|------------|--------------------|-----------|
| Factual lookup | `entities/`, `concepts/`, `synthesis/`, `sources/` | topic match |
| Time-scoped | `books/` (incl. `_archived/`), `sources/` | `date-start`, `date-end`, `created` |
| Status-scoped (open questions) | `questions/` | `status: open` |
| Comparison | `entities/`, `concepts/` | both topics |
| Exploration | `synthesis/`, `index.md` | broad |
| Source-tracing | `sources/` | mention of topic |
| Archive lookup | `books/_archived/` | `envelope-number`, `archived-on` |

**Important: book pages live in two locations.** When searching `wiki/books/`, scan recursively to include `wiki/books/_archived/`:

```bash
# Find all book pages, active and archived
find wiki/books -type f -name '*.md'

# Search book content recursively
grep -rn "search terms" wiki/books/
```

For time-scoped queries ("what was I working on in March 2026?"), older time ranges are more likely to hit archived books than active ones. Don't filter `_archived/` out — that's where most historical answers live.

For archive-lookup queries ("what's in envelope 7?", "find my notes from the book I archived last year"), search `wiki/books/_archived/` filtered by `envelope-number` or `archived-on` in the frontmatter.

### 6. Last resort: read raw sources

Only if wiki pages don't contain the answer should you read files in `raw/`. Wiki summaries are designed to surface what's important; going to raw means the source page is incomplete (which is itself a finding worth noting).

If you find raw content that answers the question but isn't in the wiki, tell the user — they may want to re-ingest the source to capture what was missed.

---

## Synthesize the Answer

### Format

Match the answer format to the query type:

- **Factual lookup** → direct answer with citations
- **Time-scoped** → chronological list or narrative
- **Status-scoped** → bulleted list grouped by category
- **Comparison** → table or structured side-by-side
- **Exploration** → narrative connecting linked concepts
- **Source-tracing** → bulleted list of sources with one-line context

### Citations

Cite wiki pages using `[[wikilink]]` syntax with **kebab-case page names** (matching the actual filenames per SCHEMA.md Section 6.1). 

**Correct:**

> According to [[karpathy-llm-wiki]], the key insight was X. This relates to the broader pattern in [[zettelkasten]], which [[niklas-luhmann]] developed.

**Incorrect** (these break wikilinks lint will flag):

> According to [[Karpathy LLM Wiki]] or [[Source - Karpathy's Article]]...

Every factual claim should link to the wiki page it came from. Untraced claims are a smell — if you can't cite a page for it, ask yourself whether the claim came from training data instead of the wiki (see "The Most Important Rule" above).

### Preserve external URLs

If a cited source contains a bit.ly slug or external URL, include it in the citation when relevant:

> [[fl-vol-001-page-007]] notes this, with reference to [<F13LdN0t3>](https://bit.ly/F13LdN0t3).

### Cite archived books with their physical location

When citing a source from an archived book, optionally include the envelope number so the user knows where to find the physical book if needed:

> Your earliest notes on this topic are in [[fl-vol-001-page-007]] (archived in envelope 7), where you wrote that...

This is purely a convenience — wikilinks resolve the same way whether a book is active or archived. But for queries that lead to an archived source, the envelope number turns "I want to revisit my original handwritten notes" from a search problem into a single physical reach.

### Acknowledge gaps

If the wiki partially answers the question, say what's covered and what isn't:

> Your wiki has detailed notes on the historical context (see [[zettelkasten]]) but doesn't cover modern digital implementations. Want me to web-search for those, or treat this as a question to ingest?

---

## Offer to Save Valuable Answers

If the answer represents new analysis worth keeping — a non-trivial comparison, a synthesis across multiple sources, a connection the wiki didn't already make explicit — offer to save it:

> "This comparison synthesizes [[page-a]], [[page-b]], and [[page-c]] in a way the wiki doesn't capture yet. Want me to save it as a synthesis page?"

If the user agrees:

### 1. Create the synthesis page

Filename: kebab-case description (`note-taking-systems-compared.md`).

Frontmatter (matching SCHEMA.md Section 3.6):

```yaml
---
type: synthesis
sources: [[page-a]], [[page-b]], [[page-c]]
tags: [tag1, tag2]
created: 2026-05-01T14:32:00Z
updated: 2026-05-01T14:32:00Z
---
```

Body: the answer, with all wikilink citations preserved.

### 2. Update wiki/index.md

Add an entry under `## Synthesis` with the page name and a one-line description (under 120 characters). Update the "Last updated" timestamp at the top of index.md.

### 3. Cross-link from cited pages (optional, recommended)

Consider adding a wikilink to the new synthesis from the source/concept/entity pages it draws from. This prevents the synthesis from being orphaned (which lint would flag).

---

## Always Log the Query

Per SCHEMA.md Section 6.1 rule 3, every operation appends to `wiki/log.md` — including queries that don't save anything. Use SCHEMA.md Section 3.9's format:

```markdown
## 2026-05-01 14:32 — query

- **Operation:** query
- **Question:** "What note-taking systems have I researched?"
- **Pages read:** [[zettelkasten]], [[para-method]], [[karpathy-llm-wiki]] (3 pages)
- **Answered from wiki:** yes
- **Synthesis saved:** [[note-taking-systems-compared]]
- **Notes:** Wiki had partial coverage; gap noted on digital implementations.
```

Field guidance:
- **Question** — the user's actual question, quoted
- **Pages read** — wikilinks to pages consulted, with a count
- **Answered from wiki** — `yes`, `partial`, or `no` (so lint and future queries can see knowledge gaps)
- **Synthesis saved** — wikilink to the new synthesis page, or omit
- **Notes** — anything notable: gaps, contradictions, unresolved slugs encountered

---

## Conventions

- **Wiki first, raw last.** Only read raw sources if wiki summaries are insufficient.
- **Cite everything.** Untraced claims hide the line between captured knowledge and fabrication.
- **Don't fabricate.** Say "the wiki doesn't have this" when it doesn't.
- **One-hop wikilink traversal.** Follow links from the pages you read, but don't follow their links.
- **Always log the query**, even when nothing is saved.
- **Wikilinks are kebab-case** matching real filenames.
- **`raw/` is read-only.** Never write to it.

---

## Related Skills

- `/kos-ingest` — process new sources into wiki pages (use this when you find raw content the wiki missed)
- `/kos-lint` — health-check the wiki for issues
