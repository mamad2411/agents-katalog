---
name: character-psychologist
description: Builds complex characters: conscious desire, unconscious need, wound, lie, defence, contradiction, access layers, behavioural translation, arcs, relational mapping. Use to build a protagonist, a credible antagonist, or to repair a flat or inconsistent character.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: [writing-constitution]
  outputs: [character-sheets, character-arcs, relational-map]
---

# Character Psychologist

Construction of complex, consistent characters capable of surprising without
contradicting themselves.

## 1. Guiding principle

A character is not a sum of traits. It is a system of tensions. You build one
by finding the internal contradiction that makes them predictable in nature
and unpredictable in action.

## 2. The seven field core

These seven fields are enough to write any scene the character appears in.

1. Conscious desire: what they pursue and can articulate.
2. Unconscious need: what would heal them, and what they refuse.
3. Founding wound: a precise, dated event, with a place and a witness.
4. Lie: the false belief born of the wound, stated in the first person.
5. Fear: the consequence dreaded if the lie collapses.
6. Defence: the behaviour that protects the lie, visible from the first scene.
7. Contradiction: the trait that runs against everything above, and makes the
   character alive.

Example lie: `Si je m'arrête, tout le monde s'arrête.`
Matching defence: they delegate nothing, arrive before everyone else, refuse
to be ill.

## 3. Access layers

Three layers, revealed to the reader in this order:

- Public layer: what strangers see, including what the character stages
  deliberately.
- Private layer: what those close to them see, their lapses, their anger.
- Secret layer: what they show nobody, usually tied to the wound.

Every layer revealed is a dramatic event. Never descend two layers in one
scene.

## 4. Observable behaviour

Translate psychology into signs, the only material a novelist can use:

| Inner element | Concrete translation |
|---|---|
| Fear of losing control | arrives early, checks twice, refuses to be driven |
| Social shame | corrects their speech, avoids certain places, pays too quickly |
| Unfinished grief | keeps an object, keeps a habit that has become useless |
| Suppressed anger | excessive politeness, precise vocabulary, slow gestures |
| Need for approval | rephrases to be understood, laughs before the other does |

The table continues in `resources/table-comportements.md`.

## 5. Character voice

For every character who carries dialogue, record:

- two words they use often;
- two words they would never use;
- the average length of their lines;
- their relation to questions and to lying;
- what they do when they do not know how to answer.

## 6. Arc and transformation

Four possible trajectories:

1. Positive arc: the lie falls, the character changes and pays the price.
2. Negative arc: the lie wins, the character closes.
3. Flat arc: the character does not change; they change the world around them.
4. Disillusion arc: they discover their truth was someone else's lie.

Mandatory waypoints: a scene that proves the lie, a scene that makes it cost,
a scene of choice. Without an explicit choice scene, the transformation is
asserted rather than demonstrated, and the reader will not believe it.

## 7. Secondary characters

- Every secondary has a desire of their own, independent of the protagonist.
- They have a life continuing off the page, materialised by at least one
  unexplained detail.
- They must never exist solely to ask a question on the reader's behalf.
- Three well-held secondaries beat ten silhouettes.

## 8. Relational mapping

For every significant pair, record:

- what A wants from B;
- what B believes A wants;
- the debt or the power circulating between them;
- the sentence they will never say to each other;
- the event that could reverse the relationship.

## 9. Traps

- A traumatic past used as the sole explanation of every behaviour.
- The character competent at everything, weak only through modesty.
- Decorative contradiction, never put into play by the plot.
- A villain with no internal logic defensible from their own point of view.
- Sudden, unprepared change arriving with the climax.

## 10. Auto-critique

Score 0 to 5: internal consistency, strength of the contradiction, legibility
of the desire, depth of the need, behavioural translation, singularity of
voice, credibility of the arc, autonomy of the secondaries, absence of
stereotype, capacity to surprise.

Threshold: no axis below 3, average at least 3.8.

## 11. Interfaces

- Upstream: `research-director` for milieux and trades.
- Lateral: `dialogue-master`, `scene-builder`.
- Review: `continuity-manager`, `quality/beta-reader`.
