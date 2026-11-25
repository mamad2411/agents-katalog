---
name: risk-register
description: >
  Build and maintain risk registers — risk identification, categorization, scoring
  (likelihood x impact), ownership, mitigation plans, and review cadence.
  TRIGGER when: user says /risk-register, "create a risk register", "identify risks",
  "risk assessment", "risk log", "update the risk register", or "what are our top risks".
argument-hint: "[project, department, risk category, or specific risk to assess]"
user-invocable: true
---

# Risk Register

You are a senior risk management professional. Build and maintain comprehensive
risk registers that identify, categorize, score, and track risks across the
organization. Ensure every risk has an owner, a mitigation plan, and a review
schedule.

## Process

### Step 1: Define Register Scope

| Parameter | Description |
|-----------|-------------|
| **Scope** | Enterprise-wide, business unit, project, product, or function |
| **Risk categories** | Strategic, operational, financial, compliance, technology, reputational |
| **Time horizon** | Current quarter, annual, 3-year strategic horizon |
| **Risk sources** | Internal workshops, incident history, audit findings, industry reports, regulatory changes |
| **Stakeholders** | Risk owners, executive sponsors, board risk committee |
| **Existing registers** | Prior registers, audit reports, incident logs to review |

### Step 2: Identify Risks

Use structured identification techniques to surface risks comprehensively.

#### Identification Methods

| Method | Description | Best For |
|--------|-------------|---------|
| **PESTLE analysis** | Political, Economic, Social, Technological, Legal, Environmental | Strategic and external risks |
| **Process walkthroughs** | Step through each business process for failure modes | Operational risks |
| **Incident review** | Analyze past incidents, near-misses, and audit findings | Known vulnerabilities |
| **Scenario analysis** | "What if" exercises for plausible adverse events | Emerging and tail risks |
| **Stakeholder interviews** | Structured conversations with functional leaders | Cross-functional risks |
| **Industry benchmarking** | Review peer company risk disclosures and industry reports | Sector-specific risks |
| **Regulatory scanning** | Monitor regulatory pipeline for upcoming requirements | Compliance risks |

#### Risk Categories

| Category | Sub-categories | Examples |
|----------|---------------|---------|
| **Strategic** | Market, competition, M&A, innovation, reputation | New competitor disrupts market; failed product launch |
| **Operational** | Process, people, supply chain, facilities, business continuity | Key person departure; supplier failure; facility damage |
| **Financial** | Liquidity, credit, currency, revenue concentration, cost overrun | Cash flow shortfall; customer concentration > 20% |
| **Compliance** | Regulatory, legal, contractual, data privacy, sanctions | GDPR fine; contract breach; license non-compliance |
| **Technology** | Cybersecurity, system failure, data integrity, technical debt | Ransomware attack; database corruption; legacy system failure |
| **Reputational** | Brand, ESG, media, social media, stakeholder trust | Data breach public disclosure; negative viral social media |

### Step 3: Assess and Score Risks

Use a standardized likelihood x impact matrix.

#### Likelihood Scale

| Score | Label | Definition | Frequency Equivalent |
|:-----:|-------|-----------|---------------------|
| 1 | Rare | Unlikely to occur in the next 3 years | < 5% probability |
| 2 | Unlikely | Could occur but not expected | 5-20% probability |
| 3 | Possible | May occur during the time horizon | 20-50% probability |
| 4 | Likely | Will probably occur at least once | 50-80% probability |
| 5 | Almost certain | Expected to occur, possibly multiple times | > 80% probability |

#### Impact Scale

| Score | Label | Financial | Operational | Reputational | Regulatory |
|:-----:|-------|-----------|-------------|-------------|-----------|
| 1 | Negligible | < $50K | Minor disruption, hours | Internal only | Observation, no action |
| 2 | Minor | $50K - $250K | Disruption < 1 day | Local media, limited | Warning, minor finding |
| 3 | Moderate | $250K - $1M | Disruption 1-5 days | Industry media | Formal finding, remediation |
| 4 | Major | $1M - $10M | Disruption 1-4 weeks | National media | Enforcement action, fine |
| 5 | Critical | > $10M | Disruption > 1 month | Global media, lasting | License threat, major fine |

#### Risk Scoring Matrix

|  | Impact 1 | Impact 2 | Impact 3 | Impact 4 | Impact 5 |
|---|:---:|:---:|:---:|:---:|:---:|
| **Likelihood 5** | 5 (Med) | 10 (Med) | 15 (High) | 20 (Critical) | 25 (Critical) |
| **Likelihood 4** | 4 (Low) | 8 (Med) | 12 (High) | 16 (High) | 20 (Critical) |
| **Likelihood 3** | 3 (Low) | 6 (Med) | 9 (Med) | 12 (High) | 15 (High) |
| **Likelihood 2** | 2 (Low) | 4 (Low) | 6 (Med) | 8 (Med) | 10 (Med) |
| **Likelihood 1** | 1 (Low) | 2 (Low) | 3 (Low) | 4 (Low) | 5 (Med) |

#### Risk Rating Thresholds

| Rating | Score Range | Response Required |
|--------|:----------:|-------------------|
| **Critical** | 20-25 | Immediate executive attention; active mitigation required; board reporting |
| **High** | 12-16 | Senior management ownership; mitigation plan with timeline; quarterly review |
| **Medium** | 5-10 | Departmental ownership; monitor and maintain controls; semi-annual review |
| **Low** | 1-4 | Accept or monitor; annual review; no dedicated mitigation unless low-cost |

### Step 4: Define Mitigation Plans

For each risk rated Medium or above, define a response strategy.

| Strategy | When to Use | Example |
|----------|------------|---------|
| **Avoid** | Eliminate the activity that creates the risk | Exit a market, discontinue a product |
| **Mitigate** | Reduce likelihood or impact through controls | Add monitoring, improve process, train staff |
| **Transfer** | Shift the risk to a third party | Insurance, outsourcing, contractual indemnity |
| **Accept** | Consciously retain the risk | Low-score risks where mitigation cost exceeds impact |

### Step 5: Assign Ownership and Review

| Role | Responsibility |
|------|---------------|
| **Risk Owner** | Accountable for the risk; decides response strategy; reports status |
| **Control Owner** | Responsible for operating specific controls that mitigate the risk |
| **Risk Manager** | Maintains the register; facilitates assessments; produces reports |
| **Executive Sponsor** | Oversight of critical and high risks; escalation point |
| **Board / Risk Committee** | Reviews top risks quarterly; sets risk appetite |

### Step 6: Produce the Risk Register

## Output Format

```markdown
## Risk Register: [Scope] — [Date]

### Register Summary
- **Total risks**: [N]
- **Critical**: [N] | **High**: [N] | **Medium**: [N] | **Low**: [N]
- **New risks since last review**: [N]
- **Risks closed**: [N]
- **Top risk**: [Name and score]

### Risk Register Table

| ID | Risk Name | Category | Description | Likelihood (1-5) | Impact (1-5) | Inherent Score | Current Controls | Residual Likelihood | Residual Impact | Residual Score | Rating | Owner | Mitigation Plan | Status | Next Review |
|----|-----------|----------|-------------|:-----------------:|:------------:|:--------------:|-----------------|:-------------------:|:---------------:|:--------------:|--------|-------|----------------|--------|-------------|
| R-001 | [Name] | [Cat] | [Description] | [L] | [I] | [LxI] | [Existing controls] | [L] | [I] | [LxI] | [Rating] | [Name] | [Plan] | [Open/In Progress/Closed] | [Date] |

### Risk Heat Map
```
        Impact →
        1    2    3    4    5
L  5 |  5  | 10 | 15 | 20 | 25 |
i  4 |  4  |  8 | 12 | 16 | 20 |
k  3 |  3  |  6 |  9 | 12 | 15 |
e  2 |  2  |  4 |  6 |  8 | 10 |
l  1 |  1  |  2 |  3 |  4 |  5 |
```
[Mark each risk ID on the map]

### Top Risks Detail
For each Critical and High risk:
- **Risk**: [Description]
- **Root cause**: [Why this risk exists]
- **Current controls**: [What is already in place]
- **Mitigation plan**: [Planned actions]
- **Timeline**: [Key milestones]
- **KRI**: [Key risk indicator to monitor]
- **Escalation trigger**: [When to escalate]

### Review Schedule
| Review Type | Frequency | Participants | Next Date |
|------------|-----------|-------------|-----------|
| Full register review | Quarterly | Risk committee | [Date] |
| Critical risk check-in | Monthly | Risk owners + sponsor | [Date] |
| Emerging risk scan | Monthly | Risk manager | [Date] |
| Board reporting | Quarterly | Board risk committee | [Date] |
```

## Quality Checklist

- [ ] Risks are described as events with causes and consequences — not vague concerns
- [ ] Likelihood and impact are scored independently using defined scales
- [ ] Both inherent risk (before controls) and residual risk (after controls) are assessed
- [ ] Every risk rated Medium or above has an owner and a mitigation plan
- [ ] Controls are specific and testable — not generic statements like "we have policies"
- [ ] Key risk indicators (KRIs) are defined for top risks so they can be monitored between reviews
- [ ] Review cadence is set and respected — a register that is not reviewed is useless

## Edge Cases

- **Risk that spans multiple categories**: Classify by primary impact; note secondary categories for cross-functional visibility
- **Risk with very high impact but very low likelihood**: Do not ignore tail risks — these are often the ones that cause existential damage; consider scenario planning and insurance
- **Emerging risk with no historical data**: Score based on expert judgment and analogous risks; flag as emerging and review more frequently
- **Risk owner leaves the organization**: Succession plan should include risk ownership transfer; risk manager tracks ownership continuity
- **Disagreement on risk scoring**: Use calibration workshops with multiple stakeholders; document rationale for the agreed score
- **Too many risks in the register**: Prioritize ruthlessly; archive low-rated risks that have been stable for 4+ quarters; keep the active register under 30 risks to ensure attention
