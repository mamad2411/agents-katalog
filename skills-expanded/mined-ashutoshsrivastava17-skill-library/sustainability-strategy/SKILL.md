---
name: sustainability-strategy
description: >
  Develop comprehensive sustainability strategies including baseline assessment, Science Based Targets
  goal setting, initiative prioritization, stakeholder engagement, and roadmap creation.
  TRIGGER when: user says /sustainability-strategy, "sustainability strategy", "ESG strategy", "sustainability roadmap", "net zero strategy", "sustainability plan".
argument-hint: "[organization-or-BU] [time-horizon] [focus-area]"
user-invocable: true
---

# Sustainability Strategy

Design and operationalize a sustainability strategy that creates measurable environmental and social impact while driving business value.

---

## Input Gathering

| Input                          | Description                                                    | Required |
|--------------------------------|----------------------------------------------------------------|----------|
| Business strategy              | Corporate strategy, growth plans, value proposition            | Yes      |
| Current sustainability state   | Existing programs, metrics, reports, certifications            | Yes      |
| Industry benchmarks            | Peer company strategies, sector commitments, best practices    | Yes      |
| Stakeholder expectations       | Investor, customer, employee, regulator, community priorities  | Yes      |
| Regulatory landscape           | Current and upcoming ESG regulations by jurisdiction           | No       |
| Resource constraints           | Budget, headcount, executive sponsorship availability          | No       |
| Materiality assessment         | Prioritized ESG topics from stakeholder engagement             | No       |

---

## Step-by-Step Process

### Step 1 — Baseline Assessment and Maturity Evaluation

Evaluate current sustainability maturity across five dimensions:

| Dimension            | Level 1: Ad Hoc     | Level 2: Developing | Level 3: Established | Level 4: Leading  | Level 5: Transformative |
|----------------------|----------------------|---------------------|----------------------|-------------------|-------------------------|
| Governance           | No formal ownership  | Designated lead     | Committee + policy   | Board oversight   | Integrated into all decisions |
| Measurement          | Minimal data         | Basic metrics       | Comprehensive KPIs   | Assured data      | Real-time dashboards    |
| Strategy             | Reactive             | Compliance-driven   | Goal-oriented        | Science-based     | Systems-change focused  |
| Integration          | Siloed               | Some dept. involvement | Cross-functional  | Embedded in ops   | Value chain wide        |
| Communication        | None                 | Internal only       | Annual report        | Multi-channel     | Thought leadership      |

Score each dimension (1-5) and identify the biggest gaps between current state and desired state.

### Step 2 — Goal Setting and Target Definition

Set targets at three levels:

**Aspirational Vision** (10-30 year):
- Net-zero emissions by [year]
- Zero waste to landfill
- 100% renewable energy
- Living wage across value chain

**Science-Based Targets** (5-10 year):
| Target Area          | Framework         | Example Target                              |
|----------------------|-------------------|---------------------------------------------|
| Climate              | SBTi 1.5C pathway | 42% absolute Scope 1+2 reduction by 2030    |
| Climate (Scope 3)    | SBTi              | 25% Scope 3 reduction by 2030               |
| Water                | SBTN (pilot)      | Context-based water targets per basin        |
| Nature               | SBTN / TNFD       | No net loss of biodiversity from operations  |
| Social               | Living wage, DEI   | 100% living wage by 2027                     |

**Operational Targets** (1-3 year):
- Annual milestones that ladder up to the 5-10 year targets.
- Specific, measurable, assignable, realistic, time-bound (SMART).

### Step 3 — Initiative Identification and Prioritization

Build and prioritize an initiative portfolio:

| Initiative                          | Impact (1-5) | Feasibility (1-5) | Cost      | Timeline   | Score |
|-------------------------------------|:------------:|:-----------------:|-----------|------------|:-----:|
| Renewable electricity procurement   | 5            | 4                 | Medium    | 6-12 mo    | 20    |
| Supplier engagement program         | 4            | 3                 | Medium    | 12-18 mo   | 12    |
| Circular packaging redesign         | 4            | 3                 | High      | 12-24 mo   | 12    |
| Employee sustainability training    | 3            | 5                 | Low       | 3-6 mo     | 15    |
| Fleet electrification               | 4            | 2                 | High      | 24-36 mo   | 8     |
| Water recycling systems             | 3            | 3                 | Medium    | 12-18 mo   | 9     |
| Community investment program        | 3            | 4                 | Low       | 6-12 mo    | 12    |
| Green building certification        | 3            | 3                 | High      | 18-24 mo   | 9     |

Score = Impact x Feasibility. Prioritize by quadrant: high-impact/high-feasibility first, then high-impact/lower-feasibility with phased rollout.

### Step 4 — Stakeholder Engagement Plan

Design engagement for each stakeholder group:

| Stakeholder      | Key Concerns                        | Engagement Method                   | Cadence        |
|------------------|-------------------------------------|-------------------------------------|----------------|
| Board / C-suite  | Risk, value creation, compliance    | Strategy presentations, dashboards  | Quarterly      |
| Investors        | Targets, progress, financial impact | ESG report, investor calls, ratings | Annual + ad hoc|
| Employees        | Purpose, culture, personal impact   | Training, champions network, surveys| Ongoing        |
| Customers        | Product sustainability, transparency| Labels, reports, co-innovation      | Ongoing        |
| Suppliers        | Requirements, capacity building     | Scorecards, workshops, audits       | Annual         |
| Regulators       | Compliance, disclosure              | Filings, engagement, industry groups| As required    |
| Communities      | Local impact, investment, jobs      | Partnerships, town halls, grants    | Semi-annual    |
| NGOs / advocacy  | Ambition, transparency, accountability| Partnerships, dialogue, reporting  | Annual         |

Identify sustainability champions within each stakeholder group to amplify messaging.

### Step 5 — Roadmap and Resource Planning

Build a phased implementation roadmap:

| Phase               | Timeline     | Focus                                          | Investment |
|---------------------|--------------|-------------------------------------------------|-----------|
| Foundation          | 0-6 months   | Governance, baseline measurement, quick wins    | Low       |
| Acceleration        | 6-18 months  | Priority initiatives, target publication, reporting | Medium |
| Transformation      | 18-36 months | Value chain engagement, innovation, deep decarbonization | High |
| Leadership          | 36+ months   | Systems change, advocacy, circular models        | Medium    |

For each phase, specify:
- Key deliverables and milestones
- Resource requirements (FTE, budget, technology)
- Dependencies and risks
- Success metrics

### Step 6 — Governance, Tracking, and Adaptive Management

Establish the operating model for ongoing strategy execution:

| Governance Element       | Detail                                                   |
|--------------------------|----------------------------------------------------------|
| Executive sponsor        | C-level owner (CSO, CFO, or COO)                        |
| Steering committee       | Cross-functional leaders, quarterly meetings             |
| Working groups           | Topic-specific teams (climate, social, governance)       |
| Performance dashboard    | Monthly KPI tracking against targets                     |
| Annual strategy review   | Refresh priorities based on progress and external changes|
| External advisory        | Sustainability advisory board or expert panel            |

Build feedback loops: if an initiative underperforms at the 12-month mark, reallocate resources or pivot. Apply adaptive management principles to respond to regulatory, market, and scientific developments.

---

## Output Format

```
## Sustainability Strategy — [Organization] — [Time Horizon]

### Executive Summary
- Current maturity score: [X/5]
- Vision: [aspirational statement]
- Key targets: [3-5 headline targets with years]
- Investment required: [$X over Y years]
- Expected outcomes: [environmental, social, business value]

### Maturity Assessment
| Dimension     | Current | Target (Year 1) | Target (Year 3) |
|---------------|---------|------------------|------------------|
| Governance    | ...     | ...              | ...              |
| Measurement   | ...     | ...              | ...              |
| Strategy      | ...     | ...              | ...              |
| Integration   | ...     | ...              | ...              |
| Communication | ...     | ...              | ...              |

### Targets
| Target Area   | Baseline | 2025 Target | 2030 Target | Framework |
|---------------|----------|-------------|-------------|-----------|
| ...           | ...      | ...         | ...         | ...       |

### Priority Initiatives
| # | Initiative                  | Impact | Phase   | Owner | Budget |
|---|-----------------------------|--------|---------|-------|--------|
| 1 | ...                         | ...    | ...     | ...   | ...    |

### Implementation Roadmap
- Foundation (0-6 mo): [key milestones]
- Acceleration (6-18 mo): [key milestones]
- Transformation (18-36 mo): [key milestones]
- Leadership (36+ mo): [key milestones]

### Stakeholder Engagement Summary
| Stakeholder | Priority Message | Channel | Cadence |
|-------------|------------------|---------|---------|
| ...         | ...              | ...     | ...     |

### Governance Model
- Executive sponsor: [name/role]
- Steering committee: [composition, cadence]
- Reporting: [dashboard, review cycle]

### Recommendations
1. [Immediate priorities]
2. [Strategic investments]
3. [Capability building needs]
```

---

## Quality Checklist

- [ ] Baseline assessment completed with data-backed maturity scores
- [ ] Targets aligned with recognized frameworks (SBTi, SBTN, SDGs)
- [ ] Strategy linked to business strategy and value creation narrative
- [ ] Initiatives prioritized using consistent criteria (impact, feasibility, cost)
- [ ] Stakeholder mapping covers all material groups with tailored engagement
- [ ] Roadmap phased realistically with dependencies identified
- [ ] Resource requirements specified (budget, FTE, technology)
- [ ] Governance model includes clear accountability and decision rights
- [ ] Adaptive management process built in for annual strategy refresh
- [ ] Quick wins identified to build momentum in the first 6 months

---

## Edge Cases

- **Small or mid-size company with limited sustainability resources**: Start with a focused strategy covering 3-5 most material topics; leverage industry associations and free tools (e.g., SME Climate Hub); combine sustainability roles with existing functions.
- **Company in a hard-to-abate sector (cement, steel, aviation)**: Acknowledge longer decarbonization timelines; invest in breakthrough technologies; engage in sector collaborations (e.g., First Movers Coalition); set aggressive intensity targets while managing absolute reduction pace.
- **Rapidly growing company where absolute emissions are increasing**: Set intensity targets alongside absolute targets; demonstrate decoupling of growth from environmental impact; use acquisition integration as an opportunity to uplift sustainability practices.
- **Company with operations primarily in developing economies**: Adapt targets to local context; invest in community development as a core pillar; address access-to-energy, water, and livelihoods; align with national climate commitments (NDCs).
- **Board or leadership skepticism about sustainability investment**: Build the business case with risk mitigation (regulatory, market access), cost savings (energy efficiency), and revenue opportunities (green products); start with ROI-positive initiatives.
- **Conflicting stakeholder priorities (e.g., cost reduction vs. sustainability investment)**: Use double materiality to show where sustainability and financial performance align; phase investments to balance short-term cost discipline with long-term value creation.
