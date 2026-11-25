---
name: esg-report
description: >
  Create comprehensive ESG reports with framework alignment (GRI, SASB, TCFD), materiality assessment,
  metric collection, narrative writing, and stakeholder communication.
  TRIGGER when: user says /esg-report, "ESG report", "sustainability report", "ESG disclosure", "GRI report", "SASB report".
argument-hint: "[reporting-period] [framework] [audience]"
user-invocable: true
---

# ESG Report

Produce a credible, framework-aligned Environmental, Social, and Governance (ESG) report that meets stakeholder expectations and regulatory requirements.

---

## Input Gathering

| Input                          | Description                                                   | Required |
|--------------------------------|---------------------------------------------------------------|----------|
| Reporting period               | Fiscal year or calendar year covered                          | Yes      |
| Target framework(s)            | GRI, SASB, TCFD, ISSB/IFRS S1-S2, CDP, or custom            | Yes      |
| Prior year report              | Previous ESG report for trend comparison                       | Yes      |
| Materiality assessment results | Prioritized ESG topics from stakeholder engagement            | Yes      |
| Data collection package        | Environmental, social, and governance metrics                  | Yes      |
| Industry classification        | SASB industry, GICS sector for relevant disclosures           | No       |
| Stakeholder feedback           | Investor requests, rating agency questionnaires               | No       |

---

## Step-by-Step Process

### Step 1 — Framework Selection and Gap Analysis

Map current disclosures against target frameworks:

| Framework | Focus Area              | Audience           | Key Requirement                        |
|-----------|------------------------|--------------------|----------------------------------------|
| GRI       | Broad stakeholder impact| All stakeholders   | Universal + Topic Standards, materiality|
| SASB      | Financially material ESG| Investors          | Industry-specific metrics               |
| TCFD      | Climate risk/opportunity| Investors, lenders | Governance, Strategy, Risk Mgmt, Metrics|
| ISSB (IFRS S1/S2) | Sustainability-related financial | Investors | Enterprise value focus, climate first  |
| CDP       | Climate, water, forests | Investors, buyers  | Questionnaire-based scoring             |

Conduct a gap analysis: for each required disclosure, identify whether data is available, partially available, or missing. Prioritize closing gaps for material topics.

### Step 2 — Materiality Assessment

Conduct or refresh a double materiality assessment:

| Step                         | Method                                              |
|------------------------------|-----------------------------------------------------|
| Identify ESG topics          | Use GRI sector standards + SASB industry list       |
| Assess impact materiality    | Stakeholder surveys, interviews, peer benchmarking  |
| Assess financial materiality | Revenue risk, cost exposure, regulatory probability  |
| Plot materiality matrix      | X = financial materiality, Y = impact materiality   |
| Validate with leadership     | Board or C-suite sign-off on priority topics        |

Material topics drive report content, metrics, and narrative depth. Report boundary (operations, supply chain, products) should be defined for each material topic.

### Step 3 — Data Collection and Validation

Organize data collection by ESG pillar:

**Environmental**:
| Metric                          | Unit           | Source                | Validation Method      |
|---------------------------------|----------------|-----------------------|------------------------|
| GHG emissions (Scope 1, 2, 3)  | tCO2e          | Utility bills, EFs    | Third-party assurance  |
| Energy consumption              | MWh            | Meter readings        | Utility cross-check    |
| Water withdrawal                | Megaliters     | Meter / invoices      | Facility reconciliation|
| Waste generated / diverted      | Metric tons    | Waste hauler reports  | Manifest audit         |

**Social**:
| Metric                          | Unit           | Source                | Validation Method      |
|---------------------------------|----------------|-----------------------|------------------------|
| Total workforce / diversity     | Headcount, %   | HRIS                  | HR audit               |
| Recordable injury rate (TRIR)   | Per 200K hours | EHS system            | OSHA log reconciliation|
| Employee engagement score       | %              | Survey platform       | Response rate check    |
| Community investment            | $              | Finance / CSR records | Grant agreement audit  |

**Governance**:
| Metric                          | Unit           | Source                | Validation Method      |
|---------------------------------|----------------|-----------------------|------------------------|
| Board independence              | %              | Board charter         | Proxy statement        |
| Board diversity (gender, ethnic)| %              | Board records         | Self-identification    |
| Ethics violations reported      | Count          | Hotline / compliance  | Case management system |
| Data breaches                   | Count          | IT security           | Incident log           |

Implement data owner sign-off for every metric before inclusion.

### Step 4 — Narrative Writing

Structure the report following framework guidance:

| Section                    | Content                                                         | Length Guide   |
|----------------------------|-----------------------------------------------------------------|----------------|
| CEO / Chair letter         | Tone-setting, key achievements, forward look                    | 1-2 pages      |
| About the company          | Business model, value chain, ESG governance structure            | 2-3 pages      |
| Materiality and strategy   | Material topics, ESG strategy, targets, progress                 | 3-5 pages      |
| Environmental performance  | Climate, energy, water, waste, biodiversity                      | 5-10 pages     |
| Social performance         | Workforce, health & safety, DEI, community, human rights         | 5-10 pages     |
| Governance performance     | Board oversight, ethics, risk management, data privacy           | 3-5 pages      |
| Performance data tables    | Multi-year metrics with methodological notes                     | 3-5 pages      |
| Framework index            | GRI Content Index, SASB Index, TCFD mapping                      | 2-5 pages      |

Write in third person, present tense. Balance achievements with transparency about challenges and areas for improvement. Avoid greenwashing; support claims with data.

### Step 5 — Review, Assurance, and Approval

| Review Stage              | Reviewer                    | Focus                                  |
|---------------------------|-----------------------------|----------------------------------------|
| Technical review          | Subject matter experts      | Data accuracy, methodology consistency |
| Legal review              | General counsel             | Claims, forward-looking statements     |
| Communications review     | Corporate comms / marketing | Tone, brand alignment, readability     |
| External assurance        | Third-party auditor         | Limited or reasonable assurance on data|
| Executive approval        | C-suite / Board committee   | Final sign-off                         |

Obtain at minimum limited assurance on Scope 1 and 2 GHG emissions and key social metrics.

### Step 6 — Publication and Stakeholder Communication

- Publish the report in PDF and interactive web formats.
- Submit to relevant platforms: CDP questionnaire, DJSI, MSCI, ISS, Sustainalytics.
- Brief investor relations, sales, and customer success teams on key messages.
- Respond proactively to ESG rating agency inquiries using report data.
- Archive data and methodology notes for year-over-year comparability.
- Schedule a post-publication retrospective to improve next cycle.

---

## Output Format

```
## ESG Report Plan — [Company] — [Reporting Period]

### Scope and Framework Alignment
- Primary framework(s): [GRI / SASB / TCFD / ISSB]
- Reporting boundary: [operations, supply chain, products]
- Assurance level: [limited / reasonable]

### Materiality Matrix Summary
| Priority | Topic                    | Impact Materiality | Financial Materiality |
|----------|--------------------------|--------------------|-----------------------|
| High     | ...                      | ...                | ...                   |
| High     | ...                      | ...                | ...                   |
| Medium   | ...                      | ...                | ...                   |

### Data Collection Status
| Pillar         | Metrics Required | Data Available | Gaps | Gap Closure Plan |
|----------------|------------------|----------------|------|------------------|
| Environmental  | ...              | ...            | ...  | ...              |
| Social         | ...              | ...            | ...  | ...              |
| Governance     | ...              | ...            | ...  | ...              |

### Report Outline
1. [Section — owner — draft deadline]
2. ...

### Review and Publication Timeline
| Milestone                | Date       | Owner           |
|--------------------------|------------|-----------------|
| Data collection complete | ...        | ...             |
| First draft              | ...        | ...             |
| Legal review             | ...        | ...             |
| External assurance       | ...        | ...             |
| Board approval           | ...        | ...             |
| Publication              | ...        | ...             |

### Key Messages
- [3-5 headline messages for stakeholder communication]
```

---

## Quality Checklist

- [ ] Materiality assessment conducted or refreshed within the last 2 years
- [ ] All material topics covered with quantitative metrics and narrative
- [ ] Data validated by data owners and cross-checked against source systems
- [ ] Year-over-year trends provided for all key metrics
- [ ] Methodology notes included for calculated metrics (e.g., emission factors)
- [ ] Framework index maps every required disclosure to report content
- [ ] Legal review completed; no unsubstantiated claims
- [ ] External assurance obtained on priority metrics
- [ ] Report accessible in multiple formats (PDF, web, data download)
- [ ] Stakeholder communication plan activated on publication

---

## Edge Cases

- **First-time ESG report with no baseline data**: Start with a limited scope focused on the most material topics; clearly state the reporting boundary and commit to expanding scope in future years.
- **Operating in multiple jurisdictions with different regulations**: Map regulatory requirements (EU CSRD, SEC Climate, Singapore SGX) per jurisdiction; align to the most stringent standard as the baseline.
- **Acquired company with different ESG maturity**: Define a boundary approach (e.g., include acquisitions after 12 months of ownership); disclose the integration timeline transparently.
- **Stakeholders requesting different frameworks**: Produce a consolidated report referencing multiple frameworks via content indices; prioritize based on investor and regulatory requirements.
- **Incomplete Scope 3 emissions data**: Disclose the categories calculated and those excluded with rationale; use industry benchmarks or spend-based estimates for initial reporting and commit to improving data quality.
- **ESG rating agency methodology changes mid-cycle**: Monitor methodology updates from MSCI, Sustainalytics, CDP annually; adjust data collection to capture newly weighted metrics before the next submission.
