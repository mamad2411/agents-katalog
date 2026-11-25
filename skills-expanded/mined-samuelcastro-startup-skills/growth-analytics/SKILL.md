---
name: growth-analytics
description: Guide founders through metrics frameworks, experimentation, and data-driven growth. Use when a founder says "help me set up my metrics framework", "what should my north star metric be?", "design an A/B test", "help me analyze retention/churn", "build me a dashboard to track growth", "how do I do cohort analysis?", "what metrics should I track?", "pirate metrics", "AARRR funnel", or needs to make sense of their growth data.
---

# Growth & Analytics

Guide founders from defining their first metrics (pre-launch) through sophisticated retention analysis and experimentation (post-launch).

## Workflow

### 1. Diagnose Current State

Ask: "Where are you in your analytics journey?"

| State | Signals | Next Step |
|-------|---------|-----------|
| **Pre-launch** | No users yet, needs to define what to track | → Step 2: Metrics Framework |
| **Early traction** | Has users, unclear what metrics matter | → Step 2: Metrics Framework |
| **Tracking basics** | Has metrics, needs North Star focus | → Step 2: North Star Selection |
| **Ready to experiment** | Solid metrics, wants to run tests | → Step 3: A/B Testing |
| **Retention concerns** | Users churning, needs analysis | → Step 4: Retention & Cohorts |
| **Dashboard needed** | Wants visibility for team/investors | → Step 5: Dashboard Design |

### 2. Metrics Framework

Build a metrics system that drives the right behavior. See `references/metrics-frameworks.md` for complete framework library.

#### AARRR Pirate Metrics

The universal startup funnel framework:

| Stage | Question | Example Metrics |
|-------|----------|-----------------|
| **Acquisition** | How do users find you? | Visitors, signups, CAC by channel |
| **Activation** | Do they have a great first experience? | Completed onboarding, "aha moment" reached |
| **Retention** | Do they come back? | DAU/MAU, D1/D7/D30 retention, churn |
| **Revenue** | Do they pay? | Conversion rate, ARPU, LTV |
| **Referral** | Do they tell others? | NPS, referral rate, viral coefficient |

**Stage-Appropriate Focus:**

| Stage | Primary Focus | Why |
|-------|---------------|-----|
| Pre-PMF | Activation + Retention | Nothing else matters if product doesn't stick |
| Post-PMF | Revenue + Acquisition | Time to scale what works |
| Growth | All five, plus efficiency | Optimize the full funnel |

#### North Star Metric

One metric that best captures core value delivered to customers.

**Selection Criteria:**
1. **Measures value** — Correlates with customers getting value
2. **Leading indicator** — Predicts future revenue/growth
3. **Actionable** — Team can influence it
4. **Simple** — Easy to understand and communicate

**North Star Examples by Business Model:**

| Model | North Star | Why |
|-------|------------|-----|
| **B2B SaaS** | Weekly Active Users, Features Used | Value = engagement with product |
| **Marketplace** | Transactions completed | Both sides getting value |
| **Subscription** | Weekly active subscribers | Retention predicts LTV |
| **E-commerce** | Repeat purchase rate | Loyalty = sustainable revenue |
| **Usage-based** | Monthly usage volume | Usage = revenue |
| **Social/Consumer** | DAU/MAU ratio | Engagement intensity |

**Supporting Metrics:**

Every North Star needs 3-5 supporting metrics that explain HOW to move it:

```
North Star: Weekly Active Teams (B2B SaaS)
├── Activation: Teams completing onboarding
├── Engagement: Features used per team
├── Expansion: Seats added per team
└── Retention: Team churn rate
```

#### One Metric That Matters (OMTM)

For early-stage focus, pick ONE metric for a defined period:

**OMTM Selection:**
1. What's the biggest constraint right now?
2. What metric would prove that constraint is solved?
3. Can you move it in 4-8 weeks?

**Examples:**
- Pre-launch: "Waitlist signups" (validate demand)
- Beta: "D7 retention" (validate stickiness)
- Post-launch: "Activation rate" (validate onboarding)
- Growth: "Payback period" (validate unit economics)

### 3. A/B Testing & Experimentation

Run experiments that generate reliable insights. See `references/ab-testing.md` for templates and calculators.

#### Experiment Design Framework

**Hypothesis Structure:**
```
If we [change], then [metric] will [improve/decrease] by [amount]
because [reason based on user insight].
```

**Example:**
> If we reduce signup form from 5 fields to 3 fields, then signup completion rate will increase by 15% because user research shows form length is the #1 drop-off reason.

#### Before Running Any Test

**Pre-flight Checklist:**

| Check | Question | Action |
|-------|----------|--------|
| **Sample size** | Do we have enough traffic? | Calculate minimum sample (see below) |
| **Duration** | How long to reach significance? | Usually 1-4 weeks minimum |
| **Metric clarity** | What exactly are we measuring? | Define primary + guardrail metrics |
| **Segment impact** | Should we segment results? | Pre-define segments (new vs returning, mobile vs desktop) |

**Sample Size Estimation:**

For 80% power and 95% confidence:
- 10% baseline, detect 10% relative lift → ~15,000 per variant
- 10% baseline, detect 20% relative lift → ~4,000 per variant
- 2% baseline, detect 20% relative lift → ~20,000 per variant

**Rule of thumb:** Multiply expected traffic by test duration. If you can't reach minimum sample in 4 weeks, the test isn't worth running—make a bigger change.

#### Running the Test

**Test Execution Rules:**
1. Run for full weeks (capture day-of-week effects)
2. Don't peek early—commit to duration
3. Track guardrail metrics (what shouldn't break)
4. Document everything before launch

**Guardrail Metrics Examples:**
- Revenue per user (main metric might improve but hurt revenue)
- Page load time (change might slow performance)
- Support tickets (change might confuse users)

#### Interpreting Results

| Result | Interpretation | Action |
|--------|----------------|--------|
| **Significant win** | p < 0.05, metric improved | Ship it, document learnings |
| **Significant loss** | p < 0.05, metric declined | Don't ship, learn why |
| **Inconclusive** | p > 0.05 | Not enough data OR no real effect |
| **Flat** | Large sample, no movement | Effect likely too small to matter |

**Common Pitfalls:**
- Stopping early when results look good (inflates false positives)
- Testing too many variants (dilutes sample)
- Ignoring segments (average hides important differences)
- No hypothesis (test without learning)

### 4. Retention & Cohort Analysis

Understand if users stick around. See `references/retention-cohorts.md` for SQL templates and benchmarks.

#### Retention Fundamentals

**Types of Retention:**

| Type | Definition | Use When |
|------|------------|----------|
| **N-day retention** | % of users active on exactly day N | Daily-use products (social, games) |
| **Bounded retention** | % active within day range (e.g., week 1) | Weekly-use products (SaaS) |
| **Unbounded retention** | % active on day N or any day after | Long purchase cycles (e-commerce) |

**Critical Retention Points:**

| Timeframe | What It Measures | Healthy Benchmark |
|-----------|------------------|-------------------|
| **D1** | First impression | >25% (consumer), >40% (B2B) |
| **D7** | Habit forming | >15% (consumer), >30% (B2B) |
| **D30** | Stickiness | >10% (consumer), >25% (B2B) |
| **D90** | Long-term value | Product-dependent |

#### Cohort Analysis

Group users by signup date (or other dimension) to track behavior over time.

**Cohort Table Structure:**

| Cohort | Week 0 | Week 1 | Week 2 | Week 3 | Week 4 |
|--------|--------|--------|--------|--------|--------|
| Jan 1-7 | 100% | 40% | 30% | 25% | 22% |
| Jan 8-14 | 100% | 45% | 35% | 28% | 25% |
| Jan 15-21 | 100% | 48% | 38% | 32% | — |

**Reading Cohort Tables:**
- **Rows** = Compare cohorts (are newer users retaining better?)
- **Columns** = Retention decay (where's the biggest drop-off?)
- **Diagonals** = Same calendar week (external events)

**Cohort Dimensions Beyond Time:**
- Acquisition channel (organic vs. paid)
- Plan type (free vs. paid)
- First action taken (feature X vs. feature Y)
- Geography

#### Retention Curves

**Healthy Curve Shape:**
```
100% ─┐
      │╲
      │ ╲
      │  ╲____________________  ← Flattens = retention
      │
  0% ─┴─────────────────────────
      D1   D7   D30   D60   D90
```

**Danger Signs:**
- Curve never flattens (continuous bleed)
- Steep drop after D1 (activation problem)
- Drop at specific point (feature/billing issue)

#### Churn Analysis

**Churn Rate Calculation:**

```
Monthly Churn = Customers Lost This Month / Customers at Start of Month
```

**Churn Benchmarks (SaaS):**

| Segment | Good | Great |
|---------|------|-------|
| SMB | <5% monthly | <3% monthly |
| Mid-market | <2% monthly | <1% monthly |
| Enterprise | <1% monthly | <0.5% monthly |

**Churn Diagnosis Questions:**
1. When do they churn? (Tenure analysis)
2. Who churns? (Segment analysis)
3. Why do they churn? (Exit surveys, support tickets)
4. What predicts churn? (Behavioral signals)

### 5. Dashboard Design

Create visibility that drives action. See `references/dashboard-design.md` for templates and tool recommendations.

#### Dashboard Hierarchy

**Level 1: Executive Dashboard (weekly, whole company)**
- 3-5 top-level KPIs
- Trend vs. target
- One screen, no scrolling

**Level 2: Functional Dashboards (daily, by team)**
- Sales: Pipeline, conversion, activity
- Product: Engagement, retention, feature adoption
- Marketing: Acquisition, CAC, channel performance
- Support: Tickets, response time, CSAT

**Level 3: Operational Dashboards (real-time, by function)**
- Engineering: Uptime, latency, errors
- Sales: Daily activity, quota attainment

#### KPI Selection

**For Each Metric, Answer:**
1. What decision does this inform?
2. Who needs to see it and how often?
3. What's the target and why?
4. What action triggers if it's off-track?

**Metric Types to Include:**

| Type | Purpose | Example |
|------|---------|---------|
| **Leading** | Predict future outcomes | Pipeline, activation rate |
| **Lagging** | Confirm results | Revenue, churn |
| **Input** | Activities you control | Calls made, features shipped |
| **Output** | Outcomes you want | Deals closed, retention |

#### Visualization Principles

**Choosing Chart Types:**

| Data Type | Best Chart |
|-----------|------------|
| Trend over time | Line chart |
| Comparison across categories | Bar chart |
| Part-to-whole | Pie (if <5 segments), stacked bar |
| Distribution | Histogram |
| Correlation | Scatter plot |
| Funnel stages | Funnel chart |

**Dashboard Anti-Patterns:**
- ❌ Too many metrics (more than 8-10 per view)
- ❌ No context (numbers without targets/trends)
- ❌ Vanity metrics (impressive but not actionable)
- ❌ Stale data (updated monthly when weekly needed)
- ❌ No owner (who acts on this?)

#### Tool Selection

**Tool Recommendations by Stage:**

| Stage | Recommended Approach |
|-------|---------------------|
| Pre-launch | Spreadsheet (Google Sheets) |
| MVP/Beta | Simple analytics (Mixpanel free, Amplitude free, PostHog) |
| Post-PMF | Full stack (Mixpanel/Amplitude + data warehouse + BI tool) |
| Scaling | Custom (Segment → warehouse → Looker/Metabase) |

**Tool Comparison:**

| Tool | Best For | Limitation |
|------|----------|------------|
| **Google Analytics** | Web traffic, acquisition | Weak on product analytics |
| **Mixpanel** | Product analytics, funnels | Can get expensive at scale |
| **Amplitude** | Product analytics, cohorts | Learning curve |
| **PostHog** | Open source, self-hosted option | Younger product |
| **Heap** | Auto-capture everything | Data can be messy |
| **Metabase** | SQL-based, self-hosted BI | Requires data warehouse |
| **Looker** | Enterprise BI | Complex, expensive |

### 6. Anti-Patterns

**Metrics Mistakes:**
- Tracking everything, focusing on nothing
- Vanity metrics (total signups vs. active users)
- Lagging-only metrics (revenue without leading indicators)
- No targets (data without context)

**Experimentation Mistakes:**
- Testing small changes on low-traffic pages
- Multiple changes in one test (can't isolate effect)
- Stopping tests early based on early results
- No hypothesis (random changes)

**Retention Mistakes:**
- Only looking at aggregate retention (hiding segment issues)
- Ignoring activation (retention starts at first experience)
- Not defining "active" clearly

**Dashboard Mistakes:**
- Dashboard nobody checks
- Real-time when weekly is sufficient
- No owners assigned to metrics

## Deliverables

### 1. Metrics Framework Document

Create as markdown:
- North Star metric with rationale
- AARRR funnel with specific metrics
- Supporting metrics hierarchy
- Targets and owners

### 2. Metrics Tracker Spreadsheet

Create using `xlsx` skill:
- AARRR funnel metrics with weekly/monthly tracking
- Formulas for calculated metrics (conversion rates, growth rates)
- Target vs. actual comparison
- Charts for trends

### 3. A/B Test Plan

Create as markdown:
- Hypothesis statement
- Variants description
- Primary and guardrail metrics
- Sample size and duration calculation
- Success criteria

### 4. Cohort Analysis Spreadsheet

Create using `xlsx` skill:
- Cohort table (rows = cohorts, columns = time periods)
- Retention percentages with conditional formatting
- Retention curve visualization
- Cohort comparison charts

### 5. Dashboard Specification

Create as markdown:
- KPI hierarchy (executive → functional → operational)
- Metric definitions with formulas
- Visualization recommendations
- Data sources and refresh frequency
- Tool recommendation with rationale

### 6. SQL Query Templates

Create as markdown:
- Cohort retention query
- Funnel conversion query
- Active user calculation
- Churn identification query

## Reference Files

- `references/metrics-frameworks.md` — AARRR deep dive, North Star selection guide, metrics by business model, anti-patterns
- `references/ab-testing.md` — Experiment templates, sample size calculator, significance interpretation, SQL queries
- `references/retention-cohorts.md` — Cohort methods, retention curves, SQL templates, benchmarks by model
- `references/dashboard-design.md` — Dashboard templates, visualization guide, tool comparison

## Integration with Other Skills

- Use `business-model` skill for unit economics metrics (LTV, CAC, payback)
- Use `product` skill for feature prioritization based on analytics
- Use `go-to-market` skill for channel-specific acquisition metrics
- Use `operations` skill for OKRs aligned with metrics framework
- Use `fundraising` skill for investor-ready metrics presentation
- Use `xlsx` skill for metrics trackers and cohort spreadsheets
- Use `docx` skill for analytics documentation

---

*Adapted from [Linas Beliūnas's](https://linas.substack.com/p/onepersonunicorn) **The One-Person Unicorn** founder skill set.*
