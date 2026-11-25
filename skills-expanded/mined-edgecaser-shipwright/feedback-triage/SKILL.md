---
name: feedback-triage
description: "Ingests raw customer feedback from multiple channels (support tickets, NPS responses, app store reviews, feature requests, sales call notes, social media) and produces a categorized, deduplicated, prioritized view of what customers are telling you. Turns noisy signal into actionable intelligence."
category: customer-intelligence
default_depth: standard
---

# Feedback Triage & Taxonomy

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Ingests raw customer feedback from multiple channels (support tickets, NPS responses, app store reviews, feature requests, sales call notes, social media) and produces a categorized, deduplicated, prioritized view of what customers are telling you. Turns noisy signal into actionable intelligence.

## When to Use

- Monthly or quarterly feedback synthesis across channels
- After a spike in support tickets or negative reviews
- Before prioritization or planning sessions to ground decisions in customer evidence
- Building a "voice of the customer" report for leadership
- Onboarding onto a new product area and need to understand the feedback landscape

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick read on a single channel or post-incident feedback spike | Ingest & Normalize, Deduplicate & Cluster (top 5 clusters only) |
| **Standard** | Monthly or quarterly multi-channel feedback synthesis | All sections |
| **Deep** | Annual voice-of-customer program or pre-strategy feedback audit | All sections + longitudinal trend analysis, segment-level breakdowns, competitive mention mapping |

**Omit rules:** At Light depth, skip Categorize by Type, Prioritize, and Produce the Feedback Report. Produce only a ranked cluster list with volume counts and representative quotes.

## Framework

### Step 1: Ingest & Normalize

Collect raw feedback and normalize it into a common format:

```markdown
## Feedback Register

| ID | Source | Date | Customer Segment | Verbatim | Sentiment | Topic (auto) |
|---|---|---|---|---|---|---|
| F001 | Support ticket | [date] | Enterprise | "[raw quote]" | Negative | [initial tag] |
| F002 | NPS (score: 3) | [date] | SMB | "[raw quote]" | Negative | [initial tag] |
| F003 | App Store | [date] | Unknown | "[raw quote]" | Positive | [initial tag] |
| F004 | Feature request | [date] | Mid-market | "[raw quote]" | Neutral | [initial tag] |
| F005 | Sales call note | [date] | Enterprise | "[raw quote]" | Negative | [initial tag] |
```

**Normalization rules:**
- Preserve verbatim quotes, don't paraphrase at this stage
- Tag sentiment: Positive / Neutral / Negative / Mixed
- Tag source channel
- Tag customer segment if identifiable (plan tier, company size, persona)
- Assign a preliminary topic tag (will be refined in clustering)

### Step 2: Deduplicate & Cluster

Group related feedback into themes using bottom-up clustering:

```markdown
## Feedback Clusters

### Cluster: [Theme Name, e.g., "Export functionality is unreliable"]
**Volume:** [N] pieces of feedback across [N] channels
**Segments affected:** [Enterprise, SMB, etc.]
**Sentiment distribution:** [N] negative, [N] neutral, [N] positive
**Trend:** [Increasing / Stable / Decreasing over past [timeframe]]

**Representative quotes:**
- "[Quote 1]", [Source, Segment, Date]
- "[Quote 2]", [Source, Segment, Date]
- "[Quote 3]", [Source, Segment, Date]

**Variations within this cluster:**
- Sub-theme A: [description] ([N] mentions)
- Sub-theme B: [description] ([N] mentions)
```

**Clustering rules:**
- Name clusters as assertions, not labels: "Users can't reliably export to PDF" not "Export"
- A cluster needs 3+ independent pieces of feedback to be meaningful
- Track cross-channel confirmation (same theme from support AND reviews = stronger signal)
- Separate "feature requests" from "bug reports" from "usability complaints", they need different responses

### Step 3: Categorize by Type

```markdown
## Feedback Taxonomy

### Bugs & Reliability Issues
| Cluster | Volume | Severity | Segments | Trend |
|---|---|---|---|---|
| [Cluster name] | [N] | Critical/High/Med/Low | [segments] | [↑/→/↓] |

### Usability & Experience Issues
| Cluster | Volume | Severity | Segments | Trend |
|---|---|---|---|---|

### Feature Requests & Enhancements
| Cluster | Volume | Revenue Signal | Segments | Trend |
|---|---|---|---|---|

### Praise & Positive Signal
| Cluster | Volume | Segments | What They Love |
|---|---|---|---|

### Churn & Competitive Mentions
| Cluster | Volume | Competitor Named | Reason for Leaving |
|---|---|---|---|
```

### Step 4: Prioritize

Score each cluster for action priority:

```markdown
## Priority Scoring

| Cluster | Volume | Revenue Impact | Segment Value | Trend | Solvability | Priority Score |
|---|---|---|---|---|---|---|
| [Cluster] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [weighted avg] |

**Weighting:**
- Volume (20%): How many customers mention this
- Revenue Impact (25%): Does this affect paying/high-value customers?
- Segment Value (20%): Are affected customers in our ICP?
- Trend (15%): Is this getting worse?
- Solvability (20%): Can we realistically address this?
```

### Step 5: Produce the Feedback Report

```markdown
## Voice of the Customer Report, [Period]

### Executive Summary
- **Total feedback processed:** [N] items from [N] channels
- **Top 3 themes:** [Theme 1], [Theme 2], [Theme 3]
- **Emerging signal:** [New theme that appeared this period]
- **Positive signal:** [What customers love most]

### Priority Action Items
1. [Highest priority cluster], Recommended action: [specific]
2. [Second priority], Recommended action: [specific]
3. [Third priority], Recommended action: [specific]

### Detailed Cluster Analysis
[Full cluster details as structured above]

### Methodology
- Sources: [list of channels analyzed]
- Period: [date range]
- Total items: [N]
- Deduplication rate: [X]% (N raw → N unique)
```

## Minimum Evidence Bar

**Required inputs:** Raw feedback for a defined period, with source/channel identifiers. Use the available sample; identify which channels and customer segments it represents.

**Acceptable evidence:** Support tickets, NPS verbatims, app store reviews, feature request logs, sales call notes, social media mentions, community forum posts, churned-customer exit surveys.

**Insufficient evidence:** With no raw feedback, request it. Small or single-channel samples can support scoped triage; label limits and avoid cross-channel or population claims. Retain isolated high-severity reports separately instead of manufacturing clusters.

**Hypotheses vs. findings:**
- **Findings:** Cluster volumes, sentiment distributions, and trend directions must be grounded in the raw data.
- **Hypotheses:** Inferred underlying needs behind feature requests (e.g., "50 dark mode requests = eye strain during evening use") must be labeled "Hypothesis, validate with user interviews."

## Output Format

Produce a Feedback Intelligence Report with:
1. **Executive Summary**, top-line themes and recommended actions
2. **Feedback Register**, normalized raw data
3. **Cluster Analysis**, themed groupings with volume, sentiment, and trends
4. **Taxonomy**, categorized by type (bugs, UX, feature requests, praise, churn)
5. **Priority Matrix**, scored and ranked for action

**Shipwright Signature (required closing):**
6. **Decision Frame**, top clusters with response options (fix, build, investigate, or defer) and trade-offs between high-volume and high-revenue-impact items, confidence level with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, clusters with single-channel signal only, segments with no feedback representation, underlying needs inferred but not validated
8. **Pass/Fail Readiness**, PASS if every cluster links to independent source items, counts are deduplicated, sample limits are explicit, and priorities are justified (priority scoring optional at Light depth); FAIL if evidence is missing or the report generalizes beyond the sample. Singleton incidents may be reported as such.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Counting votes, not understanding needs**, 50 people asking for "dark mode" might really mean "the UI is hard on my eyes during evening use"
- **Recency bias**, This week's angry ticket is not automatically the highest priority; look at trends
- **Ignoring positive feedback**, What customers love tells you what NOT to break
- **Single-channel blindness**, Support tickets skew toward bugs; NPS skews toward overall sentiment; you need multiple channels
- **No deduplication**, One customer submitting 10 tickets about the same issue is 1 signal, not 10

## Weak vs. Strong Output

**Weak:**
> "Cluster: Export issues (15 mentions)"

A label with a count. No assertion about what the problem actually is, no segment, no trend.

**Strong:**
> "Cluster: PDF exports drop formatting and images for documents over 10 pages (15 mentions, 9 support tickets, 4 app store reviews, 2 NPS comments). Segments: Enterprise (11), Mid-Market (4). Trend: increasing, 3 mentions in Q1, 12 in Q2. Cross-channel confirmed."

Names the specific failure, quantifies across channels, identifies affected segments, and flags the trend direction.
