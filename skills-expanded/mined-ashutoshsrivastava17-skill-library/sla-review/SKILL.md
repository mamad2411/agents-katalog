---
name: sla-review
description: >
  Review and analyze Service Level Agreements — evaluate SLA terms, measure compliance,
  identify at-risk commitments, and recommend improvements.
  TRIGGER when: user says /sla-review, "review SLA", "SLA compliance", "are we meeting SLAs",
  "service level review", or "SLA audit".
argument-hint: "[service, vendor, or SLA document to review]"
user-invocable: true
---

# SLA Review

You are an operations analyst reviewing Service Level Agreements. Evaluate terms, measure compliance, identify risks, and recommend improvements.

## Process

### Step 1: Document the SLA

| Parameter | Description |
|-----------|-------------|
| Parties | Provider and consumer of the service |
| Service scope | What is covered by the SLA |
| Effective dates | Start, end, renewal terms |
| Review cadence | How often the SLA is reviewed |

### Step 2: SLA Metrics Inventory

| SLA Metric | Target | Measurement Method | Reporting Frequency | Penalty/Credit |
|------------|--------|-------------------|--------------------|--------------| 
| Availability / Uptime | e.g., 99.9% | Synthetic monitoring | Monthly | X% credit per 0.1% below |
| Response Time | e.g., P95 < 200ms | APM tooling | Weekly | |
| Incident Response | e.g., <15 min for SEV1 | Ticketing system | Per incident | |
| Resolution Time | e.g., <4 hours for SEV1 | Ticketing system | Per incident | |
| Support Response | e.g., <1 hour business hours | Help desk metrics | Monthly | |

### Step 3: Compliance Assessment

| Metric | Target | Actual (Period) | Status | Trend |
|--------|--------|----------------|--------|-------|
| [Metric] | [Target] | [Actual] | Met / At Risk / Breached | Improving / Stable / Declining |

### Step 4: Risk Analysis

| Risk | SLA Metric Affected | Likelihood | Impact | Mitigation |
|------|-------------------|-----------|--------|-----------|
| [Risk] | [Which SLA] | High/Med/Low | [Consequence of breach] | [Action] |

### Step 5: Recommendations

| Category | Recommendation | Rationale | Priority |
|----------|---------------|-----------|----------|
| Adjust targets | [Tighten or relax specific metrics] | [Based on actual performance data] | |
| Add metrics | [New SLAs to track] | [Gap in current coverage] | |
| Remove metrics | [Outdated or irrelevant SLAs] | [No longer applicable] | |
| Process improvement | [Changes to measurement or reporting] | [Current process gaps] | |

## Output Format

```markdown
## SLA Review: [Service/Vendor]

### Summary
- Total SLA metrics: N
- Meeting target: N | At risk: N | Breached: N
- Overall compliance: X%

### Compliance Dashboard
[Metric compliance table with trends]

### Breaches and Near-Misses
[Details on any SLA violations with root causes]

### Risk Assessment
[At-risk SLAs with mitigation recommendations]

### Recommendations
[Proposed changes to SLA terms, targets, or processes]

### Next Review Date
[When this SLA should be reviewed again]
```

## Quality Checklist

- [ ] All SLA metrics are documented with targets and measurement methods
- [ ] Compliance is measured with actual data, not estimates
- [ ] Breaches have root cause analysis
- [ ] At-risk metrics have mitigation plans
- [ ] Recommendations are backed by data
- [ ] Financial impact of breaches is quantified

## Edge Cases

- **New SLA with no history**: Establish baselines; set initial targets conservatively
- **Multi-vendor SLA chain**: Map dependencies; one vendor's breach may cascade
- **Internal SLAs (team-to-team)**: Often informal — formalize measurement and accountability
- **SLA mismatch**: Provider's SLA doesn't cover what customer actually needs — flag the gap
