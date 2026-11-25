---
name: litigation-management
description: >
  Manage litigation matters — case tracking, document holds, timeline management,
  cost tracking, settlement analysis, and reporting.
  TRIGGER when: user says /litigation-management, needs to track legal cases,
  or asks about litigation process management.
argument-hint: "[case or legal matter to manage]"
user-invocable: true
---
# Litigation Management

> **Disclaimer:** Not legal advice. Work with qualified legal counsel for all litigation matters.

## Process
### Step 1: Case Intake
| Field | Details |
|-------|---------|
| Case name | [Parties] |
| Case number | [Court filing number] |
| Type | Contract, IP, employment, regulatory, tort |
| Status | Pre-litigation / Filed / Discovery / Trial / Appeal |
| Counsel | Internal / External firm |
| Risk level | High / Medium / Low |
| Estimated exposure | $X range |
### Step 2: Implement Document Hold
| Action | Owner | Status |
|--------|-------|--------|
| Issue litigation hold notice | Legal | ☐ |
| Identify custodians | Legal + IT | ☐ |
| Preserve relevant data | IT | ☐ |
| Confirm receipt of hold | All custodians | ☐ |
### Step 3: Track Timeline
| Date | Event | Action Required |
|------|-------|----------------|
| [date] | Filing/service | Respond within [days] |
| [date] | Discovery deadline | Complete document production |
| [date] | Depositions | Prepare witnesses |
| [date] | Mediation | Settlement preparation |
| [date] | Trial date | Trial preparation |
### Step 4: Manage Costs
| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| Outside counsel | $X | $X | $X |
| E-discovery | $X | $X | $X |
| Expert witnesses | $X | $X | $X |
| Court costs | $X | $X | $X |
### Step 5: Evaluate Settlement
| Factor | Assessment |
|--------|-----------|
| Likelihood of success | X% |
| Potential judgment | $X |
| Litigation cost to completion | $X |
| Settlement demand/offer | $X |
| Non-monetary factors | Precedent, reputation, time |
### Step 6: Report
| Audience | Content | Frequency |
|----------|---------|-----------|
| Board/Exec | Portfolio summary, material cases | Quarterly |
| Finance | Reserves, accruals, costs | Monthly |
| Insurance | Coverage, claims status | Per case |
## Output Format
```markdown
## Case: [Name]
### Status: [phase] | Risk: [level] | Exposure: [$X]
### Timeline: [key dates]
### Costs: [budget vs actual]
### Recommendation: [settle/litigate/dismiss with rationale]
```
## Quality Checklist
- [ ] Document hold properly implemented
- [ ] Timeline and deadlines tracked
- [ ] Costs monitored against budget
- [ ] Settlement analysis based on data
- [ ] Regular reporting to stakeholders
## Edge Cases
- For class actions, track additional complexity of class certification
- For multi-jurisdiction matters, coordinate local counsel
- If insurance covers the claim, involve carrier early
