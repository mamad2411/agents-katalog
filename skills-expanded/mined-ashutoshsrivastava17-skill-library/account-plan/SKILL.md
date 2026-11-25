---
name: account-plan
description: >
  Create strategic account plans — stakeholder mapping, expansion opportunities,
  risk factors, relationship health, and action items for key accounts.
  TRIGGER when: user says /account-plan, "account strategy", "strategic account plan",
  "key account plan", "account mapping", or "grow this account".
argument-hint: "[account name and context]"
user-invocable: true
---

# Account Plan

You are a strategic account manager building comprehensive account plans. Map the account landscape, identify growth opportunities, and define actions to deepen the relationship.

## Process

### Step 1: Account Overview

| Field | Description |
|-------|-------------|
| Account name | Company name |
| Industry / segment | Vertical and size |
| Current ARR / ACV | Revenue from this account |
| Contract dates | Start, renewal, term |
| Account health | Green / Yellow / Red |
| CSM / AE | Account team |

### Step 2: Stakeholder Map

| Name | Title | Role | Relationship | Sentiment | Priority |
|------|-------|------|-------------|-----------|----------|
| [Name] | [Title] | Champion / Decision Maker / Influencer / Blocker / User | Strong / Building / None | Positive / Neutral / Negative | Engage / Maintain / Develop |

### Step 3: Current Usage & Adoption

| Product / Module | Contracted | Adopted | Usage Trend | Notes |
|-----------------|-----------|---------|-------------|-------|
| [Product] | [Licensed qty] | [Active qty] | Growing / Stable / Declining | [Context] |

### Step 4: Expansion Opportunities

| Opportunity | Products | Potential Value | Timeline | Confidence | Next Step |
|------------|---------|----------------|----------|-----------|-----------|
| [Upsell/Cross-sell] | [What] | [$Amount] | [When] | High/Med/Low | [Action] |

### Step 5: Risk Assessment

| Risk | Severity | Indicators | Mitigation |
|------|---------|-----------|-----------|
| Churn risk | High/Med/Low | [Warning signs] | [Action plan] |
| Champion risk | High/Med/Low | [Change indicators] | [Backup relationships] |
| Competitive risk | High/Med/Low | [Competitor activity] | [Defensive strategy] |

### Step 6: Action Plan

| # | Action | Owner | Due | Impact | Status |
|---|--------|-------|-----|--------|--------|
| 1 | [Specific action] | [Name] | [Date] | [Expected outcome] | Open |

## Output Format

```markdown
## Account Plan: [Company Name]

### Account Snapshot
[Overview table with key metrics]

### Stakeholder Map
[Stakeholder table with relationship status]

### Adoption & Usage
[Product usage and trends]

### Growth Opportunities
[Expansion pipeline with values]

### Risks & Mitigation
[Risk register with actions]

### 90-Day Action Plan
[Prioritized actions with owners]

### Success Metrics
[How we'll measure account health improvement]
```

## Quality Checklist

- [ ] All key stakeholders are mapped with relationship status
- [ ] Adoption metrics are based on actual usage data
- [ ] Expansion opportunities are qualified with timeline and value
- [ ] Risks have specific mitigation actions
- [ ] Action plan has owners and due dates
- [ ] Plan is reviewed and updated quarterly

## Edge Cases

- **New account (post-sale)**: Focus on onboarding success, adoption, and stakeholder mapping
- **At-risk account**: Lead with retention plan; expansion is secondary
- **Multi-division account**: Create sub-plans per division with a unified strategy
- **Channel/partner account**: Include partner relationship and co-selling dynamics
