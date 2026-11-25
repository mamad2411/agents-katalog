---
name: meeting-prep
description: Use this skill when the user asks to prepare for a meeting, build a briefing for a one-on-one, anticipate stakeholder reactions, or plan the opening move for a hard conversation. Trigger phrases include "prep me for this meeting", "brief for tomorrow's meeting", "how should I run this conversation", "preparar esta reunión", "brief para la reunión", "what's the plan for this call". Produces a briefing that names the desired outcome, maps stakeholders, anticipates objections, and plans the opening move.
---

# meeting-prep

> **Anchor:** Prep for the meeting you intend to have, not the one on the invite.

## When to use

Use this skill when the user needs a structured briefing before a meeting. Works for:

- A stakeholder meeting with real decisions on the line.
- A one-on-one that has a hard conversation inside it.
- A cross-functional sync where alignment is uncertain.
- A sales, partner, or investor meeting where the opening move matters.

Do not use when:

- The user is producing the day's agenda. Use `agenda-synthesis`.
- The user is writing post-meeting notes. That is a documentation task.
- The meeting has no stakes. Not every meeting is worth prepping.

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

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: one-on-one, stakeholder, pushback, escalation, agenda, follow-up, buy-in, alignment, talking points.
- **EN.** Direct US business register. A briefing is not a pitch; do not write toward the meeting as if persuading it already.
- Names of people and titles appear in the language they are used internally.

## Method

### Step 1. Name the outcome

A meeting without a named outcome is a meeting that spends the attendees' time and produces nothing.

Pick one primary outcome:

- **Decision.** A specific decision made, by whom, with what evidence on hand.
- **Alignment.** A shared view of a situation, even if no decision is made.
- **Information transfer.** The user learns something concrete or teaches something concrete.
- **Relationship.** Trust, rapport, context exchange, with no transactional output needed.

A briefing that cannot name one is a briefing that has not asked the right question of the user.

### Step 2. Map the stakeholders

One subsection per person in the room. Include:

- **Name and role.**
- **What they want from this meeting.** Their interest.
- **What they fear.** The failure mode they are guarding against.
- **What they know.** Context they bring.
- **What they do not know.** Context they are missing.
- **Their typical move.** How this person usually behaves in meetings like this.

Do not map people who will not speak.

### Step 3. Pull the history

A fast compression of what has already been said or decided.

- Prior meetings on this topic. Date, outcome, link to notes.
- Prior commitments made by any of the stakeholders.
- Recent messages or threads that shape the meeting.
- Any open action items owed by someone in the room.

If the user is about to ask for something that a stakeholder already declined, that needs to show up here.

### Step 4. Anticipate objections

Three to five likely objections or hard questions. For each:

- **The objection.** In the words the objector will use.
- **The fear underneath.** What the objection is protecting.
- **The response.** Direct, short, honest.

An objection that cannot be answered is a signal to revise the meeting's goal, not to hope it does not come up.

### Step 5. Plan the opening move

The first 60 seconds set the meeting. Write the opening move as a short script or as three beats:

- **Frame.** What this meeting is about, stated by the user.
- **Signal of respect for time.** Duration, scope, what is and is not on the table.
- **Ask or handoff.** What is being asked of the group, or who speaks next.

Do not open with small talk beyond a single sentence.

### Step 6. Prepare materials

Only if they will be read or used.

- One-pager, chart, or memo.
- Pre-read shared in advance.
- Live artifact, such as a document shown or a dashboard opened during the meeting.

No material beats a bad material. If the user cannot name how the artifact helps the outcome, do not prepare it.

### Step 7. Plan the exits

A meeting can go sideways. Write exits:

- **Too long.** What gets cut.
- **Off-topic.** How to redirect.
- **Emotional or hostile.** How to hold the room or end the meeting.
- **Stalled decision.** What the fallback ask is if the primary decision is not reached.

### Step 8. Plan the after

The meeting does not end with the meeting.

- **Notes.** Who writes them, who they go to, by when.
- **Actions.** Who owns each, by when.
- **Follow-up with absent stakeholders.** What they are told, by whom.

## Templates

- `templates/en/meeting-brief.md`: briefing for a group meeting.
- `templates/en/one-on-one-brief.md`: briefing for a one-on-one.
- `templates/es/meeting-brief.md`: brief para una reunión grupal.
- `templates/es/one-on-one-brief.md`: brief para un uno a uno.

## Related skills

- `agenda-synthesis`: use it when producing the day or week plan across meetings, not prepping one.
- `documentation-extraction`: use it after the meeting to turn notes into a durable doc.
- `ticket-triage`: use it when the meeting is a backlog review and you need dispositions, not a brief.

## Anti-patterns

This skill must never produce:

- A briefing without a named outcome.
- A stakeholder map that covers people who will not speak.
- A list of "talking points" with no stakeholder interests attached.
- Objection handling that relies on deflection rather than a direct answer.
- A briefing longer than the meeting.
- A plan that has no exits.
- A briefing that reads as a script to read aloud.

## Checklist before delivery

- [ ] Outcome is named and is one of decision, alignment, information, relationship.
- [ ] Every speaking stakeholder has interest, fear, context, typical move.
- [ ] History is pulled and relevant prior commitments are named.
- [ ] Three to five likely objections are drafted with direct answers.
- [ ] Opening move is three beats or a short script.
- [ ] Materials listed are actually needed.
- [ ] Exits are planned for long, off-topic, hostile, and stalled.
- [ ] After-meeting plan covers notes, actions, and absent stakeholders.
- [ ] No buzzwords from the voice rules appear.
