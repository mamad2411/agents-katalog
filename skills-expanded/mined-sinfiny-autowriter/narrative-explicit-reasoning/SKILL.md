---
name: narrative-explicit-reasoning
description: Use when planning fiction before drafting, checking character motivation, surfacing assumptions, validating lore constraints, resolving emotional contradictions, or evaluating plot twist tradeoffs. Based primarily on the David Perell interview with Morgan Housel and intended as a narrative reasoning protocol, not a prose style imitation.
---

# Narrative Explicit Reasoning

Use this skill before drafting or changing fiction when the story depends on character motive, established lore, reader expectations, or a major hidden assumption.

## Source Protocol

- Read `references/source-notes.md` for the Morgan Housel transcript-derived operating model.
- Use this skill as a reasoning and planning layer, not as Morgan Housel voice imitation.
- Do not quote transcript passages unless the user asks for source analysis; paraphrase the principle and apply it to the user's story.

## Operating Loop

1. Identify the narrative decision: scene action, character choice, reveal, twist, continuation, contradiction, or lore expansion.
2. Extract known facts from the user's material: character history, current desire, emotional wound, relationship pressure, timeline, genre promise, and lore limits.
3. State assumptions before using them. Mark each as confirmed, inferred, or missing.
4. Define the point of the beat in one sentence.
5. Test whether the action follows from the character and world state.
6. If the beat contradicts known context, stop and ask one precise question or propose a bridge event.

## Required Block

Use this before prose or major story decisions:

```xml
<reasoning>
Task:
Point of the beat:
Known facts:
Assumptions:
Character emotional goal:
Character outward goal:
Lore constraints:
Reader promise:
Tradeoffs:
Chosen path:
Stop condition:
</reasoning>
```

## Plot Twist Protocol

When a prompt asks for a major twist:

```text
Twist request:
Current story contract:
Option A:
Option B:
Option C:
Recommended option:
Setup required:
Continuity cost:
Payoff risk:
```

Pick the option that recontextualizes prior context without making earlier scenes feel dishonest.

## Stop Conditions

Stop instead of drafting when:

- The emotional beat contradicts the character's established motive and no bridge is supplied.
- The lore change creates a new power, faction, magic rule, prophecy, or timeline fact without permission.
- The twist invalidates the reader's prior investment rather than deepening it.
- The prompt asks for certainty where the existing canon only supports ambiguity.

## Output Rules

- Keep reasoning concise and decision-useful.
- Ask one question only when missing information materially changes the story.
- Do not invent backstory to make a convenient beat work.
- End planning with a draftable next move when the path is clear.
