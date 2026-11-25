---
name: "product-intelligence"
description: "Automated competitor feature tracking, user feedback clustering, and feature validation for the Product department. Monitors competitor launches, aggregates user feedback signals, clusters by theme, and feeds the product self-improvement loop. Use when tracking competitor features, analyzing user feedback, validating feature hypotheses, or running the product UAOP pipeline."
risk: low
tags: [product, research, competitive-intel, feedback]
created: 2026-03-23
updated: 2026-03-23
---

# Product Intelligence — Product Department Intelligence Engine

Automated competitor feature tracking and user feedback synthesis. UAOP Stage 1 + Stage 5 for Product.

## When to use

- Tracking competitor product launches and feature changes
- Synthesizing user feedback from multiple channels
- Validating feature hypotheses before building
- Quarterly product roadmap planning
- Sprint prioritization — "what should we build next?"

## Pipeline

### Step 1: Competitor Feature Scan
- Monitor competitor changelogs, release notes, Product Hunt launches
- Track feature additions/removals across LangChain, CrewAI, AutoGen
- Identify feature gaps (they have it, we don't) and advantages (we have it, they don't)

### Step 2: User Feedback Aggregation
- Collect signals: support tickets, app reviews, community posts, NPS comments, sales call notes
- Cluster by theme using frequency + sentiment analysis
- Rank by impact: revenue-tied requests > nice-to-haves

### Step 3: Feature Validation
- For each proposed feature: hypothesis, success metric, estimated effort (RICE score)
- Cross-reference against competitor data — are we filling a gap or innovating?
- Check ICP alignment — does the target user actually want this?

### Step 4: Product Intel Report
- Top feature requests (by cluster frequency)
- Competitor moves (new features, pricing changes, positioning shifts)
- Recommended priorities (RICE-ranked)
- Experiment proposals (hypothesis + metric + sample size)

### Step 5: Self-Improvement Loop
- Track feature adoption rates post-launch
- Measure experiment win rates
- Reinforce: features with high adoption → invest more; low adoption → investigate why
- Feed outcomes into next cycle's prioritization

## Cadence
```
WEEKLY:   Competitor changelog scan + feedback triage
MONTHLY:  Full product intel report + RICE re-ranking
QUARTERLY: Roadmap review informed by cumulative intelligence
```

## Agents
| Agent | Role |
|-------|------|
| pm-agent (L0) | Owns product strategy, approves priorities |
| feedback-synthesizer (L4) | Clusters and themes user feedback |
| trend-researcher (L4) | Tracks competitor movements |
| experiment-tracker (L4) | Monitors experiment results |
| requirements-analyst (L4) | Validates feature specs |
