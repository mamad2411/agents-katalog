---
name: ab-test-plan
description: "Designs A/B test plans with hypothesis, variants, sample size calculations, success metrics, and statistical significance criteria. Use when optimizing conversions or UX."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# A/B Test Plan

## When to Use This Skill

Use this skill when you need to:
- Plan an A/B test for a landing page, email, ad, or feature
- Calculate required sample size and test duration
- Define clear success criteria before running an experiment
- Document test results and decide whether to implement the winner

**DO NOT** use this skill for multivariate tests with 5+ variables, scientific research experiments, or theoretical statistics exercises. This is for practical business A/B testing.

---

## Core Principle

EVERY TEST MUST HAVE A HYPOTHESIS WRITTEN BEFORE THE TEST STARTS — IF YOU CANNOT STATE WHAT YOU EXPECT AND WHY, YOU ARE GUESSING, NOT TESTING.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **What to test** | "What are you testing? (headline, CTA, pricing page, email subject, ad creative)" | Must be provided |
| **Current metric** | "What is the current conversion rate or metric you want to improve?" | Must be provided or estimated |
| **Goal** | "What improvement would be meaningful? (e.g., +20% conversion rate)" | 10-20% relative improvement |
| **Traffic/volume** | "How much traffic or how many impressions does this asset get per week?" | Must be provided |
| **Tool** | "What testing tool will you use? (Google Optimize, VWO, Optimizely, built-in)" | Google Optimize or native platform |
| **Risk tolerance** | "How confident do you need to be? (90%, 95%, 99%)" | 95% statistical significance |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Design

### Hypothesis Framework

Write the hypothesis using this format:

**"If we [change], then [metric] will [improve/increase/decrease] because [reason based on user behavior insight]."**

Example: "If we change the CTA button text from 'Learn More' to 'Start Free Trial,' then click-through rate will increase by 15% because it sets a clearer expectation of the next step."

### Test Design Elements

1. **Control (A)** — current version, described specifically
2. **Variant (B)** — changed version, with one clear difference
3. **Primary metric** — the single metric that determines the winner
4. **Secondary metrics** — supporting metrics to watch for unintended effects
5. **Sample size calculation** — minimum visitors per variant
6. **Test duration** — days to run based on traffic and sample size
7. **Segmentation** — any audience segments to analyze separately

### Sample Size Guidance

Provide the formula context:
- Baseline conversion rate + minimum detectable effect + significance level = required sample per variant
- Rule of thumb: at 5% baseline, detecting a 20% relative lift at 95% significance requires ~4,000 visitors per variant

**GATE: Present the test plan and wait for approval.**

---

## Phase 3: Build

### Deliverables

**1. Complete Test Plan Document**
- Hypothesis statement
- Control and variant descriptions with visual mockup notes
- Primary and secondary metrics
- Sample size and duration estimate
- Start and end dates
- Decision criteria (what score means "winner")

**2. Pre-Launch Checklist**
- [ ] Hypothesis documented
- [ ] Control and variant built and QA tested
- [ ] Tracking verified on both versions
- [ ] Traffic split configured (50/50 default)
- [ ] No other tests running on the same page/audience
- [ ] Minimum duration committed (do not peek early)

**3. Results Documentation Template**
- Variant performance table (metric, sample, conversion rate, confidence interval)
- Winner declaration with confidence level
- Recommendation: implement, iterate, or discard
- Learnings for future tests

---

## Phase 4: Polish

### Post-Test Analysis Framework

1. **Did it reach significance?** If no, extend or call it inconclusive — never declare a winner below threshold.
2. **Check secondary metrics** — did the winner hurt anything else? (e.g., more clicks but lower purchase rate)
3. **Segment analysis** — did the variant win across all segments or only specific ones?
4. **Document the learning** — even failed tests teach something. Record the insight.

### Test Velocity Recommendation

Suggest a testing cadence: 1-2 tests per month for small businesses. Maintain a test backlog ranked by potential impact.

---

## Example 1: Landing Page Headline Test

**Hypothesis:** Changing the headline from benefit-focused ("Save 10 Hours a Week") to pain-focused ("Stop Wasting 10 Hours on Tasks AI Can Handle") will increase signup rate by 15%.
**Duration:** 3 weeks at 500 visitors/week. **Primary metric:** Email signup rate.

## Example 2: Email Subject Line Test

**Hypothesis:** Adding the recipient's first name to the subject line will increase open rate by 10%.
**Duration:** Single send to 5,000 subscribers, split 50/50. **Primary metric:** Open rate.

---

## Anti-Patterns

- **Testing without a hypothesis** — random changes teach nothing. State your prediction and reasoning first.
- **Peeking at results early** — checking daily and stopping when it "looks good" inflates false positives. Commit to the duration.
- **Testing too many variables** — if you change the headline, image, AND CTA, you cannot attribute the result. One change per test.
- **Tiny sample sizes** — 50 visitors per variant proves nothing. Calculate the minimum before starting.
- **Ignoring negative secondary metrics** — a headline that gets more clicks but fewer purchases is not a winner.

---

## Recovery

- **Not enough traffic:** Test higher-impact changes (bigger minimum detectable effect needs smaller sample). Or test in email/ads where volume is controllable.
- **Test is inconclusive:** Do not declare a winner. Either extend the test or accept that the difference is too small to matter and move on.
- **Stakeholder wants to pick the winner by gut:** Show the math. If results are not significant, implementing the "winner" is a coin flip.
- **No testing tool budget:** Use free tools (Google Optimize successor, email platform built-in splits) or manual URL splits with analytics tracking.
