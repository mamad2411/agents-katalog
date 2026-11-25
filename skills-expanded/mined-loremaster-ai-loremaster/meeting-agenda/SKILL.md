---
name: meeting-agenda
description: >
  Invoked only by explicit /meeting-agenda right before the team's recurring meetings
  (e.g., Mon/Thu) to scan the **entire lore vault** and draft the agenda in the PM role —
  an extra meeting separate from daily/retro; **only items needing discussion or decision
  become agenda items** (not plain progress reports); this channel = this project only.
# Port note: the original states the team's fixed meeting days as fact; deliberately
# genericized here to an example cadence ("e.g., Mon/Thu") — substitute your team's
# actual recurring meeting days.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [scrum, agenda, PM, meeting]
    related_skills: [sprint-retro, conflict-detection]
---

# Regular Meeting Agenda Generation (PM)

Distill "what the team must **judge and decide together**" into agenda items. This is not plain progress reporting (that is the daily's job).

## Behavior
1. **Extract agenda candidates from the entire lore vault (structured via graphify):** the meeting covers the whole project, so look broadly — but **do not read everything wholesale; narrow down the "discussion material" with graphify first:**
   - Treat the **god-nodes** in `graphify-out/GRAPH_REPORT.md` (highly connected core concepts = large ripple effect if changed, likely contentious) and the **surprising connections** (unexpected cross-links = issues the team may miss) as first-priority agenda candidates.
   - Open conflicts in `conflicts/` (the meeting = the venue for verdicts), unresolved backlog items, incomplete actions from the previous meeting.
   - Confirm each candidate concept's connections and evidence with `graphify explain "<concept>"` and read only those sources. If graph.json is missing, fall back to `wiki/index.md` + a direct scan of `wiki/`.
2. **Ask the PM-role team member and wait for the response:**
   - **Show the vault-extracted candidates first**, then ask (reduces duplicate input):
     "Anything to include in today's agenda? (beyond the automatic vault extraction — e.g., mentor meetings, external schedules, discussion topics not yet in the vault)"
   - **Do not finalize the agenda without a response.**
3. **Merge:** vault agenda items + team-member additions.

## Agenda Generation Rules
1. Only what needs **"discussion/decision"**, not "reporting". Exclude areas that are going smoothly.
2. Each item carries **why it must be discussed now (evidence) + source links**.
3. **Open conflicts must be included** (the meeting = the venue for verdicts).
4. Put the previous meeting's **incomplete actions at the very top**.
5. **Priority order** (so the bottom can be cut if time runs short).
6. **Do not pre-draw conclusions.** Phrase items as discussion questions.

## Agenda Source Labels
- `[vault]` auto-extracted item with evidence links.
- `[PM added]` direct team-member input (mentor meetings, etc.). Sources are not enforced.

## Output & Scope
- Post the agenda draft to Slack (items + evidence + sources). Post-meeting decisions are **recorded by a human as meeting notes in `raw/` → the normal pipeline.**
- **No automatic meeting minutes. The scope ends at agenda "generation".**

## Fallback (operational adjustment)
- If team members have not responded by a set time (e.g., 30 minutes before the meeting), **post the draft with vault items only** + note "raise any additional items at the meeting".

## Isolation
- This channel = this project only. No mentioning or referencing other projects.
