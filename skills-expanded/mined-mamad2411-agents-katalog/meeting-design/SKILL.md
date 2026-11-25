---
name: meeting-design
description: "When to activate: meeting design, meeting agenda, facilitation, decision meetings, async alternatives, meeting culture, no-meeting days, follow-up protocols, meeting effectiveness"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: productivity
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Meeting Design Patterns

## Meeting Decision Framework

### Should This Be a Meeting?
```
Ask before scheduling:
1. Is a real-time decision required?
2. Is the topic complex enough that async would take longer?
3. Are there >2 people whose input is needed simultaneously?
4. Does this require emotional/sensitive discussion?

If NO to all → don't schedule, use async instead
```

### Meeting Type Matrix
| Type | When | Format |
|------|------|--------|
| Decision | Need alignment + buy-in | 30-60 min, small group |
| Status update | Regular progress tracking | Replace with async doc |
| Problem-solving | Complex issue, need diverse input | 60-90 min, structured |
| Brainstorming | Generating options | 60 min, diverge then converge |
| 1:1 | Manager-report, peer coaching | 30-60 min, standing |
| Kickoff | Start new project | 60 min, full team |
| Retrospective | Learn from past work | 60-90 min, team |
| Planning | Roadmap, OKRs | Half day, leadership |

## Agenda Design

### Agenda Template
```
Meeting: [Name]
Date/Time: [When]
Duration: [How long]
Owner: [Who called it]
Pre-read: [Link to pre-read doc — required if >15 min meeting]

OBJECTIVE: By end of meeting we will have [decision made / problem solved / plan aligned]

Agenda:
00-05 | Context: Why we're here, what we need to decide
05-20 | [Agenda item 1] — Owner: [Name] — Outcome: [Decision or alignment]
20-40 | [Agenda item 2] — Owner: [Name] — Outcome: ___
40-50 | Open Q&A / concerns
50-60 | Next steps: who does what by when

Required: [Names — their decision-making role]
Optional: [Names — FYI, may leave early]
```

### Timing Rules
- **30 min max** for single-topic decisions
- **60 min max** for complex discussions
- **No more than 90 min** without a break
- Default to 25 or 50 min (not 30 or 60) — buffer between meetings

## Facilitation Techniques

### Opening Protocol
```
State at start:
1. "Our goal today is [specific outcome]"
2. "We have [X] minutes"
3. "At the end we need to leave with [decision / action items]"
4. "I'll timekeep. Raise your hand if you think we're going off track."
```

### Discussion Management
```
Converge technique:
"We've heard several options. Let me summarize: [A], [B], [C].
 Let's spend 10 minutes deciding between them."

Quieter voices:
"[Name], you've been quiet — any thoughts on this?"

Dominant voices:
"Great point. Let's hear from someone who hasn't spoken yet."

Going off-topic:
"That's important — let me park it. [Write on parking lot]
 Can we return to [original topic]?"

Time pressure:
"We have 5 minutes left. Do we have enough to decide or
 do we need a follow-up?"
```

### Decision Modes
| Mode | Description | When |
|------|-------------|------|
| **Autocratic** | Leader decides alone | Time-critical, low stakes |
| **Consultative** | Leader decides after input | Most technical decisions |
| **Consensus** | Everyone must agree | Major cultural/values decisions |
| **Consent** | No one has a blocking objection | Policy, process decisions |
| **Delegate** | Explicitly assign to one person | Operational decisions |

Always state which mode before discussion begins. "I'll decide, but I want your input first" removes ambiguity.

## Meeting Formats

### Pre-Mortem Meeting
```
Purpose: Identify risks before project starts

Structure (60 min):
5 min: Describe the project goal
15 min: "Imagine it's 12 months from now and the project failed.
         Write down what went wrong." (solo writing)
20 min: Share and cluster failure causes
15 min: Prioritize top 5 risks
5 min: Assign mitigation owners
```

### Retrospective Meeting (4Ls)
```
Liked: What went well?
Lacked: What was missing?
Learned: What do we know now that we didn't?
Longed For: What did we wish existed?

Tool: FigJam or Miro board with 4 columns
Time: 10 min write, 15 min cluster, 20 min discuss, 15 min actions
```

### Decision Meeting Structure
```
0-5: Distribute decision brief (if not pre-read)
5-15: Owner presents recommendation + reasoning
15-30: Q&A — clarifying questions only (not debate)
30-45: Alternatives discussion — other paths considered?
45-55: Decision + rationale stated by decision-maker
55-60: Next steps documented
```

## Async Alternatives

### Replace Status Update Meetings With
```
Loom video update (5 min):
- Record: screen + face
- Structure: What I did, what's next, any blockers
- Post in Slack/Notion channel with written summary

Weekly async standup in Slack:
Yesterday: [List]
Today: [List]
Blockers: [List]
Share by 9am Monday in #team-updates
```

### Replace Brainstorm Meetings With
```
Async ideation document:
1. Share brief with problem statement + constraints
2. Give 48 hours for individuals to add ideas async
3. Everyone comments on others' ideas
4. Synthesize top ideas in shorter sync session (30 min)

Benefits: introverts contribute equally, ideas incubate,
no groupthink from first-spoken idea
```

## Meeting Culture

### No-Meeting Days
```
Implementation:
- Pick 1-2 days/week (typically Tue + Thu, or Mon + Wed)
- Block calendar permanently
- Communicate to team: "Please don't schedule on these days"
- Leadership must model: decline requests on protected days

Research: Asana/Harvard study shows focus-time protection
increases team output 20%+ without loss of collaboration
```

### Meeting Hygiene Rules
```
Team agreements:
□ Cameras on for decisions, off for status OK
□ No phones/laptops during discussions unless taking notes
□ Start on time, end on time (or early)
□ Rotating facilitator for recurring team meetings
□ Action items captured in real-time by note-taker
□ Decline meetings without an agenda
□ No last-minute adds to calendar without consent
```

## Follow-Up Protocol

### Meeting Notes Template
```
Meeting: [Name]
Date: [Date]
Attendees: [Names]
Absent: [Names, reason]

DECISION MADE: [Exactly what was decided]
RATIONALE: [Why]

ACTION ITEMS:
| Action | Owner | Due Date |
|--------|-------|---------|
| [Task] | [Name] | [Date] |

PARKING LOT (not discussed, needs follow-up):
• [Item]

NEXT MEETING: [Date/time if applicable]

Notes distributed within: 24 hours
```

### Accountability System
```
Post meeting notes in shared location (Notion, Confluence, Slack thread)
within 24 hours — ideally within 1 hour

Tag action item owners with explicit due dates
Use project management tool (Linear, Asana, Jira) for persistent tracking
Not just in meeting notes (people don't re-read them)

Follow-up: If not completed by due date, visible in standup/weekly review
```
