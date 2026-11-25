---
name: feedback-analysis
description: "Analyzes customer feedback data to identify themes, sentiment patterns, and actionable improvement priorities for product and service decisions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Feedback Analysis

## When to Use This Skill

Use this skill when you need to:
- Analyze a collection of customer feedback to find actionable patterns
- Identify recurring themes and sentiment trends across reviews, surveys, or support tickets
- Prioritize improvements based on feedback frequency and business impact
- Create a feedback summary report for decision-making

**DO NOT** use this skill for collecting feedback (use satisfaction-survey or nps-survey), responding to individual reviews, or building feedback collection systems. This is for analyzing existing feedback data.

---

## Core Principle

CUSTOMER FEEDBACK IS NOISY — THE VALUE IS NOT IN ANY SINGLE RESPONSE BUT IN THE PATTERNS ACROSS MANY. YOUR JOB IS TO FIND THE SIGNAL IN THE NOISE AND TURN IT INTO ACTION.

---

## Phase 1: Gather Data

Collect and organize the feedback before analysis.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Feedback source** | "Where is the feedback? (surveys, reviews, support tickets, social media, emails)" | Mixed sources |
| **Volume** | "Roughly how many pieces of feedback are we analyzing?" | 20-100 |
| **Time period** | "What time period does this feedback cover?" | Last 90 days |
| **Product/service** | "What product or service does this feedback relate to?" | No default |
| **Known issues** | "Are there any issues you already suspect will appear?" | No default |

### Data Organization

```
## Feedback Inventory

| Source | Count | Date Range | Format |
|--------|-------|-----------|--------|
| Survey responses | [#] | [Range] | Ratings + open text |
| Online reviews | [#] | [Range] | Star rating + text |
| Support tickets | [#] | [Range] | Text |
| Social mentions | [#] | [Range] | Text |
| Direct emails | [#] | [Range] | Text |
| **Total** | **[#]** | | |
```

**GATE: Confirm data sources and volume before starting analysis.**

---

## Phase 2: Analyze

Identify themes, sentiment, and patterns.

### Theme Identification

Group feedback into themes by tagging each piece:

```
## Theme Analysis

| Theme | Frequency | % of Total | Sentiment | Sample Quotes |
|-------|-----------|-----------|-----------|---------------|
| [Theme 1] | [#] mentions | [%] | Positive/Negative/Mixed | "[Quote]" |
| [Theme 2] | [#] mentions | [%] | Positive/Negative/Mixed | "[Quote]" |
| [Theme 3] | [#] mentions | [%] | Positive/Negative/Mixed | "[Quote]" |
```

### Sentiment Breakdown

```
## Overall Sentiment

| Sentiment | Count | % of Total |
|-----------|-------|-----------|
| Positive | [#] | [%] |
| Neutral | [#] | [%] |
| Negative | [#] | [%] |

**Net sentiment:** [Positive % - Negative %]
**Trend vs. prior period:** Improving / Stable / Declining
```

### Theme-Sentiment Matrix

Cross-reference themes with sentiment to find where problems and strengths cluster:

```
## Theme x Sentiment Matrix

| Theme | Positive | Neutral | Negative | Net |
|-------|----------|---------|----------|-----|
| Product quality | [#] | [#] | [#] | [+/-] |
| Customer support | [#] | [#] | [#] | [+/-] |
| Pricing/value | [#] | [#] | [#] | [+/-] |
| Ease of use | [#] | [#] | [#] | [+/-] |
```

**GATE: Present analysis for review before building recommendations.**

---

## Phase 3: Prioritize

Turn analysis into prioritized action items.

### Impact-Effort Matrix

Score each theme by business impact and effort to fix:

```
## Improvement Priority Matrix

| Theme | Frequency | Business Impact (1-5) | Effort to Fix (1-5) | Priority Score | Action |
|-------|-----------|---------------------|--------------------|--------------:|--------|
| [Theme] | [#] | [X] | [X] | [Impact x Freq / Effort] | Fix Now / Plan / Monitor |
```

### Action Plan

```
## Feedback-Driven Action Plan

### Fix Now (High impact, manageable effort)
1. **[Theme]:** [Specific action] — Owner: [Name] — Deadline: [Date]
2. **[Theme]:** [Specific action] — Owner: [Name] — Deadline: [Date]

### Plan for Next Quarter (High impact, high effort)
1. **[Theme]:** [Approach and timeline]

### Monitor (Low frequency, but watch for growth)
1. **[Theme]:** Review again in [timeframe]

### Celebrate (Positive themes to amplify)
1. **[Theme]:** Use in marketing, testimonials, and case studies
```

---

## Phase 4: Report

Deliver a clear feedback summary for stakeholders.

### Executive Summary Template

```
## Customer Feedback Analysis — [Period]

### Key Numbers
- **Total feedback analyzed:** [#]
- **Overall sentiment:** [X]% positive, [X]% negative
- **Top positive theme:** [Theme] ([#] mentions)
- **Top negative theme:** [Theme] ([#] mentions)

### Top 3 Findings
1. [Finding with data point]
2. [Finding with data point]
3. [Finding with data point]

### Recommended Actions
1. [Action + expected impact]
2. [Action + expected impact]
3. [Action + expected impact]

### Notable Quotes
- "[Powerful customer quote — positive]"
- "[Powerful customer quote — negative]"
```

### Close the Loop

After implementing changes, communicate back to customers:
- "You asked, we listened" email or post
- Reference specific feedback themes and what changed
- This builds trust and encourages future feedback

---

## Anti-Patterns

- **Cherry-picking feedback** — analyzing only positive or only negative responses skews the picture. Include everything.
- **Acting on one loud complaint** — one angry email is anecdotal. Three people saying the same thing is a pattern.
- **Analysis without action** — a report that sits in a folder changes nothing. Every analysis needs an action plan.
- **Ignoring positive feedback** — positive themes reveal your competitive advantage. Amplify them in marketing.
- **Analyzing without context** — 10 complaints about pricing after a price increase is expected, not alarming. Context matters.

---

## Recovery

- **Not enough feedback to find patterns:** Under 20 responses, treat each piece individually. Patterns emerge at 30+ responses.
- **All feedback is positive (seems too good):** Check for selection bias — are only happy customers responding? Add follow-up questions that invite constructive criticism.
- **Overwhelmed by volume:** Start with the most recent 30 days. Look for themes in the negative feedback first — that is where the highest-value insights live.
- **Feedback contradicts itself:** Segment by customer type. Power users and new users often have opposite feedback. Both are valid for their segment.
- **User does not know what to do with findings:** Start with the single highest-frequency negative theme. Fix that one thing. Then repeat.
