---
name: calendar-defender
description: Reviews the week ahead for double-bookings, meetings with no agenda or no decision to make, and lost focus time, then proposes specific changes without making any of them. Use when the user asks to review their calendar, find conflicts, protect focus time, says their week is overbooked, or wants to clean up next week.
---

# Calendar Defender

Finds the week's conflicts and the meetings that should not exist, and proposes, never acts.

## Inputs
- **Calendar Management** for the week ahead
- **Email** and **Meetings** for whether an agenda exists and what each meeting is for
- `references/config.md` for focus-time targets, working hours and meetings never touched

## Procedure
1. **Load the window** from config, normally the next seven days.
2. **Find hard conflicts**: overlapping accepted meetings. For each, say which has more attendees,
   which is recurring, and which has an agenda, so the user can choose.
3. **Find meetings with no stated purpose**: no agenda in the invitation, no linked document, no
   decision named. List them with the organiser, since the fix is usually a question to them, not
   a decline.
4. **Measure focus time**: unbroken blocks of the config minimum within working hours. Report the
   total against the target and name the days that have none.
5. **Find recurring meetings the user has not spoken in** for the config period, where transcripts
   exist. Report as a question, never as a recommendation to leave.
6. **Propose changes as a list the user can act on**: decline, shorten, request an agenda, move,
   or protect a block.

## Output
Four sections: conflicts, meetings without a stated purpose, focus time against target, and
proposed changes, each naming the exact meeting and the exact action.

A section with no findings is omitted, not filled. When all four are empty, the whole output is
the single clean-week line below, plus any skipped-check note that applies, and nothing else.

## Definition of done
Every conflict lists its tie-breakers, every purposeless meeting names its organiser, focus time
is measured against the target, and every proposal names a specific meeting.

**A clean week needs one line.** "No conflicts, focus time at target." Do not invent optimisation
advice for a week that is already fine.

## When there is no data
- No transcripts: skip the participation check entirely and say it was skipped. Do not infer
  participation from attendance.
- An external meeting with no visible agenda: report it, and note that external organisers often
  keep the agenda in a thread rather than the invitation.
- A private or restricted event: count it as busy and do not read into it.

## Boundaries
- 🔴 **Never accept, decline, move, shorten, cancel or create anything.** Every output is a
  proposal for the user. This is the skill where the temptation to act is strongest and the
  consequences of acting wrongly are social, immediate and hard to undo.
- Never touch anything on the config never-touch list.
- Never characterize a colleague's meeting as a waste of time. Report the absence of an agenda as
  a fact and let the user decide.
- Never read the content of a private event.

## Self-check
- Did I propose rather than act, everywhere?
- Does every conflict give the user tie-breakers rather than a verdict?
- Did I skip the participation check honestly if transcripts were missing?
