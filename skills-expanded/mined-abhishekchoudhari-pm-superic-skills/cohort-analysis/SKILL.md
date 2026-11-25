---
name: cohort-analysis
description: "Perform cohort analysis on user engagement data — build retention curves, interpret curve shapes, benchmark against industry standards, segment cohorts by acquisition channel and behavior, and identify which cohort vintage drives today's MAU. Use when analyzing user retention by cohort, studying feature adoption over time, investigating churn patterns, running resurrection analysis, or identifying engagement trends."
---

# Cohort Analysis and Retention Explorer

Analyze user retention and engagement patterns by cohort with enough specificity to diagnose the root cause and recommend the next action.

---

## Context

You are running a cohort analysis for **$ARGUMENTS**.

If the user provides data files (CSV, Excel, SQL exports), read and analyze them directly. Generate Python/pandas scripts for calculations when needed.

---

## Part 1: The Most Important Decision — Activation Event

The activation event defines when a user "enters" a cohort. This single decision determines whether your retention numbers look good or bad, accurately or misleadingly.

**Wrong activation events:**
- Account created — includes users who signed up but never engaged
- Email verified — same problem, one step further

**Right activation events — examples by product type:**
| Product type | Strong activation event |
|---|---|
| Mobile app (social) | Followed 5+ users OR posted first content |
| E-commerce | Completed first purchase |
| SaaS (B2B) | Completed onboarding AND used core feature |
| Consumer subscription | First session after payment |
| Marketplace | Both sides: buyer places order, seller receives order |

**How to find the right activation event:** Run correlation analysis between Day 1 actions and D30 retention. The action with the highest correlation to D30 retention is your activation event. If you do not have this correlation, use the action that represents delivery of the product's core value proposition.

---

## Part 2: Retention Event Definition

The retention event must reflect genuine engagement, not incidental activity.

| Weak retention event | Strong retention event |
|---|---|
| Logged in | Completed core workflow |
| Opened app | Reached a spending/usage threshold |
| Clicked any button | Used the primary feature |
| Received a notification | Initiated a user-driven action |

Define both the activation event and the retention event before building the cohort table. Changing either one retroactively makes cohorts incomparable.

---

## Part 3: Building the Retention Table

### Time period selection

| Product use frequency | Retention periods to track |
|---|---|
| Daily-use apps (social, games, news) | D1, D3, D7, D14, D30, D60, D90 |
| Weekly-use apps (productivity, fitness) | W1, W2, W4, W8, W12 |
| Monthly-use apps (finance, subscription) | M1, M2, M3, M6, M12 |

### Table format

| Cohort | Size | D1 | D7 | D14 | D30 | D60 | D90 |
|---|---|---|---|---|---|---|---|
| Jan 2025 | 12,400 | 38% | 21% | 16% | 13% | 9% | 7% |
| Feb 2025 | 10,200 | 41% | 23% | 18% | 15% | 11% | 8% |

Each cell = % of cohort active in that period. Size = activated users, not all signups.

---

## Part 4: Retention Benchmarks

### B2C mobile app benchmarks

| Metric | Poor | Median | Good | Top quartile |
|---|---|---|---|---|
| D1 retention | <15% | 25-30% | 35-40% | >45% |
| D7 retention | <8% | 10-15% | 16-20% | >25% |
| D30 retention | <5% | 8-12% | 15-20% | >25% |
| D90 retention | <3% | 5-8% | 10-15% | >20% |

**Rule of thumb:** a D30 retention above 20% is considered strong for B2C apps. Above 30% is exceptional.

### SaaS (subscription) benchmarks

| Metric | Poor | Healthy | Strong | Top quartile |
|---|---|---|---|---|
| Monthly retention | <88% | 90-93% | 94-95% | >96% |
| Annual churn | >25% | 15-25% | 5-15% | <5% |
| Net Revenue Retention | <90% | 95-100% | 100-110% | >120% |

### Consumer subscription benchmarks

| Metric | Weak | Healthy |
|---|---|---|
| Month 1 to Month 2 | <50% | >65% |
| Month 3 retention | <35% | >50% |
| 12-month retention | <25% | >40% |

---

## Part 5: Retention Curve Shapes and Diagnoses

The shape of the retention curve tells you what kind of problem (or success) you have.

### L-shaped curve (steep initial drop, then flat)
- **Pattern:** D7 drops to 15%, but D30 to D90 stays flat at 12-13%
- **Diagnosis:** Most users churn fast but a loyal core remains. This is common in B2C apps. The question is: can you expand the core?
- **Action:** Identify what the retained 12% did in their first session that the churned 85% did not. That action is your activation target.

### Fast-decay curve (continuous decline, no flattening)
- **Pattern:** D7 = 20%, D30 = 8%, D90 = 3%, D180 = 1%
- **Diagnosis:** No habit is forming. Users try the product and permanently leave. This is an engagement or value delivery problem.
- **Action:** Product redesign or feature pivot needed. Run qualitative research with churned users.

### Gradual decay curve (slow, steady decline)
- **Pattern:** D7 = 45%, D30 = 35%, D90 = 28%, D180 = 22%
- **Diagnosis:** Expected for discretionary or lower-frequency products. Healthy if flattening occurs within 3-6 months.
- **Action:** Identify the floor. If the curve shows no sign of flattening, treat it as fast-decay.

### Cliff at specific tenure (sharp drop at one time point)
- **Pattern:** Normal decay to M3, then M4 drops by 30%
- **Diagnosis:** Billing event (annual subscription renewal), product change, or competitive event at that tenure mark. Check for product releases, pricing changes, or external events coinciding with the cliff.
- **Action:** Investigate what happened at that exact time point before assuming churn is organic.

### Rising retention in recent cohorts
- **Pattern:** Jan cohort D30 = 12%, Mar cohort D30 = 19%, May cohort D30 = 24%
- **Diagnosis:** Product improvements are working. Validate by checking if a specific feature release or onboarding change coincides with the improvement.

---

## Part 6: Cohort Segmentation Dimensions

Never analyze only time-based cohorts. Cut cohorts by these dimensions to find root causes.

| Dimension | Why it matters | What to look for |
|---|---|---|
| Acquisition channel | Different channels bring users with different intent | Organic users often retain 30-50% better than paid users |
| Device / platform | iOS vs Android, mobile vs desktop | Mobile may show 2x higher D1 churn if onboarding is not mobile-optimized |
| Feature adoption depth | Users who adopted core feature vs didn't | Typically 2-3x retention difference — this is the activation signal |
| Plan tier | Free vs paid, basic vs premium | Paid users retain better; free-to-paid conversion signals health |
| Geography | Regional behavior differences | Useful for localization and go-to-market decisions |
| Signup source | Direct, referral, app store search | Referral-acquired users often have higher LTV |

---

## Part 7: Behavioral Cohorts vs Time Cohorts

These are different analytical tools for different questions.

**Time cohorts** — group users by when they joined. Use to measure:
- Whether product improvements are lifting retention over time
- Seasonal patterns in cohort quality
- Impact of a specific product launch

**Behavioral cohorts** — group users by an action they took. Use to measure:
- Whether a specific feature drives long-term retention
- Whether completing onboarding predicts D30 retention
- The value of a specific user behavior

**Example of behavioral cohort question:** "Do users who use the search feature in their first session retain 2x better than those who don't?"
- Build two cohorts: used search in session 1 vs did not
- Compare D30 retention
- If the difference is large and consistent across time cohorts, improving search discoverability is a retention lever

---

## Part 8: Resurrection Analysis

Resurrection = a churned user returns after a period of inactivity.

**Why it matters:** Resurrection tells you whether users have permanently abandoned the product or temporarily deprioritized it. High resurrection rates suggest the product has value but is losing to habit formation or lifecycle events.

### Resurrection thresholds

| Gap | Classification |
|---|---|
| 8-30 days inactive, then returns | Mild churn - likely a habit lapse |
| 31-90 days inactive, then returns | Medium churn - product was deprioritized |
| 90+ days inactive, then returns | Real churn - a specific trigger brought them back (notification, word of mouth, lifecycle event) |

### What to track

- Monthly resurrection rate: resurrected users / users who churned in prior 3 months
- Time-to-resurrection distribution: what % come back within 30 days vs 30-90 days vs 90+ days
- Resurrection trigger: what action brought them back (push notification, email, organic)

**Benchmark:** B2C apps with strong resurrection (>15% of churned users returning within 90 days) can sustain MAU even with moderate new user growth.

---

## Part 9: Cohort Contribution to Current MAU

For any given month, decompose MAU by the cohort vintage that generated it.

**Example table:**

| Cohort vintage | Users in MAU | % of MAU |
|---|---|---|
| Last 30 days (new users) | 45,000 | 18% |
| 1-3 months ago | 62,000 | 25% |
| 3-6 months ago | 48,000 | 19% |
| 6-12 months ago | 55,000 | 22% |
| 12+ months ago | 40,000 | 16% |

**What this tells you:**
- If new users dominate MAU: growth is primarily acquisition-driven; retention is weak
- If older cohorts dominate MAU: product has strong retention; growth depends on existing user engagement
- If 1-3 month cohorts are largest: healthy new user pipeline and reasonable early retention

---

## Part 10: Analysis Output Format

Produce this structure when running a cohort analysis.

```
## Cohort Analysis: [Product / Feature Name]

**Activation event:** [definition]
**Retention event:** [definition]
**Cohort type:** [time-based / behavioral]
**Date range:** [start to end]

### Retention table
[Insert table with cohort x period matrix]

### Retention curve shape
[L-shaped / fast-decay / gradual / cliff — and what it means for this product]

### Benchmark comparison
[How results compare to B2C / SaaS benchmarks above]

### Segmentation findings
[2-3 segments with the most significant retention difference]

### Cohort trend
[Is retention improving, declining, or flat across recent cohorts?]

### Top 3 findings
1. [Finding with specific numbers]
2. [Finding with specific numbers]
3. [Finding with specific numbers]

### Recommendations
1. [Specific action - owner - timeline]
2. [Specific action - owner - timeline]

### Follow-up questions this data cannot answer
[List gaps]
```

---

### Further Reading

- [Cohort Analysis 101: How to Reduce Churn and Make Better Product Decisions](https://www.productcompass.pm/p/cohort-analysis)
- [The Product Analytics Playbook](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
