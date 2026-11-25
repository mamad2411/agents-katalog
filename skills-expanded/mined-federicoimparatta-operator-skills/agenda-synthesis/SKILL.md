---
name: agenda-synthesis
description: Use this skill when the user asks to synthesize a daily or weekly agenda across multiple calendars, orgs, or commitments, or to turn a dumped list of events into a prioritized plan. Trigger phrases include "plan my day", "what does my week look like", "synthesize my agenda", "review my calendar", "armar la agenda", "qué tengo esta semana", "prep for tomorrow". Produces an agenda that flags conflicts, prep needs, and declinable items, not a reformatted calendar export.
---

# agenda-synthesis

> **Anchor:** An agenda is a plan, not a list of meetings.

## When to use

Use this skill when the user needs to convert scattered commitments into a working plan. Works for:

- A daily plan the night before or the morning of.
- A weekly plan on Sunday night or Monday morning.
- A handover document when someone else will run the calendar for a day.
- A rebuild of the agenda after an unexpected day blows up the original plan.

Do not use when:

- The user is preparing for a single meeting. Use `meeting-prep`.
- The user is triaging inbound tickets. Use `ticket-triage`.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: focus block, prep, buffer, back-to-back, standup, one-on-one, deep work, context switch.
- **EN.** Direct US business register. Short sentences. No "productivity porn" vocabulary.
- Meeting titles stay in the language they are on the calendar.

## Method

### Step 1. Pull every source

A synthesis is only as good as its inputs. Collect, in one place:

- All calendars the user is on, including shared calendars they watch.
- Deadlines or commitments that do not live on a calendar.
- Standing cadences implicit in the role (weekly one-on-one, monthly board, quarterly close).
- Prep that was committed elsewhere (Slack promise, email thread, PR review request).

Missing one source silently is the most common failure mode.

### Step 2. Classify each item

Every item gets one of:

- **Meeting.** Requires the user live.
- **Focus block.** Deliberately reserved solo work.
- **Deadline.** Due at a specific time, not tied to a meeting.
- **Prep.** Work that must happen before a later item.
- **Blocker.** Unavailable time (travel, personal, off).

An item that does not fit one of these is either useless and should be declined or miscategorized and should be rewritten.

### Step 3. Find the conflicts

Three kinds to surface explicitly:

- **Double-booked.** Two meetings overlap.
- **Back-to-back with no buffer.** Two meetings are adjacent and the first one will run over.
- **Missing prep time.** A meeting requires prep and there is no block for it earlier in the day.

Do not leave these for the user to notice. Name them in the agenda with a proposed fix per conflict.

### Step 4. Surface what is not on the calendar but should be

The things that usually get missed:

- Transit and commute time.
- Lunch and natural breaks.
- Buffer before a high-stakes meeting.
- The actual focus block for whatever the week's deliverable is.
- Post-meeting follow-up windows.

Add them or flag them, depending on authority.

### Step 5. Rank by what must happen

A working agenda separates three groups:

- **Must happen.** Non-movable, non-declinable.
- **Should happen unless.** Movable if something bigger lands.
- **Candidate to decline.** The user should consider skipping or rescheduling.

Most lists are treated as entirely "must happen". Most lists are wrong.

### Step 6. Name the one thing for the day or week

One item, chosen deliberately, that is the point of the day or the week. Write it at the top. Everything else is logistics.

If you cannot name it, the calendar is driving the person.

### Step 7. Deliver in the format the user will actually read

A long document for a morning review will not be read. A one-glance table for a week review will not carry nuance.

Two defaults:

- **Daily.** Short. Top-of-day summary. Time-ordered list. Conflicts and prep needs first.
- **Weekly.** One-pager. The one thing first. Then days, ordered.

## Templates

- `templates/en/daily-agenda.md`: daily plan.
- `templates/en/weekly-agenda.md`: weekly plan.
- `templates/es/daily-agenda.md`: plan diario.
- `templates/es/weekly-agenda.md`: plan semanal.

## Related skills

- `meeting-prep`: move to it when one meeting on the agenda needs a real briefing.
- `ticket-triage`: use it when the queue to process is inbound tickets, not calendar items.

## Anti-patterns

This skill must never produce:

- A reformatted calendar dump.
- A list with no classification.
- An agenda that hides conflicts at the bottom.
- A plan with no focus block.
- A plan that treats every meeting as mandatory.
- A document that takes longer to read than the first meeting.
- An agenda that ignores prep requirements.

## Checklist before delivery

- [ ] Every source was pulled.
- [ ] Every item is classified.
- [ ] Conflicts are flagged at the top with proposed fixes.
- [ ] Prep needs are written for each meeting that needs them.
- [ ] The one thing for the day or week is named.
- [ ] Declinable items are flagged.
- [ ] Format matches the user's actual reading habit.
- [ ] No buzzwords from the voice rules appear.
