---
name: decision-record
description: Use this skill when the user asks to write, draft, structure, or revise a record of a decision that has been made. Trigger phrases include "write a decision record", "ADR for X", "document this decision", "registrar la decisión", "ADR", "log this decision", "decision log entry". Produces a record of a bet placed under uncertainty, not a proposal. Works in English and Rioplatense Spanish.
---

# decision-record

> **Anchor:** Every decision is a bet under uncertainty. Record the bet so the next person knows you knew.

## When to use

Use this skill when a decision has already been made and needs to be written down so future readers understand the reasoning, the alternatives, and the trade. Works for:

- A technical or product decision that changes the shape of the system and needs a durable record.
- A choice between options where the rejected paths matter as much as the chosen one.
- A reversal or supersession of a prior decision that needs to be linked and dated.

Do not use when:

- The decision has not been made yet and you want to pressure-test it first. Use `red-team-review` to stress-test a decision before making it.
- The outcome has already played out and you are analyzing what happened. Use `post-mortem` after an outcome.

## Philosophy

Product is a portfolio of bets. A decision record is one bet in that portfolio, written down at the moment it was placed, before the outcome is known. The point is not to predict correctly. The point is to make the reasoning legible, so the next person can tell whether a bad outcome came from a bad bet or from bad luck.

The PM as anthropologist applies here too. The forcing function and the constraints came from observation of the real situation, not from a clean abstraction. Record what was actually true at the time: the deadline, the missing data, the org politics, the thing you could not change. A record that hides the mess is a record that lies to the future.

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

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: trade-off, rollback, deadline, stakeholder, feature flag, ADR, backlog. Do not translate those to Spanish equivalents that no one uses in meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- The ADR itself stays in English even when the surrounding conversation is in Spanish, because ADRs are a shared engineering artifact. The decision log entry follows the language of the audience that reads it.
- Choose the language of the audience that will read the record, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. Context and the forcing function

Write what was true when the decision was made. The forcing function is the thing that made a decision necessary now rather than later: a deadline, a dependency, an incident, a constraint that just appeared. Name it. A decision with no forcing function is usually premature.

### Step 2. The decision in one sentence

State what was decided in a single sentence a stranger could read and understand. If you cannot compress it to one sentence, the decision is still two decisions wearing one coat.

### Step 3. Options considered and why each was rejected

List the real alternatives, including the one you chose. For each rejected option, write the concrete reason it lost. "Too slow" is not a reason. "Adds 400ms to the checkout path, which fails our budget" is a reason. Do not invent strawman options to make the choice look obvious.

### Step 4. The bet and its size

Name the bet plainly and size it. A small bet is cheap to reverse and low blast radius. A large bet is expensive to reverse or touches many surfaces. The size tells the next person how much scrutiny the record deserves.

### Step 5. Consequences accepted, including the bad ones

Every decision buys something and pays for something. Write the costs you knowingly accepted, not just the upside. A record that lists only benefits is marketing, not a record. The bad consequences are the most useful part for the next reader.

### Step 6. Revisit trigger

Write what would make us reopen this decision. A new data point, a scale threshold, a dependency that ships, a metric that crosses a line. A decision with no revisit trigger is a one-way door pretending to be permanent.

### Step 7. Status

Mark the record: proposed, accepted, or superseded. If superseded, link the record that replaced it and the date. Status is what keeps a folder of records from rotting into a folder of lies.

## Templates

- `templates/en/decision-record.md`: full ADR-style record for one decision.
- `templates/en/decision-log-entry.md`: compact one-line-per-decision log row.
- `templates/es/decision-record.md`: registro estilo ADR completo para una decisión.
- `templates/es/decision-log-entry.md`: fila de log compacta, una línea por decisión.

## Related skills

- `red-team-review`: use it before the decision is made, to stress-test the bet rather than record it.
- `post-mortem`: use it after the outcome is known, to analyze what happened rather than what was decided.
- `proposal-scoping`: use it when scoping the delivery work that a decision unlocks, not the decision itself.

## Anti-patterns

This skill must never produce:

- A record that states the decision but hides the rejected options.
- A record with no forcing function, so the reader cannot tell why now.
- A record that lists only benefits and no accepted costs.
- A record with no revisit trigger, treating every decision as permanent.
- A record where the decision needs more than one sentence to state.
- A record with strawman alternatives built to flatter the chosen path.
- A record with no status, so a stranger cannot tell if it still holds.
- A record that buries a supersession instead of linking it.
- A record written as a proposal for a decision not yet made.
- A record that mixes English and Spanish inconsistently within a single section.

## Checklist before delivery

- [ ] Context names a concrete forcing function.
- [ ] The decision is stated in a single sentence.
- [ ] Every rejected option has a concrete reason, not a label.
- [ ] The bet is named and its size is stated.
- [ ] At least one accepted cost is written down.
- [ ] A revisit trigger is concrete and checkable.
- [ ] Status is set to proposed, accepted, or superseded.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] The record reads cleanly to a stranger who was not in the room.
