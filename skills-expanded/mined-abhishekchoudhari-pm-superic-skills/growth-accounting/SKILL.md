---
name: growth-accounting
description: "Decompose user and revenue growth into new, retained, resurrected, and churned — identify where growth is really coming from, calculate quick ratio, compute Net Revenue Retention, and identify which growth lever to pull next. Use when diagnosing whether growth is healthy or acquisition-dependent, running weekly or monthly growth reviews, computing NRR, understanding quick ratio, or presenting growth health to leadership."
---

# Growth Accounting

Decompose growth into its components to understand where users and revenue are actually coming from, and which lever to pull next.

---

## Context

You are running a growth accounting analysis for **$ARGUMENTS**.

If the user provides data files (CSV, Excel, SQL exports), read and analyze them directly. Generate Python scripts or SQL queries when needed.

---

## Part 1: The Growth Accounting Framework

### User growth accounting formula

```
Net MAU change = New users + Resurrected users - Churned users

Where:
  New users     = users active this month who were NEVER active in any prior month
  Retained users = users active this month who were also active last month
  Resurrected users = users active this month who were NOT active last month but were active in some prior month
  Churned users = users active last month who are NOT active this month
```

Net MAU = Retained + New + Resurrected (the total active this month)
MAU growth = New + Resurrected - Churned

**Critical decision before building the model:** choose the dormancy threshold — the number of days of inactivity that defines "churned." This threshold determines what gets counted as resurrected vs churned.

| Product use frequency | Recommended dormancy threshold |
|---|---|
| Daily-use apps (social, news, games) | 30 days |
| Weekly-use apps (productivity, fitness) | 60 days |
| Monthly-use apps (finance, subscription) | 90 days |
| Low-frequency apps (travel, insurance) | 180 days |

**Rule:** pick one threshold and never change it retroactively. Changing the threshold makes historical cohorts incomparable.

---

## Part 2: Quick Ratio

The quick ratio measures whether a product is gaining or losing users on net, accounting for both acquisition and retention.

```
Quick ratio = (New users + Resurrected users) / Churned users
```

| Quick ratio | Interpretation |
|---|---|
| >4 | Hyper-growth — adding users much faster than losing them |
| 2-4 | Healthy growth — sustainable if maintained |
| 1-2 | Struggling — barely replacing churned users |
| <1 | Shrinking — losing more users than gaining |

### Industry benchmarks

| Stage / type | Typical quick ratio range |
|---|---|
| B2C app in growth phase (top quartile) | 3-5 |
| B2C app at scale (steady state) | 1.5-3 |
| Mature SaaS product | 1.5-2.5 |
| Product in decline | <1 |

**Caveat:** quick ratio can be gamed by inflating new user acquisition while retention collapses. Always review quick ratio alongside D30 retention. A high quick ratio + declining D30 retention = acquisition-dependent growth that will stall.

---

## Part 3: Revenue Growth Accounting (MRR Decomposition)

For subscription or recurring revenue products, decompose Monthly Recurring Revenue (MRR) the same way.

```
Net MRR change = New MRR + Expansion MRR - Contraction MRR - Churned MRR

Where:
  New MRR        = revenue from new subscribers or paying customers this month
  Expansion MRR  = revenue increase from existing customers (upsell, cross-sell, usage growth)
  Contraction MRR = revenue decrease from existing customers (downgrade, reduced usage)
  Churned MRR    = revenue lost from customers who cancelled
```

### Net Revenue Retention (NRR)

NRR measures whether your existing customer base is growing or shrinking in revenue, without counting new customers.

```
NRR = (Starting MRR + Expansion MRR - Contraction MRR - Churned MRR) / Starting MRR × 100%
```

**Example:** Starting MRR = $1,000,000; Expansion = $120,000; Contraction = $30,000; Churn = $80,000
NRR = ($1,000,000 + $120,000 - $30,000 - $80,000) / $1,000,000 = 101%

**What NRR above 100% means:** even if you acquired zero new customers this month, revenue would still grow. This is the most powerful growth state for a subscription business.

### NRR benchmarks

| NRR | Interpretation |
|---|---|
| >130% | World-class — strong expansion, minimal churn (typical: top SaaS with land-and-expand model) |
| 110-130% | Top quartile SaaS |
| 100-110% | Healthy — growing from within |
| 90-100% | Needs attention — churn is offsetting expansion |
| <90% | Problem — contraction + churn exceed expansion; growth depends entirely on new customers |

**Consumer subscription benchmarks:**
- NRR >100%: exceptional (rare without a usage-based pricing component)
- NRR 90-100%: healthy
- NRR <85%: high churn is a structural problem

---

## Part 4: Growth Accounting Diagnosis

Use the breakdown to identify which lever to pull.

### Scenario 1: New users declining, quick ratio still above 1
- **Diagnosis:** channel efficiency problem — cost per acquisition (CPA) is rising, or top-of-funnel traffic is declining
- **Action:** audit acquisition channels by volume and conversion rate; identify which channel is declining; test new channels or creative

### Scenario 2: Resurrected users are unusually high (>25% of new + resurrected)
- **Diagnosis:** the product has inherent value but the initial experience fails to create habits — users leave and come back when triggered
- **Action:** this is primarily a retention and onboarding problem, not a resurrection strategy. Improve D7-D30 retention so fewer users require resurrection

### Scenario 3: Churned users are rising faster than new users
- **Diagnosis:** retention / lifecycle problem — the product is leaking faster than it fills. Quick ratio trending below 1.5.
- **Action:** run cohort analysis to identify which vintage has the worst churn; run segmentation to find which user type churns first; address the root cause (onboarding, feature gaps, pricing)

### Scenario 4: Quick ratio is declining despite flat churn
- **Diagnosis:** acquisition is slowing — fewer new and resurrected users are entering the top of funnel
- **Action:** review acquisition channel health, paid media efficiency, and organic growth drivers

### Scenario 5: NRR above 110%, but quick ratio is below 2
- **Diagnosis:** strong revenue expansion from existing customers, but new customer acquisition is weak — the business is healthy financially but dependent on a shrinking customer base long-term
- **Action:** invest in new customer acquisition without compromising the expansion motion; review onboarding for new users

---

## Part 5: Growth Accounting Output Table

The standard weekly or monthly growth accounting table.

| Period | New | Retained | Resurrected | Churned | Net MAU change | MAU | Quick ratio |
|---|---|---|---|---|---|---|---|
| Jan 2025 | 45,000 | 180,000 | 12,000 | 38,000 | +19,000 | 237,000 | 1.50 |
| Feb 2025 | 48,000 | 185,000 | 14,000 | 41,000 | +21,000 | 258,000 | 1.51 |
| Mar 2025 | 52,000 | 192,000 | 18,000 | 35,000 | +35,000 | 293,000 | 2.00 |

**Revenue version:**

| Period | Starting MRR | New MRR | Expansion MRR | Contraction MRR | Churned MRR | Ending MRR | NRR |
|---|---|---|---|---|---|---|---|
| Jan 2025 | $500K | $42K | $28K | $8K | $22K | $540K | 99.6% |

---

## Part 6: SQL for Growth Accounting

```sql
-- Monthly growth accounting: new, retained, resurrected, churned
-- Dormancy threshold: 30 days (adjust for your product)
-- Assumes: events table (user_id, event_date)

WITH monthly_active AS (
  SELECT
    user_id,
    DATE_TRUNC(event_date, MONTH) AS activity_month -- BigQuery
    -- Snowflake/Redshift: DATE_TRUNC('month', event_date)
  FROM events
  GROUP BY 1, 2
),
user_states AS (
  SELECT
    curr.user_id,
    curr.activity_month,
    CASE
      WHEN prev.user_id IS NULL AND first_seen.user_id IS NULL THEN 'new'
      WHEN prev.user_id IS NOT NULL THEN 'retained'
      WHEN prev.user_id IS NULL AND first_seen.user_id IS NOT NULL THEN 'resurrected'
    END AS user_state
  FROM monthly_active curr
  -- Check if active last month (retained)
  LEFT JOIN monthly_active prev
    ON curr.user_id = prev.user_id
    AND prev.activity_month = DATE_SUB(curr.activity_month, INTERVAL 1 MONTH)
  -- Check if ever seen before (to distinguish new from resurrected)
  LEFT JOIN (
    SELECT user_id, MIN(activity_month) AS first_month
    FROM monthly_active
    GROUP BY 1
  ) first_seen
    ON curr.user_id = first_seen.user_id
    AND first_seen.first_month < curr.activity_month
),
churned AS (
  -- Users active last month but not this month
  SELECT
    prev.user_id,
    DATE_ADD(prev.activity_month, INTERVAL 1 MONTH) AS activity_month,
    'churned' AS user_state
  FROM monthly_active prev
  WHERE NOT EXISTS (
    SELECT 1 FROM monthly_active curr
    WHERE curr.user_id = prev.user_id
    AND curr.activity_month = DATE_ADD(prev.activity_month, INTERVAL 1 MONTH)
  )
),
all_states AS (
  SELECT user_id, activity_month, user_state FROM user_states
  UNION ALL
  SELECT user_id, activity_month, user_state FROM churned
)
SELECT
  activity_month,
  user_state,
  COUNT(DISTINCT user_id) AS users
FROM all_states
GROUP BY 1, 2
ORDER BY 1, 2
```

---

## Part 7: Weekly Leadership Presentation Template

Present growth accounting in a 10-minute standup. Structure:

**Slide or section 1: The number (30 seconds)**
- MAU this week/month: [X], change vs prior period: [+/- Y%]
- Quick ratio: [X.X] — [healthy / needs attention / improving]

**Slide or section 2: The breakdown (2 minutes)**
- Show the growth accounting table with this period and prior 3 periods
- Highlight which bucket is the primary driver of the change

**Slide or section 3: The diagnosis (3 minutes)**
- If quick ratio improved: which bucket drove it (new acquisition up? churn down?)
- If quick ratio declined: which bucket is the problem?
- One data point that explains the diagnosis (e.g., "churn rose because March cohort D30 retention dropped 6pp")

**Slide or section 4: The action (2 minutes)**
- One specific action in flight to address the biggest bucket
- Leading indicator that will show whether the action is working (and when to check it)

**Format rule:** lead with the number, then the breakdown, then the story. Never lead with methodology or data sources.

---

## Part 8: Common Mistakes

| Mistake | Effect | Fix |
|---|---|---|
| Counting inactive accounts as MAU | Inflates MAU, deflates quick ratio and DAU/MAU | Define active as "completed at least one meaningful action" |
| Changing dormancy threshold retroactively | Makes historical comparisons invalid | Fix the threshold before the first public report |
| Reporting quick ratio without D30 retention | Misses the case where high acquisition masks retention collapse | Always show both |
| Reporting NRR without MRR breakdown | Hides whether churn or contraction is the driver | Show the four MRR components separately |
| Treating all churn as equal | Early churn (day 1-7) has a different root cause than long-term churn | Segment churn by user tenure |

---

### Further Reading

- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Cohort Analysis 101](https://www.productcompass.pm/p/cohort-analysis)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
