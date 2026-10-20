---
name: PMF Validation Plan
description: Designs product-market fit validation using JTBD interviews, willingness-to-pay probes, activation metrics, and retention cohorts. Use before scaling GTM.
version: 1.0.0
dependencies: none
---

# PMF Validation Plan

## Overview

Product-Market Fit (PMF) is **not** a binary state—it's a spectrum. This skill provides a systematic framework for measuring where you are on that spectrum and what actions will move you toward strong PMF.

**When to use this skill:**
- Before scaling go-to-market (GTM)
- When retention is weak (<40% month-2)
- When you're unsure if you've hit PMF
- When pivoting product positioning or target customer

## What is PMF?

**Marc Andreessen's definition:**
> "Product-market fit means being in a good market with a product that can satisfy that market."

**Rahul Vohra's (Superhuman) operational definition:**
> ≥40% of users would be "very disappointed" if the product disappeared.

**Sean Ellis's test:**
> ≥40% of users say the product is a "must-have."

**This skill's definition:**
> PMF exists when you have **repeatable, profitable customer acquisition** and **strong retention** (≥60% active after 3 months).

## The PMF Spectrum

```
No PMF → Weak PMF → Moderate PMF → Strong PMF
  |          |            |             |
  0%        20%          40%           60%+

Retention (Month 3)
Willing to pay
NPS ≥40
```

**No PMF (0-20%):**
- Low retention (most users churn after 1 month)
- Users won't pay or will pay very little
- NPS <0 (more detractors than promoters)

**Weak PMF (20-40%):**
- Some users love it, most are lukewarm
- Retention is inconsistent (varies by cohort)
- Willingness-to-pay exists but low (<$20/month)

**Moderate PMF (40-60%):**
- Solid core of passionate users
- Retention is stable (≥40% month-3)
- Clear JTBD, users can articulate value
- WTP is healthy ($50-100/month for B2B)

**Strong PMF (60%+):**
- Users describe product as "indispensable"
- Retention curve flattens (little churn after month 1)
- High NPS (≥50)
- Word-of-mouth growth (organic referrals)

## The 4 Pillars of PMF Validation

### 1. Jobs-to-be-Done (JTBD) Clarity

**Question:** What "job" are users hiring your product to do?

**Framework (Clayton Christensen):**
> "When [situation], I want to [motivation], so I can [outcome]."

**Example (Superhuman email client):**
> "When I'm drowning in email, I want to process my inbox to zero in <30 minutes, so I can focus on deep work without anxiety."

**Validation Method:**

1. **Interview 20-30 users** (mix of active and churned)
2. Ask: "When was the last time you used [product]? What were you trying to accomplish?"
3. Look for **convergence**:
   - If 80% describe the same job → JTBD clarity is high
   - If answers are scattered → JTBD clarity is low (weak PMF signal)

**Red Flags:**
- Users can't articulate why they use it ("I don't know, it's cool?")
- Different user segments describe completely different jobs
- Job described is not important/urgent ("Nice to have" vs "Must have")

**Output:** JTBD statement(s) for each user segment

### 2. Willingness-to-Pay (WTP) Probes

**Question:** How much would users pay? What's the ceiling?

**Van Westendorp Price Sensitivity Meter:**

Ask 4 questions:
1. **Too cheap:** At what price would you question the quality?
2. **Bargain:** At what price would you consider it a great deal?
3. **Expensive:** At what price does it start to feel expensive (but you'd still buy)?
4. **Too expensive:** At what price would you not consider buying?

**Analysis:**

Plot cumulative responses:
- **Optimal Price Point (OPP):** Intersection of "Too cheap" and "Too expensive"
- **Acceptable Price Range:** Between "Bargain" and "Expensive"

**Example (AI coding agent):**

Survey 100 users:

| Price | Too Cheap | Bargain | Expensive | Too Expensive |
|-------|-----------|---------|-----------|---------------|
| $10   | 80%       | 10%     | 0%        | 0%            |
| $20   | 50%       | 30%     | 5%        | 0%            |
| $30   | 20%       | 60%     | 15%       | 5%            |
| $40   | 5%        | 75%     | 30%       | 10%           |
| $50   | 0%        | 60%     | 50%       | 20%           |
| $60   | 0%        | 40%     | 70%       | 35%           |

**OPP:** ~$40/month (maximize revenue while minimizing churn)

**PMF Signal:**
- **Strong PMF:** OPP is ≥3x COGS (healthy margin)
- **Weak PMF:** Users won't pay above COGS (no value perception)

### 3. Activation Metrics (Aha Moment)

**Question:** What's the earliest indicator that a user will retain?

**Framework (Chamath Palihapitiya, Facebook):**
> Find the "aha moment"—the action that correlates most strongly with retention.

**Examples:**
- **Facebook:** "7 friends in 10 days"
- **Slack:** "2,000 messages sent by team"
- **Dropbox:** "1 file uploaded from 1 device"

**How to Find Your Activation Metric:**

1. **Cohort Analysis:**
   - Segment users by retention (retained vs churned)
   - Identify actions taken in first 7 days

2. **Correlation Analysis:**
   - Which action has highest correlation with month-1 retention?
   - Example: Users who complete onboarding tutorial retain at 60% vs 15% who skip

3. **Define Activation:**
   - "A user is activated when they [action] within [time window]."
   - Example: "User is activated when they resolve ≥10 support tickets in first 14 days."

**PMF Signal:**
- **Strong PMF:** Activated users retain at ≥60%
- **Weak PMF:** Even activated users churn at >50%

### 4. Retention Cohorts

**Question:** Are users sticking around? Is retention improving over time?

**Retention Curve Analysis:**

```
Month 0: 100%
Month 1: 60%
Month 2: 45%
Month 3: 40%
Month 4: 38%
Month 5: 37%
Month 6: 36%
```

**PMF Signals:**

**Strong PMF:**
- Month-1 retention ≥60%
- Curve flattens by month 3 (churn rate <5%/month after that)
- Improving over time (newer cohorts retain better)

**Weak PMF:**
- Month-1 retention <40%
- Curve keeps declining (no flattening)
- Newer cohorts retain worse (product is getting worse?)

**Cohort Comparison:**

| Cohort | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Jan 2025 | 50% | 30% | 20% |
| Feb 2025 | 55% | 35% | 25% |
| Mar 2025 | 62% | 42% | — |

**Interpretation:** PMF is improving (each cohort retains better than prior).

---

## PMF Validation Plan Template

```json
{
  "validation_plan": {
    "objective": "Determine if AI Support Agent has achieved moderate PMF (≥40% month-3 retention, ≥$50/month WTP)",
    "timeline": "6 weeks",
    "sample_size": {
      "jtbd_interviews": 30,
      "wtp_survey": 100,
      "activation_analysis": "all users (cohorts since Jan 2025)",
      "retention_cohorts": "all users (6-month window)"
    }
  },

  "jtbd_validation": {
    "method": "30 customer interviews (15 active, 15 churned)",
    "questions": [
      "When was the last time you used the AI Support Agent?",
      "What were you trying to accomplish?",
      "What would happen if the AI Support Agent disappeared tomorrow?",
      "What did you use before the AI Support Agent?"
    ],
    "success_criteria": {
      "convergence_threshold": "≥70% describe same core job",
      "importance": "≥60% say job is 'very important' or 'critical'"
    },
    "hypothesis": "Users hire AI Support Agent to reclaim ≥10 hours/week spent on repetitive support tickets."
  },

  "wtp_validation": {
    "method": "Van Westendorp survey (100 users)",
    "questions": [
      "At what price would you question the quality? (Too cheap)",
      "At what price is it a great deal? (Bargain)",
      "At what price does it feel expensive but you'd still buy? (Expensive)",
      "At what price would you not buy? (Too expensive)"
    ],
    "success_criteria": {
      "opp_target": "≥$50/month",
      "margin_check": "OPP ≥3x COGS ($15/month)"
    },
    "hypothesis": "Users will pay $50-100/month (current pricing is $99/month, may be too high)."
  },

  "activation_validation": {
    "method": "Cohort analysis (retained vs churned users)",
    "candidate_metrics": [
      "Tickets resolved in first 14 days",
      "Days to first resolved ticket",
      "Documentation pages connected",
      "Custom rules created"
    ],
    "analysis": "Logistic regression to find strongest predictor of month-1 retention",
    "success_criteria": {
      "activation_rate": "≥50% of users hit activation metric",
      "activated_retention": "≥60% of activated users retain to month 1"
    },
    "hypothesis": "Users who resolve ≥10 tickets in first 14 days retain at ≥60%."
  },

  "retention_validation": {
    "method": "Cohort retention curves (Jan-Sep 2025 cohorts)",
    "metrics": [
      "Month-1 retention",
      "Month-3 retention",
      "Month-6 retention",
      "Churn rate by month"
    ],
    "success_criteria": {
      "month1_retention": "≥60%",
      "month3_retention": "≥40%",
      "curve_flattening": "Churn <5%/month after month 3",
      "cohort_improvement": "Newer cohorts retain ≥10% better than older"
    },
    "hypothesis": "We have moderate PMF (40-60% month-3 retention)."
  },

  "supplementary_metrics": {
    "nps": {
      "method": "Survey 100 users: 'How likely are you to recommend (0-10)?'",
      "target": "≥40 (moderate PMF)"
    },
    "sean_ellis_test": {
      "method": "Survey 100 users: 'How would you feel if you could no longer use this product?'",
      "options": ["Very disappointed", "Somewhat disappointed", "Not disappointed"],
      "target": "≥40% 'Very disappointed'"
    },
    "organic_growth": {
      "method": "Track % of new signups from referrals (not paid ads)",
      "target": "≥20% organic (word-of-mouth signal)"
    }
  },

  "decision_framework": {
    "strong_pmf": {
      "criteria": [
        "Month-3 retention ≥60%",
        "WTP ≥$75/month",
        "NPS ≥50",
        "Sean Ellis test ≥60%"
      ],
      "action": "Scale GTM: Increase ad spend, hire sales team"
    },
    "moderate_pmf": {
      "criteria": [
        "Month-3 retention 40-60%",
        "WTP $50-75/month",
        "NPS 40-50",
        "Sean Ellis test 40-60%"
      ],
      "action": "Iterate on activation: Improve onboarding, focus on aha moment"
    },
    "weak_pmf": {
      "criteria": [
        "Month-3 retention 20-40%",
        "WTP <$50/month",
        "NPS <40",
        "Sean Ellis test <40%"
      ],
      "action": "Product changes: Fix core JTBD, improve accuracy, re-interview users"
    },
    "no_pmf": {
      "criteria": [
        "Month-3 retention <20%",
        "WTP <$20/month",
        "NPS <0"
      ],
      "action": "Pivot: Consider different target customer, different JTBD, or shut down"
    }
  },

  "timeline": {
    "week1": "Design surveys, recruit interview participants",
    "week2-3": "Conduct JTBD interviews (30 users)",
    "week3-4": "Run WTP survey (100 users)",
    "week4-5": "Analyze activation metrics (cohort data)",
    "week5-6": "Analyze retention curves, synthesize findings",
    "week6": "Present PMF assessment and recommendations"
  }
}
```

---

## Common PMF Mistakes

❌ **Vanity Metrics:** "We have 10,000 signups!" (but 90% churn)
✅ **Retention Focus:** "We have 1,000 users, 60% active after 3 months."

❌ **Premature Scaling:** Spending on ads before PMF
✅ **Earn PMF First:** Achieve ≥40% month-3 retention, then scale

❌ **Ignoring Churn Reasons:** "Users just didn't get it."
✅ **Churn Interviews:** "Why did you stop using? What did you switch to?"

❌ **Generic JTBD:** "Users want to be more productive."
✅ **Specific JTBD:** "Solo founders want to reclaim 10+ hours/week spent on repetitive support tickets."

❌ **Assuming PMF is Binary:** "We either have it or we don't."
✅ **PMF is a Spectrum:** Measure where you are (weak/moderate/strong).

---

## Output Files

1. **Primary:** `pmf/pmf_plan.md` - Validation plan with methods, timelines, success criteria
2. **Data:** `pmf/jtbd_synthesis.json` - JTBD interview findings
3. **Data:** `pmf/wtp_analysis.json` - Van Westendorp curve, OPP
4. **Data:** `pmf/activation_analysis.json` - Activation metric definition, retention by activation
5. **Data:** `pmf/retention_cohorts.json` - Cohort retention curves
6. **Summary:** `pmf/pmf_assessment.md` - Final assessment (strong/moderate/weak/no PMF) + recommendations

---

## Quality Checklist

Before declaring PMF assessment complete:

- [ ] JTBD interviews conducted (≥20 users)
- [ ] WTP survey conducted (≥100 users)
- [ ] Activation metric identified (correlation with retention)
- [ ] Retention cohorts analyzed (≥3 months data)
- [ ] NPS measured
- [ ] Sean Ellis test conducted
- [ ] Decision made: strong/moderate/weak/no PMF
- [ ] Next actions defined based on PMF level

---

## References

See Rahul Vohra's Superhuman PMF Engine (First Round Review)
See Sean Ellis's PMF Survey methodology
See Clayton Christensen's *Competing Against Luck* (JTBD framework)
See Andrew Chen's *Cold Start Problem* (retention curve analysis)
See Lenny Rachitsky's PMF Survey (compilation of PMF metrics across 40+ companies)
