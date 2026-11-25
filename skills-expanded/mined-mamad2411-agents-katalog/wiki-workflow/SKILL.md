---
name: wiki-workflow
description: Manage a persistent, LLM-maintained knowledge wiki for accumulated knowledge that compounds over time. Use this skill when the user has a domain where knowledge accumulates over weeks/months (research, business context, infrastructure knowledge, personal notes), or when they ask about "wiki", "knowledge base", "memory", or accumulated context. Complements the kit's other knowledge layers (data-sources, ADRs, specs) without replacing them.
---

# Wiki Workflow Skill

## What This Is

This skill orchestrates use of the `wiki-skills` plugin (kfchou/wiki-skills) which implements Karpathy's LLM Wiki pattern. It tells you WHEN to use the wiki, HOW it relates to the kit's other knowledge layers, and HOW to keep it healthy.

The wiki-skills plugin must be installed separately:
```
/plugin marketplace add kfchou/wiki-skills
/plugin install wiki-skills@kfchou/wiki-skills
```

This skill does NOT replace the plugin - it explains how to use it well in the context of solo development with this kit.

## The Knowledge Layers (use the right one)

The kit now has FOUR distinct knowledge layers. Each serves a different purpose. Mixing them up = chaos.

### Layer 1: `docs/specs/<feature>/`
**Per-feature briefs and PRDs.** Created by `interview` and `prd-writer` skills. Lifecycle: born when feature starts, frozen when feature ships. Good for: "what was this feature supposed to do?"

### Layer 2: `docs/architecture/`
**Decisions and designs.** ADRs, C4 diagrams, design docs. Created by `architecture` and `adr-writer` skills. Lifecycle: append-only. Good for: "why did we choose X over Y?"

### Layer 3: `docs/data-sources/<source>.md`
**One-shot data source reference.** Created by `data-source-research` skill. Investigate ONCE, save permanently. Good for: "what's the schema of orders table?", "what columns does the Stripe API return?".

### Layer 4: `wiki/` (THIS skill)
**Living knowledge base that compounds.** LLM-maintained, not feature-bound. Good for: domain knowledge, accumulated learnings, research, business context, infra topology, personal research.

## When to Use Which Layer

| Question | Layer |
|---|---|
| "What does FR-007 in the new dashboard say?" | specs |
| "Why did we pick Kafka over RabbitMQ?" | architecture (ADR) |
| "What columns does the orders table have?" | data-sources |
| "How does our pricing logic work across all our products?" | wiki |
| "What did we learn about ClickHouse partitioning over the last 6 months?" | wiki |
| "Who's the BI lead at <vendor>?" | wiki |
| "What's our team's convention for error wrapping in Go?" | wiki |
| "What protocols do we run for biohacking?" | wiki |

Rule of thumb:
- **Single fact, single moment** → data-sources / specs / ADR
- **Knowledge that grows over time** → wiki

## When to Bootstrap a Wiki

Trigger `/wiki-init` when:
1. User starts a long-term research/learning project (weeks+)
2. User wants to consolidate scattered notes into a structured base
3. User starts onboarding a new domain (new client, new tech, new business area)
4. User explicitly asks for a knowledge base, second brain, or "wiki"

Don't bootstrap a wiki for:
- A single feature (use specs instead)
- A one-time question (use search instead)
- Per-project documentation (use README + ADRs)

A user can have MULTIPLE wikis - one per long-running domain. E.g., for Anton: one for EKF software ecosystem, one for biohacking research, one for personal goals.

## The Five Wiki Operations

### `/wiki-init <domain>`
Bootstrap. Creates SCHEMA.md (conventions), wiki/index.md (catalog), wiki/log.md (chronological), wiki/overview.md (synthesis), wiki/pages/ (all pages), raw/ (immutable sources).

### `/wiki-ingest <source>`
Add a source. Source can be: a URL, a PDF, a transcript, a meeting note, a research paper, an article. The plugin will:
1. Read the source
2. Extract key takeaways
3. Discuss with you what to emphasize
4. Write a summary page
5. Update the index
6. Cross-link to existing pages (10-15 pages may be touched)
7. Append to log

### `/wiki-query <question>`
Ask the wiki. The plugin reads only relevant pages (via index), synthesizes answer with citations. Always offers to file the answer back as a new page - DO this for non-trivial answers, your explorations should compound.

### `/wiki-lint`
Health check. Find: contradictions, stale claims, orphan pages, missing concepts, broken links, gaps. Run every 5-10 ingests.

### `/wiki-update <claim>`
Revise pages when knowledge changes. Always shows diffs before writing.

## Critical Discipline

The wiki only works if you maintain hygiene:

### Source provenance
EVERY claim in a wiki page should trace to a raw source. The plugin does this with `[[citations]]`. Don't let the LLM write things from training data without flagging.

### Don't trust silent rewrites
When the LLM updates a page during ingest, READ THE DIFF. Use git for the wiki - every ingest is a commit, you can review and revert.

### Index is sacred
The wiki/index.md is how the LLM finds pages. If it gets stale or wrong, queries return wrong results. `/wiki-lint` checks this.

### Periodic /wiki-lint
Without this the wiki rots. Set a cadence: after every 5-10 ingests, OR weekly.

### git the wiki
The wiki is just markdown files. Treat as code: git commit, branch for big revisions, tag stable points.

## Anti-patterns to flag

- **Using wiki for things that change** (e.g., "current API rate limits") - those go in data-sources/, not wiki, because they need refresh policy
- **Using wiki for one-shot questions** - use search instead
- **Mixing multiple unrelated domains in one wiki** - separate them
- **Letting LLM ingest silently in background** - you should be in the loop for at least the first dozen sources to catch drift early
- **Treating wiki pages as ground truth** - they're LLM-summarized; for high-stakes decisions, go back to raw/

## Example workflows for typical EKF cases

### Domain: EKF software ecosystem knowledge
```
/wiki-init "EKF software platform"
# now ingest things over time:
/wiki-ingest <link to architecture meeting transcript>
/wiki-ingest <PSA project README>
/wiki-ingest <Kafka topology doc>
/wiki-ingest <CRM phase plan>
# weekly:
/wiki-query "What's the data flow from 1C:UT to MERIDIAN dashboard?"
# every 5-10 ingests:
/wiki-lint
```
After 2-3 months you have a compact, queryable knowledge base for the entire EKF software platform.

### Domain: biohacking research
```
/wiki-init "biohacking and supplements"
/wiki-ingest <article about creatine monohydrate>
/wiki-ingest <PubMed paper on tirzepatide>
/wiki-ingest <Peter Attia podcast transcript>
# the wiki accumulates evidence-based info, with citations
# query later:
/wiki-query "Best protocols for managing autoimmune thyroiditis based on what I've read?"
# answer is grounded in your sources, not training data
```

### Domain: production incidents library
```
/wiki-init "EKF production incidents"
# after each incident:
/wiki-ingest <incident postmortem>
# the wiki accumulates patterns:
/wiki-query "What are the top 3 root causes we've seen in Q1?"
```

## Recommendations

After helping a user with the wiki:
- If they have multiple unrelated topics in one wiki - suggest splitting
- If pages are getting too long - suggest extracting concepts to their own pages
- If queries return contradictions - run `/wiki-lint` and resolve
- If the wiki feels stale - it's been over 30 days since last ingest probably; suggest sweeping recent reading into it
- For long-lived wikis: suggest annual `/wiki-lint` with structural review

## Why this is better than claude-mem for token cost

- claude-mem injects a summary of past sessions into EVERY session start. Constant token cost.
- wiki-skills loads pages ONLY when relevant to current question. Pay-per-use cost.

For long-term knowledge accumulation, wiki wins on tokens AND on quality (because you control what gets remembered, instead of an automatic summarizer deciding).
