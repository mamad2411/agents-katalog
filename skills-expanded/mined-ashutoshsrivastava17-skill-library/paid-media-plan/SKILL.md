---
name: paid-media-plan
description: >
  Plan paid media campaigns — channel selection, budget allocation, targeting, creative requirements, bidding strategy, and benchmarks.
  TRIGGER when: user says /paid-media-plan, needs to plan advertising spend, or asks about PPC/paid social strategy.
argument-hint: "[relevant context]"
user-invocable: true
---

# Paid Media Plan
## Process
### Step 1: Define Campaign Objectives
| Objective | KPI | Channel Fit |
|-----------|-----|------------|
| Awareness | CPM, Reach | Display, Video, Social |
| Consideration | CPC, CTR | Search, Social, Native |
| Conversion | CPA, ROAS | Search, Retargeting, Shopping |
| Retention | LTV, Repeat rate | Email, Social retargeting |
### Step 2: Select Channels
| Channel | Strengths | Best For | Budget % |
|---------|----------|---------|----------|
| Google Search | High intent | Bottom funnel | X% |
| Google Display | Scale, targeting | Awareness, retargeting | X% |
| Meta (FB/IG) | Targeting, creative | Full funnel | X% |
| LinkedIn | B2B targeting | B2B awareness, leads | X% |
| YouTube | Video reach | Brand, education | X% |
| TikTok | Young audience, virality | Awareness, engagement | X% |
### Step 3: Allocate Budget
| Channel | Monthly Budget | Target CPA | Expected Volume |
|---------|---------------|-----------|----------------|
| [channel] | $X | $X | X conversions |
### Step 4: Define Targeting
| Dimension | Strategy |
|-----------|---------|
| Demographics | Age, gender, income, education |
| Geography | Countries, regions, cities, radius |
| Interests | Platform-specific interest categories |
| Behavior | Purchase behavior, device usage |
| Custom audiences | CRM lists, website visitors, lookalikes |
| Exclusions | Existing customers, irrelevant audiences |
### Step 5: Plan Creative
| Format | Specs | Variants Needed |
|--------|-------|----------------|
| Static image | Per platform specs | 3-5 per audience |
| Video | 15s/30s/60s | 2-3 per message |
| Carousel | 3-10 cards | 2 per audience |
| Text ads | Headlines + descriptions | 5-10 per ad group |
### Step 6: Set Optimization Plan
| Week | Action |
|------|--------|
| 1 | Launch all variants, broad targeting |
| 2 | Pause underperformers, reallocate budget |
| 3 | Test new creative based on learnings |
| 4 | Optimize bids, narrow targeting |
| Monthly | Full performance review, budget reallocation |
## Output Format
```markdown
## Paid Media Plan: [Campaign]
### Budget: $[X]/month across [N] channels
### Channels: [allocation table]
### Targeting: [strategy summary]
### Creative: [requirements list]
### Optimization: [cadence and approach]
```
## Quality Checklist
- [ ] Objectives tied to business goals
- [ ] Channel mix matches funnel stage
- [ ] Budget allocation based on historical performance
- [ ] Creative plan covers all ad formats
- [ ] Optimization cadence defined
## Edge Cases
- For limited budgets, focus on 1-2 channels rather than spreading thin
- For new brands with no data, start with awareness before conversion
- For B2B, LinkedIn often outperforms despite higher CPMs
