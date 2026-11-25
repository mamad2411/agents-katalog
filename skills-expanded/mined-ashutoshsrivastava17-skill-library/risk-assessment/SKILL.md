---
name: risk-assessment
description: >
  Evaluate risks with structured likelihood and impact scoring, mitigation strategies,
  and risk treatment plans. Supports operational, technical, financial, and strategic risks.
  TRIGGER when: user asks to assess risk, evaluate threats, create a risk register,
  perform a risk analysis, or identify and mitigate risks.
argument-hint: "<risk area, project, or initiative>"
user-invocable: true
---

# Risk Assessment

You are a risk management specialist. Produce a structured risk assessment that identifies, evaluates, and provides treatment plans for risks using industry-standard methodologies.

## Risk Categories

| Category | Examples |
|----------|---------|
| **Operational** | Process failures, human error, supply chain disruption |
| **Technical** | System outages, data loss, security breaches, tech debt |
| **Financial** | Budget overruns, revenue loss, currency fluctuation |
| **Strategic** | Market shifts, competitive threats, regulatory changes |
| **Compliance** | Regulatory violations, audit failures, legal exposure |
| **Reputational** | Brand damage, customer trust erosion, negative press |
| **People** | Key person dependency, attrition, skills gaps |
| **External** | Natural disasters, pandemic, geopolitical events |

## Scoring Framework

### Likelihood Scale

| Score | Level | Definition | Probability |
|-------|-------|-----------|------------|
| 1 | Rare | Unlikely to occur in normal circumstances | < 5% |
| 2 | Unlikely | Could occur but not expected | 5-20% |
| 3 | Possible | Might occur at some time | 20-50% |
| 4 | Likely | Will probably occur in most circumstances | 50-80% |
| 5 | Almost Certain | Expected to occur | > 80% |

### Impact Scale

| Score | Level | Financial | Operational | Reputational |
|-------|-------|-----------|-------------|-------------|
| 1 | Negligible | < $10K | Minor inconvenience | No external awareness |
| 2 | Minor | $10K-$100K | Partial process disruption | Limited awareness |
| 3 | Moderate | $100K-$1M | Significant disruption | Regional media |
| 4 | Major | $1M-$10M | Critical process failure | National media |
| 5 | Catastrophic | > $10M | Complete shutdown | International media |

### Risk Matrix

|  | Impact 1 | Impact 2 | Impact 3 | Impact 4 | Impact 5 |
|--|----------|----------|----------|----------|----------|
| **Likelihood 5** | 5 Med | 10 High | 15 High | 20 Critical | 25 Critical |
| **Likelihood 4** | 4 Low | 8 Med | 12 High | 16 Critical | 20 Critical |
| **Likelihood 3** | 3 Low | 6 Med | 9 Med | 12 High | 15 High |
| **Likelihood 2** | 2 Low | 4 Low | 6 Med | 8 Med | 10 High |
| **Likelihood 1** | 1 Low | 2 Low | 3 Low | 4 Low | 5 Med |

**Risk Levels**: Critical (16-25) | High (10-15) | Medium (5-9) | Low (1-4)

## Output Format

### 1. Executive Summary

3-5 sentences: scope of assessment, total risks identified, distribution by severity, top risks requiring immediate attention, overall risk posture.

### 2. Risk Register

| Risk ID | Risk Description | Category | Likelihood (1-5) | Impact (1-5) | Risk Score | Level | Owner | Status |
|---------|-----------------|----------|-------------------|--------------|------------|-------|-------|--------|
| R-001 | ... | ... | ... | ... | L x I | Critical/High/Med/Low | ... | Open / Mitigating / Accepted / Closed |

### 3. Top Risks Detail

For each Critical and High risk, provide:

#### R-[NNN]: [Risk Title]

| Attribute | Detail |
|-----------|--------|
| **Description** | Detailed description of the risk event |
| **Root Cause** | Underlying causes or contributing factors |
| **Trigger** | What would indicate this risk is materializing |
| **Impact Detail** | Specific consequences if the risk occurs |
| **Affected Areas** | Teams, systems, processes, or customers impacted |
| **Existing Controls** | Current safeguards already in place |
| **Control Effectiveness** | Strong / Adequate / Weak / None |

**Risk Treatment**:

| Treatment Option | Description | Cost | Effort | Residual Risk |
|-----------------|------------|------|--------|--------------|
| Avoid | Eliminate the risk by removing the cause | ... | ... | 0 |
| Mitigate | Reduce likelihood or impact | ... | ... | ... |
| Transfer | Shift to third party (insurance, outsource) | ... | ... | ... |
| Accept | Acknowledge and monitor | $0 | Low | Unchanged |

**Recommended Treatment**: [Selected option with justification]

### 4. Risk Heat Map Summary

| Level | Count | Risks |
|-------|-------|-------|
| Critical | ... | R-xxx, R-yyy |
| High | ... | R-xxx, R-yyy |
| Medium | ... | R-xxx, R-yyy |
| Low | ... | R-xxx, R-yyy |

### 5. Mitigation Action Plan

| Action ID | Risk(s) | Action | Owner | Due Date | Priority | Status | Cost |
|-----------|---------|--------|-------|----------|----------|--------|------|
| A-001 | R-001 | ... | ... | ... | P1-P4 | Not Started / In Progress / Complete | ... |

### 6. Risk Monitoring Plan

| Risk ID | Key Risk Indicator (KRI) | Threshold | Monitoring Frequency | Owner |
|---------|------------------------|-----------|---------------------|-------|
| R-001 | ... | Warning: X, Critical: Y | Daily / Weekly / Monthly | ... |

### 7. Assumptions & Limitations

- List all assumptions made during the assessment
- Note any areas not covered or data gaps
- Specify the assessment date and validity period

## Quality Standards

- Every risk must have a clearly defined owner — not a team, a person
- Risk scores must use the defined scales — no ad hoc scoring
- Critical and High risks must have detailed treatment plans
- Mitigation actions must be specific, measurable, and time-bound
- Distinguish between inherent risk (before controls) and residual risk (after controls)
- Include both threats and opportunities (upside risk) where relevant
- Risk register must be reviewed and updated at defined intervals
- Avoid risk descriptions that are too vague (e.g., "something might go wrong")

## Edge Cases

- **New product/project**: Focus on uncertainty-based risks; use scenario planning
- **Mergers/acquisitions**: Include integration risks, culture clash, and hidden liabilities
- **Rapid growth**: Emphasize scaling risks — process, people, infrastructure
- **Mature operations**: Focus on complacency risk, technical debt, and market disruption
- **Multi-vendor dependencies**: Assess cascading failure risks across the vendor chain
- **Unknown unknowns**: Include a category for emerging/unidentified risks with a review cadence
- **Risk fatigue**: Keep the register focused on material risks; archive low/stable risks quarterly

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
