---
name: green-procurement
description: >
  Implement green procurement practices including environmental criteria definition, supplier
  assessment, lifecycle analysis, certification requirements, and impact tracking.
  TRIGGER when: user says /green-procurement, "green procurement", "sustainable procurement", "eco-friendly sourcing", "sustainable purchasing", "green supply chain".
argument-hint: "[category] [spend-threshold] [certification-standard]"
user-invocable: true
---

# Green Procurement

Integrate environmental and social criteria into procurement decisions to reduce supply chain impact, meet regulatory requirements, and drive market transformation.

---

## Input Gathering

| Input                          | Description                                                     | Required |
|--------------------------------|-----------------------------------------------------------------|----------|
| Procurement spend data         | Category spend, supplier list, volumes by commodity             | Yes      |
| Current procurement policies   | Existing sourcing guidelines, approved supplier lists           | Yes      |
| Environmental priorities       | Carbon, water, waste, biodiversity, chemicals of concern        | Yes      |
| Regulatory requirements        | Mandatory green procurement rules by jurisdiction               | Yes      |
| Supplier environmental data    | Certifications, emissions data, environmental management systems| No       |
| Product lifecycle data         | LCA studies, environmental product declarations (EPDs)          | No       |
| Organizational sustainability targets | Corporate net-zero, zero-waste, or circularity goals     | No       |

---

## Step-by-Step Process

### Step 1 — Spend Analysis and Category Prioritization

Identify the highest-impact procurement categories:

| Category               | Annual Spend | Environmental Hotspot         | Prioritization Score |
|------------------------|-------------|-------------------------------|:--------------------:|
| Raw materials          | $...        | Extraction, emissions, water  | High                 |
| Energy                 | $...        | GHG emissions (Scope 2)      | High                 |
| Packaging              | $...        | Waste, plastics, deforestation| High                 |
| Logistics / transport  | $...        | GHG emissions, air quality    | High                 |
| IT equipment           | $...        | E-waste, conflict minerals    | Medium               |
| Office supplies        | $...        | Paper, single-use plastics    | Low                  |
| Facilities / MRO       | $...        | Chemicals, energy, water      | Medium               |
| Professional services  | $...        | Limited direct impact          | Low                  |

Prioritize categories by: environmental impact magnitude x spend volume x influence ability. Focus on the top 5-10 categories that represent 80% of environmental impact.

### Step 2 — Environmental Criteria Development

Define green criteria for priority categories:

| Criteria Type           | Examples                                                       | Application        |
|-------------------------|----------------------------------------------------------------|--------------------|
| Mandatory (pass/fail)   | Regulatory compliance, banned substance free, no deforestation | All suppliers      |
| Weighted (scored)       | Carbon intensity, recycled content %, water efficiency          | Bid evaluation     |
| Preferential            | Certified organic, circular design, carbon neutral              | Tie-breaking       |
| Aspirational            | Science-based targets, cradle-to-cradle, net positive          | Supplier development|

Build category-specific scorecards:

| Criterion (example: Packaging) | Weight | Measurement                     | Scoring Scale      |
|--------------------------------|--------|---------------------------------|--------------------|
| Recycled content               | 25%    | % post-consumer recycled        | 0-100% = 0-5 pts  |
| Recyclability                  | 20%    | % recyclable in standard stream | 0-100% = 0-5 pts  |
| Carbon footprint               | 20%    | kg CO2e per unit                | Benchmark vs peers |
| Certified sustainable sourcing | 15%    | FSC, SFI, or equivalent        | Yes/No = 5/0 pts   |
| Supplier environmental mgmt    | 10%    | ISO 14001 or equivalent         | Certified = 5 pts  |
| Innovation / circularity       | 10%    | Reuse, refill, take-back model  | Qualitative 0-5    |

### Step 3 — Supplier Environmental Assessment

Evaluate existing and prospective suppliers:

| Assessment Level       | Method                                | Scope                  | Frequency  |
|------------------------|---------------------------------------|------------------------|------------|
| Self-assessment        | Questionnaire on environmental mgmt   | All priority suppliers | Annual     |
| Desktop review         | Public disclosures, certifications    | Top 50% by spend       | Annual     |
| On-site audit          | Environmental compliance, practices   | Strategic suppliers    | Biennial   |
| Third-party rating     | EcoVadis, CDP Supply Chain, Sedex     | Top 20% by spend       | Annual     |

Key assessment areas:
- **Environmental management system**: ISO 14001 or equivalent certified?
- **GHG emissions**: Does the supplier measure and report? What is the trajectory?
- **Water stewardship**: Water-intensive operations? Water stress areas? Reduction targets?
- **Waste and circularity**: Waste diversion rate? Circular design principles?
- **Chemical management**: Compliance with REACH, RoHS, TSCA? Substance restriction list?
- **Biodiversity**: Operations near sensitive ecosystems? Deforestation-free sourcing?

### Step 4 — Lifecycle Analysis Integration

Incorporate lifecycle thinking into procurement decisions:

| Lifecycle Stage        | Cost / Impact Factors                         | Data Source                     |
|------------------------|-----------------------------------------------|---------------------------------|
| Raw material extraction| Resource depletion, habitat impact, emissions  | LCA databases (ecoinvent, GaBi)|
| Manufacturing          | Energy, water, waste, chemical use             | Supplier data, EPDs             |
| Transportation         | Distance, mode, fuel type, packaging           | Logistics data, EFs             |
| Use phase              | Energy consumption, maintenance, consumables   | Product specifications          |
| End of life            | Recyclability, disposal impact, recovery value | Waste management data           |

Apply Total Cost of Ownership (TCO) including environmental externalities:
- TCO = Purchase price + Operating cost + Environmental cost + Disposal cost
- Environmental cost = Carbon price x lifecycle emissions + waste management + water use

Compare alternatives on TCO, not just unit price. Document when the green option costs more and quantify the environmental benefit per dollar of premium.

### Step 5 — Certification and Standards Requirements

Map relevant certifications by category:

| Category          | Recognized Certifications                              | Verification                  |
|-------------------|--------------------------------------------------------|-------------------------------|
| Paper / wood      | FSC, PEFC, SFI                                         | Chain of custody certificate  |
| Food / agriculture| USDA Organic, Rainforest Alliance, Fair Trade           | Annual audit certificate      |
| Electronics       | EPEAT, Energy Star, TCO Certified                      | Registry verification         |
| Cleaning products | Green Seal, EPA Safer Choice, EU Ecolabel              | Product label verification    |
| Textiles          | GOTS, OEKO-TEX, Bluesign                               | Certificate of compliance     |
| Building materials| LEED-compliant, Cradle to Cradle, GreenGuard           | Product documentation         |
| General suppliers | ISO 14001, EcoVadis, B Corp                            | Certificate or scorecard      |
| Carbon neutrality | PAS 2060, Climate Neutral, CarbonNeutral               | Verification statement        |

Require valid certification copies during onboarding and track expiration dates for renewal.

### Step 6 — Impact Tracking and Continuous Improvement

Measure and report on green procurement outcomes:

| Metric                                  | Formula / Measurement                          | Target            |
|-----------------------------------------|------------------------------------------------|-------------------|
| Green spend ratio                       | Green-certified spend / Total spend            | > 50% by [year]   |
| Supplier environmental score (avg)      | Weighted average of supplier assessment scores | > 3.5/5           |
| Scope 3 reduction from procurement      | tCO2e avoided through green choices            | [X]% YoY reduction|
| Recycled content rate                   | % recycled material in purchased goods         | > 30%             |
| Supplier certification rate             | % of top suppliers with ISO 14001 or equiv     | > 80%             |
| Cost premium / savings                  | Green option cost vs. conventional baseline     | Track and report  |

Build a quarterly reporting dashboard and integrate green procurement KPIs into procurement team performance reviews.

---

## Output Format

```
## Green Procurement Plan — [Organization] — [Categories]

### Executive Summary
- Categories prioritized: [count]
- Suppliers assessed: [count]
- Current green spend ratio: [%]
- Target green spend ratio: [%] by [year]
- Estimated Scope 3 reduction potential: [X] tCO2e

### Category Prioritization
| Category       | Spend   | Impact Score | Priority | Green Criteria Status |
|----------------|---------|:------------:|:--------:|:---------------------:|
| ...            | ...     | ...          | ...      | ...                   |

### Environmental Criteria (by Category)
| Category | Criterion          | Weight | Measurement           | Threshold     |
|----------|--------------------|--------|-----------------------|---------------|
| ...      | ...                | ...    | ...                   | ...           |

### Supplier Assessment Results
| Supplier | Category | EcoVadis/Score | ISO 14001 | GHG Reporting | Overall |
|----------|----------|:--------------:|:---------:|:-------------:|:-------:|
| ...      | ...      | ...            | ...       | ...           | ...     |

### TCO Comparison (Key Purchases)
| Item    | Conventional Price | Green Option Price | TCO (Conventional) | TCO (Green) | Delta |
|---------|--------------------|--------------------|---------------------|-------------|-------|
| ...     | ...                | ...                | ...                 | ...         | ...   |

### Implementation Roadmap
- Phase 1 (0-6 mo): [Policy update, criteria for top categories]
- Phase 2 (6-12 mo): [Supplier assessments, certification requirements]
- Phase 3 (12-24 mo): [Full rollout, TCO integration, impact reporting]

### Recommendations
1. [Prioritized actions]
```

---

## Quality Checklist

- [ ] Spend analysis completed and categories prioritized by environmental impact
- [ ] Environmental criteria defined for each priority category
- [ ] Criteria weighted and integrated into bid evaluation scorecards
- [ ] Supplier assessment covers environmental management, emissions, and certifications
- [ ] Lifecycle perspective applied (not just manufacturing stage)
- [ ] TCO model includes environmental cost alongside financial cost
- [ ] Recognized certifications identified and required for relevant categories
- [ ] Green spend tracking metric established and baselined
- [ ] Procurement team trained on green criteria and evaluation process
- [ ] Continuous improvement cadence set (annual criteria review, quarterly tracking)

---

## Edge Cases

- **Green option significantly more expensive (>20% premium)**: Quantify the environmental benefit per dollar of premium; explore volume commitments for better pricing; phase in requirements over 2-3 contract cycles to give suppliers time to scale.
- **No green-certified alternatives available in the market**: Engage top suppliers in development programs; set aspirational timelines; participate in industry consortia to drive market creation.
- **Small or local suppliers unable to afford certifications**: Accept equivalent practices with self-assessment and spot audits; offer co-investment in certification costs for strategic small suppliers.
- **Greenwashing risk (suppliers making unsubstantiated claims)**: Require third-party verified claims only; cross-reference certifications against registries; conduct periodic audits of claimed credentials.
- **Conflicting environmental objectives (e.g., lighter packaging increases waste but reduces transport emissions)**: Use lifecycle analysis to identify the net-best option; document tradeoffs transparently; prioritize the objective most aligned with corporate sustainability targets.
- **Regulatory divergence across geographies**: Build a compliance matrix by jurisdiction; design procurement criteria that meet the most stringent applicable standard; monitor regulatory evolution for upcoming requirements.
