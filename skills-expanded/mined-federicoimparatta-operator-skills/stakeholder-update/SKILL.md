---
name: stakeholder-update
description: Use this skill when the user asks to write, draft, or revise a status update for an external client or stakeholder. Trigger phrases include "client update", "stakeholder update", "delivery status update", "write the update for the client", "update para el cliente", "escalar un retraso al cliente". Produces a client-facing update that reads as a conversation about delivery, not a contract recital. Works in English and Rioplatense Spanish.
---

# stakeholder-update

> **Anchor:** A roadmap is a conversation, not a contract. Cultural signals are delivery.

## When to use

Use this skill when the user needs to write or restructure an update aimed at an external client or stakeholder: what shipped, what is on track, what is at risk, what changed, and what you need back from them. Works for:

- A routine delivery update on a project or engagement.
- An escalation when a date will slip and the client needs to hear it early and plainly.
- A reset of expectations when scope or a deadline has moved.

Do not use when:

- The update is for the internal team, not a client. Use `status-update`.
- The user needs an upward one-pager for an executive sponsor. Use `exec-brief`.
- There is a live incident in progress that needs real-time customer comms. Use `incident-comms`.

## Philosophy

A stakeholder update manages a relationship under uncertainty, not a paper trail. Two concepts from the handbook apply directly.

**Roadmap as a conversation, not a contract.** Dates and scope are the current best read, held openly, revised when reality moves. The update is where that conversation happens. Treating the roadmap as a contract turns every change into a breach and every honest update into a confession. Treating it as a conversation lets you name a slip early, with its reason, and keep trust intact.

**Cultural signals are delivery.** How you communicate is part of what you deliver. A clear, early, plainly-named update is itself a deliverable the client receives. Clarity, candor about risk, and a specific ask are signals that the work is in good hands. Vagueness and silence are signals too, and the client reads them.

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

- **ES.** Rioplatense register. Vos over tú. Keep technical and delivery terms in English where that is standard in industry use: roadmap, sprint, milestone, stakeholder, rollout, scope, deadline, blocker, deliverable, go-live. Do not translate those to Spanish equivalents that no one uses in client meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the client who will read the update, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. What shipped since the last update, in their terms not yours

Lead with what the client can now see, use, or rely on. Phrase it as outcomes for them, not tasks the team closed. "You can now export the full report to PDF" beats "completed the PDF export ticket". If nothing user-visible shipped, say what moved internally and why it matters to them.

### Step 2. What is on track vs at risk, named plainly

Two short lists. On track is what you still expect to hit as planned. At risk is what might not, named without hedging. Do not bury a risk inside a paragraph of context. If something is at risk, the client should be able to find it in one read.

### Step 3. Any change to scope or date, and the reason

If scope or a date moved since the last update, state the change and the reason in the same breath. The reason is not an excuse, it is information the client needs to plan. Never let the client discover a slip by inference. Name it.

### Step 4. What you need from them, with a date

Most updates require something back: a decision, an approval, access, a contact, a review. State each ask with the specific date you need it by and what is blocked until then. An update with no ask and no date is a broadcast, not a conversation.

### Step 5. Next milestone and its date

Close with the next concrete milestone and the date you are aiming for. One milestone, not a full replanned roadmap. The client should finish the update knowing what comes next and when.

### Step 6. Escalation-note variant for when a date will slip

When a date will slip, do not wait for the routine cadence. Use the escalation-note variant. It is shorter and sharper: what is slipping, by how much, why, what you are doing about it, and what you need from the client to limit the damage. Send it early. A slip named two weeks out is a planning input. The same slip named on the due date is a failure.

## Templates

- `templates/en/delivery-update.md`: routine client delivery status.
- `templates/en/escalation-note.md`: a date is going to slip and the client needs to hear it early.
- `templates/es/delivery-update.md`: estado de entrega rutinario para el cliente.
- `templates/es/escalation-note.md`: una fecha se va a atrasar y el cliente tiene que enterarse temprano.

## Related skills

- `status-update`: use it when the update is for the internal team rather than an external client.
- `exec-brief`: use it when the audience is an executive sponsor who needs an upward one-pager.
- `incident-comms`: use it when there is a live incident that needs real-time customer communication.
- `proposal-scoping`: use it when a scope or date change is large enough to need a re-scope, not just an update.

## Anti-patterns

This skill must never produce:

- An update that lists completed tasks instead of outcomes the client can see.
- An update that hides a slip or a risk inside a wall of context.
- An update that announces a slipped date for the first time on the day it was due.
- An update with no specific ask, or an ask with no date.
- An update that reframes a missed deadline as a win.
- An update that recites the roadmap as if it were a signed contract.
- An update that opens with filler before getting to what changed.
- An escalation note that buries the slip below paragraphs of reassurance.
- An update that mixes English and Spanish inconsistently within a single section.
- An update written in press-release voice when the client wants a plain delivery read.

## Checklist before delivery

- [ ] Opens with what shipped, phrased in the client's terms.
- [ ] On track and at risk are separated and each item is named plainly.
- [ ] Any scope or date change appears with its reason in the same sentence.
- [ ] Every ask has a specific date and names what it blocks.
- [ ] The next milestone and its date are stated once and clearly.
- [ ] A slipping date is escalated early, not on the due date.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] Update reads cleanly to the client without prior meeting context.
