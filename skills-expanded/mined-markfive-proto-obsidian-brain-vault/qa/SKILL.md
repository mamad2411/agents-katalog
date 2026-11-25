---
name: qa
description: "Ask complex questions against a compiled markdown wiki. The LLM searches relevant notes, synthesizes an answer, and files the result back into outputs/ as a linked markdown report. Use when the user asks 'what does my vault say about X', 'research Y using my notes', 'summarize everything I know about Z'. Part of the knowledge-base pack implementing Karpathy's raw→wiki→Q&A workflow."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: knowledge-base
---

# QA Pack — "Ask the vault anything"

`qa` is the **read layer** of the Karpathy-style KB. It treats your compiled wiki as an always-available context store, pulls the relevant slices, answers, and files the result back so your own explorations accumulate in the vault.

## Core principle

Every answer is a new note in `outputs/`. Never reply in chat-only. Reason: Karpathy's insight — "my own explorations and queries always 'add up' in the knowledge base." Chat-only answers evaporate.

## Directory output

```
outputs/
  answers/                # one file per QA session
    <YYYY-MM-DD>-<slug>.md
  reports/                # curated / multi-step research
  briefs/                 # exec summaries
```

## Commands

### /ask — Single-question research

When the user invokes `/ask <question>`:

1. **Extract entities & concepts** from the question. Use them as search seeds.
2. **Search the wiki** in this order (merge results, dedupe):
   - `obs search content "<entity>" --path compiled/ --json`
   - `obs search content "<entity>" --path raw/ --json` (deeper context)
   - `obs tags find <entity>` for tag-based hits.
   - `obs links backlinks "<concept-file>"` to follow the graph 1 hop.
3. **Rank** the top 10-20 notes by relevance (exact match > partial > tag match > backlink).
4. **Read** each note fully (concept pages preferred; raw as supporting).
5. **Write the answer** directly to `outputs/answers/<YYYY-MM-DD>-<slug>.md` with this structure:
   ```markdown
   ---
   title: <question restated as noun phrase>
   type: answer
   question: <original question>
   asked_at: <ISO date>
   sources_used: <N>
   tags: [output, answer, <domain-tags>]
   ---

   # <Question restated>

   ## TL;DR
   <3-5 bullet synthesis>

   ## Detailed answer
   <the real answer with inline [[wikilinks]] to every source>

   ## Evidence map
   | Claim | Sources |
   |---|---|
   | <claim 1> | [[source-A]], [[source-B]] |

   ## What my vault does NOT cover
   <explicit gaps — seeds for future /ingest runs>

   ## Confidence
   <High / Medium / Low, with one-line justification>

   ## Related notes
   - [[<concept>]] — why related
   - [[<concept-2>]] — why related
   ```
6. Link back: append a one-line backlink from each source concept page to the new answer under a `## Derived answers` section (optional but recommended).
7. **Report** the file path, TL;DR, and "read the full answer at [[<path>]]".

### /deep — Multi-step research dive

When the user invokes `/deep <topic>`:

1. Generate 5-10 sub-questions that would collectively cover the topic.
2. Run `/ask` on each sub-question, chaining answers as context for the next.
3. Merge into a single `outputs/reports/<topic>.md` with sections per sub-question.
4. At the end, write a "Synthesis" section that ties threads together.
5. Add a "Further questions" list. Offer to `/ingest` each one as a future research target.

### /compare — Compare 2+ concepts from the wiki

When the user invokes `/compare <A> <B> [<C> ...]`:

1. Load each concept's `compiled/concepts/<slug>.md`.
2. Pull supporting raw sources for each.
3. Build a comparison table: dimensions × concepts. Let the dimensions emerge from the material (don't hardcode).
4. Save to `outputs/reports/compare-<A>-vs-<B>.md`.

### /timeline — Build a timeline of events on a topic

When the user invokes `/timeline <topic>`:

1. Search sources; extract date-stamped events.
2. Normalize dates (approximate → quarterly buckets).
3. Build a markdown table or Mermaid `gantt` diagram.
4. Save to `outputs/reports/timeline-<topic>.md`.

### /what-do-I-think — Pull together your own notes on a topic

When the user invokes `/what-do-I-think <topic>`:

1. Restrict search to notes with tag `my-notes` OR frontmatter `author: me` OR inside a user-designated "journal" folder.
2. Synthesize ONLY the user's own writing — exclude external-source material.
3. Output `outputs/reports/my-take-<topic>.md` with a "Evolution over time" section if timestamps support it.

## Evidence discipline

Every factual claim in the answer must have an inline wikilink to its source. If a claim has no source, either:
- Mark it `(inferred)` and explain the inference, OR
- Remove it.

If the wiki is silent on the question, **say so explicitly**. Do not fill gaps from model priors without flagging: "Not in vault; pulled from general knowledge → consider `/ingest <url>` to harden this."

## Search fallback order

1. `obs search` against compiled/ (fastest, most curated).
2. `obs search` against raw/ (deeper, noisier).
3. `obs links path <A> <B>` for graph-based relevance.
4. Last resort: web search — and when used, `/ingest` the fetched source so future runs hit the vault first.

## When to widen context

If initial hit set is <3 notes or relevance is weak, offer to:
- Re-search with broader terms.
- Run `/ingest <url>` to add a specific source.
- Run `/deep` instead of `/ask`.

## Output hygiene

- Every output note gets `tags: [output, answer|report|brief, ...]` so `lint` and search can filter it.
- Outputs are never read back as sources by `compile` (avoid echo loops). The compile skill must ignore the `outputs/` directory.

## Related skills (same pack)

- `[[ingest]]` — feed new sources when the wiki is thin
- `[[compile]]` — must run before qa sees new raw material
- `[[lint]]` — checks that qa outputs cite sources
- `[[render]]` — convert qa answers to slides / briefs

## Attribution

Pack inspired by Andrej Karpathy's KB workflow, which notes that at ~100-article scale, LLMs can answer complex questions against a wiki without needing vector RAG — the auto-maintained index and summaries are enough.
