---
name: feature-adoption-analysis
description: "Measure and improve feature adoption — define adoption, build the adoption funnel from aware to habitual, find the Aha moment, diagnose low adoption by stage, segment by user type, identify feature retirement signals, and produce a roadmap to 2x adoption. Use when a new feature is underperforming, when measuring the impact of a feature launch, when deciding whether to retire a feature, or when building an adoption improvement plan."
---

# Feature Adoption Analysis

Measure how deeply users are adopting a feature, diagnose where adoption is failing, and produce a specific improvement plan.

---

## Context

You are analyzing feature adoption for **$ARGUMENTS**.

If the user provides data files (CSV, Excel, SQL exports), read and analyze them directly. Generate Python scripts or SQL queries when needed.

---

## Part 1: Adoption Dimensions

Feature adoption is not one number. It has three dimensions that together tell the full story.

| Dimension | Definition | Question it answers |
|---|---|---|
| Breadth | % of MAU who used the feature at least once in the period | How many users know about and try the feature? |
| Depth | Average number of times adopted users used the feature per week | How central is the feature to active users' workflows? |
| Frequency | % of active sessions that include the feature | Is the feature embedded in the product habit or used occasionally? |

**Example reading:**
- Breadth = 22%, Depth = 1.4 uses/week, Frequency = 8%
- Interpretation: 22% of MAU tried it; those who adopted it use it about once a week; it shows up in 1 in 12 sessions
- Diagnosis: breadth is low (awareness or UX entry point problem); depth is acceptable; frequency suggests the feature is not on the critical path

Use all three dimensions when presenting adoption. A feature with 60% breadth but 0.3 depth/week is being tried but not used. A feature with 8% breadth but 4 depth/week is niche but loved.

---

## Part 2: Adoption Benchmarks

### New feature adoption benchmarks (first 30 days after launch)

| Feature type | Expected breadth at 30 days | Benchmark |
|---|---|---|
| Non-core / supplementary feature | 5-15% | Reaching 20% is strong |
| Core feature (on the main user flow) | 25-50% | Below 20% signals discoverability or UX problem |
| Default-on feature (no opt-in required) | 60-80% | Below 50% suggests users actively avoiding it |
| Opt-in premium feature | 3-10% | Highly dependent on conversion and paywall design |

### Long-term adoption benchmarks (90 days post-launch)

| Feature type | Healthy breadth at 90 days |
|---|---|
| Core feature | >50% of MAU |
| Non-core feature | >15% of MAU |
| Power feature (complex, high value) | >10% of power users |

---

## Part 3: The Feature Adoption Funnel

Every feature has its own micro-funnel. Map each stage before diagnosing the problem.

| Stage | Definition | How to measure |
|---|---|---|
| Aware | User saw the feature entry point (tooltip, menu item, button) | Impression events: feature_entry_point_seen |
| Activated | User tried the feature at least once | First-use event: feature_first_used |
| Adopted | User used the feature 3+ times in a 30-day period | Count: feature_used >= 3 in 30 days |
| Habitual | User uses the feature at least once per week, consistently | Streak: feature_used in 4+ of last 6 weeks |

**Example funnel:**

| Stage | Users | Conversion from prior stage | Conversion from Aware |
|---|---|---|---|
| Aware | 180,000 | - | 100% |
| Activated | 54,000 | 30% | 30% |
| Adopted | 22,000 | 41% | 12% |
| Habitual | 9,000 | 41% | 5% |

**Reading this funnel:** the biggest absolute drop is Aware to Activated (126,000 users lost). Only 30% of users who saw the feature tried it. The most actionable fix is improving the entry point design to increase the Aware-to-Activated rate. If that moves from 30% to 45%, habitual users would increase by 50%.

---

## Part 4: The Aha Moment

The Aha moment is the specific action that converts a first-time user into a habitual one. Finding it is the most important analytical task in feature adoption.

### How to find the Aha moment

1. Define your "habitual" cohort: users who used the feature 4+ times in their first 30 days after trying it
2. For each possible Aha action (completing a specific sub-step, reaching a milestone, seeing a result), calculate: what % of users who took this action became habitual?
3. Compare habitual conversion rates across actions
4. The action with the highest correlation to habitual adoption is the Aha moment candidate
5. Validate: compare D30 retention of users who hit the Aha moment vs those who didn't

**Example (note-taking feature in a productivity app):**
| Action | % who became habitual |
|---|---|
| Created 1 note | 18% |
| Created 3+ notes | 51% |
| Added a tag to a note | 62% |
| Shared a note | 71% |

Aha moment = sharing a note. The feature's value is collaborative; solo note creation has much lower habitual conversion.

**Product decision:** redesign the onboarding for this feature to guide users toward sharing a note in their first session.

---

## Part 5: Adoption Diagnostics by Stage

Use this table to match the symptom to the root cause.

| Symptom | Root cause | Action |
|---|---|---|
| Low breadth (<50% of benchmark) | Discoverability problem — users don't know the feature exists | Improve feature entry point; add in-app education; test different placement |
| High aware-to-activated drop (>80% drop) | UX friction or unclear value prop at first contact | Simplify the first step; add micro-copy explaining the benefit before the first click |
| High activated-to-adopted drop (>70% drop) | Feature delivers value in first use but not enough to return | Review what value the feature delivers on second and third use; add progress/reward signals |
| High adopted-to-habitual drop (>60% drop) | No habit trigger — users are using the feature but not building a routine | Add a recurring prompt, scheduled reminder, or contextual trigger to bring users back |
| Strong adoption in one segment only | Feature is niche — designed for one use case but positioned as universal | Either expand the feature to serve the broader population or explicitly target the niche segment |
| Adoption declining in existing users | Feature regressed, competing feature launched, or use case has been automated | Check for recent product changes; compare retention of feature users vs non-users before and after |

---

## Part 6: Segment Adoption Analysis

Find the user segment with 2x average adoption — their behavior is the blueprint.

### Standard segmentation dimensions for feature adoption

| Dimension | Why it matters |
|---|---|
| User tenure (new vs. established) | New users may not know the feature; established users may have entrenched habits |
| Plan / tier | Premium users often adopt faster; free users may not have access |
| Acquisition channel | Organic users often adopt more features than paid-acquisition users |
| Device type | Feature may be desktop-only or mobile-optimized differently |
| Activation depth (onboarding score) | Users who completed more onboarding steps adopt more features |
| Power user vs casual user | Power users are often early adopters and show what depth looks like at maximum |

### What to do with the 2x segment

1. Identify the 2x adoption segment (e.g., "users who completed full onboarding have 3x breadth")
2. Understand what they do differently in their first session (session replay, interview)
3. Test whether other users can replicate that experience (A/B test on onboarding flow)
4. Use this segment as your beta group for future feature improvements

---

## Part 7: Feature Retirement Signal

Not all features deserve to live forever. Use this checklist to identify retirement candidates.

| Signal | Threshold | Weight |
|---|---|---|
| Breadth after 90 days | <5% of MAU | High |
| Breadth trend | Declining for 3+ consecutive months | High |
| Correlation with retention | Feature use has no correlation with D30 retention | High |
| Engineering maintenance cost | Requires ongoing maintenance with no roadmap investment | Medium |
| User complaint / confusion | Support tickets or negative NPS comments mention the feature | Medium |
| Competitive parity | Feature exists only to match a competitor, not because users need it | Low |

**Retirement decision rule:** if a feature scores high on 2+ High signals, it is a candidate for retirement or redesign. Before retiring, run a user survey with the small % who use it — sometimes a low-breadth feature has disproportionate value for a specific segment.

**Retirement options:**
- Full removal (deprecation) — highest risk; requires user communication
- Default off (opt-in only) — reduces surface area without full removal
- Redesign — if the concept is valid but the execution is wrong

---

## Part 8: Adoption Improvement Playbook

Systematic tactics by stage of the adoption funnel.

### Improving Aware-to-Activated (discoverability)

| Tactic | When to use |
|---|---|
| In-app tooltip on the entry point | Feature exists but users walk past it |
| Onboarding checklist that includes the feature | Feature should be part of first-session setup |
| Contextual nudge (right time, right trigger) | Feature is relevant at a specific user action (e.g., "Try X when you Y") |
| Progressive disclosure (reveal after N uses of related feature) | Feature requires context before it makes sense |
| Default-on (enable for all users with opt-out) | High-value feature where the risk of forced exposure is low |

### Improving Activated-to-Adopted (value delivery on repeat use)

| Tactic | When to use |
|---|---|
| Reduce friction on the second use (save settings, remember context) | First use requires setup; second use should be instant |
| Show results clearly after each use | Feature output is not obvious — users don't see the value |
| Add a progress indicator (e.g., "You've saved 3 items — try X next") | Users need a sense of progress to return |
| Pair with a notification at the natural re-use moment | Users forget to return; a well-timed prompt brings them back |

### Improving Adopted-to-Habitual (habit formation)

| Tactic | When to use |
|---|---|
| Scheduled trigger (e.g., "Your weekly summary is ready") | Feature has a natural weekly or daily cadence |
| Streak or progress mechanic | Feature benefits from consistent use; gamification is appropriate |
| Make the feature part of a workflow the user already has | Attach the feature to an existing habit rather than creating a new one |
| Personalization to increase relevance | Generic feature outputs reduce return motivation; personalized outputs increase it |

---

## Part 9: SQL Pattern for Feature Adoption Funnel

```sql
-- Feature adoption funnel: Aware → Activated → Adopted → Habitual
-- Replace event names with your actual tracking events
-- Assumes: events table (user_id, event_name, event_date)
-- Analysis window: last 30 days

WITH user_base AS (
  -- MAU as the denominator for breadth
  SELECT DISTINCT user_id
  FROM events
  WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
),
adoption_stages AS (
  SELECT
    ub.user_id,
    MAX(CASE WHEN e.event_name = 'feature_entry_point_seen' THEN 1 ELSE 0 END) AS is_aware,
    MAX(CASE WHEN e.event_name = 'feature_first_used' THEN 1 ELSE 0 END) AS is_activated,
    CASE WHEN COUNT(CASE WHEN e.event_name = 'feature_used' THEN 1 END) >= 3 THEN 1 ELSE 0 END AS is_adopted,
    -- Habitual: used in at least 3 of the last 4 weeks
    COUNT(DISTINCT CASE
      WHEN e.event_name = 'feature_used'
      THEN DATE_TRUNC(e.event_date, WEEK) -- BigQuery
    END) AS active_weeks_with_feature
  FROM user_base ub
  LEFT JOIN events e
    ON ub.user_id = e.user_id
    AND e.event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY ub.user_id
)
SELECT
  COUNT(DISTINCT user_id)                                              AS mau,
  SUM(is_aware)                                                        AS aware,
  SUM(is_activated)                                                    AS activated,
  SUM(is_adopted)                                                      AS adopted,
  SUM(CASE WHEN active_weeks_with_feature >= 3 THEN 1 ELSE 0 END)     AS habitual,
  ROUND(SUM(is_aware)     / COUNT(DISTINCT user_id), 4)                AS breadth_aware,
  ROUND(SUM(is_activated) / NULLIF(SUM(is_aware), 0), 4)              AS aware_to_activated,
  ROUND(SUM(is_adopted)   / NULLIF(SUM(is_activated), 0), 4)          AS activated_to_adopted,
  ROUND(SUM(CASE WHEN active_weeks_with_feature >= 3 THEN 1 ELSE 0 END) / NULLIF(SUM(is_adopted), 0), 4) AS adopted_to_habitual
FROM adoption_stages
```

---

## Part 10: Analysis Output Format

```
## Feature Adoption Analysis: [Feature Name]

**Analysis window:** [date range]
**MAU base:** [N]

### Adoption dimensions
- Breadth: [X%] of MAU (benchmark: [Y%])
- Depth: [X] uses per adopted user per week
- Frequency: [X%] of active sessions include this feature

### Adoption funnel

| Stage | Users | Conversion from prior | Conversion from Aware |
|---|---|---|---|
| Aware | | | 100% |
| Activated | | | |
| Adopted | | | |
| Habitual | | | |

### Aha moment hypothesis
[Action most correlated with habitual adoption, with conversion data]

### Adoption by segment
[Top 2 segments with best and worst adoption — include breadth numbers]

### Diagnosis
[Which stage is the biggest bottleneck and root cause]

### Improvement roadmap
| Priority | Tactic | Stage it addresses | Expected lift | Effort |
|---|---|---|---|---|
| P0 | | | | |
| P1 | | | | |

### Feature retirement risk
[Low / Medium / High — with supporting data points]

### Follow-up questions
[What this analysis cannot answer and what data is needed]
```

---

### Further Reading

- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
- [The Product Analytics Playbook](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Cohort Analysis 101](https://www.productcompass.pm/p/cohort-analysis)
