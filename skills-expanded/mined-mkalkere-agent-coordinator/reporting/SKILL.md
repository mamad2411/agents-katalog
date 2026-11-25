---
name: reporting
version: 1.0.0
description: Produce structured status reports, summaries, and briefings from raw activity data
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - report:generate
  requires_approval: false
---

# Reporting

Produce structured status reports, summaries, and briefings from raw activity data — what's done, in progress, blocked, and upcoming.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `generate_report` is invoked, you (the agent) follow the methodology below using your writing and reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `communication/reporting` in its skill list.

## When to Use

- Summarizing work completed during a period (daily, weekly, sprint)
- Briefing stakeholders on project status
- Communicating blockers and risks to decision-makers
- Creating retrospectives or post-mortems
- Providing context for handoffs between team members or shifts
- Any time raw activity needs to be distilled into actionable communication

## Report Types

### Status Update
Regular progress report for ongoing work. Answers: "Where do we stand?"

### Executive Summary
High-level overview for leadership. Answers: "What do I need to know?"

### Technical Briefing
Detailed technical context for practitioners. Answers: "How does this work?"

### Retrospective
Reflective analysis of completed work. Answers: "What did we learn?"

### Handoff Brief
Context transfer between agents or team members. Answers: "What do I need to continue?"

## Methodology

### 1. Gather Raw Data

Collect activity data from all available sources:
- Task lists, issue trackers, project boards
- Git history (commits, PRs, merges)
- Communication logs (messages, discussions, decisions)
- Metrics and measurements
- Blockers and incidents

### 2. Categorize

Sort all items into status categories:
- **Completed**: Done and verified since last report
- **In Progress**: Actively being worked on
- **Blocked**: Cannot proceed — identify the blocker and owner
- **Upcoming**: Planned for next period
- **Risks**: Issues that may affect future work

### 3. Calibrate Detail Level

Match detail to audience and report type:

| Detail Level | Content | Length | Audience |
|-------------|---------|--------|----------|
| **One-liner** | Single sentence status | 1 sentence | Busy executives, chat updates |
| **Brief** | Key highlights only | 3-5 bullets | Managers, daily standups |
| **Standard** | Full categorized status | 1 page | Team leads, weekly reviews |
| **Comprehensive** | Detailed with context | 2-3 pages | Stakeholders, retrospectives |

### 4. Structure by Report Type

#### Status Update Template
```
## Status Update: [Period]

### Summary
[1-2 sentence overview of overall status: on track / at risk / blocked]

### Completed
- [Item]: [Brief outcome or result]

### In Progress
- [Item]: [Current state, expected completion]

### Blocked
- [Item]: Blocked by [cause]. Owner: [who]. Impact: [what's affected]

### Upcoming
- [Item]: [Expected start, priority]

### Risks
- [Risk]: Likelihood [L/M/H], Impact [L/M/H]. Mitigation: [action]
```

#### Executive Summary Template
```
## Executive Summary: [Topic]

### Bottom Line
[The single most important thing to know — lead with the conclusion]

### Key Metrics
- [Metric 1]: [Value] ([trend: up/down/flat])
- [Metric 2]: [Value] ([trend])

### Highlights
- [Most important achievement]
- [Second most important achievement]

### Attention Needed
- [Decision required or risk to escalate]

### Next Steps
- [What happens next and who owns it]
```

#### Technical Briefing Template
```
## Technical Briefing: [Topic]

### Context
[Background needed to understand the technical details]

### Current State
[Technical description of where things stand]

### Architecture / Design
[Relevant technical details, diagrams, or code references]

### Trade-offs
- [Decision]: Chose [A] over [B] because [reason]

### Open Issues
- [Technical issue]: [Impact and proposed resolution]
```

#### Retrospective Template
```
## Retrospective: [Period/Project]

### Outcomes
- [What was delivered vs. what was planned]

### What Went Well
- [Positive pattern]: [Why it worked]

### What Could Improve
- [Issue]: [Root cause] → [Suggested improvement]

### Action Items
- [ ] [Specific action] — Owner: [who], Due: [when]

### Metrics
- [Metric comparison: planned vs. actual]
```

#### Handoff Brief Template
```
## Handoff: [Context]

### Current State
[Where things stand right now]

### What's Done
- [Completed item with relevant details for continuity]

### What's In Progress
- [Active item]: [Current state, what's next, any gotchas]

### What's Blocked
- [Blocked item]: [Cause, who to contact, workarounds tried]

### Key Context
- [Important decision or constraint the next person needs to know]
- [File/resource locations]

### Immediate Next Steps
1. [First thing to do when picking this up]
```

### 5. Apply Quality Filters

Before finalizing any report:
- **Accuracy**: Are all facts verifiable? Remove unverified claims.
- **Completeness**: Is anything missing that the audience needs?
- **Actionability**: Can the reader act on this? Are blockers clear? Are owners identified?
- **Brevity**: Can anything be removed without losing information?
- **Tone**: Does it match the audience's expectations?

## Output Format

Use the template matching the selected report type. Always include:
1. A clear title with the report type and time period
2. A summary or bottom line at the top
3. Categorized content (completed, in progress, blocked, etc.)
4. Actionable next steps or items needing attention

## Quality Criteria

- Report type matches the communication need
- Detail level matches the audience
- All items are categorized correctly (done/in-progress/blocked)
- Blockers identify the cause AND the owner
- Next steps are specific and assigned
- No stale information from previous reports
- Summary accurately reflects the detailed content

## Common Mistakes

- **Burying bad news**: Lead with blockers and risks — they need attention first
- **Activity vs. outcomes**: Report what was accomplished, not just what was done
- **Stale data**: Every item should reflect current state, not when it was first recorded
- **Missing owners**: Every blocker and action item needs a responsible party
- **Wrong detail level**: An executive summary with code snippets, or a technical brief without code
- **Mixing report types**: A status update is not a retrospective. Choose one type and commit.
- **No summary**: Every report needs a top-level summary. Readers may not read past it.

## Completion

Reporting is complete when:
- The report type matches the communication need
- Detail level matches the audience
- All relevant activity is categorized and included
- Blockers have causes and owners
- Next steps are specific and actionable
- A clear summary appears at the top
- The report could be sent to its audience without additional context
