---
name: customer-segmentation
description: >
  Build customer segments — behavioral, demographic, psychographic, and needs-based
  segmentation with persona creation and targeting strategy.
  TRIGGER when: user says /customer-segmentation, "segment our customers", "build customer personas",
  "customer segmentation", "targeting strategy", "who are our customers", or "audience segmentation".
argument-hint: "[data sources, segmentation criteria, product, or market]"
user-invocable: true
---

# Customer Segmentation

You are a customer analytics strategist. Build actionable customer segments using
behavioral, demographic, psychographic, and needs-based dimensions. Translate
segments into personas, targeting strategies, and differentiated experience plans
that product, marketing, sales, and CX teams can execute against.

## Process

### Step 1: Define Segmentation Objectives

| Parameter | Description |
|-----------|-------------|
| **Business objective** | Personalize marketing, optimize pricing, reduce churn, prioritize product features, improve CX |
| **Segmentation type** | Behavioral, demographic, psychographic, needs-based, value-based, or hybrid |
| **Data available** | CRM, product usage, transactions, surveys, third-party enrichment |
| **Customer base size** | Total customers or prospects to segment |
| **Current segmentation** | Existing segments and their limitations |
| **Target segment count** | 3-7 segments (fewer is usually more actionable) |

### Step 2: Select Segmentation Dimensions

#### Dimension Framework

| Category | Dimensions | Data Source | Actionability |
|----------|-----------|-------------|--------------|
| **Demographic** | Company size, industry, geography, revenue, employee count | CRM, firmographic data | Medium — stable but broad |
| **Behavioral** | Product usage frequency, feature adoption, purchase patterns, support interactions | Product analytics, CRM | High — directly observable |
| **Value-based** | ARR, LTV, expansion potential, cost to serve, margin | Finance, CRM | High — directly tied to revenue |
| **Needs-based** | Jobs to be done, desired outcomes, problems to solve | Surveys, interviews, sales notes | High — drives product and messaging |
| **Psychographic** | Technology adoption curve, risk tolerance, decision-making style | Surveys, behavioral inference | Medium — hard to measure at scale |
| **Engagement** | NPS, CSAT, community participation, event attendance, content consumption | Surveys, marketing automation | Medium — lagging indicator |

#### Recommended Dimension Combinations

| Objective | Primary Dimension | Secondary Dimension | Tertiary Dimension |
|-----------|------------------|--------------------|--------------------|
| Product roadmap | Needs-based | Behavioral (usage) | Value-based (ARR) |
| Marketing personalization | Behavioral (engagement) | Demographic (industry) | Psychographic |
| Pricing optimization | Value-based (willingness to pay) | Needs-based (use case) | Demographic (size) |
| Churn prevention | Behavioral (usage trends) | Value-based (ARR at risk) | Engagement (NPS) |
| Sales prioritization | Value-based (LTV potential) | Behavioral (buying signals) | Demographic (fit) |

### Step 3: Build Segments

For each segment, define clear boundaries and characteristics.

| Segment | Size | % of Base | Avg. ARR | Key Behaviors | Primary Need | Engagement Level |
|---------|:----:|:---------:|:--------:|--------------|-------------|:----------------:|
| Power Users | [N] | [%] | $[X] | Daily use, all features, API integrations | Advanced capabilities, customization | High |
| Growth Seekers | [N] | [%] | $[X] | Expanding usage, adding seats, exploring features | Scalability, team collaboration | High |
| Steady Operators | [N] | [%] | $[X] | Consistent use of core features, low expansion | Reliability, simplicity, value | Medium |
| At-Risk | [N] | [%] | $[X] | Declining usage, support escalations, late renewals | Problem resolution, proven ROI | Low |
| New / Onboarding | [N] | [%] | $[X] | Setup phase, learning features, early questions | Quick time to value, guidance | Medium |

**Segment validation criteria:**

| Criterion | Description | Test |
|-----------|-------------|------|
| **Measurable** | Can you identify who is in each segment? | Data query returns clean lists |
| **Substantial** | Is the segment large enough to justify differentiated treatment? | Minimum 5-10% of base or $X revenue |
| **Accessible** | Can you reach the segment through your channels? | Marketing, sales, or product can target them |
| **Differentiable** | Do segments respond differently to the same treatment? | A/B test shows different conversion rates |
| **Actionable** | Can you design a different strategy for each segment? | Team can articulate distinct approach |

### Step 4: Create Personas

For each segment, build a representative persona.

#### Persona Template

```
### Persona: [Name] — [Segment Label]

**Demographics**
- Role: [Job title]
- Company: [Size, industry, stage]
- Reports to: [Title]
- Team size: [N]

**Goals**
- Primary: [What they are trying to accomplish]
- Secondary: [Supporting objectives]

**Pain Points**
- [Pain 1]: [Impact on their work]
- [Pain 2]: [Impact on their work]
- [Pain 3]: [Impact on their work]

**Behaviors**
- Product usage: [Frequency, features used, depth]
- Buying process: [Self-serve, sales-assisted, committee]
- Information sources: [Where they learn about solutions]
- Decision criteria: [What matters most — price, features, support, brand]

**Messaging That Resonates**
- Lead with: [Value proposition that speaks to their primary goal]
- Prove with: [Evidence type — case studies, data, demos, testimonials]
- Avoid: [Messaging that alienates this persona]

**Preferred Channels**
- Marketing: [Email, webinars, content, events, social]
- Sales: [Self-serve, inside sales, field sales, partner]
- Support: [Self-service, chat, phone, dedicated CSM]
```

### Step 5: Design Targeting Strategy

Map each segment to differentiated strategies across functions.

| Dimension | Power Users | Growth Seekers | Steady Operators | At-Risk | New / Onboarding |
|-----------|------------|----------------|-----------------|---------|-------------------|
| **Product** | Beta access, API, advanced features | Collaboration, scaling tools | Core reliability, simplicity | Stability, bug fixes | Onboarding wizard, templates |
| **Marketing** | Technical content, community | Growth stories, ROI calculators | Tips and best practices | Win-back campaigns | Getting started guides |
| **Sales** | Upsell enterprise features | Expand seats and use cases | Retain with value review | Save plays, executive outreach | Onboarding calls |
| **Support** | Dedicated TAM, priority queue | Proactive CSM check-ins | Self-service, knowledge base | Urgent intervention | High-touch onboarding |
| **Pricing** | Premium tier, custom contracts | Volume discounts, growth pricing | Standard pricing, long-term lock | Discount or flex terms | Trial extension, starter pricing |

### Step 6: Document and Operationalize

## Output Format

```markdown
## Customer Segmentation: [Product / Market]

### Segmentation Summary
- **Base size**: [N] customers
- **Segments**: [N] segments
- **Primary dimension**: [Behavioral / Value / Needs]
- **Data sources**: [List]

### Segment Profiles
| Segment | Size | Revenue Share | Growth Trend | Key Differentiator |

### Detailed Personas
[Full persona for each segment]

### Targeting Strategy Matrix
[Function x Segment strategy table]

### Segment Migration Paths
[How customers move between segments — desired and undesired transitions]
| From | To | Trigger | Desired? | Action to Encourage/Prevent |

### Measurement Plan
| Metric | Segment | Current | Target | Tracking Method |
|--------|---------|---------|--------|----------------|
| Retention rate | At-Risk | [%] | [%] | Monthly cohort analysis |
| Expansion revenue | Growth Seekers | $[X] | $[X] | Quarterly pipeline review |
| Onboarding completion | New | [%] | [%] | Product analytics |

### Implementation Roadmap
| Phase | Action | Segments Affected | Owner | Timeline |
|-------|--------|------------------|-------|----------|

### Governance
- Segmentation refresh cadence: [Quarterly / Semi-annual]
- Data quality owner: [Role]
- Segment definition owner: [Role]
```

## Quality Checklist

- [ ] Segments are based on data, not intuition — dimensions are grounded in actual customer attributes
- [ ] Each segment passes the five validation criteria (measurable, substantial, accessible, differentiable, actionable)
- [ ] Personas include behaviors and needs, not just demographics
- [ ] Targeting strategy is differentiated — if every segment gets the same treatment, the segmentation is not useful
- [ ] Segment migration paths are mapped — segments are not static
- [ ] Segmentation is operationalized in systems (CRM, marketing automation, product) — not just in a slide deck
- [ ] Refresh cadence is defined to prevent staleness

## Edge Cases

- **Too few data points per customer**: Start with a simpler segmentation (e.g., 3 segments on one dimension) and add complexity as data matures
- **One segment is 80% of the base**: Either the segmentation is too coarse, or the business genuinely has a dominant use case — validate with behavioral sub-segmentation
- **B2B accounts with multiple personas inside**: Segment at both account level (firmographic/value) and user level (behavioral/needs)
- **Rapidly changing customer base**: Increase segmentation refresh frequency; use real-time behavioral signals rather than static demographics
- **Segments that overlap significantly**: Rethink dimension selection — overlapping segments suggest the dimensions are correlated, not independent
- **New market entry**: Use hypothesis-based segments initially; plan for rapid iteration as real customer data comes in
