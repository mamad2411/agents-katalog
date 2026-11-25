---
name: data-analysis
description: "Expert PM data analysis across multiple modes — error RCA, cohort retention, funnel drop-off, trend investigation, user segmentation, A/B test evaluation, and exploratory analysis. Use when the analysis type is unclear, when the data needs classification before analysis, or when the question spans more than one analytical framework. Includes problem framing, data quality checks, visualization selection, and communication of findings."
---

# PM Data Analysis — Expert Mode

Analyze any product or engineering dataset with the depth of an experienced data analyst and the judgment of a senior PM. The output is not a data summary — it is a diagnosis with a decision at the end.

---

## Context

You are analyzing data for **$ARGUMENTS**.

If the user provides data files (CSV, Excel, or analytics exports), read and analyze them directly. Generate Python scripts for statistical calculations when needed.

---

## Part 1: Problem Framing

Before touching any data, translate the business question into a specific data question. This is the most important step — the wrong data question produces a technically correct but useless answer.

### Translation examples

| Business question | Data question |
|---|---|
| Why is revenue down this month? | Which cohort, segment, or product line is driving the decline, and when did it start? |
| Why are users not using the new feature? | What % of MAU have seen the feature entry point, and what % of those clicked? Where does adoption drop? |
| Are users satisfied? | What is the D30 retention rate, and how does it compare to the prior 3 months? |
| Should we invest in market X? | What is the activation rate and 90-day retention rate for users from market X vs baseline? |
| Is the experiment working? | What is the conversion rate lift, p-value, and confidence interval for the primary metric? |

**Rule:** if you cannot describe what the answer looks like before querying the data, the question is not specific enough. Narrow it down.

---

## Part 2: Data Quality Checklist

Run this check before any analysis. Presenting analysis built on bad data destroys credibility.

| Check | How to run | Pass threshold |
|---|---|---|
| Completeness | Count nulls per column: SELECT column, COUNT(*) - COUNT(column) AS nulls FROM table | <5% nulls for key dimensions, <1% for key metrics |
| Consistency | Check for duplicate IDs: SELECT id, COUNT(*) FROM table GROUP BY id HAVING COUNT(*) > 1 | Zero duplicates for user/transaction IDs |
| Recency | Check max timestamp: SELECT MAX(event_timestamp) FROM events | Data pipeline lag under 2 hours for real-time; under 24 hours for daily batch |
| Representativeness | Compare sample characteristics to known population (e.g., device split in sample vs platform stats) | Sample skew under 10% on key dimensions |
| Volume sanity | Compare daily row counts to prior 30-day average | Flag any day with >50% deviation from average |

**When to stop:** if completeness is below 90% for a key dimension, stop and escalate to the data engineering team before proceeding. Analysis on incomplete data is misleading.

---

## Part 3: Five Analytical Patterns Every PM Must Know

Select the pattern that matches the question, or combine multiple patterns for complex questions.

### Pattern 1: Trend analysis
**When to use:** a metric is moving and you need to understand direction and inflection point.
- Plot daily granularity for 30-90 days
- Find the exact date the trend changed (aggregates hide this)
- Decompose: split the metric into components (DAU = new + retained + resurrected)
- Match the inflection date to product releases, campaigns, or external events

### Pattern 2: Funnel analysis
**When to use:** users complete multi-step flows and you need to find where they drop.
- List all funnel steps with event names and user counts
- Calculate step-to-step conversion AND cumulative conversion from step 1
- Find the step with the largest absolute user loss (not just highest relative drop rate)
- Segment the funnel by device, channel, and user type

### Pattern 3: Cohort analysis
**When to use:** understanding long-term retention, engagement decay, or the impact of product changes on user behavior over time.
- Define activation event and retention event precisely
- Build a cohort x period matrix
- Compare recent cohorts to older cohorts for trend direction
- For full methodology, use the cohort-analysis skill

### Pattern 4: Segmentation
**When to use:** an overall metric is ambiguous — understanding WHO is driving the number is more important than the number itself.
- Break by acquisition channel, device, geography, user tier, plan type
- Find the segment where the metric is 2x better or worse than average
- Size each segment to understand business impact
- The segment with the largest gap and highest volume is the priority

### Pattern 5: Correlation analysis (with causation caution)
**When to use:** you have a hypothesis that two things are related and want to test it.
- Calculate Pearson or Spearman correlation coefficient
- Interpret: r>0.7 is strong, r=0.4-0.7 is moderate, r<0.4 is weak
- **Never claim causation from correlation in a product presentation.** Add the caveat explicitly.
- For causation, run an A/B test or use instrumental variable analysis

---

## Part 4: Outlier Handling

Outliers are not errors by default. The right treatment depends on what they are.

| Outlier type | Example | Correct treatment |
|---|---|---|
| Bug / tracking error | 1 user with 10,000 sessions in a day | Remove — investigate and fix tracking |
| Power user | Top 1% of users generate 30% of revenue | Keep — they are the most important users |
| Fraud / bot | 500 signups from one IP in 1 hour | Remove from product metrics, flag for security |
| Genuine anomaly | One day with 3x normal traffic | Investigate the cause — do not remove until you know why |
| Funnel skip | Users who reached step 5 without step 3 | Keep and investigate — reveals optional vs required steps |

**Practical rule:** remove outliers from conversion funnel analysis when they represent tracking errors. Never remove outliers from revenue or retention analysis without understanding what they represent first.

---

## Part 5: Visualization Selection Guide

| Analysis type | Best chart | Why |
|---|---|---|
| Metric over time | Line chart | Shows trend and inflection points clearly |
| Comparison across categories | Horizontal bar chart | Easy to rank and compare |
| Cohort retention | Heat map (cohort x period) | Shows both the retention curve and cohort-over-cohort trend |
| Conversion funnel | Funnel / waterfall chart | Absolute drop is more visible than a table |
| Correlation between two metrics | Scatter plot | Shows relationship and outliers simultaneously |
| Distribution of a metric | Histogram or box plot | Shows spread, skew, and outliers |
| Segment composition | Stacked bar or pie | Shows relative contribution (use sparingly) |

**Design rules:**
- Lead with the finding in the chart title ("D30 retention fell 8pp in Q4 cohorts"), not the description ("D30 retention by cohort")
- Always label the y-axis with units
- Highlight the most important data point with a callout or contrasting color
- Keep the color palette to 3 colors maximum for categorical charts

---

## Part 6: Benchmarks by Product Type

Use these to calibrate whether a metric is strong, weak, or typical.

### Conversion benchmarks

| Flow | Poor | Median | Strong |
|---|---|---|---|
| Landing page to signup | <1% | 2-4% | >6% |
| Signup to activation | <20% | 30-45% | >55% |
| Activation to first transaction | <15% | 25-40% | >50% |
| Session to transaction (e-commerce) | <8% | 15-25% | >30% |
| Session to transaction (financial products) | <3% | 5-12% | >15% |
| Free to paid (consumer app) | <1% | 2-5% | >7% |
| Free to paid (B2B SaaS trial) | <5% | 10-20% | >25% |

### Engagement benchmarks

| Metric | Poor | Median | Strong |
|---|---|---|---|
| DAU/MAU ratio (daily-use app) | <10% | 15-25% | >30% |
| DAU/MAU ratio (weekly-use app) | <5% | 8-15% | >20% |
| Session length (mobile app) | <2 min | 3-6 min | >8 min |
| Sessions per active user per week | <1.5 | 2-4 | >5 |

---

## Part 7: Communicating Findings

The test for every finding: "So what?" If you cannot answer that question in one sentence, the finding is not ready to present.

### Structure every finding as:
1. **Observation** — what the data shows (with a specific number)
2. **Significance** — why it matters to the business
3. **Hypothesis** — the most likely explanation
4. **Recommendation** — the specific next action

**Example:**
- Observation: "D30 retention for the March cohort is 8%, down from 15% in February."
- Significance: "If this holds, March users will generate 47% less lifetime revenue than February users."
- Hypothesis: "The new onboarding flow launched in March removed the step that drove activation to the core feature."
- Recommendation: "Restore the activation step for the next 2 weeks as an A/B test. Measure D7 retention as the leading indicator."

### Presentation anti-patterns to avoid

| Anti-pattern | Fix |
|---|---|
| Leading with methodology ("first I ran a query...") | Lead with the conclusion |
| Showing every metric you computed | Show only the 3-5 most actionable |
| Saying "data suggests" without a number | Attach a specific number to every claim |
| Ending with "further analysis needed" | End with a specific recommendation |
| Presenting data without a benchmark | Always compare to a prior period or industry standard |

---

## Part 8: Analysis Modes

Select the mode that matches the data and question.

### Mode 1: Error / incident RCA
Use when data is error logs, failure counts, or repeated failures per entity.
- Classify each entity as: chronic (10+ errors over 48+ hours), transient (3-9 errors, resolved), or single-event
- Analyze retry cadence: high concentration in under-20-minute buckets = aggressive retrying without backoff
- Calculate: total entities affected, % still active, estimated conversion impact

### Mode 2: Cohort and retention analysis
Use when data has user IDs, activation dates, and subsequent activity.
- Follow the cohort-analysis skill for full methodology
- Produce a cohort x period retention table
- Identify curve shape and compare to benchmarks

### Mode 3: Funnel analysis
Use when data has sequential steps with user counts per step.
- Follow the funnel-analysis skill for full methodology
- Produce step-by-step and cumulative conversion table
- Segment by device, channel, and user type

### Mode 4: Trend and anomaly investigation
Use when a specific metric is moving unexpectedly.
- Find the exact inflection date at daily granularity
- Decompose the metric into components
- Match inflection to product or external events
- Validate hypothesis with a second signal

### Mode 5: User segmentation
Use when raw user or event data has no prior segmentation.
- Calculate RFM dimensions (recency, frequency, magnitude/value)
- Classify into behavioral segments with descriptive names
- Size each segment and show the trend (growing or shrinking)

### Mode 6: A/B test evaluation
Use when data has control and variant groups.
- Follow the ab-test-analysis skill for full methodology
- Validate setup before reading results (SRM check, power analysis)
- Apply the decision framework: ship / extend / deprioritize / drop

### Mode 7: Exploratory analysis
Use when there is no specific question and the data needs characterization.
- Describe the dataset: row count, date range, unique entities, null rates
- Surface the three most actionable patterns
- Flag statistical outliers
- Propose 2-3 follow-up questions the dataset can answer

---

## Part 9: Output Standards

Every analysis output must include:

1. **Data classification** — what the data is, what it is not, data quality findings
2. **Problem statement** — the specific data question being answered
3. **Analysis mode selected** — which mode and why
4. **Numbered findings** — each with a specific number, not a directional statement
5. **Mode-specific table** — retention table, funnel table, error cohort table, etc.
6. **Business impact** — connection to a user flow, conversion metric, or revenue implication with an estimate
7. **Recommendations** — specific, ownable, measurable within 30 days
8. **Follow-up queries** — SQL to go deeper on the top findings (or reference sql-queries skill)
9. **Data gaps** — what this analysis cannot answer and what additional data would fill the gap

---

### Further Reading

- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
- [Cohort Analysis 101](https://www.productcompass.pm/p/cohort-analysis)
