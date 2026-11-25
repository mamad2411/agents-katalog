---
name: llm-wiki-query
description: Query an llm-wiki (single-wiki or monorepo) and synthesize answers from existing pages, with optional file-back to compound knowledge. Use when the user says "query the wiki", "ask the wiki about X", "what does the wiki say about Y", "synthesize from wiki", "search wiki for Z", "file this answer back", or asks a factual/synthesis/comparison question that should be answered from wiki contents rather than fresh research.
---

# llm-wiki-query

A cold-start playbook for querying an llm-wiki and synthesizing answers from its existing pages. This skill covers everything from session startup through answer synthesis, gap detection, and optional file-back. The Query operation is NOT a chatbot — it is a disciplined workflow that answers from what the wiki actually contains, flags what it cannot answer, and optionally compounds knowledge by filing good answers back as new wiki pages. Read this file in full before taking any action.

---

## When to Use This Skill

- User asks "what does the wiki say about X?" or "query the wiki for Y"
- User asks a factual question that should be answered from stored knowledge, not fresh research
- User asks an exploratory or synthesis question spanning multiple wiki topics ("how do A, B, and C relate?")
- User asks for a comparison between two or more topics covered in the wiki
- User says "synthesize what the wiki knows about X" or "file this answer back"
- User wants to understand coverage gaps: "does the wiki cover X?" or "what's missing on Y?"

---

## When NOT to Use This Skill

- The question is clearly outside the wiki's domain — use `llm-wiki-ingest` to bring in new sources first, then query
- The task is a coding, debugging, or implementation task — use the appropriate coding agent
- The user wants fresh research from the internet — use a research agent, not the wiki
- The wiki does not exist yet or has no `wiki/index.md` — initialize it with the ingest skill first
- The user just wants a quick clarification about something they said in this same conversation — no wiki read needed

---

## Prerequisites

Before querying, the following must exist:

- A wiki repo with a `CLAUDE.md` (or `WIKI.md`) schema file
- A `wiki/` directory with `index.md` — the one-line catalog of all pages (this is the primary search surface)
- A `wiki/log.md` for recording query events

If `wiki/index.md` does not exist or is empty, the index-first search cannot run. Ask the user to ingest sources first.

---

## Mode Detection: Single-Wiki vs Monorepo

Before doing anything else, determine which mode you are in.

**Check for monorepo:** Does a file called `index.md` exist at the repo root (not inside `wiki/`)? AND do multiple subdirectories each contain their own `WIKI.md`? If both are true, you are in a monorepo.

**Single-wiki:** A single `CLAUDE.md` at the root governs the entire repo. There is one `wiki/` and no master router.

| Indicator | Monorepo | Single-wiki |
|-----------|----------|-------------|
| Root-level `index.md` exists | Yes | No |
| Multiple subdirs each have `WIKI.md` | Yes | No |
| Single `CLAUDE.md` at root | Shared methodology file | Entire schema |
| `wiki/` location | Inside each domain subdir | At repo root |

---

## Session Startup Sequence

**CRITICAL: Do not skip this.** Every session starts cold. Read the index before answering.

### Monorepo startup

1. Read `CLAUDE.md` (shared methodology, conventions, rules)
2. Read `index.md` at repo root (master domain router — which domain owns which topic)
3. Identify which domain(s) are relevant to the query using the routing rules in `index.md`
4. Read `<domain>/wiki/index.md` for each relevant domain (the one-line page catalog)
5. Now proceed with the query workflow

Skipping step 2 means you may search the wrong domain's index and miss pages that answer the question.

### Single-wiki startup

1. Read `CLAUDE.md` (the full schema: page types, directory structure, conventions)
2. Read `wiki/index.md` to understand what pages exist and their one-line descriptions
3. Now proceed with the query workflow

---

## Query Workflow

### Step 1: Parse Intent

Before searching, classify the query into one of four intent types. The intent determines how aggressively to search and whether file-back is likely warranted.

| Intent | Description | File-back likely? |
|--------|-------------|-------------------|
| **Factual lookup** | Specific fact about a single topic ("what is the fee rate for Lido?") | No — factual answers are already in the source page |
| **Synthesis** | Drawing together themes from 3+ pages to build understanding ("how does the wiki describe caching trade-offs across different architectures?") | Yes — if the synthesis is novel and substantive |
| **Comparison** | Side-by-side analysis of two or more topics already in the wiki | Yes — comparison pages compound knowledge |
| **Exploration** | Open-ended, "tell me everything about X" | Yes — if the answer spans multiple pages and would be useful to retrieve again |

If the intent is ambiguous, default to treating it as a synthesis query.

### Step 2: Index-First Search

Read `wiki/index.md` and scan the one-line descriptions for entries relevant to the query. This is the primary search mechanism — no embeddings needed at small/medium wiki scale (Karpathy principle: index-first is sufficient up to ~500 pages).

**How to scan the index:**

1. Read the full `wiki/index.md`
2. Identify every entry whose one-line description is plausibly relevant to the query
3. List the candidate pages with their paths
4. If the index has sections (Source Summaries, Concepts, Techniques, etc.), scan each section systematically

**Index search is exhaustive, not selective.** Do not stop at the first relevant entry. Scan the whole index before deciding which pages to read in full.

**When the index is unhelpful:** If `wiki/index.md` has one-line descriptions that are too generic to match the query (e.g., "Concept about caching"), scan the wiki directories directly with a glob to find pages by filename. Filename search is the fallback when index descriptions are poor.

**Genuine gap vs. description quality problem:** If you scanned the full index and found no relevant entries, ask yourself: are the descriptions specific and accurate, or are they vague? If the descriptions are reasonably specific and still nothing matches, treat the absence as a genuine coverage gap — do not proceed to glob scan. Only fall back to glob scan when index descriptions appear too generic to be reliable. Glob-scanning a well-described index that simply has no relevant entries wastes effort and may produce spurious matches.

### Step 3: Read Relevant Pages

For each candidate page identified in Step 2:

1. Read the page in full
2. Check the page's `related` frontmatter for additional pages to follow
3. Follow wikilinks in the page body if they point to topics relevant to the query
4. Add any newly discovered relevant pages to your reading list
5. Stop expanding when new pages add no new relevant information (typically after 2-3 expansion hops)

**Read depth guidance:**

| Query intent | Read depth |
|---|---|
| Factual lookup | 1-3 pages — stop when the fact is found |
| Synthesis | Up to 8 pages — follow `related` links one hop |
| Comparison | All pages for each subject being compared |
| Exploration | Up to 10 pages — follow `related` two hops max |

**Never read a page twice.** Keep a working list of pages already read in this session.

### Step 4: Synthesize Answer

Compose the answer from the content you read. Every claim in the answer must be traceable to a specific wiki page.

**Inline citation format:**

- For claims from wiki pages: `[[page-name]]`
- For claims where you want to cite the ultimate raw source: `(raw:path/to/source.md)`
- Use both forms in the same answer when needed: "Lido charges a 10% fee `[[lido-protocol]]` (raw:protocols/raw/lido-whitepaper.md)"

**Synthesis rules:**

- Do not add information from general knowledge. If the wiki does not cover it, mark the gap (see Step 5).
- Do not paraphrase away from what the pages actually say. Quote or closely paraphrase with citation.
- Resolve apparent contradictions by citing both versions and flagging: "Note: [[page-a]] says X while [[page-b]] says Y — see [[page-a]] for context."
- If multiple pages say the same thing, cite the most authoritative one (usually the protocol or concept page, not the source summary).

**Answer structure:**

For factual lookups: one paragraph with inline citations.

For synthesis/comparison/exploration:
1. Direct answer (1-2 sentences)
2. Supporting detail (with citations, organized by theme or by subject for comparisons)
3. Connections noticed (wikilinks to related pages the user may want to read next)
4. Wiki gaps detected (if any — see Step 5)

### Step 5: Gap Detection

After synthesizing, assess whether the answer is complete relative to the question.

**A gap exists when:**
- The question clearly implies a subtopic the wiki does not cover
- A page the answer depends on does not exist (broken wikilink target)
- The wiki has only surface-level coverage (a one-paragraph mention where depth is needed)
- Key context for the answer exists in a domain the wiki has not ingested

**How to phrase gap detection:**

```
Wiki gaps detected:
- [topic X] is not covered in the wiki. Suggested ingest: <source type or file description>
- [topic Y] is mentioned in [[page-name]] but not developed. A dedicated page would improve coverage.
- [topic Z] appears to be a dependency for this answer but no page exists.
```

**Gap detection is mandatory for synthesis and exploration queries.** For factual lookups, only flag a gap if the question cannot be answered at all.

**Never fabricate an answer to fill a gap.** If the wiki cannot answer the question, say so explicitly and list suggested ingests.

### Step 6: File-Back Decision

After synthesizing the answer, decide whether to file it back as a new wiki page.

**File-back criteria (ALL must be true):**

1. The answer is a synthesis, comparison, or exploration (not a simple factual lookup)
2. The answer drew from 3 or more distinct wiki pages
3. The answer would be useful to retrieve again in the future without re-reading all those pages
4. No existing wiki page already covers this synthesis

**File-back is optional for factual lookups** — if the answer is already in one page, filing back would be redundant duplication.

**In single-source mode (one wiki):** If running interactively (user is present in the session), ask the user for confirmation before filing back. The user may not want the wiki to grow syntheses it did not explicitly commission. If running as a subagent or in a non-interactive context (e.g., a test, CI pipeline, or automated task), proceed with file-back if the task description authorizes it, and flag the file-back action in your report so the caller can review it.

**In a session where the user said "file this answer back":** Proceed with file-back without further confirmation.

**If file-back is appropriate:** spawn a file-back agent (see [agent-prompts.md](agent-prompts.md)) or proceed to write the page directly.

---

## File-Back Rules

### When to file

File back when the answer:
- Draws from 3+ distinct wiki pages (synthesis rule)
- Is a comparison between two or more distinct topics
- Would serve as a useful entry point for future queries on this theme
- Represents an insight or connection that is not explicit in any single existing page

Do NOT file back when:
- The answer is a verbatim quote from one page
- The answer is a simple factual lookup that belongs in the source page
- A page with the same synthesis already exists (check index before filing)
- The answer contains significant unresolved gaps (file after those gaps are filled via ingest)

### Where to file

**Single-wiki mode:**

| Answer type | Directory |
|-------------|-----------|
| Synthesis (drawing from concepts, techniques, protocols) | `wiki/syntheses/` |
| Comparison (two or more subjects side-by-side) | `wiki/comparisons/` |
| Exploration (open-ended topic overview) | `wiki/syntheses/` |

**Monorepo mode:**

| Scope | Answer type | Directory |
|-------|-------------|-----------|
| Single-domain synthesis (all source pages from one domain) | Synthesis / Exploration | `<domain>/wiki/syntheses/` |
| Single-domain synthesis (all source pages from one domain) | Comparison | `<domain>/wiki/comparisons/` |
| Cross-domain synthesis (source pages from ≥2 domains) | Synthesis / Exploration | `cross-domain/wiki/syntheses/` |
| Cross-domain synthesis (source pages from ≥2 domains) | Comparison | `cross-domain/wiki/comparisons/` |

For cross-domain file-back: if `cross-domain/wiki/syntheses/` or `cross-domain/wiki/comparisons/` does not exist, create it before writing the page. Cite source pages using the `wiki:<domain>/<slug>` prefix (e.g., `wiki:system-design/lru-eviction`) instead of `raw:` paths, so the cross-domain origin is unambiguous.

### Frontmatter requirements

Every filed-back page MUST have:

```yaml
---
type: synthesis | comparison
llm_generated: true
query_origin: "<original question verbatim>"
confidence: high | medium | low
sources:
  - wiki:<domain>/wiki/concepts/page-name.md
  - wiki:<domain>/wiki/techniques/another-page.md
  - raw:path/to/original/source.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - synthesis
  - <topic-tags>
related:
  - [[source-page-1]]
  - [[source-page-2]]
---
```

**`llm_generated: true` is non-negotiable.** It marks the page as LLM-composed, not human-authored. Future readers and ingest agents must know the provenance.

**`confidence` levels:**

- `high` — all claims are directly supported by multiple wiki pages; no gaps
- `medium` — most claims are supported; minor gaps exist or some inference was required
- `low` — significant gaps exist; the answer is partially speculative; should be revisited after more ingests

---

## Page Conventions for Filed-Back Pages

### File naming

Kebab-case. Descriptive. No spaces. Based on the question, not on the date or session.

Good names:
- `caching-tradeoffs-synthesis.md`
- `lido-vs-rocketpool-comparison.md`
- `ethereum-staking-overview.md`

Bad names:
- `query-2026-04-16.md` (date-based)
- `synthesis-1.md` (opaque)
- `answer.md` (too generic)

### Slug collision rules

Before writing, check `wiki/index.md` for an existing page with the same base name.

If a collision exists:
1. Read the existing page. If it covers the same synthesis, update it instead of creating a new one.
2. If it covers something adjacent but distinct, add a distinguishing suffix: `-synthesis`, `-comparison`, `-overview`, or a topic qualifier.
3. Never create two pages with the same base filename in different subdirectories.

### Page structure

1. One-paragraph abstract (what question this page answers, what it draws from)
2. Key findings (bullet list — the most important claims, with citations)
3. Main body (organized by theme or by comparison dimensions)
4. Connections (wikilinks to the source pages with one-sentence context notes)
5. Sources section

### Sources section format

Every filed-back page must end with:

```markdown
## Sources

### Wiki pages synthesized
- `wiki:<domain>/wiki/concepts/page-a.md`
- `wiki:<domain>/wiki/techniques/page-b.md`

### Original sources (via wiki pages)
- `raw:path/to/original-source.md`
```

**Single-wiki repos (no domain subdirectory):** Omit the domain segment. Use `wiki:wiki/<dir>/page-a.md` directly:

```markdown
## Sources

### Wiki pages synthesized
- `wiki:wiki/concepts/page-a.md`
- `wiki:wiki/techniques/page-b.md`

### Original sources (via wiki pages)
- `raw:path/to/original-source.md`
```

Use `wiki:` prefix for pages within the wiki. Use `raw:` prefix for the original ingested files that the wiki pages were derived from. Both are useful: `wiki:` for navigating the wiki graph, `raw:` for tracing claims all the way back to primary sources.

---

## Citation Format

### Inline citations in answer text

| What you're citing | Format | Example |
|---|---|---|
| A wiki page | `[[page-name]]` | "LRU eviction is described in `[[lru-eviction]]`" |
| A raw source file | `(raw:path/to/file.md)` | "According to `(raw:system-design/raw/caching-guide.md)`" |
| Both wiki page and raw source | `[[page-name]] (raw:path)` | "`[[lru-eviction]]` (raw:system-design/raw/caching-guide.md)" |

### Rules

- Never cite a page you did not read in this session. Only cite pages you actually read.
- Never invent a page name. If you are not sure of the exact filename, check `wiki/index.md`.
- If a claim cannot be cited to any wiki page, either mark it `[UNVERIFIED]` or omit it.
- Do not cite the same page more than once per paragraph — consolidate references.

---

## Gap Detection and Suggested Ingests

When the wiki cannot answer part of the question, produce a structured gap report at the end of the answer.

**Standard phrasing:**

```
## Wiki gaps detected

The following topics were needed to fully answer this question but are not covered in the wiki:

1. **[Topic name]** — [one sentence on why it matters for this query]
   Suggested ingest: [description of what to find and ingest, e.g., "the official Lido documentation on node operator fees"]

2. **[Topic name]** — [why it matters]
   Suggested ingest: [what source would fill this gap]
```

**Rules:**

- Only flag a gap when the missing information was genuinely needed for the answer
- Do not flag gaps for tangentially related topics the user did not ask about
- Do not fabricate a partial answer and mark it as a gap at the same time — either answer or flag the gap, do not do both
- A gap flagged here is a first-class ingest suggestion. The user can act on it with `llm-wiki-ingest`.

---

## Log Entry Format

Every query must be logged. The log is append-only — never edit existing entries.

```markdown
## [YYYY-MM-DD] query | <original question>
Pages read: [[page-1]], [[page-2]], [[page-3]]
Answer filed: [[filed-back-page-name]]
Answer filed: no (factual lookup only)
Answer filed: no (wiki coverage gap — could not answer)
Gaps flagged: [topic-a], [topic-b]
Gaps flagged: none
Notes: One sentence on anything notable about this query.
```

Use exactly one of the three `Answer filed:` lines:
- `[[filed-back-page-name]]` — a synthesis was written and filed
- `no (factual lookup only)` — query was answered inline from one page; no file-back needed
- `no (wiki coverage gap — could not answer)` — the wiki had no relevant coverage; answer was not possible

Use exactly one of the two `Gaps flagged:` lines. Do not leave multiple alternatives in the log.

**For gap-only queries (zero pages read):** When the gap is detected at index scan time and no pages were read, write:
```markdown
Pages read: (none — gap detected at index scan stage)
```

**Date awareness (CRITICAL):** Use today's actual date in the log entry header. Do not copy a date from an example in this skill or from an existing log entry.

**Sourcing the current date:** Obtain today's date using one of these methods, in priority order:
1. If a system reminder or task description explicitly states today's date, use that value.
2. If the `{{TODAY}}` placeholder was filled in by the orchestrator when spawning you, use that value.
3. Otherwise, run `date +%Y-%m-%d` via the Bash tool to get the current date from the system.

Never guess or infer the date from context clues in the wiki. Always use one of the three methods above.

---

## Critical Non-Negotiables

1. **Index-first, always.** Never read individual wiki pages before scanning `wiki/index.md`. The index is the search surface. Reading pages without searching the index first means you may miss the most relevant pages.

2. **No fabricated citations.** Never cite a page you did not read. Never invent a page name or path. If you cannot cite it, mark it `[UNVERIFIED]` or omit the claim.

3. **Never answer outside wiki scope.** If the wiki does not contain the answer, say so explicitly and flag the gap. Do not fill the gap with general knowledge.

4. **No silent overwrite of existing pages.** If a filed-back page would overwrite an existing synthesis, read the existing page first. Either update it or give the new page a distinct name.

5. **File-back requires user confirmation in single-source mode (interactive sessions).** Do not write new wiki pages without user approval unless the user has already said "file this back" in the current session, or you are running as a non-interactive subagent whose task description authorizes file-back. In the latter case, flag the file-back action in your report.

6. **Log every query.** Even factual lookups that file nothing back must appear in `wiki/log.md`. The log is how the user tracks what the wiki has been asked.

7. **Confidence must be accurate.** Do not mark a synthesis `confidence: high` if it has gaps. Overconfident syntheses erode trust in the wiki.

8. **`llm_generated: true` is mandatory on all filed-back pages.** This is the provenance marker that distinguishes human-authored pages from LLM synthesized pages. Never omit it.

---

## Orchestrator vs Subagent Roles

When running this skill in Claude Code:

**Orchestrator (the main agent, with user context):**
- Reads the schema and index (Steps 1-2 of startup)
- Parses the intent (Step 1 of query workflow)
- Decides whether to spawn a search-synthesis agent or answer inline
- Presents the answer and gap report to the user
- Gets user confirmation for file-back (single-source mode)
- Spawns a file-back agent if confirmation is given

**Search-synthesis subagent (spawned for complex queries):**
- Receives: query, wiki root path, list of candidate pages from orchestrator's index scan
- Does: reads candidate pages, expands via `related` links, synthesizes answer with citations, produces gap report and file-back recommendation
- Returns: answer text, list of pages read, gap report, file-back recommendation with draft frontmatter

**File-back subagent (spawned when user confirms file-back):**
- Receives: answer draft, query, wiki root path, target directory, today's date
- Does: writes the page, updates `wiki/index.md`, appends `wiki/log.md`
- Returns: page path, index entry added, log entry appended

For simple factual lookups (1-2 pages), the orchestrator can answer inline without spawning subagents. For synthesis/comparison/exploration queries (3+ pages), spawn a search-synthesis agent to keep the orchestrator context lean.

See [agent-prompts.md](agent-prompts.md) for ready-to-use agent templates.

---

## Example: End-to-End Query Walkthrough

**User question:** "What does the wiki say about caching eviction strategies and when to prefer LRU vs LFU?"

**Step 1 — Parse intent:** Comparison query. Will likely span 2-4 pages. File-back possible if 3+ pages are drawn from.

**Step 2 — Index search:** Scan `wiki/index.md`. Found candidates:
- `wiki/concepts/lru-eviction.md` — "LRU cache eviction: least-recently-used algorithm and time complexity"
- `wiki/concepts/lfu-eviction.md` — "LFU cache eviction: frequency-based strategy and counter management"
- `wiki/techniques/cache-sizing.md` — "Guidelines for cache size and eviction policy selection"
- `wiki/source-summaries/caching-deep-dive.md` — "Synthesis of three caching articles covering distributed patterns"

**Step 3 — Read pages:** Read all four. `cache-sizing.md` links to `[[cache-warming]]` — follow it. Now 5 pages read.

**Step 4 — Synthesize:**
> LRU (Least Recently Used) eviction removes the item accessed longest ago. It performs well when access patterns have temporal locality — recently-used items are likely to be used again [[lru-eviction]]. LFU (Least Frequently Used) eviction removes the item accessed least often, which is preferable when access patterns are stable over time and some items are permanently "hot" [[lfu-eviction]].
>
> The wiki recommends LRU for general-purpose caching and LFU for recommendation or ranking workloads where item popularity is stable [[cache-sizing]]. Both strategies have O(1) implementations using hash maps with doubly-linked lists (LRU) or min-heaps (LFU) [[lru-eviction]] [[lfu-eviction]].

**Step 5 — Gap detection:**
> Wiki gaps detected:
> 1. **ARC (Adaptive Replacement Cache)** — mentioned briefly in [[caching-deep-dive]] as superior to both LRU and LFU in mixed workloads, but no dedicated page exists. Suggested ingest: the ARC paper by Megiddo and Modha.

**Step 6 — File-back decision:** 5 pages read, synthesis is a comparison, would be useful to retrieve again. Recommend file-back to `wiki/comparisons/lru-vs-lfu-comparison.md`. Ask user for confirmation.

**User confirms.** Spawn file-back agent. Page written. Index updated. Log appended:
```markdown
## [YYYY-MM-DD] query | What does the wiki say about caching eviction strategies and when to prefer LRU vs LFU?
Pages read: [[lru-eviction]], [[lfu-eviction]], [[cache-sizing]], [[caching-deep-dive]], [[cache-warming]]
Answer filed: [[lru-vs-lfu-comparison]]
Gaps flagged: ARC (Adaptive Replacement Cache)
Notes: ARC is an ingest opportunity; caching-deep-dive mentions it without a dedicated page.
```

---

## Reference: When to Branch

- **[agent-prompts.md](agent-prompts.md)** — use when spawning a search-synthesis agent or file-back agent
- **[ISSUES.md](ISSUES.md)** — read before trusting this skill; tracks known limitations
- **[TEST.md](TEST.md)** — run when modifying this skill; 3 validation scenarios covering factual lookup, multi-page synthesis, and gap detection
