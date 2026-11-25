---
name: stakeholder-mapping
description: "Maps stakeholders on a Power × Interest grid, defines engagement strategies per quadrant, tracks alignment over time, and produces a communication plan. Ensures PMs invest their limited influence capital where it matters most."
category: planning
default_depth: standard
---

# Stakeholder Mapping (Power × Interest)

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Maps stakeholders on a Power × Interest grid, defines engagement strategies per quadrant, tracks alignment over time, and produces a communication plan. Ensures PMs invest their limited influence capital where it matters most.

## When to Use

- Kicking off a new initiative that touches multiple teams or executives
- Navigating organizational complexity around a controversial decision
- New PM onboarding to understand the political landscape
- Before a major launch that requires cross-functional buy-in
- When stakeholder misalignment is blocking progress

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Small initiative, <5 stakeholders, low political complexity | Step 1: Identify Stakeholders, Step 2: Map Power x Interest |
| **Standard** | Cross-functional initiative with mixed support and resistance | All sections |
| **Deep** | High-stakes or politically charged initiative with exec-level resistors | All sections + influence network diagram, resistor-specific persuasion briefs, pre-mortem on stakeholder derailment scenarios |

**Omit rules:** At Light depth, skip Step 3: Analyze Alignment & Risk, Step 4: Build the Communication Plan, and Step 5: Track Over Time. Produce only the Stakeholder Register and Power x Interest Grid.

## Framework

### Step 1: Identify Stakeholders

```markdown
## Stakeholder Register: [Initiative Name]

| # | Name | Role / Title | Team | Relationship to Initiative |
|---|---|---|---|---|
| S1 | [Name] | [Title] | [Team] | [Decision-maker / Influencer / Contributor / Informed] |
| S2 | [Name] | [Title] | [Team] | [Role] |
| S3 | [Name] | [Title] | [Team] | [Role] |

### Stakeholder Types
- **Decision-maker:** Has authority to approve, block, or fund
- **Influencer:** Shapes the decision-maker's opinion
- **Contributor:** Provides expertise, resources, or execution
- **Informed:** Needs to know but doesn't decide
```

### Step 2: Map Power × Interest

```markdown
## Power × Interest Grid

Rate each stakeholder:
- **Power (1-5):** Ability to impact the initiative's success (budget, authority, resources, political influence)
- **Interest (1-5):** How much they care about this initiative's outcome

| Stakeholder | Power | Interest | Quadrant | Current Stance |
|---|---|---|---|---|
| [S1] | [1-5] | [1-5] | [Manage Closely / Keep Satisfied / Keep Informed / Monitor] | [Champion / Supportive / Neutral / Resistant / Hostile] |

### Quadrant Definitions

```
                LOW INTEREST           HIGH INTEREST
               ┌──────────────────┬──────────────────┐
               │  Keep Satisfied  │  Manage Closely  │
  HIGH POWER   │  (High Power,    │  (High Power,    │
               │   Low Interest)  │   High Interest) │
               ├──────────────────┼──────────────────┤
               │  Monitor         │  Keep Informed   │
  LOW POWER    │  (Low Power,     │  (Low Power,     │
               │   Low Interest)  │   High Interest) │
               └──────────────────┴──────────────────┘
```

### Engagement Strategy by Quadrant

| Quadrant | Strategy | Frequency | Channel |
|---|---|---|---|
| **Manage Closely** | Deep partnership. Regular 1:1s. Co-create the solution. Address concerns proactively. | Weekly | 1:1 meetings, Slack DM |
| **Keep Satisfied** | Keep them happy without overwhelming. Executive summaries. Escalate decisions to them. | Biweekly | Email summaries, steering committee |
| **Keep Informed** | Regular updates. Invite to demos. Give them a voice. | Monthly | Team updates, all-hands |
| **Monitor** | Light touch. Don't ignore, but don't over-invest. | Quarterly | Broad comms, newsletters |
```

### Step 3: Analyze Alignment & Risk

```markdown
## Alignment Analysis

### Champions (actively support)
| Stakeholder | Why They Support | How to Leverage |
|---|---|---|
| [Name] | [Their motivation] | [How they can help, e.g., "Can advocate in exec meeting"] |

### Resistors (actively oppose or passively block)
| Stakeholder | Why They Resist | Risk Level | Engagement Plan |
|---|---|---|---|
| [Name] | [Their concern] | [High/Med/Low] | [Specific plan to address their concern] |

### Swing Votes (could go either way)
| Stakeholder | What They Care About | What Would Win Them | What Would Lose Them |
|---|---|---|---|
| [Name] | [Their priorities] | [How to get their support] | [What would push them to resist] |

### Influence Network
Who influences whom?
- [Decision-maker A] is heavily influenced by [Influencer B]
- [Resistor C] reports to [Champion D], potential path to resolution
- [Swing Vote E] trusts [F's] technical judgment
```

### Step 4: Build the Communication Plan

```markdown
## Stakeholder Communication Plan

| Stakeholder | Quadrant | Key Message | Channel | Frequency | Owner | Next Touch |
|---|---|---|---|---|---|---|
| [S1] | Manage Closely | [Tailored message, what they care about] | 1:1 | Weekly | [PM] | [Date] |
| [S2] | Keep Satisfied | [Executive summary focus] | Email | Biweekly | [PM] | [Date] |

### Communication Principles
1. **Tailor the message**, Each stakeholder cares about different things; don't send the same update to everyone
2. **Bad news travels fast**, Tell "Manage Closely" stakeholders about risks BEFORE they hear from someone else
3. **Ask, don't just inform**, Engagement is more powerful than broadcasting
4. **Track commitments**, If you promised to follow up, follow up
```

### Step 5: Track Over Time

```markdown
## Alignment Tracking

| Stakeholder | Start | Month 1 | Month 2 | Month 3 | Trend | Notes |
|---|---|---|---|---|---|---|
| [S1] | Neutral | Supportive | Supportive | Champion | ↑ | Won over after demo |
| [S2] | Resistant | Resistant | Neutral | Neutral | → | Concern partially addressed |
| [S3] | Champion | Champion | Champion | Champion | → | Consistent ally |

### Escalation Triggers
If any "Manage Closely" stakeholder moves to "Resistant":
- [ ] Schedule urgent 1:1 within 48 hours
- [ ] Understand the specific concern (don't assume)
- [ ] Develop a resolution plan
- [ ] Involve their champion/influencer if direct approach fails
```

## Minimum Evidence Bar

**Required inputs:** The initiative name, a list of stakeholders (or org chart to derive them from), and at least a rough read on each stakeholder's current stance toward the initiative.

**Acceptable evidence:** 1:1 conversations, meeting behavior, email/Slack tone, org chart reporting lines, prior project history with the stakeholder, direct quotes or stated positions.

**Insufficient evidence:** If a stakeholder's stance is based solely on title or assumption with no interaction data, produce a partial stakeholder map with unverified stakeholders marked `[TBD, requires: discovery 1:1 with <Name> to validate stance and interest level]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Stakeholder roles, reporting lines, and observed behavior (champion/resistant/neutral) must be grounded in evidence.
- **Hypotheses:** Influence network connections and swing vote predictions may be inferred, label these as "Estimated" until validated through engagement.

## Output Format

Produce a Stakeholder Map with:
1. **Register**, all stakeholders with roles
2. **Power × Interest Grid**, mapped and quadranted
3. **Alignment Analysis**, champions, resistors, swing votes, influence network
4. **Communication Plan**, tailored by stakeholder
5. **Tracking Sheet**, alignment over time with escalation triggers

**Shipwright Signature (required closing):**
6. **Decision Frame**, Top engagement priority (which stakeholder relationship to invest in first), trade-off between breadth and depth of engagement, confidence based on evidence quality of stance assessments, map owner, date, revisit trigger
7. **Unknowns & Evidence Gaps**, Stakeholders whose stance is assumed not observed, influence relationships not yet validated, hidden decision-makers not yet identified
8. **Pass/Fail Readiness**, PASS if every "Manage Closely" stakeholder has a documented stance based on direct interaction; FAIL if any high-power stakeholder's stance is unverified assumption. (At Light depth, the tailored engagement plan requirement is waived since the Communication Plan is omitted.)
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Mapping only the obvious stakeholders**, Include indirect influencers, executive assistants, and "shadow" decision-makers
- **Static map**, Stakeholder positions change; update monthly
- **Same message to everyone**, The VP of Engineering cares about different things than the VP of Sales
- **Ignoring resistors**, Unaddressed resistance becomes sabotage; engage early
- **Over-investing in "Monitor" quadrant**, Don't spend weekly 1:1 time on people who have low power and low interest

## Weak vs. Strong Output

**Weak:**
> **VP Engineering, Resistant.** Engagement plan: Set up a meeting to discuss concerns.

No stated reason for resistance, no tailored approach, "set up a meeting" is not a plan.

**Strong:**
> **VP Engineering, Resistant (Power: 5, Interest: 4, Manage Closely).** Resists because migration threatens Q2 uptime SLA. Engagement plan: Share load-test results from staging (available April 3) in a 1:1 before the steering committee vote; frame as risk reduction, not feature delivery. Fallback: escalate to CTO with joint risk brief if stance doesn't shift.

Names the specific concern, ties the engagement to concrete evidence, provides a fallback path.
