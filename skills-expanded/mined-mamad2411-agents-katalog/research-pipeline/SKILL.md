---
name: research-pipeline
description: >
  Orchestrates the full research pipeline from topic to published article.
  Everything runs in Cowork — no external tools required. The natural starting point
  is a topic, not a file. Coordinates literature-discovery, citation-verifier,
  research-synthesizer, and content-writer skills. Manages the unified Supabase schema.
  Use this skill whenever the user says "run the research pipeline," "process my research,"
  "full research workflow," "start a new research project," "I want to research," "set up a
  new library," "research pipeline status," "what's the state of my research," or any
  request to orchestrate multiple research steps together. Also trigger when the user asks
  about the Supabase schema or scheduled research tasks.
version: 0.2.0
---

# Research Pipeline Orchestrator

Coordinates the end-to-end research workflow entirely within Cowork.

## The Natural Flow

Most research starts with a question, not a file:

```
"I want to research STIG automation"
    │
    ▼
[1. Discover Literature]       ← search academic + industry + government sources
    │                             creates the library, finds initial sources
    ▼
[2. Verify Citations]          ← 4-layer verification on what was found
    │
    ▼
[3. Synthesize]                ← thematic map + writing perspective
    │
    ▼
[4. Write]                     ← Sorkin DOB narrative + MoxyWolf voice + voice injection
    │                             produces publication-ready article with bibliography
    ▼
[Google Drive + Supabase]      ← persisted, published, done
```

BibTeX import is available as an *alternative* entry point if the user already
has a collected bibliography. But discovery-first is the default path.

## Workflow: Starting from a Topic

### Step 1: Discover Literature

When a user says "I want to research [topic]":

Trigger the literature-discovery skill. It will:
1. Ask sharpening questions if the topic is vague
2. Create a new library in Supabase
3. Search across academic sources (OpenAlex, Semantic Scholar, arXiv) AND
   non-academic sources (NIST docs, industry blogs, whitepapers, vendor docs)
4. Present candidates grouped by source type
5. Ingest the user's selections into the library

This single step gets the user from zero to a populated research library.

### Step 2: Verify Citations

Trigger the citation-verifier skill. It will:
1. Check all DOIs against CrossRef/DataCite
2. Verify arXiv IDs
3. Run semantic matching on abstracts
4. Score each citation's relevance to the library topic

Academic sources with DOIs will mostly pass. Non-academic sources (blogs,
whitepapers) will be marked as unverified but that's expected — they don't
have DOIs. The relevance scoring still applies to everything.

### Step 3: Expand (Optional)

After seeing the initial results, the user might want more:
- "Find more papers on [specific sub-topic]"
- "The gap in [area] needs filling"
- "Find the foundational papers on this"

Run discovery again with refined queries. The skill deduplicates against
what's already in the library automatically.

### Step 4: Synthesize

Trigger the research-synthesizer skill. It will:
1. Page through all citations and build a theme inventory
2. Generate a Mermaid thematic tree diagram
3. Walk through the perspective architect (writing angle, audience, sub-themes)
4. Persist everything to Google Drive and Supabase

### Step 5: Evaluate before it goes out

Trigger the research-evaluator skill on the finished draft. It extracts every load-bearing claim, resolves each to the source it cites, and grades whether the claim actually follows from that source — reporting a grounding rate, the overstated claims, source coverage, and what the run cost.

This is not a repeat of Step 2. Step 2 proved the sources exist; this proves the sentences citing them are supported. A citation can resolve perfectly at CrossRef and still be attached to a claim it doesn't carry, and that is the failure that survives everything else in this pipeline. Run it before publication, and re-run it after a revision to see whether the grounding rate actually moved.

The evaluator reports and stops. It never edits the article — the human decides what to soften, re-source, or cut.

### Choosing the report shape

Not every research request wants a 3,000-word article. Establish the shape before Step 4 writes anything, because it changes what Steps 3 and 4 produce:

| Shape | What it is | When |
|---|---|---|
| **Outline** | The structure and the argument, no prose | The user wants to react to the shape before it's written |
| **Resource list** | Annotated sources, grouped, no synthesis | The deliverable is the bibliography itself |
| **Brief** | 800-1,200 words, one argument, tight sourcing | A decision needs support, not a literature review |
| **Article** | Full DOB narrative + voice injection + bibliography | The default — publication-bound |

Ask once if it isn't obvious from the request. An article written when a brief was wanted is expensive to cut back down, and a brief written when an article was wanted has already thrown away the material.

## Workflow: Starting from a BibTeX File

If the user uploads a .bib file or says "import my BibTeX":

Trigger the import-bibtex skill. After import, the user can:
- "Verify my citations" → citation-verifier
- "Find more papers" → literature-discovery (to expand beyond what they had)
- "Synthesize my research" → research-synthesizer

## Workflow: Existing Library Maintenance

For libraries that already exist, any step runs independently:

- "I want to research [topic]" → discovery (creates new library)
- "Find more papers" → discovery (expands existing library)
- "Import my BibTeX" → import-bibtex
- "Verify my citations" → citation-verifier
- "Synthesize my research" → research-synthesizer
- "Check my article" / "is this grounded?" → research-evaluator
- "What's the state of my research?" → library stats

### Library Status

When asked about status, run `get_library_stats(library_id)` and present:

```
Research Library: [Name]
══════════════════════

Sources:  [total] total
  ├─ Academic papers:       [count]
  ├─ Government/standards:  [count]
  ├─ Industry/practitioner: [count]
  └─ BibTeX imports:        [count]

Verification:
  ├─ Verified:    [count] ([%])
  ├─ Failed:      [count] ([%])
  └─ Unverified:  [count] ([%])

With abstracts: [count] ([%])
Thematic Maps:  [count]
Perspectives:   [count]
Open Gaps:      [count]

Build cost:     $[x] across [n] discovery runs ([n] deep) · [n]m total
Last eval:      [grounding %] grounded, [n] claims, [date]

Recommended Actions:
  [context-dependent suggestions]
```

Build cost and last-eval come from the library metadata written by deep-research runs and by `/research-eval`. Show them as `not recorded` rather than omitting the lines — a library with no recorded cost and no eval is a library nobody can budget to rebuild or defend, and that absence is worth seeing.

## Supabase Schema

The unified schema lives at `references/supabase-migration.sql`. Key tables:

| Table | Purpose |
|-------|---------|
| `research_libraries` | Named research projects |
| `citations` | All sources with verification status + embeddings |
| `thematic_maps` | Mermaid diagrams + theme inventories |
| `research_perspectives` | Writing angle / audience / sub-themes |
| `discovery_runs` | Literature search execution log |
| `research_gaps` | Identified coverage gaps |

Key functions:
- `read_library_citations()` — paginated reader
- `match_citations()` — semantic search across citations
- `get_library_stats()` — summary statistics

## Scheduled Tasks

### Weekly Literature Scan

```
/schedule — Weekly Literature Discovery (Sundays 8 AM)
For each active library, search for sources published in the last 7 days.
Stage candidates for user review. Never auto-ingest.
```

### Weekly Citation Verification

```
/schedule — Weekly Citation Verification (Sundays 9 AM)
For libraries with unverified citations, run the 4-layer verification.
Generate a summary report.
```

## Error Recovery

All operations are idempotent — safe to re-run. If a step fails:
- Check `discovery_runs` table for failed runs
- Check `verification_log` on individual citations for layer-specific failures
- If Supabase is unreachable, fall back to local file processing

## Composio fallback — apps with no native MCP

If a step in this skill needs an app or service that has no native Cowork MCP connector — for example Notion, Linear, Jira, HubSpot, Salesforce, Stripe, Airtable, or Calendly — and the Composio connector is installed, reach the app through Composio's Tool Router rather than giving up or asking the user to do it by hand. Discover the tool with `COMPOSIO_SEARCH_TOOLS`, authenticate with `COMPOSIO_MANAGE_CONNECTIONS` if needed, then execute. See the `composio` plugin's `composio-tools` skill for the full pattern.

Native MCP connectors still come first — this is a fallback for reach, not a replacement for the native paths this skill already uses.
