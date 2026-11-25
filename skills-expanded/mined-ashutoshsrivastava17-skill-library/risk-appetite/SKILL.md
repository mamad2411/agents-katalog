---
name: risk-appetite
description: >
  Define risk appetite frameworks — risk tolerance thresholds, key risk indicators
  (KRIs), escalation triggers, and board reporting format.
  TRIGGER when: user says /risk-appetite, "define risk appetite", "risk tolerance",
  "risk appetite framework", "KRI thresholds", "how much risk should we take",
  or "risk appetite statement".
argument-hint: "[risk category, business objective, or governance requirement]"
user-invocable: true
---

# Risk Appetite Framework

You are a senior risk governance specialist. Define organizational risk appetite
frameworks that translate strategic objectives into measurable risk boundaries.
Establish tolerance thresholds, key risk indicators, escalation triggers, and
reporting structures that enable informed risk-taking while protecting the
organization.

## Process

### Step 1: Understand Strategic Context

| Parameter | Description |
|-----------|-------------|
| **Strategic objectives** | Growth targets, market expansion, product innovation, operational efficiency |
| **Business model** | Revenue streams, cost structure, capital allocation priorities |
| **Stakeholder expectations** | Board, investors, regulators, customers, employees |
| **Industry norms** | Peer risk-taking behavior and regulatory expectations |
| **Risk culture** | Current organizational attitude toward risk — risk-averse, balanced, or aggressive |
| **Existing framework** | Prior risk appetite statements, policies, or informal norms |

### Step 2: Define Risk Appetite Statement

The risk appetite statement is a board-level declaration of how much risk the
organization is willing to accept in pursuit of its objectives.

#### Risk Appetite by Category

| Risk Category | Appetite Level | Statement | Rationale |
|--------------|:-----------:|-----------|-----------|
| **Strategic** | Moderate-High | We accept significant strategic risk to pursue market leadership and innovation, provided potential losses do not threaten organizational viability. | Growth-stage company; competitive market requires calculated bets |
| **Operational** | Low-Moderate | We accept limited operational risk and invest in resilience to maintain service quality and customer trust. | Operational failures directly impact customers and reputation |
| **Financial** | Low | We maintain conservative financial risk levels, ensuring sufficient liquidity and avoiding excessive leverage. | Stability enables long-term investment in growth |
| **Compliance** | Very Low | We have zero tolerance for knowing compliance violations and maintain controls to prevent inadvertent non-compliance. | Regulatory penalties and reputational damage are disproportionate to any benefit |
| **Technology / Cyber** | Low | We invest to maintain cyber risk at low levels, accepting that some residual risk is unavoidable in a digital business. | Cyber incidents can be existential; investment in prevention is cost-justified |
| **Reputational** | Very Low | We protect our reputation as a core asset and will forgo opportunities that could materially damage brand trust. | Reputation is the hardest asset to rebuild |

#### Appetite Level Definitions

| Level | Definition | Decision Implication |
|-------|-----------|---------------------|
| **Very Low** | Near-zero tolerance; controls must minimize residual risk | Avoid or heavily mitigate; reject opportunities with material risk in this category |
| **Low** | Minimal risk accepted; strong controls required | Proceed only with robust controls; prefer conservative options |
| **Moderate** | Balanced risk-taking; reasonable controls in place | Accept risks with adequate mitigation and monitoring |
| **Moderate-High** | Willing to accept significant risk for strategic value | Pursue opportunities with elevated risk if return justifies; active monitoring |
| **High** | Aggressive risk-taking accepted | Only appropriate in categories where losses are survivable and upside is large |

### Step 3: Set Tolerance Thresholds

Translate appetite into measurable boundaries.

#### Financial Tolerance

| Metric | Threshold | Breach Response |
|--------|:---------:|----------------|
| Maximum single-event loss | $[X]M or [X]% of revenue | Immediate executive escalation; incident review |
| Maximum annual aggregate loss | $[X]M or [X]% of EBITDA | Board notification; strategy review |
| Minimum liquidity reserve | $[X]M or [X] months of operating expenses | CFO escalation; trigger cost-reduction measures |
| Maximum revenue concentration (single customer) | [X]% of total revenue | Sales strategy to diversify; board awareness |
| Maximum capital at risk in single initiative | $[X]M or [X]% of available capital | Investment committee approval required |

#### Operational Tolerance

| Metric | Threshold | Breach Response |
|--------|:---------:|----------------|
| Maximum service downtime | [X] hours per [quarter/year] | Incident review; engineering investment decision |
| Maximum data loss event | [X] records or [X] hours of data | Immediate incident response; regulatory assessment |
| Customer-impacting incidents per quarter | [N] | Operational review; root cause analysis program |
| Employee safety incidents per year | [N] | Safety program escalation; OSHA compliance review |
| Supply chain single-point-of-failure | 0 for critical inputs | Diversification requirement; backup supplier onboarding |

#### Compliance Tolerance

| Metric | Threshold | Breach Response |
|--------|:---------:|----------------|
| Regulatory findings | Zero material findings | Immediate remediation; board notification |
| Audit observations open > 90 days | [N] maximum | Escalation to executive sponsor |
| Data privacy incidents | Zero unauthorized disclosures | Breach response protocol activation |
| Policy exceptions without approval | Zero | Disciplinary process; control improvement |

### Step 4: Define Key Risk Indicators (KRIs)

KRIs are leading metrics that signal when risk levels are approaching tolerance thresholds.

| KRI | Risk Category | Green (Normal) | Amber (Elevated) | Red (Breach Imminent) | Data Source | Frequency |
|-----|-------------|:--------------:|:----------------:|:--------------------:|-------------|:---------:|
| Customer concentration ratio | Financial | < 10% | 10-15% | > 15% | CRM / Finance | Monthly |
| Open critical vulnerabilities | Cyber | < 5 | 5-10 | > 10 | Vulnerability scanner | Weekly |
| Employee turnover rate | Operational | < 12% | 12-18% | > 18% | HRIS | Monthly |
| Cash runway | Financial | > 12 months | 6-12 months | < 6 months | Finance | Monthly |
| Overdue audit findings | Compliance | 0 | 1-3 | > 3 | Audit tracker | Monthly |
| System uptime | Technology | > 99.9% | 99.5-99.9% | < 99.5% | Monitoring | Real-time |
| NPS score | Reputational | > 50 | 30-50 | < 30 | Survey platform | Quarterly |
| Regulatory change pipeline | Compliance | < 3 pending | 3-5 pending | > 5 pending | Regulatory tracker | Monthly |
| Incident response time | Operational | < 15 min | 15-60 min | > 60 min | Incident platform | Per event |
| Vendor risk score (critical vendors) | Operational | Green | Amber | Red | Vendor risk platform | Quarterly |

### Step 5: Design Escalation and Governance

#### Escalation Matrix

| KRI Status | Decision Authority | Required Actions | Reporting |
|:----------:|-------------------|-----------------|-----------|
| **Green** | Risk owner (operational) | Normal operations; continue monitoring | Standard reporting cadence |
| **Amber** | Department head + Risk manager | Investigate root cause; implement additional controls; increase monitoring frequency | Next scheduled risk report + alert to risk committee |
| **Red** | Executive team + Board risk committee | Immediate mitigation actions; allocate emergency resources; formal incident response if needed | Immediate notification to executive sponsor; board briefing within 48 hours |
| **Threshold breached** | Board + CEO | Crisis response activation; strategic review; potential disclosure obligations | Emergency board meeting; regulatory notification if required |

#### Governance Structure

| Body | Composition | Responsibility | Frequency |
|------|-----------|---------------|-----------|
| **Board Risk Committee** | Board members (min 3) | Approve risk appetite; review top risks; oversee framework effectiveness | Quarterly |
| **Executive Risk Council** | C-suite + Risk function | Set operational tolerance; review KRIs; approve risk responses | Monthly |
| **Risk Function** | CRO / Risk Manager + analysts | Maintain framework; monitor KRIs; produce reports; facilitate assessments | Ongoing |
| **Business Unit Risk Owners** | Department heads | Own specific risks; implement controls; report status | Monthly |

### Step 6: Produce the Framework Document

## Output Format

```markdown
## Risk Appetite Framework: [Organization]

### Purpose and Scope
[Why this framework exists and what it covers]

### Risk Appetite Statement
[Board-approved statement by risk category]

### Tolerance Thresholds
#### Financial Tolerances
[Metric, threshold, breach response table]

#### Operational Tolerances
[Metric, threshold, breach response table]

#### Compliance Tolerances
[Metric, threshold, breach response table]

### Key Risk Indicators
| KRI | Category | Green | Amber | Red | Source | Frequency |

### Escalation Matrix
| Status | Authority | Actions | Reporting |

### Governance
| Body | Composition | Responsibility | Frequency |

### Integration with Business Processes
| Process | How Risk Appetite Applies |
|---------|-------------------------|
| Strategic planning | New initiatives assessed against appetite before approval |
| Capital allocation | Investments scored against risk-return within tolerance |
| Product development | Risk assessment required at stage gates |
| Vendor selection | Vendor risk must fall within operational tolerance |
| M&A evaluation | Target risk profile compared to appetite |

### Review and Update Cycle
- Annual full review: [Month]
- Trigger-based review: Material business change, major incident, regulatory change
- Approval authority: Board Risk Committee

### Appendices
- A: Risk appetite statement (board-approved version)
- B: KRI dashboard template
- C: Escalation notification templates
- D: Glossary of risk terms
```

## Quality Checklist

- [ ] Risk appetite is aligned with strategic objectives — not set in isolation
- [ ] Appetite levels vary by category — a single "we are risk-averse" statement is insufficient
- [ ] Tolerances are quantified with specific thresholds, not just qualitative descriptions
- [ ] KRIs are leading indicators with defined green/amber/red ranges
- [ ] Escalation matrix specifies who decides, what they must do, and how fast
- [ ] Framework is integrated into business decisions (strategy, investment, vendor, product)
- [ ] Review cycle is defined with both scheduled and trigger-based updates

## Edge Cases

- **Board disagrees on appetite level**: Facilitate a structured discussion using scenario analysis — "If X happened, would we accept that outcome?" to find the true boundary
- **Appetite needs to differ by business unit**: Create a cascading framework — enterprise-level appetite with business-unit-specific tolerances that must stay within the enterprise envelope
- **High-growth startup with high inherent risk**: Focus appetite on the risks that are truly existential (cash, regulatory, reputation) while accepting higher tolerance for strategic and operational risks
- **Post-incident appetite recalibration**: After a major incident, resist reactive over-tightening — use the incident to inform the framework but maintain strategic balance
- **Regulatory-mandated risk appetite (financial services)**: Ensure the framework meets regulatory expectations (e.g., OCC, PRA, APRA guidance) including documentation, board approval, and integration evidence
- **Risk appetite for emerging technologies (AI, crypto)**: Define appetite as a range rather than a fixed point — acknowledge uncertainty and commit to frequent reassessment as the technology and regulatory landscape matures
