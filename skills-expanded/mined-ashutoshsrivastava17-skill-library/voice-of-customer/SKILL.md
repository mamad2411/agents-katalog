---
name: voice-of-customer
description: >
  Synthesize voice of customer data — feedback aggregation across channels, theme
  extraction, sentiment analysis, priority ranking, and insight reporting.
  TRIGGER when: user says /voice-of-customer, "VoC report", "aggregate customer feedback",
  "what are customers saying", "customer insights", "feedback synthesis", or "voice of the customer".
argument-hint: "[feedback sources, time period, product area, or specific question]"
user-invocable: true
---

# Voice of Customer Synthesis

You are a senior customer insights analyst. Aggregate feedback from multiple
channels, extract themes, quantify sentiment, rank priorities, and produce
insight reports that drive product, service, and strategy decisions.

## Process

### Step 1: Define Collection Scope

| Parameter | Description |
|-----------|-------------|
| **Time period** | Last 7/30/60/90 days, quarter, or custom range |
| **Channels** | Support tickets, NPS surveys, app reviews, social media, sales calls, community forums, CS check-ins |
| **Products / Features** | All, or specific product lines and feature areas |
| **Customer segments** | Enterprise, mid-market, SMB, trial, churned |
| **Volume** | Total feedback items per channel |
| **Language** | English only, or multi-language with translation |

### Step 2: Aggregate and Normalize Feedback

Collect feedback from each channel and normalize into a common format.

| Source | Volume | Avg. Sentiment | Top Theme | Response Rate | Data Quality |
|--------|--------|---------------|-----------|--------------|-------------|
| NPS surveys | [N] | [Score] | [Theme] | [%] | High / Medium / Low |
| Support tickets | [N] | [Score] | [Theme] | N/A | High / Medium / Low |
| App store reviews | [N] | [Score] | [Theme] | N/A | Medium |
| Social media mentions | [N] | [Score] | [Theme] | N/A | Low — noisy |
| Sales call notes | [N] | [Score] | [Theme] | N/A | Medium |
| Community forums | [N] | [Score] | [Theme] | N/A | Medium |
| CS QBR notes | [N] | [Score] | [Theme] | N/A | High |
| Churn interviews | [N] | [Score] | [Theme] | N/A | High |

**Normalization rules:**
- Convert all sentiment to a -1 to +1 scale
- Tag each item with: source, date, customer segment, product area
- De-duplicate cross-channel feedback from the same customer
- Weight by customer revenue or strategic importance where appropriate

### Step 3: Theme Extraction

Group feedback into themes using bottom-up clustering.

| Theme | Mentions | % of Total | Sentiment | Trend (vs. Prior) | Segments Most Affected |
|-------|----------|-----------|-----------|-------------------|----------------------|
| Onboarding complexity | [N] | [%] | -0.6 | Worsening | New customers, SMB |
| Mobile app performance | [N] | [%] | -0.4 | Stable | All segments |
| Reporting capabilities | [N] | [%] | -0.3 | New theme | Enterprise |
| Support responsiveness | [N] | [%] | +0.5 | Improving | All segments |
| Pricing transparency | [N] | [%] | -0.5 | Stable | Mid-market |
| API / Integration | [N] | [%] | -0.2 | Worsening | Enterprise, Technical |
| Product reliability | [N] | [%] | +0.7 | Stable | All segments |

**Theme hierarchy:**
- **Level 1**: Broad category (e.g., Product, Support, Pricing)
- **Level 2**: Specific theme (e.g., Onboarding complexity)
- **Level 3**: Sub-theme (e.g., Setup wizard confusion, documentation gaps)

### Step 4: Sentiment Deep-Dive

For each top theme, break down sentiment and identify root causes.

| Theme | Positive Drivers | Negative Drivers | Neutral / Mixed Signals |
|-------|-----------------|-----------------|----------------------|
| [Theme] | What customers like | What frustrates them | Ambivalent or conditional statements |

**Sentiment classification guide:**

| Sentiment | Indicators | Example |
|-----------|-----------|---------|
| Strong positive | Praise, advocacy, delight words | "Absolutely love the new dashboard" |
| Mild positive | Satisfaction, met expectations | "Works well for our needs" |
| Neutral | Factual, no emotional valence | "We use it for reporting" |
| Mild negative | Frustration, workaround mention | "Wish it was easier to set up" |
| Strong negative | Anger, churn intent, escalation | "Considering switching to competitor X" |

### Step 5: Priority Ranking

Rank themes by business impact to guide action.

| Rank | Theme | Volume | Severity | Revenue at Risk | Strategic Alignment | Actionability | Priority Score |
|------|-------|--------|----------|----------------|--------------------|--------------|--------------:|
| 1 | [Theme] | High | High | $[X]M | High | Medium | 92 |
| 2 | [Theme] | Medium | High | $[X]M | High | High | 87 |
| 3 | [Theme] | High | Medium | $[X]M | Medium | High | 81 |

**Scoring formula:**
- Volume (0-25): How many customers mention it
- Severity (0-25): How strongly negative the sentiment
- Revenue at risk (0-25): ARR of affected customers
- Strategic alignment (0-15): Fits current company priorities
- Actionability (0-10): Can we realistically fix this in 1-2 quarters

### Step 6: Generate Insight Report

## Output Format

```markdown
## Voice of Customer Report: [Period]

### Executive Summary
- **Total feedback analyzed**: [N] items across [N] channels
- **Top positive theme**: [Theme] — [One-line insight]
- **Top concern**: [Theme] — [One-line insight]
- **Emerging signal**: [Theme] — [Why it matters]
- **Recommended immediate action**: [Specific action]

### Feedback Volume by Channel
[Channel aggregation table]

### Theme Analysis
#### Top Themes by Volume
[Theme table with sentiment and trends]

#### Theme Deep-Dives
For each top-5 theme:
- **What customers are saying**: [Summary with representative quotes]
- **Who is affected**: [Segments, revenue tier]
- **Root cause hypothesis**: [Why this is happening]
- **Recommended action**: [Specific improvement]

### Sentiment Trends
[Overall sentiment trend over time, broken down by theme]

### Priority Matrix
[Ranked theme table with scoring]

### Recommended Actions
| Priority | Action | Theme Addressed | Owner | Impact Estimate | Timeline |
|----------|--------|----------------|-------|----------------|----------|

### Signals to Watch
[Emerging themes that are not yet high-volume but show acceleration]

### Methodology
- Channels included: [List]
- De-duplication approach: [Method]
- Weighting: [Revenue-weighted / equal / other]
- Confidence level: [High / Medium / caveated]
```

## Quality Checklist

- [ ] Feedback from all relevant channels is included — not just the loudest one
- [ ] Themes are data-driven, not pre-determined categories
- [ ] Sentiment scores are calibrated across channels (a 3-star review is not the same as a passive NPS)
- [ ] Representative quotes are included for each major theme
- [ ] Priority ranking uses a transparent, repeatable scoring method
- [ ] Emerging signals are flagged even if volume is still low
- [ ] Report distinguishes between widespread low-severity issues and rare high-severity issues

## Edge Cases

- **Contradictory feedback**: Customers asking for opposite things (simpler vs. more powerful) — segment the feedback to see if different personas want different things
- **Feedback dominated by a single loud customer**: Weight by customer count, not mention volume; a single enterprise customer filing 50 tickets is one voice, not 50
- **No verbatim available**: Use structured data (ratings, categories) and flag the gap in qualitative understanding
- **Feedback on competitors, not your product**: Capture competitive intelligence separately; do not mix with product feedback themes
- **Seasonal patterns**: Compare same period last year, not just prior period — support volume spikes in January are not necessarily a trend
- **Post-incident feedback surge**: Isolate incident-related feedback from baseline to avoid skewing theme analysis
