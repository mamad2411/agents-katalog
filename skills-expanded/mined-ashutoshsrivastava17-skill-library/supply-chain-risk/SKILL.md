---
name: supply-chain-risk
description: >
  Assess supply chain risks including single-source dependencies, geographic concentration, disruption
  scenarios, mitigation strategies, and contingency planning.
  TRIGGER when: user says /supply-chain-risk, "supply chain risk", "disruption assessment", "supply risk analysis", "resilience assessment", "contingency plan".
argument-hint: "[scope/product-line] [risk-category] [scenario]"
user-invocable: true
---

# Supply Chain Risk Assessment

Identify, quantify, and mitigate supply chain vulnerabilities to build operational resilience against disruptions ranging from supplier failures to global crises.

---

## Input Gathering

| Input                         | Description                                                   | Required |
|-------------------------------|---------------------------------------------------------------|----------|
| Supply chain map              | Tier 1 and Tier 2+ suppliers, locations, dependencies         | Yes      |
| Bill of materials (BOM)       | Components, sources, lead times, alternate parts              | Yes      |
| Historical disruption log     | Past incidents, duration, financial impact, resolution        | Yes      |
| Supplier risk data            | Financial health, geographic risk, single-source flags        | Yes      |
| Revenue and margin data       | Product contribution to prioritize risk focus                 | No       |
| Insurance and contract terms  | Force majeure clauses, business interruption coverage         | No       |
| Geopolitical intelligence     | Trade policy changes, sanctions, tariff risks                 | No       |

---

## Step-by-Step Process

### Step 1 — Supply Chain Mapping and Dependency Analysis

Build a multi-tier supply chain map:

| Analysis Layer          | What to Map                                           | Tool / Method           |
|-------------------------|-------------------------------------------------------|-------------------------|
| Tier 1 suppliers        | Direct suppliers by commodity and spend               | ERP / procurement data  |
| Tier 2+ suppliers       | Sub-suppliers of critical Tier 1s                     | Supplier disclosure, databases |
| Geographic nodes        | Manufacturing sites, warehouses, ports, border crossings | Network mapping        |
| Logistics routes        | Primary and alternate shipping lanes                   | TMS / carrier data      |
| Information systems     | EDI connections, shared platforms, cloud dependencies   | IT architecture review  |

Identify single points of failure: any node whose removal would halt production or delivery.

### Step 2 — Risk Identification and Categorization

Catalog risks across six domains:

| Risk Domain          | Example Risks                                                | Typical Indicators                    |
|----------------------|--------------------------------------------------------------|---------------------------------------|
| Supplier risk        | Bankruptcy, quality failure, capacity shortfall              | Financial ratios, audit findings      |
| Demand risk          | Sudden demand spike/collapse, forecast error                 | Demand variability, market signals    |
| Operational risk     | Equipment failure, labor disruption, IT outage               | Maintenance logs, incident history    |
| Environmental risk   | Natural disaster, pandemic, climate events                   | Hazard maps, epidemiological data     |
| Geopolitical risk    | Trade wars, sanctions, regulatory changes, conflict          | Country risk indices, policy tracking |
| Cyber risk           | Ransomware, data breach, system compromise                   | Vulnerability scans, threat intel     |

For each risk, document the trigger event, affected nodes, and propagation path through the network.

### Step 3 — Risk Quantification

Score each identified risk using a probability-impact matrix:

**Probability Scale**:

| Rating | Probability | Description                           |
|--------|------------|---------------------------------------|
| 1      | < 5%       | Rare — unlikely in next 3 years       |
| 2      | 5-15%      | Unlikely — possible but not expected  |
| 3      | 15-40%     | Possible — could occur within 1 year  |
| 4      | 40-70%     | Likely — expected within 12 months    |
| 5      | > 70%      | Almost certain — imminent or recurring|

**Impact Scale**:

| Rating | Financial Impact   | Operational Impact                        |
|--------|--------------------|-------------------------------------------|
| 1      | < $100K            | Minor delay, no customer impact            |
| 2      | $100K - $1M        | Short delay, limited customer impact       |
| 3      | $1M - $10M         | Significant delay, some orders affected    |
| 4      | $10M - $50M        | Major disruption, widespread order delays  |
| 5      | > $50M             | Catastrophic, production halt, brand damage|

**Risk Score** = Probability x Impact (range: 1-25).

Classify: Low (1-5), Medium (6-12), High (13-19), Critical (20-25).

### Step 4 — Disruption Scenario Modeling

Develop and analyze 3-5 realistic disruption scenarios:

| Scenario                         | Duration   | Revenue Impact  | Recovery Time | Probability |
|----------------------------------|-----------|-----------------|---------------|-------------|
| Single critical supplier failure | 4-12 weeks| $X M            | 8-16 weeks    | Medium      |
| Port closure / logistics blockage| 2-6 weeks | $X M            | 4-8 weeks     | Medium      |
| Regional natural disaster        | 2-8 weeks | $X M            | 6-20 weeks    | Low-Medium  |
| Pandemic / workforce disruption  | 8-26 weeks| $X M            | 12-52 weeks   | Low         |
| Cyber attack on key system       | 1-4 weeks | $X M            | 2-8 weeks     | Medium      |

For each scenario, model the cascading effects through the supply chain: which products are affected, which customers impacted, and what is the time-phased financial exposure.

### Step 5 — Mitigation Strategy Development

Define mitigation actions mapped to the highest-priority risks:

| Strategy                    | Applicable Risks              | Investment Level | Risk Reduction |
|-----------------------------|-------------------------------|-----------------|----------------|
| Dual / multi-sourcing       | Supplier failure, capacity    | Medium          | High           |
| Safety stock buffering      | Demand, supplier, logistics   | Medium          | Medium         |
| Near-shoring / reshoring    | Geopolitical, logistics       | High            | High           |
| Contractual protections     | Supplier, compliance          | Low             | Medium         |
| Supplier development        | Quality, capacity             | Medium          | Medium         |
| Digital supply chain twin   | All operational risks         | High            | Medium-High    |
| Insurance / hedging         | Environmental, financial      | Low-Medium      | Medium         |
| Inventory pre-positioning   | Logistics, environmental      | Medium          | Medium         |

Assign each mitigation an owner, budget, and implementation timeline.

### Step 6 — Contingency Planning and Response Playbooks

Create actionable playbooks for each critical scenario:

| Playbook Component         | Content                                                     |
|----------------------------|-------------------------------------------------------------|
| Trigger criteria           | Specific conditions that activate the playbook               |
| Incident commander         | Named role with decision authority                          |
| Communication plan         | Internal escalation + customer/partner notification          |
| Immediate actions (0-48h)  | Secure supply, activate alternates, assess scope             |
| Short-term actions (1-4 wk)| Reallocate inventory, expedite alternatives, manage demand   |
| Recovery actions (1-6 mo)  | Qualify new sources, rebuild buffer, root cause analysis      |
| Post-incident review       | Lessons learned, playbook updates, metric recalibration      |

Test playbooks through tabletop exercises at least annually.

---

## Output Format

```
## Supply Chain Risk Assessment — [Scope] — [Date]

### Executive Summary
- Total risks identified: [count]
- Critical risks: [count] | High: [count] | Medium: [count] | Low: [count]
- Maximum single-event exposure: [$X M]
- Current resilience score: [X/100]
- Top 3 risks requiring immediate action: [list]

### Supply Chain Map Findings
- Single-source dependencies: [count] ([% of critical components])
- Geographic concentration: [top 3 locations and % of supply]
- Tier 2+ visibility: [% mapped]

### Risk Register
| ID  | Risk Description          | Domain       | Probability | Impact | Score | Trend | Owner |
|-----|---------------------------|--------------|-------------|--------|-------|-------|-------|
| R01 | ...                       | ...          | ...         | ...    | ...   | ...   | ...   |
| R02 | ...                       | ...          | ...         | ...    | ...   | ...   | ...   |

### Scenario Analysis Summary
| Scenario                     | Exposure    | Recovery Time | Preparedness |
|------------------------------|-------------|---------------|--------------|
| ...                          | ...         | ...           | ...          |

### Mitigation Plan
| Risk ID | Mitigation Action           | Owner | Budget | Timeline   | Status |
|---------|-----------------------------|-------|--------|------------|--------|
| R01     | ...                         | ...   | ...    | ...        | ...    |

### Contingency Readiness
| Scenario            | Playbook Status | Last Tested | Next Exercise |
|---------------------|-----------------|-------------|---------------|
| ...                 | ...             | ...         | ...           |

### Recommendations
1. [Immediate actions — next 30 days]
2. [Short-term investments — next quarter]
3. [Strategic initiatives — next 12 months]
```

---

## Quality Checklist

- [ ] Supply chain mapped to at least Tier 2 for critical components
- [ ] All single-source dependencies identified and documented
- [ ] Risk register covers all six domains (supplier, demand, operational, environmental, geopolitical, cyber)
- [ ] Probability and impact scores based on data, not assumptions alone
- [ ] At least 3 disruption scenarios modeled with financial exposure estimates
- [ ] Mitigation strategies assigned to specific owners with budgets
- [ ] Contingency playbooks drafted for the top 3 critical scenarios
- [ ] Playbooks tested via tabletop exercise within the last 12 months
- [ ] Risk assessment reviewed and approved by senior leadership
- [ ] Monitoring cadence established: critical risks monthly, all risks quarterly

---

## Edge Cases

- **Complete lack of Tier 2+ visibility**: Use industry databases, supplier questionnaires, and third-party mapping services; start with the highest-spend Tier 1s and work backward.
- **Emerging risk with no historical precedent**: Use analogous events from other industries; conduct structured expert elicitation; apply scenario planning rather than probabilistic models.
- **Interconnected risks (cascading failure)**: Model dependencies between risks using fault trees or bow-tie analysis; a single event may trigger multiple simultaneous failures.
- **Global pandemic or systemic crisis**: Standard risk scoring underweights correlated, system-wide events; supplement with stress testing that assumes multiple simultaneous failures.
- **Supplier unwilling to disclose sub-tier information**: Invoke contractual transparency clauses; use third-party intelligence; treat opacity itself as a risk factor that raises the supplier's score.
- **Rapidly changing geopolitical environment**: Increase risk review frequency from quarterly to monthly; subscribe to real-time trade policy and sanctions alert services; pre-qualify alternative sources in stable regions.
