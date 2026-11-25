---
name: sprint-planning
description: Use this skill when the user asks to plan a sprint, set sprint commitments, or work out team capacity for an upcoming iteration. Trigger phrases include "plan the sprint", "sprint planning", "capacity planning", "what can we commit to this sprint", "planificar el sprint", "armar el sprint", "planificación de capacidad". Produces a sprint plan built around one outcome, with commitment and stretch separated. Works in English and Rioplatense Spanish.
---

# sprint-planning

> **Anchor:** Rituals serve results. A commitment is a forecast, not a promise. Reduce uncertainty first.

## When to use

Use this skill when the user needs to plan a single sprint or iteration: figure out real capacity, decide the one outcome the sprint exists to produce, and separate what the team commits to from what it might reach.

- A team starting a new sprint that needs a plan, not just a list of tickets.
- A team that keeps over-committing and wants commitment and stretch made explicit.
- A lead who needs to size capacity honestly after meetings, leave, and on-call.

Do not use when:

- The user is triaging an inbox of incoming tickets to decide what is worth keeping, not committing to a sprint. Use `ticket-triage` instead.
- The user is sequencing work over a longer horizon than one sprint. Use `roadmap-from-data` instead.

## Philosophy

Sprint planning is a ritual, and rituals serve results. The plan is good when it produces the outcome the sprint exists to produce, not when the ceremony ran on time or the board looked full.

Two concepts shape every plan this skill produces. **Rituals serve results:** the meeting, the board, and the points exist to make the outcome more likely, and any of them can be cut when it stops doing that. **Reduce uncertainty, not scope:** a commitment is a forecast made under uncertainty, so the sprint sequences the riskiest learning first and treats the remaining unknowns as the thing to attack, not as items to quietly drop.

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

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: sprint, backlog, on-call, story points, stakeholder, rollout, standup, velocity. Do not translate those to Spanish equivalents that no one uses in meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the audience that will read the plan, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. Compute real capacity

Start from people, not points. For each person, subtract recurring meetings, planned leave, and on-call load from the raw sprint hours. The result is real capacity, which is always lower than headcount times sprint length. Use the capacity worksheet to do this math before any item is discussed.

### Step 2. Name the one outcome

State the single outcome the sprint exists to produce. Not a theme, not a list. If the sprint succeeds, what is true at the end that was not true at the start. Everything else in the plan is justified against this one outcome or cut.

### Step 3. Sequence by uncertainty

Order the work so the riskiest learning happens first. The item most likely to invalidate the plan goes at the top, not the item that is easiest to start. Doing the riskiest learning first is how a forecast stays honest while there is still time to react.

### Step 4. Separate commitment from stretch

Write two lists, explicitly labeled. **Commitment** is what the team forecasts it will finish at real capacity. **Stretch** is what it will reach for only if commitment lands early. Never blur the two. A blurred line is how every item becomes a soft promise.

### Step 5. Assign a named owner per item

Every item has one named person accountable for it, not a team and not a placeholder. Shared ownership is no ownership. If no owner can be named, the item is not ready for this sprint.

### Step 6. State what is not in this sprint

Write down what is explicitly out, and why. This is the list that protects the outcome. Without it, mid-sprint requests look free.

### Step 7. Set the carry-over rule

Decide in advance what happens to unfinished work at sprint end: re-estimate and re-commit, or return it to the backlog for fresh prioritization. State the rule before the sprint starts so carry-over is a decision, not a default.

## Templates

- `templates/en/sprint-plan.md`: the sprint plan itself.
- `templates/en/capacity-worksheet.md`: the capacity math scaffold.
- `templates/es/sprint-plan.md`: el plan de sprint.
- `templates/es/capacity-worksheet.md`: el scaffold para el cálculo de capacidad.

## Related skills

- `ticket-triage`: use it when the work is triaging an inbox of incoming tickets, not committing to a sprint.
- `roadmap-from-data`: use it when sequencing work over a longer horizon than one sprint.
- `status-update`: use it after the sprint to report what landed against what was committed.
- `meeting-prep`: use it to prepare the planning session itself when alignment is the risk.

## Anti-patterns

This skill must never produce:

- A plan that is a flat list of tickets with no single outcome named.
- A plan where commitment and stretch are merged into one list.
- A plan built on raw headcount hours instead of real capacity.
- A plan with items owned by a team or a placeholder rather than a named person.
- A plan that sequences by ease of starting instead of by uncertainty.
- A plan with no statement of what is explicitly out of the sprint.
- A plan with no carry-over rule, so unfinished work defaults silently.
- A plan that treats the planning ritual as the goal rather than the outcome.
- A plan that mixes English and Spanish inconsistently within a single section.
- A plan that cites velocity as a commitment without naming the uncertainty behind it.

## Checklist before delivery

- [ ] Real capacity is computed from the worksheet, not from headcount.
- [ ] The one outcome the sprint exists to produce is named in a single sentence.
- [ ] Work is sequenced so the riskiest learning happens first.
- [ ] Commitment and stretch are in two explicitly labeled lists.
- [ ] Every committed item has one named owner.
- [ ] What is explicitly out of the sprint is written down with a reason.
- [ ] The carry-over rule is stated before the sprint starts.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] Plan reads cleanly to a stranger who was not in the planning session.
