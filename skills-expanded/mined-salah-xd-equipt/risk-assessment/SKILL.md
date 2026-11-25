---
name: risk-assessment
description: "Conducts business risk assessments with likelihood and impact scoring, mitigation strategies, and monitoring plans for proactive risk management."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Risk Assessment

## When to Use This Skill

Use this skill when you need to:
- Identify and score business risks by likelihood and impact
- Create mitigation strategies for high-priority risks
- Build a risk monitoring plan with early warning indicators
- Prepare for a new venture, product launch, or major business change

**DO NOT** use this skill for financial risk modeling, insurance assessments, or cybersecurity threat analysis. This is for general business risk identification and planning.

---

## Core Principle

RISK MANAGEMENT IS NOT ABOUT ELIMINATING RISK — IT IS ABOUT KNOWING WHICH RISKS ARE WORTH TAKING AND HAVING A PLAN FOR THE ONES THAT COULD KILL YOUR BUSINESS.

---

## Phase 1: Identify

Surface all relevant risks before scoring them.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business context** | "Describe your business and current stage." | No default |
| **Assessment trigger** | "Why now? (new venture, annual review, specific concern)" | Annual review |
| **Revenue model** | "How do you make money? (services, products, subscriptions)" | No default |
| **Dependencies** | "What does your business depend on most? (key clients, platforms, suppliers)" | No default |
| **Known risks** | "What risks are already on your radar?" | No default |

### Risk Categories

Walk through each category to ensure comprehensive coverage:

- **Financial:** Cash flow, revenue concentration, pricing, debt
- **Operational:** Key person dependency, tool failures, process breakdowns
- **Market:** Competition, demand shifts, economic conditions
- **Legal/Compliance:** Contracts, regulations, IP, liability
- **Reputational:** Brand damage, negative reviews, public relations
- **Technology:** Platform dependency, data loss, security

```
## Risk Register

| # | Risk | Category | Description |
|---|------|----------|-------------|
| R1 | [Risk name] | [Category] | [What could happen and how] |
| R2 | [Risk name] | [Category] | [What could happen and how] |
```

**GATE: Confirm the risk register is complete before scoring.**

---

## Phase 2: Score

Assess each risk using likelihood and impact scoring.

### Scoring Matrix

Rate each risk 1-5 on both dimensions:

| Score | Likelihood | Impact |
|-------|-----------|--------|
| 1 | Rare (less than 5% chance) | Negligible (minor inconvenience) |
| 2 | Unlikely (5-20%) | Minor (temporary disruption) |
| 3 | Possible (20-50%) | Moderate (significant effort to recover) |
| 4 | Likely (50-80%) | Major (serious financial or operational damage) |
| 5 | Almost certain (80%+) | Catastrophic (business survival threatened) |

```
## Risk Scoring

| # | Risk | Likelihood | Impact | Risk Score | Priority |
|---|------|-----------|--------|-----------|----------|
| R1 | [Name] | [1-5] | [1-5] | [L x I] | [Critical/High/Medium/Low] |

**Priority thresholds:**
- Critical: 15-25 — Immediate action required
- High: 10-14 — Mitigation plan needed within 30 days
- Medium: 5-9 — Monitor and prepare contingency
- Low: 1-4 — Accept and review quarterly
```

### Risk Heat Map

Present a visual summary:

```
         Impact →
         1    2    3    4    5
    5  | M  | H  | C  | C  | C  |
L   4  | M  | H  | H  | C  | C  |
i   3  | L  | M  | H  | H  | C  |
k   2  | L  | L  | M  | H  | H  |
e   1  | L  | L  | L  | M  | M  |
```

**GATE: Review scored risks before building mitigation plans.**

---

## Phase 3: Mitigate

Create action plans for high and critical risks.

### Mitigation Strategy Template

For each critical and high-priority risk:

```
## Mitigation Plan: [Risk Name]

**Risk score:** [X] (Likelihood [X] x Impact [X])
**Risk owner:** [Name]

**Prevention (reduce likelihood):**
- [Action to prevent the risk from occurring]
- [Action]

**Preparation (reduce impact):**
- [Action to minimize damage if it occurs]
- [Action]

**Response (if it happens):**
1. [Immediate action]
2. [Short-term recovery step]
3. [Long-term recovery step]

**Early warning indicators:**
- [Sign that this risk is becoming more likely]
- [Metric to monitor]

**Review frequency:** [Monthly / Quarterly]
```

### Common Solopreneur Mitigations

| Risk | Common Mitigation |
|------|-------------------|
| Revenue concentration (1-2 big clients) | Diversify: no client should exceed 30% of revenue |
| Key person dependency | Document processes, cross-train, build a contractor bench |
| Platform dependency | Maintain email list, diversify channels, export data regularly |
| Cash flow gaps | Maintain 3-month operating reserve, invoice promptly |

---

## Phase 4: Monitor

Set up ongoing risk monitoring.

### Risk Dashboard

```
## Risk Dashboard — [Quarter/Year]

| Risk | Score | Status | Last Reviewed | Next Review | Owner |
|------|-------|--------|--------------|-------------|-------|
| [Name] | [X] | Stable / Increasing / Decreasing | [Date] | [Date] | [Name] |
```

### Review Cadence

- **Monthly:** Review critical and high risks — any changes in likelihood or impact?
- **Quarterly:** Full risk register review — add new risks, retire resolved ones, re-score
- **After any incident:** Update the affected risk's score and mitigation plan

### Risk Appetite Statement

Help the user define their risk tolerance:

```
**Our risk appetite:**
- We ACCEPT risks scored 1-4 (Low) without active mitigation
- We MITIGATE risks scored 5-14 (Medium-High) with documented plans
- We AVOID or TRANSFER risks scored 15-25 (Critical) — these threaten business survival
```

---

## Anti-Patterns

- **Ignoring low-probability, high-impact risks** — "It will never happen" is not a strategy. Plan for catastrophic risks even if unlikely.
- **Risk register as a one-time exercise** — risks change constantly. A static register is a false sense of security.
- **No risk owner** — unowned risks are unmanaged risks. Every risk needs one accountable person.
- **Mitigation without monitoring** — you cannot know if mitigation is working without tracking indicators.
- **Analysis paralysis** — do not score 50 risks. Focus on the top 10-15 that matter most.

---

## Recovery

- **User cannot identify risks:** Walk through each category with specific prompts: "What happens if your biggest client leaves tomorrow?"
- **Everything scores as critical:** Recalibrate — compare each risk to "business cannot operate tomorrow." Only true existential threats are 5/5.
- **User wants to ignore risks:** Focus on the one risk that scares them most. Getting one mitigation plan in place builds the habit.
- **Risk has already materialized:** Switch to incident response. Document what happened, stabilize, then update the assessment with lessons learned.
- **User is overwhelmed:** Start with the top 3 risks only. A plan for 3 risks is infinitely better than no plan for 20.
