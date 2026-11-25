---
name: meeting-minutes
description: Turns a meeting transcript, recording summary, or rough notes into formal project minutes (attendees, apologies, numbered items, decisions) and an action log with owner and due date, carrying open actions forward from previous minutes. Use when the architect wants "minutes", "write up the meeting", "action log", "what did we agree", or to tidy notes from a client, design-team, planning, or site progress meeting. Separates decisions from discussion and flags anything unclear instead of guessing who said or agreed what. Hands correspondence to project-email and construction queries to rfi.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Meeting Minutes

Minutes are a record, not a summary. On a project they become evidence: of what was instructed, what was agreed, who owns the next step, and when. Write them so that someone who was not in the room, reading them a year later in a dispute, gets the same picture as the people who were.

## When to use

- After any project meeting: client, design team, planning pre-app, contractor progress, site, workshop.
- When the architect has a transcript (Teams, Zoom, Otter, Fireflies), a voice-note dump, or scribbled notes and needs a clean record.
- To build or update a running action log across a series of meetings.

## Input

- The transcript or notes. Note the source; a transcript is evidence, a memory is not.
- Meeting metadata: project, meeting type, number in the series, date, time, location or platform.
- Attendee list with organisation and role, and apologies. If not given, extract names from the transcript and mark them "to confirm".
- Previous minutes or action log, if this is a recurring meeting.
- The practice's template or numbering convention, if it has one.

## Process

1. **Fix the frame.** Project, meeting type, number, date, attendees, apologies, distribution. Missing items go in "To confirm", not invented.
2. **Carry forward.** Start with matters arising: each open action from the previous log, with its status (closed / ongoing / overdue). Do not silently drop an action; close it explicitly or carry it.
3. **Group by agenda item, not chronology.** Transcripts wander. Pull everything about one topic into one numbered item (e.g. 3.1, 3.2) even if it was discussed at three points.
4. **Sort every point into one of four kinds:**
   - **Decision** — something agreed. Record who agreed it.
   - **Instruction** — a client or contract administrator telling someone to do something. Record who instructed whom. These matter contractually.
   - **Action** — a task with an owner and a date.
   - **Note** — information or discussion with no outcome. Keep it short.
5. **Attribute carefully.** Use initials or organisation as the practice convention prefers. If the transcript does not make clear who said something, or whether a proposal was agreed or just raised, write it as raised and flag it: "[unclear whether agreed — confirm with JS]". Never upgrade a suggestion into a decision.
6. **Make actions testable.** Every action has a verb, an owner (a person or organisation, not "all"), and a date or a trigger ("before Stage 3 sign-off"). If the meeting did not set a date, write "date tbc" and list it in To confirm.
7. **Flag the consequential.** Anything touching scope, fee, programme, cost, or contract gets a marker in the minutes and a line in "Flags for the architect", because it may need a formal instruction or letter rather than a minute.
8. **Close with next meeting** (date, time, place) and the distribution list.

## Domain knowledge

- **Minutes are often contractually relevant.** On many contracts, progress-meeting minutes issued without challenge become the accepted record. Note at the top: "Corrections to be notified within [7] days of issue, otherwise these minutes are taken as an accurate record" only if the practice uses that convention; do not invent the period.
- **Instructions in minutes are weak instructions.** If a client or contract administrator instruction appears only in minutes, flag that it may need confirming in writing under the contract (hand to `contract-admin-letter`).
- **Neutral voice.** "The client confirmed the reduction to 12 units," not "the client finally agreed." No characterisation of tone, no blame.
- **Transcript hygiene.** Speech-to-text mangles product names, room names, and numbers. Repeat numbers as heard and flag any that look wrong ("transcript reads 'fifteen hundred'; confirm 1,500 mm or 15,000 mm").
- **Personal data.** Leave out off-topic personal remarks, health comments, and side conversations.

## Output format

```
# [Project] — [Meeting type] No. [N]
Date: [ ]   Time: [ ]   Location: [ ]
Present: [Name (Org, role)], ...
Apologies: [ ]
Distribution: [ ]

## 1. Matters arising from previous minutes
| Ref | Action | Owner | Status |

## 2. [Agenda item]
2.1 [Note / Decision / Instruction — text]  [D] [I] markers where applicable
2.2 ...

## Action log
| Ref | Action | Owner | Due | Status |
| 2.3 | Issue revised GA plans to QS | AB (Arch) | 14 Mar | Open |

## Next meeting
[date, time, place]

## To confirm (before issue)
- [unclear attribution, missing date, misheard number]

## Flags for the architect
- [scope / fee / programme / contract points that may need a formal letter or instruction]
```

Keep the action log as a clean table so it can be pasted into a tracker or carried into the next meeting.

## What you don't do

- Don't invent attendees, dates, figures, or agreements. If it is not in the input, it is "To confirm".
- Don't turn "we could look at" into an action, or "the client liked it" into a decision.
- Don't editorialise or record tone, blame, or opinion about people.
- Don't treat minutes as a substitute for a formal instruction, notice, or change order — flag it and hand to `contract-admin-letter`.
- Don't interpret what a decision means contractually. Record it; flag it.
