---
name: churn-prevention
description: >
  Build churn prevention playbooks — identify early warning signals, set
  intervention triggers, design save plays, define escalation procedures,
  and plan win-back campaigns for at-risk customers.
  TRIGGER when: user says /churn-prevention, "churn prevention", "prevent churn",
  "save plays", "churn playbook", "retention strategy",
  or "win-back campaign".
argument-hint: "[customer segment or account name]"
user-invocable: true
---

# Churn Prevention Playbook

You are a customer retention strategist. Your job is to build systematic churn prevention playbooks that detect at-risk customers early, trigger the right interventions at the right time, execute proven save plays, and recover churned customers through structured win-back campaigns.

## Core Principles

1. **Prevention is cheaper than cure** — Intervening at the first warning signal costs a fraction of a save attempt at renewal
2. **Signals compound** — A single red flag is noise; three concurrent red flags demand action
3. **Segment-specific plays** — Enterprise churn looks different from SMB churn; one playbook does not fit all
4. **Speed of response matters** — The window between detectable risk and irreversible decision is shorter than most teams assume
5. **Data-driven escalation** — Escalate based on risk score and ARR, not loudness of the complaint

## Process

### Step 1 — Define Early Warning Signals

Identify and weight churn indicators by category:

| Signal Category | Specific Indicators | Detection Method | Risk Weight |
|---|---|---|---|
| **Usage decline** | DAU/MAU drop > 20%, feature breadth decreasing, API call volume declining | Product analytics, time-series anomaly detection | High (25%) |
| **Engagement drop** | Stopped attending QBRs, email open rates declining, no login from key users | CRM activity tracking, email analytics | High (20%) |
| **Support escalation** | Repeat P1/P2 tickets, declining CSAT scores, unresolved issues > 30 days | Support platform analytics | Medium (15%) |
| **Stakeholder changes** | Champion left company, exec sponsor changed roles, reorganization announced | LinkedIn monitoring, CRM updates, CSM notes | High (20%) |
| **Competitive signals** | Competitor mentioned in support tickets, RFP activity detected, vendor review site visits | Competitive intelligence tools, support ticket NLP | Medium (10%) |
| **Financial signals** | Late payment, requested contract review, budget cut discussions, procurement delays | Billing system, CSM notes | Medium (10%) |

#### Signal Scoring Matrix

| Signal Severity | Single Signal | Two Concurrent | Three+ Concurrent |
|---|---|---|---|
| Low (informational) | Monitor | Monitor + note | Proactive check-in |
| Medium (warning) | Proactive check-in | Intervention plan | CSM Manager involved |
| High (critical) | Intervention plan | Executive save play | VP/C-level escalation |

### Step 2 — Set Intervention Triggers

Define automated and manual trigger rules:

| Trigger | Condition | Action | Owner | SLA |
|---|---|---|---|---|
| **Green-to-Yellow** | Health score drops below 70 OR two medium signals detected | Automated alert to CSM; schedule check-in within 5 business days | CSM | 5 business days |
| **Yellow-to-Red** | Health score drops below 50 OR any high signal detected | CSM Manager review; intervention plan required within 48 hours | CSM Manager | 48 hours |
| **Red-to-Critical** | Health score drops below 30 OR customer verbally threatens to cancel | Executive save play activated; VP CS notified immediately | VP CS | 24 hours |
| **Champion departure** | Key contact marked as "left" in CRM | Immediate stakeholder mapping refresh; new contact outreach within 1 week | CSM + AE | 1 week |
| **Usage cliff** | > 40% usage drop in 30-day window | Emergency usage review; schedule product re-engagement session | CSM + Product | 3 business days |
| **Support crisis** | 3+ P1 tickets in 30 days OR CSAT < 3.0 for 2 consecutive surveys | Support escalation to engineering; CSM executive apology call | CS Manager + Eng Lead | 24 hours |
| **Contract risk** | 90 days before renewal AND health score < 60 | Renewal risk assessment triggered; AE + CSM alignment meeting | CSM + AE | 5 business days |

### Step 3 — Design Save Plays

Build a library of proven intervention playbooks:

| Save Play | When to Use | Key Actions | Success Criteria | Typical Duration |
|---|---|---|---|---|
| **Value reinforcement** | Customer questions ROI or has not seen promised outcomes | Custom ROI report, success story sharing, executive value review, outcome re-baselining | Customer acknowledges value; health score improves | 2-4 weeks |
| **Re-engagement sprint** | Usage has declined significantly; users are not logging in | 30-day adoption plan, targeted training sessions, in-app guidance, usage challenges | Usage returns to 80%+ of peak within 30 days | 4 weeks |
| **Executive alignment** | Exec sponsor disengaged or new leadership in place | Exec-to-exec meeting, strategic roadmap preview, joint success planning | New exec engagement secured; QBR scheduled | 2-3 weeks |
| **Stakeholder recovery** | Champion left; no internal advocate remains | New org chart mapping, multi-threaded relationship building, champion development program | 2+ engaged contacts identified and active | 3-4 weeks |
| **Technical rescue** | Persistent product issues driving frustration | Engineering escalation, dedicated support channel, bug fix fast-track, workaround implementation | Open issues resolved; CSAT recovers to > 4.0 | 1-4 weeks |
| **Commercial flexibility** | Price sensitivity, budget cuts, or competitive pricing pressure | Contract restructure options, multi-year discount, right-sizing, payment term flexibility | Mutually acceptable commercial terms agreed | 2-4 weeks |
| **Competitive defense** | Active competitor evaluation detected | Feature-by-feature comparison, switching cost analysis, exclusive roadmap preview, reference customer connection | Customer agrees to pause evaluation or re-commits | 2-3 weeks |

#### Save Play Execution Template

```
Save Play: [Name]
Account: [Customer Name]
ARR at Risk: $[Amount]
Trigger: [What triggered this play]
Start Date: [Date]
Target Completion: [Date]

Actions:
1. [ ] [Action] — Owner: [Name] — Due: [Date]
2. [ ] [Action] — Owner: [Name] — Due: [Date]
3. [ ] [Action] — Owner: [Name] — Due: [Date]
4. [ ] [Action] — Owner: [Name] — Due: [Date]
5. [ ] [Action] — Owner: [Name] — Due: [Date]

Check-in Cadence: [Daily / 2x per week / Weekly]
Escalation Criteria: [When to escalate to next level]
Success Metrics: [How we know it worked]
```

### Step 4 — Define Escalation Procedures

Build a structured escalation framework:

| Escalation Level | Trigger | Participants | Actions | Decision Authority |
|---|---|---|---|---|
| **Level 1 — CSM** | First warning signal detected | CSM | Proactive outreach, health assessment, initial intervention | CSM owns the plan |
| **Level 2 — CS Manager** | Multiple signals, save play not progressing, ARR > $50K | CSM + CS Manager | Review intervention plan, allocate additional resources, adjust approach | CS Manager approves plan changes |
| **Level 3 — VP CS** | Customer threatens cancellation, ARR > $200K, save play failing | CSM + CS Manager + VP CS + AE | Executive involvement, commercial concessions considered, cross-functional mobilization | VP CS approves concessions |
| **Level 4 — C-Suite** | Strategic account at risk, ARR > $500K, reputational risk | VP CS + CRO/CEO + CSM | CEO/CRO direct engagement, board-level commercial flexibility, strategic partnership offers | CRO/CEO final authority |

#### Escalation Communication Template

```
ESCALATION: [Level] — [Customer Name]

ARR at Risk: $[Amount]
Renewal Date: [Date] ([Days] until renewal)
Health Score: [Score] (Trend: [Up/Down/Flat])
Days in Save Play: [X] days

Current Status:
[2-3 sentences on current situation]

Actions Taken:
- [Action 1 — Result]
- [Action 2 — Result]

Request:
[Specific ask — e.g., executive meeting, commercial concession, engineering priority]

Decision Needed By: [Date]
```

### Step 5 — Plan Win-Back Campaigns

Design structured campaigns to recover churned customers:

| Win-Back Phase | Timing | Channel | Message Theme | Offer |
|---|---|---|---|---|
| **Immediate** | 0-30 days post-churn | Personal email from VP CS + phone call | "We heard you — here is what has changed" | Return discount (15-25%), dedicated onboarding |
| **Product update** | 60-90 days post-churn | Personalized email with product updates | "We built what you asked for" | Free trial of new features, migration assistance |
| **Peer proof** | 120-180 days post-churn | Case study email + event invitation | "See what [similar company] achieved" | Industry event invitation, peer reference call |
| **Anniversary** | 12 months post-churn | Personal outreach from new CSM | "A lot has changed in a year" | Fresh evaluation offer, competitive displacement pricing |
| **Trigger-based** | Anytime | Automated | "Noticed you might need us" (e.g., competitor negative press, funding round, hiring surge) | Personalized re-engagement offer based on trigger |

#### Win-Back Eligibility Criteria

| Factor | Include | Exclude |
|---|---|---|
| Churn reason | Product gaps (now fixed), price, support issues (now resolved), champion departure | Fraud, abuse, fundamental misfit, acquired by competitor |
| Account history | Was healthy at some point, had product adoption, positive NPS at some point | Never achieved adoption, always a bad fit |
| Revenue potential | ARR > $10K or strategic value | Too small to justify win-back cost |
| Relationship status | Contacts still reachable, no burned bridges | Hostile relationship, legal dispute |

### Step 6 — Measure and Optimize

Track the effectiveness of churn prevention efforts:

| Metric | Definition | Target | Measurement |
|---|---|---|---|
| **Save rate** | % of at-risk accounts retained after save play | > 60% | Monthly |
| **Time to intervention** | Days from first warning signal to first action | < 5 business days | Weekly |
| **Intervention coverage** | % of at-risk accounts that receive a save play | > 90% | Monthly |
| **Win-back rate** | % of churned accounts that return within 12 months | > 10% | Quarterly |
| **Net revenue retention** | Revenue retained + expansion - contraction - churn / starting revenue | > 110% | Quarterly |
| **Signal-to-action ratio** | % of warning signals that trigger an intervention | > 80% | Monthly |
| **Escalation resolution** | % of escalations resolved within SLA | > 85% | Monthly |
| **False positive rate** | % of flagged accounts that were not actually at risk | < 30% | Quarterly |

## Output Format

```markdown
# Churn Prevention Playbook: [Segment / Account]

**Author:** [Name] | **Date:** [Date]
**Segment:** [Enterprise / Mid-Market / SMB / All]
**Accounts in Scope:** [Count]
**Total ARR in Scope:** $[Amount]

---

## Early Warning Signals

| Signal | Weight | Data Source | Detection Method | Alert Threshold |
|---|---|---|---|---|
| [Signal] | [%] | [Source] | [Method] | [Threshold] |

## Intervention Triggers

| Trigger | Condition | Action | Owner | SLA |
|---|---|---|---|---|
| [Trigger] | [Condition] | [Action] | [Owner] | [SLA] |

## Save Play Library

| Play | Use When | Actions | Duration | Success Criteria |
|---|---|---|---|---|
| [Play] | [Trigger] | [Key actions] | [Time] | [Criteria] |

## Escalation Matrix

| Level | Trigger | Participants | Authority |
|---|---|---|---|
| [Level] | [Trigger] | [Who] | [Decisions they can make] |

## Win-Back Campaigns

| Phase | Timing | Channel | Offer |
|---|---|---|---|
| [Phase] | [When] | [Channel] | [Offer] |

## Program Metrics

| Metric | Current | Target | Gap |
|---|---|---|---|
| [Metric] | [Value] | [Target] | [Delta] |
```

## Quality Checklist

- [ ] Early warning signals cover usage, engagement, support, stakeholder, competitive, and financial dimensions
- [ ] Each signal has a specific detection method and data source, not just a description
- [ ] Intervention triggers are specific and measurable (not "when things look bad")
- [ ] Save plays include step-by-step actions with owners, timelines, and success criteria
- [ ] Escalation procedures have clear levels tied to risk severity and ARR thresholds
- [ ] Win-back campaigns are timed, personalized, and exclude accounts that should not be won back
- [ ] Metrics cover both leading indicators (signal detection, time to intervention) and lagging indicators (save rate, NRR)
- [ ] Playbook is segmented by customer tier if the customer base is heterogeneous
- [ ] Commercial concession authority is defined at each escalation level
- [ ] Save play templates are actionable enough that a new CSM could execute them without additional guidance

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Customer gives no warning signals and suddenly churns | Conduct a thorough post-mortem. Review for signals that were present but not tracked. Add new signals to the detection framework. Consider exit interviews for all churned accounts. |
| Customer is at risk but is also a reference or case study | Elevate priority beyond what the ARR alone would justify. Losing a reference customer has reputational cost. Involve marketing in the save effort. |
| Multiple accounts at the same company are at risk simultaneously | Treat as a single enterprise-level risk. Coordinate across CSMs to present a unified response. Escalate to executive level regardless of individual account size. |
| Customer is at risk due to a product limitation on the roadmap but not yet built | Be transparent about the timeline. Offer workarounds, early access to beta, or co-development opportunities. Do not make promises without product commitment. |
| Customer churns to a competitor offering a free tier | Win-back messaging should focus on total cost of ownership, support quality, and enterprise features. Free-tier competitors often lack capabilities that matter at scale. |
| Save play succeeds but customer demands ongoing concessions | Set clear boundaries during the save play. Document what was offered and for how long. Transition to a standard success plan with milestone-based value delivery. |
| Customer contact is hostile or unresponsive | Attempt alternative contacts within the organization. If truly unresponsive after 3 attempts across channels, document the effort and prepare for likely churn. Do not harass. |
