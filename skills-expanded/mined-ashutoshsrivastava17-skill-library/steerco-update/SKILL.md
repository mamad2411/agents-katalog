---
name: steerco-update
description: >
  Prepare steering committee updates with executive summary, key decisions
  needed, risks, and progress highlights. Format for senior leadership
  consumption with clear asks.
  TRIGGER when: user says "steering committee", "steerco", "executive program
  update", "leadership update", or invokes /steerco-update.
argument-hint: "[program name]"
user-invocable: true
---

# Steering Committee Update Preparation

You are a senior program manager preparing a polished steering committee (steerco) update. Produce a concise, decision-oriented briefing that respects leadership time while providing the information needed to govern the program effectively.

## Process

### Step 1: Understand the Steerco Context

Ask the user if not already provided:
- **Program name** and objective
- **Steerco members**: sponsor, executives, functional leads
- **Meeting cadence**: weekly, biweekly, monthly, quarterly
- **Time allocation**: how many minutes is the program allotted
- **Standing agenda items**: what the steerco always expects to see
- **Decisions or approvals needed**: the primary purpose of this update
- **Sensitive topics**: anything requiring careful framing or offline discussion

### Step 2: Gather Program Inputs

Collect current state across these dimensions:

#### Progress and Accomplishments
- Key deliverables completed since last steerco
- Milestones achieved or on track
- Metrics and KPIs showing momentum
- Notable wins, customer feedback, or early results

#### Program Health
- Overall RAG status with justification
- Budget status (spend vs. plan)
- Resource utilization and capacity
- Scope changes since last review

#### Risks and Issues
- Top 3-5 risks with severity, mitigation status, and owner
- Open issues requiring steerco awareness or action
- Newly identified risks since last meeting
- Items escalated from the program team

#### Decisions and Asks
- Decisions the steerco must make (with options and recommendations)
- Approvals needed (budget, scope, timeline changes)
- Support requests (resources, priority calls, blocker removal)
- Information items (awareness only, no action needed)

### Step 3: Structure the Steerco Deck/Document

Use this executive-optimized format:

```
STEERING COMMITTEE UPDATE
[Program Name] — [Date]
Prepared by: [Program Manager]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY (30 seconds)
Overall Status: [RED / AMBER / GREEN]
[2-3 sentences capturing: where we are, what's changed, what we need]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISIONS REQUIRED (lead with the asks)

| # | Decision | Options | Recommendation | Deadline | Impact if Delayed |
|---|----------|---------|---------------|----------|-------------------|
| 1 |          |         |               |          |                   |
| 2 |          |         |               |          |                   |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROGRAM HEALTH DASHBOARD

| Dimension    | Status | Trend     | Comment                    |
|-------------|--------|-----------|----------------------------|
| Schedule     | R/A/G  | ↑ ↓ →    | [one-line explanation]      |
| Budget       | R/A/G  | ↑ ↓ →    | [spend vs. plan]            |
| Scope        | R/A/G  | ↑ ↓ →    | [changes or creep noted]    |
| Resources    | R/A/G  | ↑ ↓ →    | [capacity vs. demand]       |
| Quality      | R/A/G  | ↑ ↓ →    | [defects, rework, standards]|
| Stakeholders | R/A/G  | ↑ ↓ →    | [alignment and engagement]  |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROGRESS HIGHLIGHTS

| Accomplishment | Impact | Workstream |
|---------------|--------|-----------|
|               |        |           |

MILESTONE STATUS

| Milestone | Due Date | Status | Variance | Note |
|-----------|---------|--------|----------|------|
|           |         | R/A/G  |          |      |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP RISKS AND ISSUES

| ID | Type | Description | Severity | Owner | Mitigation / Resolution | Status |
|----|------|-----------|----------|-------|------------------------|--------|
|    | Risk/Issue |     |          |       |                        |        |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOOK AHEAD (next period)

Key Activities:
1. [Activity with expected outcome]
2. [Activity with expected outcome]
3. [Activity with expected outcome]

Upcoming Milestones:
- [Milestone] — [Date] — [Readiness assessment]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APPENDIX (reference only — not presented)
- Detailed RAID log
- Budget breakdown
- Resource allocation
- Dependency tracker
```

### Step 4: Calibrate for the Audience

Tailor the update based on steerco composition:

| Audience Type | Emphasis | Tone | Detail Level |
|--------------|----------|------|-------------|
| C-Suite / Sponsor | Strategic impact, decisions, blockers | Direct, concise | Headlines only; appendix for detail |
| VP / Director Level | Progress vs. plan, resource trade-offs | Professional, data-driven | Moderate detail with supporting metrics |
| Cross-Functional Leads | Dependencies, coordination needs, timeline | Collaborative, transparent | Enough detail to identify their team's actions |
| PMO / Governance | Compliance with standards, earned value, forecasts | Structured, formal | High detail; adherence to PMO templates |

### Step 5: Prepare for Discussion

Anticipate questions and prepare responses:

| Likely Question | Prepared Response | Supporting Data |
|----------------|-------------------|----------------|
| "Why is [X] behind schedule?" | | |
| "What resources do you need?" | | |
| "Can we accelerate [milestone]?" | | |
| "What's the impact on [related program]?" | | |

### Step 6: Define Follow-Up Actions

```
ACTION ITEMS FROM STEERCO

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 |        |       |          | New    |
| 2 |        |       |          | New    |

DECISIONS MADE
- [Decision 1]: [Outcome] — Approved by: [Name] — Date: [Date]
- [Decision 2]: [Outcome] — Deferred to: [Next meeting date]
```

## Output Format

1. **Steerco Update Document** (Step 3) ready to present or distribute
2. **Talking Points** for the presenter — key messages per slide/section (2-3 bullets each)
3. **Anticipated Q&A** (Step 5) with prepared responses
4. **Action Item Template** (Step 6) for capturing meeting outcomes
5. **Pre-read Summary** (optional): a 1-paragraph email to send ahead of the meeting

## Quality Standards

- Total update should be presentable in the allotted time (default: 15 minutes)
- Decisions section always comes before status — lead with what you need, not what you did
- Every risk/issue mentioned must include a mitigation or resolution, never just the problem
- RAG ratings are consistent with program-wide definitions and defensible with data
- Avoid jargon that steerco members outside the program would not understand
- Budget numbers are reconciled with finance; do not present unvalidated figures
- Trend arrows reflect at least 2 data points, not a single-period snapshot
- "No change" is a valid status — do not manufacture movement for appearance

## Edge Cases

- **First steerco for a new program**: include a "Program Overview" section with objectives, scope, timeline, team, and governance structure before diving into status
- **All-red program**: lead with the recovery plan, not the problems; show agency and a path forward; pre-brief the sponsor before the meeting
- **No decisions needed**: still present — use the time for awareness and alignment; explicitly state "no decisions required this period"
- **Steerco member is disengaged**: provide a pre-read summary and flag specific items that need their input; consider a 1:1 before the meeting
- **Conflicting information from workstreams**: reconcile before the meeting; do not present conflicting data — escalate to the program lead if alignment cannot be reached
- **Last-minute changes**: have a "changes since pre-read" callout at the top if material updates occurred after the pre-read was distributed

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
