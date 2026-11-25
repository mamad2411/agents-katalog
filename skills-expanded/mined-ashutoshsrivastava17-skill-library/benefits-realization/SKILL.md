---
name: benefits-realization
description: >
  Track benefits realization — benefit identification, measurement methodology,
  baseline establishment, tracking cadence, and variance analysis.
  TRIGGER when: user says /benefits-realization or asks about tracking program benefits and outcomes.
argument-hint: "[program or initiative to track]"
user-invocable: true
---
# Benefits Realization
## Process
### Step 1: Identify Benefits
| Benefit | Type | Beneficiary | Measurement |
|---------|------|------------|-------------|
| [benefit] | Financial/Operational/Strategic | [who] | [metric] |
### Step 2: Establish Baselines
| Metric | Current Value | Source | Date |
|--------|-------------|--------|------|
| [metric] | X | [system/report] | [date] |
### Step 3: Set Targets
| Benefit | Baseline | Target | Timeline |
|---------|----------|--------|----------|
| [benefit] | X | X | [date] |
### Step 4: Track Progress
| Benefit | Target | Actual | Variance | Status |
|---------|--------|--------|----------|--------|
| [benefit] | X | X | +/-X% | On track/At risk/Behind |
### Step 5: Analyze Variances
| Variance | Root Cause | Corrective Action |
|----------|-----------|-------------------|
| [benefit behind target] | [why] | [action to recover] |
### Step 6: Report
| Audience | Content | Frequency |
|----------|---------|-----------|
| Sponsor | Executive summary | Monthly |
| PMO | Detailed tracking | Bi-weekly |
| Stakeholders | Progress update | Quarterly |
## Output Format
```markdown
## Benefits Report: [Program]
### Benefits Tracked: [count]
### On Track: [X] | At Risk: [X] | Behind: [X]
### Key Variances: [Analysis]
### Actions: [Corrective measures]
```
## Quality Checklist
- [ ] All expected benefits identified and documented
- [ ] Baselines established before program start
- [ ] Targets are specific and measurable
- [ ] Tracking cadence is regular
- [ ] Variances are analyzed with root causes
## Edge Cases
- For strategic (non-financial) benefits, use proxy metrics
- If benefits take years to materialize, track leading indicators
- For cancelled programs, still assess realized vs expected benefits
