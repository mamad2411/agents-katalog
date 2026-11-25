---
name: churn-prevention-playbook
description: "Creates churn prevention playbooks with early warning indicators, intervention sequences, and save offer strategies. Use when reducing customer churn in subscription businesses."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Churn Prevention Playbook

## When to Use This Skill

Use this skill when you need to:
- Build a systematic churn prevention strategy for a subscription business
- Identify early warning signals that predict customer cancellation
- Design intervention sequences to save at-risk accounts
- Create save offers and retention playbooks for support teams

**DO NOT** use this skill for win-back campaigns (post-churn), customer acquisition strategies, or pricing restructuring. This is for preventing active customers from leaving.

---

## Core Principle

CHURN PREVENTION STARTS 60 DAYS BEFORE THE CANCELLATION CLICK — BY THE TIME A CUSTOMER ASKS TO CANCEL, YOU HAVE ALREADY LOST MOST OF THE BATTLE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product type** | "What is your subscription product?" | No default — must be provided |
| **Current churn rate** | "What is your monthly churn rate?" | Unknown — estimate from available data |
| **Billing cycle** | "Monthly, annual, or both?" | Monthly |
| **Top cancellation reasons** | "Why do customers say they leave? Top 3 reasons." | No default — critical input |
| **Customer segments** | "Do you have different customer tiers or segments?" | Single tier |
| **Current retention efforts** | "What do you currently do to prevent churn?" | Nothing systematic |

**GATE: Confirm the brief before building the playbook.**

---

## Phase 2: Plan

### Early Warning System

Define 5-8 behavioral signals that predict churn:

```
## Early Warning Indicators

| Signal | Risk Level | Detection Window |
|--------|-----------|-----------------|
| Login frequency drops 50%+ | High | 14 days |
| Key feature usage stops | High | 7 days |
| Support tickets increase 3x | Medium | 30 days |
| Payment failure (no update) | High | Immediate |
| Team seats decrease | Medium | Billing cycle |
| Downgrade inquiry | High | Immediate |
| NPS score drops below 6 | Medium | Survey cycle |
| No login for 14+ days | Critical | 14 days |
```

### Risk Scoring Model

Create a simple scoring framework:
- **Green (0-2 signals):** Healthy — standard engagement
- **Yellow (3-4 signals):** At risk — trigger proactive outreach
- **Red (5+ signals):** High risk — immediate intervention

**GATE: Confirm warning indicators and risk levels before designing interventions.**

---

## Phase 3: Write

### Intervention Playbook

For each risk level, define the response:

**Yellow — Proactive Engagement:**
- Automated email: "We noticed you haven't used [feature] recently. Here's a quick tip..."
- In-app message highlighting underused features
- Customer success check-in (if high-value account)

**Red — Active Retention:**
- Personal email from founder or CS lead
- Offer a 15-minute strategy call
- Share a customer success story relevant to their use case
- Present a save offer (see Save Offer Menu below)

**Cancellation Page — Last Resort:**
- Exit survey (required, 3 questions max)
- Save offer based on stated reason
- Downgrade option instead of full cancellation
- Pause subscription option (30/60/90 days)

### Save Offer Menu

Design offers matched to cancellation reasons:

| Reason | Save Offer | Terms |
|--------|-----------|-------|
| Too expensive | Discount (20-30% for 3 months) | One-time, non-renewable |
| Not using it enough | Free strategy call + usage guide | Within 7 days |
| Missing a feature | Roadmap preview + beta access | Feature ETA required |
| Switching to competitor | Match competitor pricing or feature | Case-by-case |
| Business closing | Pause subscription | Up to 90 days |

### Email Templates

Write 3 core retention emails:
1. **Check-in email** — friendly, value-focused, no mention of churn
2. **Re-engagement email** — highlight a feature they have not tried
3. **Save email** — direct, empathetic, includes a specific offer

---

## Phase 4: Polish

### 1. Metrics Framework

```
## Churn Prevention Metrics

- **Monthly churn rate:** Track month-over-month trend
- **Save rate:** % of at-risk accounts retained after intervention
- **Intervention response rate:** % of at-risk users who engage with outreach
- **Save offer acceptance rate:** % who accept a retention offer
- **Time to churn signal:** Average days between first warning signal and cancellation
- **Reactivation rate:** % of paused accounts that resume
```

### 2. Team Playbook Card

Create a quick-reference card for support/CS teams:
- Risk signals to watch for
- Approved save offers and their limits
- Escalation path for high-value accounts
- Scripts for common cancellation conversations

### 3. Quality Checklist

```
## Churn Prevention Checklist

- [ ] 5-8 early warning indicators defined with detection windows
- [ ] Risk scoring model has clear thresholds (green/yellow/red)
- [ ] Intervention sequence exists for each risk level
- [ ] Save offers are matched to specific cancellation reasons
- [ ] Cancellation page includes exit survey, save offer, and pause option
- [ ] 3 retention email templates are written
- [ ] Metrics framework tracks save rate and intervention effectiveness
- [ ] Support team has a quick-reference playbook card
- [ ] Save offers have clear terms and limits (not unlimited discounts)
```

---

## Example

**Product:** Social media scheduling SaaS, $29/month
**Churn rate:** 8% monthly
**Top reasons:** Too expensive, not posting enough to justify it, switched to free tool

**Check-in email excerpt:**
"Hey [Name], I noticed you scheduled 3 posts this month — down from 12 last month. Quick tip: our new batch scheduling feature lets you plan a full week in under 10 minutes. Here is a 2-minute walkthrough. [Watch Video]"

**Save offer for "too expensive":**
"I get it — every dollar matters when you are running your own business. I can offer you 3 months at $19/month (35% off) while you evaluate the ROI. No strings — if it is still not working after 3 months, cancel with one click."

---

## Anti-Patterns

- **Discounting everyone** — save offers for price-sensitive churners only. Usage-based churners need value, not discounts.
- **Ignoring the warning signals** — waiting until cancellation to act is too late. Intervene at yellow, not red.
- **Generic "We miss you" emails** — reference specific behavior or features. Generic emails feel automated and impersonal.
- **No exit survey** — if you do not know why people leave, you cannot fix the product. Always collect the reason.
- **Unlimited save offers** — one discount per customer, with clear terms. Otherwise you train customers to threaten cancellation for discounts.

---

## Recovery

- **No churn data exists:** Start with an exit survey on the cancellation page. Collect 30 days of data before building the full playbook.
- **Churn rate is unknown:** Calculate from billing data: (customers lost this month / customers at start of month) x 100.
- **Too few customers for patterns:** Use qualitative interviews with 5-10 recent churners. Their stories reveal the signals data cannot show yet.
- **Team too small for manual outreach:** Automate the yellow-tier interventions. Reserve manual effort for red-tier and high-value accounts only.
