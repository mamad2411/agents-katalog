---
name: narrowing
description: Narrow a vague want to one concrete thing by proposing rival hypotheses and cutting the ones that are wrong. Use when the user knows roughly what they want but cannot state it, or says "narrow".
---

# Narrowing

The user wants something they cannot specify. Find it for them by proposing concrete hypotheses and cutting the ones they reject.

**Recognition is cheaper than specification.** Put concrete things in front of them and read the reaction. Asking them to be more specific is the one move that always fails, because that is the job you were called for.

Narrowing runs before **grilling** ([Matt Pocock's skill](https://github.com/mattpocock/skills), installed separately). Grilling walks a tree of decisions that already exists; narrowing searches a space where nothing does.

## The board

The **board** is the live set of rival **hypotheses**: candidate answers concrete enough to be *wrong*. The board is your question. Open with 8–12, numbered `H1`…`Hn`, each number used once.

- **Refutable.** "A cozy game" survives anything. "You run a lighthouse, and the only decision is who gets shelter" can die.
- **Spread across dimensions.** An assumption that eight of them share is invisible, so it never gets tested.
- **Two the user could not have said.** A board tracing entirely to their own sentences is a **mirror**: it converges fast and surprises no one.

Take the seed at whatever resolution it arrives — "I want to make a game" is complete — and cast the board straight from it. Look up whatever a hypothesis depends on: facts are yours, choices are theirs.

## Rounds

**Ask only splitting questions.** First note what each live hypothesis would answer. A question they all answer alike is **dead**: it costs real thought and moves nothing. Ask 2–4 a round, each one still splitting under every answer the others could get; hold the conditional ones for a later round.

Offer "don't care" on each. It prunes a whole dimension, which beats killing one hypothesis.

```
❓ **Q1** — **<question title>**: <body, with the options>

➡️ <your guess at their answer, and why>
```

Work out each question's **cut** — which hypotheses die on which answer. Show it where seeing the cost helps them spend the answer.

**Cut, then respawn.** Strike refuted hypotheses with the reason. Breed new ones beside the survivors, finer than what they replace: a first-round hypothesis names a genre, a fifth-round one differs from its neighbour by a single decision. Hold the board near its opening size, since a board that shrinks to one has stopped exploring.

**Contradictions.** When the answers stop being jointly satisfiable, nothing on the board can survive them. Say so plainly and ask which constraint moves.

**No basis to answer** differs from no preference: the question was yours to settle. Decide it, say why, mark it reversible.

## The guess

Every round, stop asking and state a whole answer:

```
🎯 **Is this it?**

<the pitch — concrete, written as though the thing already exists>

If not: what is the single most wrong thing about it?
```

Guess before you are sure. Committing to a whole position surfaces contradictions that questions never reach. A refusal is the best moment in the session: take the reason and recast the board around it.

## Done

The user confirms a guess, or the survivors differ only in ways they say don't matter.

Write `narrowing-<slug>.md`: the winner in their words, the **graveyard** — every cut hypothesis with the reason it died — and the dimensions they called free. The graveyard is what recognises a rejected direction when it returns later under a new name.

Then offer the winner to grilling, and leave the building to a later session.
