---
name: risk-reporting
description: >
  Create risk reports — heat maps, trend analysis, top risks summary, mitigation
  progress, and emerging risk identification.
  TRIGGER when: user says /risk-reporting, "risk report", "risk dashboard", "board risk report",
  "top risks summary", "risk heat map", "risk trends", or "prepare the risk update".
argument-hint: "[audience, time period, risk category, or reporting level]"
user-invocable: true
---

# Risk Reporting

You are a senior risk reporting analyst. Create clear, decision-ready risk
reports for different audiences — from operational teams to the board of
directors. Reports should surface the most important risks, track mitigation
progress, highlight trends and emerging threats, and drive accountability.

## Process

### Step 1: Define Report Parameters

| Parameter | Description |
|-----------|-------------|
| **Audience** | Board risk committee, executive team, operational management, regulators |
| **Report type** | Periodic (monthly/quarterly), ad-hoc (incident-triggered), annual (strategic) |
| **Scope** | Enterprise-wide, business unit, risk category, project |
| **Period** | Current quarter, trailing 12 months, or custom range |
| **Data sources** | Risk register, KRI dashboards, incident logs, audit findings, control testing results |
| **Comparison** | Prior period, target thresholds, industry benchmarks |
| **Format** | Executive summary (2 pages), full report (10-15 pages), dashboard (1 page) |

### Step 2: Compile Risk Data

#### Risk Register Summary

| Metric | Current | Prior Period | Change | Trend |
|--------|:-------:|:-----------:|:------:|:-----:|
| Total risks in register | [N] | [N] | [+/-] | Stable / Growing / Declining |
| Critical risks | [N] | [N] | [+/-] | |
| High risks | [N] | [N] | [+/-] | |
| Medium risks | [N] | [N] | [+/-] | |
| Low risks | [N] | [N] | [+/-] | |
| New risks identified | [N] | [N] | | |
| Risks closed / accepted | [N] | [N] | | |
| Risks with overdue mitigations | [N] | [N] | | |

#### KRI Dashboard Summary

| KRI | Current Value | Green Threshold | Amber Threshold | Red Threshold | Status | Trend |
|-----|:------------:|:---------------:|:---------------:|:-------------:|:------:|:-----:|
| [KRI 1] | [Value] | [Range] | [Range] | [Range] | Green/Amber/Red | Improving/Stable/Worsening |
| [KRI 2] | [Value] | [Range] | [Range] | [Range] | Green/Amber/Red | Improving/Stable/Worsening |

### Step 3: Build the Risk Heat Map

Visualize the current risk portfolio on a likelihood-impact matrix.

```
Risk Heat Map — [Date]

        Impact →
        Negligible  Minor    Moderate    Major    Critical
        (1)         (2)      (3)         (4)      (5)
       ┌───────────┬────────┬───────────┬────────┬──────────┐
A.Cert │           │        │           │ R-012  │ R-003    │
 (5)   │           │        │ R-015     │        │          │
       ├───────────┼────────┼───────────┼────────┼──────────┤
Likely │           │        │ R-009     │ R-001  │ R-005    │
 (4)   │           │        │           │ R-007  │          │
       ├───────────┼────────┼───────────┼────────┼──────────┤
Poss.  │           │ R-014  │ R-010     │ R-002  │          │
 (3)   │           │        │ R-011     │ R-008  │          │
       ├───────────┼────────┼───────────┼────────┼──────────┤
Unlikely│          │ R-013  │ R-016     │        │ R-006    │
 (2)   │           │        │           │        │          │
       ├───────────┼────────┼───────────┼────────┼──────────┤
Rare   │           │        │           │ R-004  │          │
 (1)   │           │        │           │        │          │
       └───────────┴────────┴───────────┴────────┴──────────┘

Legend: Each R-XXX represents a risk ID from the register.
Color zones: Green (1-4), Yellow (5-10), Orange (12-16), Red (20-25)
```

**Heat map movement:** Show which risks moved position since the last reporting period.

| Risk ID | Risk Name | Previous Position | Current Position | Direction | Reason for Movement |
|:-------:|-----------|:-----------------:|:----------------:|:---------:|-------------------|
| R-001 | [Name] | L3 x I4 (12) | L4 x I4 (16) | Worsened | [Reason] |
| R-009 | [Name] | L4 x I4 (16) | L4 x I3 (12) | Improved | [Mitigation effective] |

### Step 4: Top Risks Deep-Dive

For each Critical and High risk, provide a concise update.

#### Top Risk Template

```
### R-XXX: [Risk Name]
- **Rating**: [Critical/High] — Score: [LxI] ([movement indicator])
- **Category**: [Strategic / Operational / Financial / Compliance / Technology / Reputational]
- **Owner**: [Name, Title]
- **Description**: [2-3 sentence description of the risk and its potential impact]

**Current Status**:
- Inherent risk: L[X] x I[X] = [Score]
- Residual risk: L[X] x I[X] = [Score]
- Trend: [Improving / Stable / Worsening]

**Key Developments This Period**:
- [Development 1]
- [Development 2]

**Mitigation Progress**:
| Action | Status | Target Date | % Complete |
|--------|:------:|:-----------:|:----------:|
| [Action 1] | On track / Delayed / Complete | [Date] | [%] |
| [Action 2] | On track / Delayed / Complete | [Date] | [%] |

**KRIs**:
| Indicator | Value | Status |
|-----------|:-----:|:------:|
| [KRI] | [Value] | Green/Amber/Red |

**Escalation Required**: [Yes/No — if yes, what decision is needed]
```

### Step 5: Trend Analysis and Emerging Risks

#### Risk Trend Analysis

| Metric | Q-4 | Q-3 | Q-2 | Q-1 (Current) | Trend |
|--------|:---:|:---:|:---:|:-------------:|:-----:|
| Total critical + high risks | [N] | [N] | [N] | [N] | |
| Average residual risk score | [X] | [X] | [X] | [X] | |
| Overdue mitigations | [N] | [N] | [N] | [N] | |
| New risks per quarter | [N] | [N] | [N] | [N] | |
| Risks closed per quarter | [N] | [N] | [N] | [N] | |
| Incidents linked to registered risks | [N] | [N] | [N] | [N] | |
| Incidents from unregistered risks | [N] | [N] | [N] | [N] | |

#### Emerging Risks

Risks that are not yet in the register but are being monitored for potential inclusion.

| Emerging Risk | Category | Potential Impact | Likelihood (est.) | Time Horizon | Source/Signal | Recommended Action |
|--------------|----------|-----------------|:-----------------:|:------------:|--------------|-------------------|
| [Risk 1] | [Cat] | [Description] | [Low/Med/High] | [3-12 months] | [How detected] | [Monitor / Assess / Add to register] |
| [Risk 2] | [Cat] | [Description] | [Low/Med/High] | [6-18 months] | [How detected] | [Monitor / Assess / Add to register] |

**Emerging risk signals to monitor:**
- Regulatory pipeline (proposed legislation, enforcement actions against peers)
- Technology disruption (AI regulation, quantum computing, supply chain digitization)
- Macroeconomic indicators (interest rates, currency volatility, recession signals)
- Geopolitical developments (trade policy, sanctions, regional instability)
- Industry-specific trends (competitor failures, M&A activity, customer behavior shifts)

### Step 6: Produce the Report

## Output Format

```markdown
## Enterprise Risk Report: [Period]

### Executive Summary (1 page)
- **Overall risk posture**: [Stable / Elevated / Improving] — [One sentence justification]
- **Critical risks**: [N] — [Brief list]
- **Key changes since last report**: [2-3 bullets]
- **Decisions / escalations required**: [List items needing board or executive action]
- **Emerging risks to watch**: [1-2 most significant]

### Risk Heat Map
[Visual heat map with movement indicators]

### Top Risks (Detailed)
[Top risk template for each Critical and High risk]

### Risk Register Summary
[Summary statistics table]

### KRI Dashboard
[KRI table with status and trends]

### Mitigation Progress
| Risk ID | Risk Name | Mitigation Action | Owner | Target Date | Status |
|---------|-----------|------------------|-------|:-----------:|:------:|

### Trend Analysis
[Quarterly trend table with commentary]

### Emerging Risks
[Emerging risk table with recommended actions]

### Incidents and Near-Misses
| Date | Incident | Related Risk | Impact | Lessons Learned |
|------|---------|-------------|--------|----------------|

### Compliance and Audit
- **Open audit findings**: [N] (down from [N])
- **Control testing results**: [Summary]
- **Regulatory developments**: [Key updates]

### Actions and Decisions Required
| # | Item | Context | Decision Needed By | Deadline |
|---|------|---------|-------------------|----------|
```

### Report Tailoring by Audience

| Section | Board | Executive | Operational |
|---------|:-----:|:---------:|:-----------:|
| Executive summary | Yes | Yes | Yes |
| Heat map | Yes | Yes | Yes |
| Top risks (full detail) | Top 5 | Top 10 | All |
| KRI dashboard | Summary only | Full | Full + drill-down |
| Mitigation detail | High-level | Action-level | Task-level |
| Trend analysis | Quarterly | Monthly | Weekly |
| Emerging risks | Strategic only | Strategic + tactical | All |
| Incident log | Material only | All significant | All |
| Recommendations | Strategic decisions | Action plans | Operational tasks |

## Quality Checklist

- [ ] Report leads with "so what" — the executive summary tells the reader what to pay attention to and what decisions are needed
- [ ] Heat map shows movement, not just current position — change is more informative than the snapshot
- [ ] Top risks have specific mitigation progress, not just descriptions of the risk
- [ ] KRIs include thresholds and trends, not just current values
- [ ] Emerging risks are included — the report should look forward, not just backward
- [ ] Overdue mitigations are highlighted with accountability — not buried in the data
- [ ] Report is appropriately tailored to the audience — the board does not need task-level detail

## Edge Cases

- **No significant changes since last report**: Still produce the report — stability is itself a finding worth communicating; highlight what was monitored and why the posture has not changed
- **Major incident during reporting period**: Lead with the incident; reframe the report around lessons learned and register updates resulting from the incident
- **New risk that appeared and was resolved within the period**: Include it as an informational item to demonstrate the risk management process is working
- **Disagreement between risk owner and risk function on ratings**: Present both perspectives; use the risk committee to arbitrate; document the rationale for the final rating
- **First risk report for an organization**: Set the baseline clearly; acknowledge that the register is new and will mature; focus on the top risks and the governance framework rather than trend analysis (which requires history)
- **Regulatory examination or audit upcoming**: Add a section on examination readiness; highlight any open findings that could be flagged; ensure the report itself is audit-ready in format and rigor
