---
name: signal-scan
description: Product signal scanner -- identifies market opportunities by analyzing pain points, demand, spend, sentiment, competitive landscape, and audience signals across Reddit, social media, course marketplaces, and other sources. Use when scanning a domain for product opportunities, running a market analysis, or identifying what to build and sell next.
license: MIT
metadata:
  context: fork
  openclaw:
    emoji: "\U0001F4E1"
---

# Signal Scan

Systematically scan a domain for product opportunities by collecting, normalizing, and scoring signals across 7 canonical types. Produces a structured JSON scan and a human-readable markdown summary with ranked opportunities and concrete ship candidates.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## When to Use

- Scanning a new domain for product opportunities
- Running market analysis before building something
- Identifying what to build and sell next
- Validating a product idea against real market signals
- Comparing opportunity strength across multiple domains

## Trigger Phrases

- "Scan [domain] for product signals"
- "What should I build in [domain]?"
- "Run a signal scan on [domain]"
- "Market analysis for [domain]"
- "/signal-scan [domain]"

---

## Prerequisites

Before starting, establish three things with the user:

1. **Domain** -- What space to scan (e.g., "DevOps education", "cybersecurity careers", "AI writing tools")
2. **Operator edge** -- What makes the user uniquely qualified (skills, audience, credentials, experience)
3. **Constraints** -- Time-to-ship target, price range preferences, format preferences, distribution channels available

If the user provides only a domain, ask about edge and constraints before proceeding. If they provide all three, proceed directly.

---

## Workflow

```
Domain + Edge + Constraints (from user)
    |
Phase 1: Domain Definition
    |
Phase 2: Signal Collection (web search -- real data required)
    |
Phase 3: Signal Normalization (structured format per type)
    |
Phase 4: Opportunity Scoring (weighted scoring matrix)
    |
Phase 5: Offer Generation (concrete ship candidates)
    |
Phase 6: Meta-Signal Synthesis (overarching thesis)
    |
Output: JSON scan + Markdown summary -> hunter/docs/
```

---

## Phase 1: Domain Definition

Define the scan parameters explicitly before collecting any data.

**Produce a scan header:**
- Domain name and boundaries (what is in scope, what is adjacent but excluded)
- Operator edge profile (1-3 sentences on unique qualification)
- Constraints (ship time target, price range, format preferences)
- Relevant subreddits, communities, and platforms to search
- Key competitors to analyze

Present this to the user for confirmation before proceeding. Scope adjustments here save hours of wasted collection.

---

## Phase 2: Signal Collection

**This phase requires extensive web search. Use real data. Do not hallucinate signals.**

For each of the 7 signal types (see [references/signal-taxonomy.md](references/signal-taxonomy.md) for full definitions), systematically search the following sources:

### Search Targets

| Source | What to Look For | Signal Types |
|--------|------------------|-------------|
| Reddit (relevant subreddits) | Pain language, "I wish..." posts, complaints, recommendations | PAIN, DEMAND, SENTIMENT |
| Udemy / Skillshare / Coursera | Bestsellers, ratings, student counts, price points | SPEND, DEMAND |
| Gumroad / AppSumo | Trending products, revenue evidence, pricing | SPEND, COMPETITIVE |
| X/Twitter | Viral threads, engagement patterns, complaints, requests | PAIN, DEMAND, AUDIENCE |
| Google Trends / search data | Search volume, trend direction, related queries | DEMAND |
| Stack Overflow / forums | Workarounds, duct-tape solutions, repeated questions | BEHAVIOR, PAIN |
| Job postings | Hiring patterns, skill demand, tool requirements | BEHAVIOR, DEMAND |
| Review sites (G2, Capterra, TrustPilot) | Satisfaction scores, switching intent, feature complaints | SENTIMENT, COMPETITIVE |
| Competitor websites | Pricing, features, positioning, recent launches/shutdowns | COMPETITIVE |
| Discord / Slack communities | Direct requests, topic resonance, engagement patterns | AUDIENCE, PAIN |

### Collection Rules

- Collect at least 3-5 raw signals per type (or explicitly note why a type has fewer)
- Every signal must have real evidence: an actual quote, a specific number, a URL, or a concrete observation
- "People generally feel..." is not evidence. "User u/devops_mike on r/devops wrote 'I spent 3 hours trying to...' (47 upvotes)" is evidence
- Search multiple subreddits and platforms per signal type -- do not rely on a single source
- Note the date/recency of evidence when possible

---

## Phase 3: Signal Normalization

Convert every raw signal into the structured format defined by its type. Each signal type has a specific schema (see [references/signal-taxonomy.md](references/signal-taxonomy.md) for field definitions).

**Normalization rules:**

- Intensity/score ratings (1-10) must be justified by the evidence, not assigned by vibes
- Provide the justification reasoning alongside the score
- Enum fields (recurrence, volume, trend, effort_level, valence, type, impact, strength) must use the exact values from the taxonomy
- Evidence fields must contain specific quotes, numbers, or observations -- not summaries
- Source fields must identify the specific platform, subreddit, or URL

---

## Phase 4: Opportunity Scoring

Cluster related signals into opportunity areas. Score each opportunity using 6 dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| pain_intensity | 2x | How much does this hurt? (from PAIN signals) |
| spend_evidence | 2x | Are people already paying? (from SPEND signals) |
| edge_match | 1x | Does this match the operator's skills? (from operator edge) |
| time_to_ship | 1x | Can this ship in 1 day? 1 week? (format/complexity assessment) |
| competition_gap | 1x | How bad are existing solutions? (from COMPETITIVE + SENTIMENT signals) |
| audience_fit | 1x | Can the operator reach these people? (from AUDIENCE signals) |

**Overall score** = weighted average: `(pain*2 + spend*2 + edge + time + gap + audience) / 8`

### Scoring Discipline

Each score must be justified. For every dimension, write one sentence explaining the rating. Example:

> pain_intensity: 8 -- "Three separate Reddit threads with 100+ upvotes describe spending 4+ hours on this task, with emotional language ('nightmare', 'insane', 'pulling my hair out')"

Do not score any dimension without citing specific signals from the collection phase.

---

## Phase 5: Offer Generation

For each opportunity scoring 6 or above, generate concrete ship candidates.

**Per candidate, define:**
- **Product**: Specific name and description
- **Format**: PDF, Notion template, video, video series, course, tool, SaaS, consultation, community, or other
- **Price point**: Derived from SPEND data (what people already pay for similar things)
- **Ship time**: Realistic estimate (1 day, 3 days, 1 week, etc.)
- **Distribution**: Where and how to sell it (the specific channel and strategy)
- **Why it works**: Connect back to specific signals -- which pain points it solves, which demand it meets, which spend patterns it matches

### Ship Candidate Rules

- Generate at least 3 candidates per top opportunity
- At least one candidate per opportunity must be shippable in 1-3 days
- Price points must be grounded in SPEND data, not aspirational
- Distribution recommendations must be specific ("post in r/devops with a value-first thread linking to Gumroad" not "social media marketing")
- Landing page copy hooks should use actual PAIN language from the collection phase

---

## Phase 6: Meta-Signal Synthesis

Step back from individual signals and identify the overarching pattern. Answer:

- What structural failure or market shift creates these opportunities?
- Why do these opportunities exist *now* and not two years ago?
- What connects the individual pain points, demand signals, and competitive gaps into a coherent thesis?
- If you could only tell someone one sentence about this domain, what would it be?

The meta-signal is not a summary of individual signals. It is the insight that ties them together into a thesis. It should explain *why* the market looks the way it does, not just *what* the market looks like.

---

## Output

The scan produces two files, saved to the Obsidian vault:

**Vault path:** `${VAULT}/Admin/Product-Discovery/Signal-Scans/`

### 1. JSON Scan: `{vault}/Admin/Product-Discovery/Signal-Scans/signal-scan-[domain-slug]-[date].json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Must validate against that schema.

### 2. Markdown Summary: `{vault}/Admin/Product-Discovery/Signal-Scans/{domain-slug}-{YYYY-MM-DD}.md`

Human-readable report with the following sections:

```markdown
# Signal Scan: [Domain]

**Date**: [date]
**Operator Edge**: [edge summary]

## Executive Summary
[2-3 sentences: meta-signal + top opportunity + recommended first ship]

## Signal Highlights
[Top 3-5 most compelling signals across all types, with evidence]

## Opportunity Ranking

| Rank | Opportunity | Score | Pain | Spend | Edge | Speed | Gap | Audience |
|------|------------|-------|------|-------|------|-------|-----|----------|
| 1 | [name] | [score] | [n] | [n] | [n] | [n] | [n] | [n] |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Top Opportunities (Detail)

### 1. [Opportunity Name] (Score: X/10)
**Thesis**: [why this exists]

**Key signals**:
- [signal + evidence]
- [signal + evidence]

**Ship candidates**:
| Product | Format | Price | Ship Time | Distribution |
|---------|--------|-------|-----------|-------------|
| [name] | [format] | [price] | [time] | [channel] |

### 2. [Next opportunity...]

## Recommended First Ship
**Product**: [name]
**From opportunity**: [which one]
**Rationale**: [why first -- speed, validation, revenue, audience-building]

## Signal Inventory
[Count per type, with notes on any gaps]

## Raw Signal Log
[Full signal details organized by type, for reference]
```

---

## Resources

### references/

- `output-schema.json` -- JSON Schema for the structured scan output. Load when producing the JSON file to validate against.
- `signal-taxonomy.md` -- Detailed definitions for all 7 signal types including fields, sources, measurement criteria, and examples. Load at the start of every scan.

---

## Quality Checklist

Run this checklist before delivering the scan:

- [ ] All 7 signal types have at least 2 entries each (or explicit note explaining the gap)
- [ ] Every signal has real evidence (quotes, numbers, URLs) -- no hypotheticals or "people generally feel..."
- [ ] Opportunity scores have justified breakdowns with per-dimension reasoning, not just vibes
- [ ] At least 3 ship candidates per opportunity scoring 6+
- [ ] At least one ship candidate per top opportunity is shippable in 1-3 days
- [ ] Meta-signal synthesizes across signal types, not just summarizes them
- [ ] JSON output validates against `references/output-schema.json`
- [ ] Markdown summary includes the ranked opportunity table
- [ ] Price points are grounded in SPEND evidence
- [ ] Distribution recommendations are specific and actionable
- [ ] Landing page copy hooks use actual PAIN language from the scan
- [ ] Both JSON and markdown files are saved to vault `Admin/Product-Discovery/Signal-Scans/`
- [ ] Pipeline kanban updated: add card to "Signal Scanned" column (see _conventions.md Pipeline Kanban Contract)
