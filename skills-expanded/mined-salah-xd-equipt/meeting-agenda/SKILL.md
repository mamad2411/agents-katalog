---
name: meeting-agenda
description: "Builds structured meeting agendas with time allocations, discussion topics, decision items, and action item templates for productive meetings."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Meeting Agenda

## When to Use This Skill

Use this skill when you need to:
- Create a structured agenda for a team, client, or stakeholder meeting
- Design recurring meeting templates (weekly standups, quarterly reviews, board meetings)
- Build an agenda that ensures decisions get made and action items get assigned
- Prepare a meeting that respects everyone's time with clear time allocations

**DO NOT** use this skill for meeting notes, post-meeting summaries, or facilitation scripts. This is for pre-meeting agenda creation only.

---

## Core Principle

EVERY MEETING EXISTS TO MAKE DECISIONS OR ALIGN ON INFORMATION — IF THE AGENDA DOES NOT SPECIFY WHICH DECISIONS NEED TO BE MADE, THE MEETING WILL END WITHOUT MAKING THEM.

---

## Phase 1: Meeting Brief

Gather meeting context before building the agenda.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Meeting type** | "What kind of meeting? (team sync, client call, strategy session, 1:1, board meeting, brainstorm)" | Team sync |
| **Duration** | "How long is the meeting?" | 30 minutes |
| **Attendees** | "Who is attending and what are their roles?" | 2-5 team members |
| **Objective** | "What MUST be decided or accomplished by the end of this meeting?" | No default — must be provided |
| **Pre-read materials** | "Any documents, reports, or context attendees should review beforehand?" | None |
| **Recurring?** | "Is this a one-time meeting or recurring?" | One-time |

**GATE: Confirm the meeting brief before building the agenda.**

---

## Phase 2: Build Agenda

Structure the agenda with time-boxed sections.

### Agenda Architecture

Every agenda follows this structure, adjusted for meeting type and duration:

1. **Opening (5% of meeting time)** — state the objective, confirm agenda
2. **Information sharing (20-30%)** — updates, context, data review
3. **Discussion (30-40%)** — debate, input gathering, problem solving
4. **Decisions (15-20%)** — explicit decision points with owners
5. **Action items + close (10%)** — assign tasks, confirm next steps, set deadlines

### Agenda Template

```
## Meeting Agenda: [Meeting Title]

**Date:** [Date]
**Time:** [Start] - [End] ([Duration])
**Attendees:** [Names and roles]
**Objective:** [One sentence — what success looks like when this meeting ends]

**Pre-read:** [Links or documents to review before the meeting]

---

| Time | Topic | Type | Owner | Notes |
|------|-------|------|-------|-------|
| 0:00 | Welcome + agenda review | Align | [Facilitator] | State objective |
| 0:02 | [Topic 1] | Info | [Name] | [Key question or context] |
| 0:10 | [Topic 2] | Discuss | [Name] | [Decision needed: Y/N] |
| 0:20 | [Topic 3] | Decide | [Name] | [Options to evaluate] |
| 0:25 | Action items + next steps | Close | [Facilitator] | Assign owners + deadlines |

---

**Decision items for this meeting:**
1. [ ] [Decision 1 — options: A, B, C]
2. [ ] [Decision 2 — options: A, B]

**Parking lot:** (topics raised but not on today's agenda)
-
```

### Time Allocation Rules

- No single topic should exceed 40% of the meeting duration
- Decision items need at least 5 minutes each — do not rush decisions into 2 minutes
- If more than 3 decisions need to be made, the meeting is too short or needs to be split
- Buffer 2-3 minutes for transitions between topics

**GATE: Present the agenda and get approval before finalizing.**

---

## Phase 3: Enhance

Add facilitation elements that keep the meeting on track.

### Discussion Prompts

For each discussion topic, provide 1-2 specific questions the facilitator can ask to keep conversation focused:

```
**Topic: Q1 marketing budget allocation**
- "Given our Q4 results, which channel deserves more budget and why?"
- "What would we cut if we had to reduce the budget by 20%?"
```

### Pre-Meeting Checklist

```
## Pre-Meeting Checklist

- [ ] Agenda sent to all attendees at least 24 hours before the meeting
- [ ] Pre-read materials linked and accessible
- [ ] Decision items clearly stated so attendees can form opinions beforehand
- [ ] Meeting room / video link confirmed
- [ ] Note-taker assigned
```

### Action Item Template

```
## Action Items from [Meeting Title] — [Date]

| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | | | | [ ] |
| 2 | | | | [ ] |
```

---

## Phase 4: Recurring Template

If the meeting is recurring, deliver a reusable template.

### Template Customization

- Mark which sections are fixed (always present) vs. variable (change each meeting)
- Include placeholders for rotating topics
- Suggest a cadence for agenda distribution (e.g., "Send every Monday by 9 AM for Tuesday meetings")
- Provide a quarterly review prompt to evaluate if the recurring meeting still needs to exist

---

## Anti-Patterns

- **No stated objective** — "Team sync" is not an objective. "Decide on Q2 launch date" is an objective.
- **Topic without owner** — every agenda item needs one person responsible for driving that section.
- **All information, no decisions** — meetings that only share updates should be emails instead.
- **No time limits** — without time boxes, one topic will consume the entire meeting.
- **Too many topics** — more than 5 topics in a 30-minute meeting means nothing gets depth.
- **Agenda sent during the meeting** — if attendees see the agenda for the first time in the meeting, they cannot prepare.

---

## Recovery

- **User cannot define the objective:** Ask "If this meeting goes perfectly, what is different afterward?" The answer is the objective.
- **Too many topics for the time:** Force-rank topics by urgency. Move lowest-priority items to a follow-up meeting or async channel.
- **User wants a meeting but it should be an email:** If there are no decisions and no discussion needed, suggest an async update instead and draft that.
- **Recurring meeting feels stale:** Recommend a meeting audit — skip the meeting for 2 weeks and see if anyone notices. If not, cancel it.
- **Attendee list is too large:** Meetings with 8+ people rarely produce decisions. Recommend a core group of decision-makers with a summary sent to the broader group.
