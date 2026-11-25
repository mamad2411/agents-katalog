---
name: lead-research-assistant
description: >-
  Researches and qualifies sales leads by defining an ideal customer profile,
  searching for matching companies, scoring fit, and generating personalized
  outreach strategies with decision-maker contacts. Use when asked to find leads,
  prospect companies, identify potential customers, do lead generation, build a
  pipeline, research target accounts, find outreach targets, or identify ICP matches.
---

# Lead Research Assistant

Research and qualify potential leads for a given product or service. Produce a scored, prioritized list of target companies with decision-maker contacts and personalized outreach strategies.

## Workflow

### 1. Understand the offering

- If inside a code repository, read the README and key source files to infer the product.
- Clarify: what problem does it solve, for whom, and what is the core value proposition?
- Confirm the user's target market constraints (industry, geography, company size, budget range).

### 2. Define the Ideal Customer Profile (ICP)

Produce a short ICP summary covering:

| Dimension | Detail |
|-----------|--------|
| Industry / sector | e.g., fintech, healthtech |
| Company size | employee count or revenue band |
| Geography | target regions |
| Pain points | problems the offering addresses |
| Tech signals | relevant stack, tools, or platforms |
| Budget indicators | funding stage, revenue tier |

**Checkpoint:** confirm the ICP with the user before researching.

### 3. Research and identify leads

Use web search to find companies matching the ICP. For each candidate:

- Verify the company is active (recent news, job postings, social presence).
- Look for need signals: relevant job listings, tech stack mentions, recent funding, expansion announcements.
- Identify the decision-maker role (e.g., VP Engineering, Head of Security) and locate their LinkedIn profile when possible.
- Cross-check at least two sources before including a lead.

**Checkpoint:** if fewer than half the requested leads pass verification, widen search criteria and inform the user.

### 4. Score and prioritize

Assign each lead a fit score (1-10) based on:

- ICP alignment (industry, size, geography)
- Strength of need signals
- Budget likelihood
- Competitive gap (no incumbent solution visible)
- Timing (recent trigger events)

Sort leads by score descending.

### 5. Produce the output

Use this template for each lead:

```markdown
## [Company Name]

**Website:** [URL]
**Score:** [X/10] - [one-line rationale]
**Industry:** [sector] | **Size:** [employees/revenue] | **Location:** [HQ]

**Why they fit:** [2-3 sentences citing specific evidence]

**Decision-maker:** [Title] - [Name if found] | [LinkedIn URL if available]

**Outreach angle:**
- Reference: [specific company event, pain point, or public statement]
- Value hook: [how the offering solves their specific problem]
- Opener: [one concrete conversation starter]
```

Prefix the list with a summary table:

```markdown
# Lead Research Results

| # | Company | Score | Industry | Decision-maker |
|---|---------|-------|----------|----------------|
| 1 | ...     | 9/10  | ...      | ...            |
```

### 6. Offer next steps

After presenting results:

- Offer to export as CSV for CRM import.
- Offer to draft personalized outreach emails for top-scored leads.
- Suggest deeper research on any lead the user flags.
