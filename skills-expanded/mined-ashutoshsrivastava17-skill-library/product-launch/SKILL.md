---
name: product-launch
description: >
  Plan product launches — launch tiers, go/no-go criteria, cross-functional
  checklist, communication plan, enablement, and post-launch review.
  TRIGGER when: user says /product-launch or asks about launching a product or feature.
argument-hint: "[product or feature to launch]"
user-invocable: true
---
# Product Launch Plan
## Process
### Step 1: Define Launch Tier
| Tier | Scope | Activities |
|------|-------|-----------|
| T1 (Major) | New product, major feature | Full GTM, PR, event, enablement |
| T2 (Standard) | Significant feature | Blog, email, in-app, enablement |
| T3 (Minor) | Improvement, fix | Changelog, in-app notification |
### Step 2: Set Go/No-Go Criteria
| Category | Criteria | Status |
|----------|---------|--------|
| Product | Feature complete, QA passed | ☐ |
| Performance | Load tested, SLAs met | ☐ |
| Documentation | Help docs, API docs updated | ☐ |
| Enablement | Sales/support trained | ☐ |
| Marketing | Assets ready, campaigns scheduled | ☐ |
| Legal | Terms updated, compliance reviewed | ☐ |
### Step 3: Cross-Functional Checklist
| Team | Deliverables | Owner | Due |
|------|-------------|-------|-----|
| Engineering | Feature deployed, monitoring live | [name] | [date] |
| Design | Assets, screenshots, demo video | [name] | [date] |
| Marketing | Blog, email, social, landing page | [name] | [date] |
| Sales | Pitch deck, battle card, FAQ | [name] | [date] |
| Support | KB articles, runbook, training | [name] | [date] |
| Legal | Terms, privacy, compliance | [name] | [date] |
### Step 4: Communication Plan
| Audience | Channel | Timing | Message |
|----------|---------|--------|---------|
| Internal | All-hands, Slack | T-1 week | Preview and enablement |
| Customers | Email, in-app | Launch day | Announcement |
| Prospects | Blog, social, PR | Launch day | Value proposition |
| Partners | Email, portal | T-1 day | Enablement materials |
### Step 5: Launch Execution
| Time | Action | Owner |
|------|--------|-------|
| T-7 days | Final go/no-go meeting | PM |
| T-1 day | Staged deployment | Engineering |
| Launch day | Flip feature flag, publish content | PM + Marketing |
| T+1 day | Monitor metrics, respond to feedback | All |
| T+7 days | First week review | PM |
### Step 6: Post-Launch Review
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| Adoption | X% in first month | X% | |
| Satisfaction | X/5 CSAT | X/5 | |
| Support tickets | < X related tickets | X | |
| Revenue impact | $X pipeline influenced | $X | |
## Output Format
```markdown
## Launch Plan: [Product/Feature]
### Tier: [T1/T2/T3]
### Go/No-Go: [Criteria with status]
### Timeline: [Key dates]
### Metrics: [Success criteria]
```
## Quality Checklist
- [ ] Launch tier determines appropriate activities
- [ ] Go/no-go criteria are specific and measurable
- [ ] All teams have clear deliverables and deadlines
- [ ] Communication covers all audiences
- [ ] Post-launch review scheduled
## Edge Cases
- For beta-to-GA transitions, communicate changes since beta
- For breaking changes, extend communication timeline
- If launch timing is competitive, plan for confidentiality
